"""Seed script to initialize and preload campus data."""

from __future__ import annotations

from models import get_connection, init_db

# Coordinates are stored as percentages so frontend can plot markers over the map image.
BUILDINGS = [
    ("Hostel", 24, 24),
    ("Library", 48, 42),
    ("Block A", 63, 60),
    ("Block B", 70, 70),
    ("Admin Office", 44, 86),
    ("Lab 1", 56, 78),
    ("Lab 2", 60, 72),
    ("Canteen", 77, 74),
]

CONNECTIONS = [
    ("Hostel", "Library", 18),
    ("Library", "Block A", 20),
    ("Block A", "Block B", 10),
    ("Block B", "Canteen", 9),
    ("Library", "Lab 2", 16),
    ("Lab 2", "Lab 1", 8),
    ("Lab 1", "Admin Office", 12),
    ("Admin Office", "Block B", 14),
    ("Block A", "Lab 2", 11),
    ("Canteen", "Lab 1", 13),
]


def seed() -> None:
    """Create tables and insert deterministic sample data."""
    init_db()

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM Connections")
    cursor.execute("DELETE FROM Buildings")

    cursor.executemany(
        "INSERT INTO Buildings (name, x_coordinate, y_coordinate) VALUES (?, ?, ?)",
        BUILDINGS,
    )

    for from_building, to_building, distance in CONNECTIONS:
        cursor.execute(
            "INSERT INTO Connections (from_building, to_building, distance) VALUES (?, ?, ?)",
            (from_building, to_building, distance),
        )
        cursor.execute(
            "INSERT INTO Connections (from_building, to_building, distance) VALUES (?, ?, ?)",
            (to_building, from_building, distance),
        )

    conn.commit()
    conn.close()
    print("Database seeded successfully with sample campus data.")


if __name__ == "__main__":
    seed()
