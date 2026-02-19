"""REST API routes for the Smart Campus Navigation System."""

from __future__ import annotations

from flask import Blueprint, jsonify, request

from graph import shortest_path
from models import get_connection

api = Blueprint("api", __name__)


@api.get("/buildings")
def get_buildings():
    """Return all campus buildings with coordinates."""
    conn = get_connection()
    cursor = conn.cursor()
    rows = cursor.execute(
        "SELECT id, name, x_coordinate, y_coordinate FROM Buildings ORDER BY name"
    ).fetchall()
    conn.close()

    buildings = [dict(row) for row in rows]
    return jsonify(buildings)


@api.get("/navigate")
def navigate():
    """Compute shortest route between start and end building names."""
    start = request.args.get("start", "").strip()
    end = request.args.get("end", "").strip()

    if not start or not end:
        return jsonify({"error": "Both 'start' and 'end' query parameters are required."}), 400

    try:
        result = shortest_path(start, end)
        return jsonify(result)
    except ValueError as exc:
        return jsonify({"error": str(exc)}), 404
    except Exception as exc:  # Safety fallback for malformed graph states
        return jsonify({"error": f"Unable to calculate route: {exc}"}), 400


@api.post("/scan_qr")
def scan_qr():
    """Simulate QR scan by validating and returning current location from building ID."""
    payload = request.get_json(silent=True) or {}
    qr_id = str(payload.get("qr_id", "")).strip()

    if not qr_id:
        return jsonify({"error": "'qr_id' is required."}), 400

    conn = get_connection()
    cursor = conn.cursor()
    building = cursor.execute(
        "SELECT id, name FROM Buildings WHERE name = ?", (qr_id,)
    ).fetchone()
    conn.close()

    if building is None:
        return jsonify({"error": f"QR ID '{qr_id}' is invalid."}), 404

    return jsonify(
        {
            "message": "QR scanned successfully.",
            "current_location": building["name"],
        }
    )


@api.post("/admin/add_building")
def add_building():
    """Add a building with coordinates from admin panel."""
    payload = request.get_json(silent=True) or {}

    name = str(payload.get("name", "")).strip()
    x_coordinate = payload.get("x_coordinate")
    y_coordinate = payload.get("y_coordinate")

    if not name or x_coordinate is None or y_coordinate is None:
        return jsonify({"error": "'name', 'x_coordinate', and 'y_coordinate' are required."}), 400

    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute(
            "INSERT INTO Buildings (name, x_coordinate, y_coordinate) VALUES (?, ?, ?)",
            (name, float(x_coordinate), float(y_coordinate)),
        )
        conn.commit()
    except Exception as exc:
        conn.rollback()
        conn.close()
        return jsonify({"error": f"Could not add building: {exc}"}), 400

    conn.close()
    return jsonify({"message": f"Building '{name}' added successfully."}), 201


@api.post("/admin/connect")
def connect_buildings():
    """Add a weighted path (edge) between two buildings."""
    payload = request.get_json(silent=True) or {}

    from_building = str(payload.get("from_building", "")).strip()
    to_building = str(payload.get("to_building", "")).strip()
    distance = payload.get("distance")

    if not from_building or not to_building or distance is None:
        return jsonify({"error": "'from_building', 'to_building', and 'distance' are required."}), 400

    if from_building == to_building:
        return jsonify({"error": "Cannot connect a building to itself."}), 400

    conn = get_connection()
    cursor = conn.cursor()

    existing = cursor.execute(
        "SELECT name FROM Buildings WHERE name IN (?, ?)", (from_building, to_building)
    ).fetchall()

    if len(existing) != 2:
        conn.close()
        return jsonify({"error": "Both buildings must exist before creating a connection."}), 404

    try:
        dist_value = float(distance)
        cursor.execute(
            "INSERT INTO Connections (from_building, to_building, distance) VALUES (?, ?, ?)",
            (from_building, to_building, dist_value),
        )
        cursor.execute(
            "INSERT INTO Connections (from_building, to_building, distance) VALUES (?, ?, ?)",
            (to_building, from_building, dist_value),
        )
        conn.commit()
    except Exception as exc:
        conn.rollback()
        conn.close()
        return jsonify({"error": f"Could not connect buildings: {exc}"}), 400

    conn.close()
    return jsonify(
        {
            "message": f"Connection created between '{from_building}' and '{to_building}' with distance {dist_value}."
        }
    ), 201
