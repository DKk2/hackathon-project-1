"""Seed script to initialize and preload campus data."""

from __future__ import annotations

from models import get_connection, init_db

BUILDINGS = [
    ("Library", 10, 20),
    ("Canteen", 30, 15),
    ("Block A", 20, 30),
    ("Block B", 35, 35),
    ("Admin Office", 15, 10),
    ("Lab 1", 25, 28),
    ("Lab 2", 28, 40),
    ("Hostel", 45, 20),
]

CONNECTIONS = [
    ("Library", "Block A", 12),
    ("Library", "Admin Office", 11),
    ("Admin Office", "Canteen", 16),
    ("Block A", "Lab 1", 7),
    ("Lab 1", "Lab 2", 9),
    ("Block A", "Block B", 14),
    ("Block B", "Lab 2", 8),
    ("Canteen", "Hostel", 10),
    ("Block B", "Hostel", 12),
    ("Lab 1", "Canteen", 13),
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
