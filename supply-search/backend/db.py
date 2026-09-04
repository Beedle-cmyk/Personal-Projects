"""
Small sqlite helpers shared by main.py.

Every function opens a short-lived connection, runs one query, and closes.
That's fine at this scale (a few thousand rows, low request volume) and
keeps the code simple - no connection pooling needed.
"""

import sqlite3
from contextlib import contextmanager


@contextmanager
def connect(db_path: str):
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    try:
        yield conn
    finally:
        conn.close()


def fetch_all(db_path: str, query: str, params: tuple = ()):
    with connect(db_path) as conn:
        rows = conn.execute(query, params).fetchall()
        return [dict(r) for r in rows]


def fetch_one(db_path: str, query: str, params: tuple = ()):
    with connect(db_path) as conn:
        row = conn.execute(query, params).fetchone()
        return dict(row) if row else None


def table_exists(db_path: str, table: str) -> bool:
    row = fetch_one(
        db_path,
        "SELECT name FROM sqlite_master WHERE type='table' AND name=?",
        (table,),
    )
    return row is not None
