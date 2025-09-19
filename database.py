import sqlite3
import json
import csv
from datetime import datetime

DB_NAME = "extracted_entities.db"

def init_db():
    """Initialize the SQLite database and table."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS documents (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            text TEXT,
            persons TEXT,
            orgs TEXT,
            locations TEXT,
            dates TEXT,
            entities TEXT,
            text_length INTEGER,
            request_id TEXT
        )
    """)
    conn.commit()
    conn.close()

def save_results(results, request_id=None):
    """
    Save a list of result dictionaries to the database.
    Each result is linked to a request_id (unique per batch).
    """
    if request_id is None:
        request_id = datetime.now().strftime("%Y%m%d_%H%M%S")

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    for res in results:
        cursor.execute("""
            INSERT INTO documents (text, persons, orgs, locations, dates, entities, text_length, request_id)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            res["text"],
            json.dumps(res["persons"]),
            json.dumps(res["orgs"]),
            json.dumps(res["locations"]),
            json.dumps(res["dates"]),
            json.dumps(res["entities"]),
            res["text_length"],
            request_id
        ))

    conn.commit()
    conn.close()
    return request_id

def export_to_csv(request_id, prefix="extracted_results"):
    """
    Export only the results for the given request_id to a new CSV file.
    Filename includes timestamp.
    """
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{prefix}_{timestamp}.csv"

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT id, text, persons, orgs, locations, dates, entities, text_length "
                   "FROM documents WHERE request_id = ?", (request_id,))
    rows = cursor.fetchall()

    headers = [desc[0] for desc in cursor.description]

    with open(filename, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(headers)
        writer.writerows(rows)

    conn.close()
    print(f"✅ Data exported to {filename}")
    return filename
