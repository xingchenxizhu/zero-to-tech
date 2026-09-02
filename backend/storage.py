# # backend/storage.py
# import json
#
# HISTORY_FILE = "history.json"
#
# def load_history():
#     try:
#         with open(HISTORY_FILE, "r", encoding="utf-8") as f:
#             return json.load(f)
#     except FileNotFoundError:
#         return []
#
# def save_record(record):
#     records = load_history()
#     records.append(record)
#     with open(HISTORY_FILE, "w", encoding="utf-8") as f:
#         json.dump(records, f, ensure_ascii=False, indent=2)
#
# # def get_history():
# #     records = load_history()
# #     records.reverse()
# #     return records[:10]
#
#
# def get_history(limit):
#     records = load_history()
#     records.reverse()
#     return records[:limit]



# backend/storage.py
import sqlite3

DB_FILE = "history.db"

def get_conn():
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("""
    CREATE TABLE IF NOT EXISTS history (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        text TEXT,
        score REAL,
        label TEXT,
        pinyin TEXT,
        created_at TEXT
    )
    """)
    conn.commit()
    conn.close()

def save_record(record):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO history (text, score, label, pinyin, created_at) VALUES (?, ?, ?, ?, ?)",
        [record["text"], record["score"], record["label"], record["pinyin"], record["created_at"]],
    )

    cur.execute("CREATE INDEX IF NOT EXISTS idx_history_created ON history(created_at)")

    conn.commit()
    conn.close()

def get_history(limit):
    conn = get_conn()
    cur = conn.cursor()
    rows = cur.execute(
        "SELECT * FROM history ORDER BY created_at DESC LIMIT ?",
        [limit],
    ).fetchall()
    conn.close()

    records = []
    for row in rows:
        records.append(dict(row))
    return records

