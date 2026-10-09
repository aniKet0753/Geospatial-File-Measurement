import json
import sqlite3
import uuid
from pathlib import Path

DB_PATH = Path(__file__).resolve().parent.parent / "geospatial.db"


def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def init_db():
    with get_connection() as conn:
        conn.executescript(
            """
            CREATE TABLE IF NOT EXISTS files (
                id TEXT PRIMARY KEY,
                filename TEXT NOT NULL,
                feature_count INTEGER NOT NULL,
                crs TEXT,
                measurement_crs TEXT,
                status TEXT NOT NULL,
                created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
            );

            CREATE TABLE IF NOT EXISTS features (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                file_id TEXT NOT NULL,
                feature_index INTEGER NOT NULL,
                geometry_type TEXT NOT NULL,
                geometry TEXT NOT NULL,
                properties TEXT NOT NULL,
                crs TEXT,
                area_m2 REAL,
                perimeter_m REAL,
                length_m REAL,
                measurement_supported INTEGER NOT NULL DEFAULT 1,
                message TEXT,
                FOREIGN KEY(file_id) REFERENCES files(id) ON DELETE CASCADE
            );
            """
        )


def create_file_record(filename: str, parsed: dict) -> str:
    file_id = uuid.uuid4().hex[:12]
    with get_connection() as conn:
        conn.execute(
            """
            INSERT INTO files
            (id, filename, feature_count, crs, measurement_crs, status)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (
                file_id,
                filename,
                parsed["feature_count"],
                parsed["original_crs"],
                parsed["measurement_crs"],
                "COMPLETED",
            ),
        )
        conn.executemany(
            """
            INSERT INTO features
            (file_id, feature_index, geometry_type, geometry, properties, crs,
             area_m2, perimeter_m, length_m, measurement_supported, message)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            [
                (
                    file_id,
                    feature["id"],
                    feature["geometry_type"],
                    json.dumps(feature["geometry"]),
                    json.dumps(feature["properties"]),
                    feature["crs"],
                    feature.get("area_m2"),
                    feature.get("perimeter_m"),
                    feature.get("length_m"),
                    1 if feature["measurement_supported"] else 0,
                    feature.get("message"),
                )
                for feature in parsed["features"]
            ],
        )
    return file_id


def get_file_record(file_id: str):
    with get_connection() as conn:
        row = conn.execute(
            """
            SELECT id, filename, feature_count, crs, measurement_crs,
                   status, created_at
            FROM files WHERE id = ?
            """,
            (file_id,),
        ).fetchone()
    return dict(row) if row else None


def get_measurements(file_id: str):
    with get_connection() as conn:
        rows = conn.execute(
            """
            SELECT feature_index, geometry_type, geometry, properties, crs,
                   area_m2, perimeter_m, length_m, measurement_supported, message
            FROM features
            WHERE file_id = ?
            ORDER BY feature_index
            """,
            (file_id,),
        ).fetchall()

    result = []
    for row in rows:
        item = dict(row)
        item["geometry"] = json.loads(item["geometry"])
        item["properties"] = json.loads(item["properties"])
        item["id"] = item.pop("feature_index")
        item["measurement_supported"] = bool(item["measurement_supported"])
        result.append(item)
    return result
