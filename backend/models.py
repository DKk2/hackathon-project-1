"""Database models and helpers for the Smart Campus Navigation System."""

from __future__ import annotations

import sqlite3
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "database.db"


def get_connection() -> sqlite3.Connection:
    """Return a SQLite connection with row factory enabled."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db() -> None:
    """Create required tables if they do not exist."""
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS Buildings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL UNIQUE,
            x_coordinate REAL NOT NULL,
            y_coordinate REAL NOT NULL
        )
        """
    )

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS Connections (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            from_building TEXT NOT NULL,
            to_building TEXT NOT NULL,
            distance REAL NOT NULL,
            UNIQUE(from_building, to_building)
        )
        """
    )

    conn.commit()
    conn.close()
