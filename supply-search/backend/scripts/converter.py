"""
Generic .xlsx -> .db converter, reused for suppliers.xlsx, tags.xlsx, and
data.xlsx so you don't need three separate converter scripts.

Usage:
    python converter.py suppliers
    python converter.py tags
    python converter.py data
    python converter.py all
"""

import sys
from pathlib import Path

import pandas as pd
import sqlite3

sys.path.append(str(Path(__file__).resolve().parent.parent))
from config import (  # noqa: E402
    SUPPLIERS_XLSX, SUPPLIERS_DB, SUPPLIERS_TABLE,
    TAGS_XLSX, TAGS_DB, TAGS_TABLE,
    OFFERINGS_XLSX, OFFERINGS_DB, OFFERINGS_TABLE,
)

JOBS = {
    "suppliers": (SUPPLIERS_XLSX, SUPPLIERS_DB, SUPPLIERS_TABLE),
    "tags": (TAGS_XLSX, TAGS_DB, TAGS_TABLE),
    "data": (OFFERINGS_XLSX, OFFERINGS_DB, OFFERINGS_TABLE),
}


def convert(xlsx_path: str, db_path: str, table_name: str):
    df = pd.read_excel(xlsx_path)

    # sqlite has no native "id" unless we add one; keep an explicit
    # autoincrement id column so the frontend can link to /offerings/{id}
    df.insert(0, "id", range(1, len(df) + 1))

    conn = sqlite3.connect(db_path)
    df.to_sql(table_name, conn, if_exists="replace", index=False)
    conn.close()
    print(f"Wrote {len(df)} rows from {xlsx_path} -> {db_path} [{table_name}]")


if __name__ == "__main__":
    target = sys.argv[1] if len(sys.argv) > 1 else "all"

    if target == "all":
        for name, (xlsx, db, table) in JOBS.items():
            convert(xlsx, db, table)
    elif target in JOBS:
        convert(*JOBS[target])
    else:
        print(f"Unknown target '{target}'. Choose one of: {', '.join(JOBS)}, all")
        sys.exit(1)
