"""
uvicorn main:app --reload --port 8000

Endpoints:
  GET /suppliers                        -> all suppliers (Supplier Info page)
  GET /suppliers/company/{name}         -> one supplier by name (Supplier Info detail)
  GET /meta/last-updated                -> ISO date string for the Home page badge
  GET /tags                             -> all rows from tags.db (Tag, Keywords, Profession)
  GET /professions                      -> distinct professions, for a filter dropdown
  GET /offerings                        -> offerings, with optional filters + smart search
  GET /offerings/{offering_id}          -> one offering by id
"""

import datetime
import os
from urllib.parse import unquote

from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware

from config import (
    SUPPLIERS_DB,
    OFFERINGS_DB,
    TAGS_DB,
    SUPPLIERS_TABLE,
    OFFERINGS_TABLE,
    TAGS_TABLE,
    REACT_ORIGIN,
    LAST_UPDATED_OVERRIDE,
)
from db import fetch_all, fetch_one, table_exists
import search as search_mod

app = FastAPI(title="Supply Search API")
app.add_middleware(
    CORSMiddleware,
    allow_origins=[REACT_ORIGIN],
    allow_methods=["*"],
    allow_headers=["*"],
)


# ---------------------------------------------------------------------------
# Home page
# ---------------------------------------------------------------------------

@app.get("/meta/last-updated")
def last_updated():
    if LAST_UPDATED_OVERRIDE:
        return {"last_updated": LAST_UPDATED_OVERRIDE}

    newest = None
    for path in (SUPPLIERS_DB, OFFERINGS_DB, TAGS_DB):
        if os.path.exists(path):
            mtime = os.path.getmtime(path)
            if newest is None or mtime > newest:
                newest = mtime

    if newest is None:
        return {"last_updated": None}

    return {"last_updated": datetime.datetime.fromtimestamp(newest).strftime("%Y-%m-%d")}


# ---------------------------------------------------------------------------
# Supplier Info page (browse suppliers.xlsx data, link embedded in name)
# ---------------------------------------------------------------------------

@app.get("/suppliers")
def get_suppliers():
    if not table_exists(SUPPLIERS_DB, SUPPLIERS_TABLE):
        return []
    return fetch_all(SUPPLIERS_DB, f"SELECT * FROM {SUPPLIERS_TABLE}")


@app.get("/suppliers/company/{supplier_name}")
def get_supplier_by_name(supplier_name: str):
    supplier_name = unquote(supplier_name)
    row = fetch_one(
        SUPPLIERS_DB,
        f'SELECT * FROM {SUPPLIERS_TABLE} WHERE "Supplier Name" = ?',
        (supplier_name,),
    )
    if row is None:
        return {"error": "Supplier not found"}
    return row


# ---------------------------------------------------------------------------
# Supplier Search page (data.xlsx offerings, filters + smart search)
# ---------------------------------------------------------------------------

@app.get("/tags")
def get_tags():
    if not table_exists(TAGS_DB, TAGS_TABLE):
        return []
    return fetch_all(TAGS_DB, f"SELECT * FROM {TAGS_TABLE}")


@app.get("/professions")
def get_professions():
    if not table_exists(TAGS_DB, TAGS_TABLE):
        return []
    rows = fetch_all(TAGS_DB, f"SELECT DISTINCT Profession FROM {TAGS_TABLE} WHERE Profession IS NOT NULL")
    return sorted({r["Profession"] for r in rows if r["Profession"]})


def _tag_to_profession_map() -> dict:
    """Tags.xlsx maps Tag -> Profession, so an offering's Tags column can be
    joined against it to know which profession(s) an offering serves."""
    if not table_exists(TAGS_DB, TAGS_TABLE):
        return {}
    rows = fetch_all(TAGS_DB, f"SELECT Tag, Profession FROM {TAGS_TABLE}")
    return {r["Tag"]: r["Profession"] for r in rows if r.get("Tag")}


@app.get("/offerings")
def get_offerings(
    q: str | None = Query(None, description="Free-text 'search by description' box"),
    supplier: str | None = None,
    type: str | None = None,
    tag: str | None = None,
    profession: str | None = None,
    keyword: str | None = None,
):
    if not table_exists(OFFERINGS_DB, OFFERINGS_TABLE):
        return []

    rows = fetch_all(OFFERINGS_DB, f"SELECT * FROM {OFFERINGS_TABLE}")

    tag_to_profession = _tag_to_profession_map()
    for row in rows:
        row_tags = [t.strip() for t in str(row.get("Tags", "")).split(",") if t.strip()]
        row["Profession"] = ", ".join(
            sorted({tag_to_profession[t] for t in row_tags if t in tag_to_profession})
        )

    # ---- hard filters (exact/substring, from dropdowns) ----
    if supplier:
        rows = [r for r in rows if r.get("Supplier Name", "").lower() == supplier.lower()]
    if type:
        rows = [r for r in rows if r.get("Type", "").lower() == type.lower()]
    if tag:
        rows = [r for r in rows if tag.lower() in [t.strip().lower() for t in str(r.get("Tags", "")).split(",")]]
    if profession:
        rows = [r for r in rows if profession.lower() in r.get("Profession", "").lower()]
    if keyword:
        kw = keyword.lower()
        rows = [
            r for r in rows
            if kw in " ".join(str(v) for v in r.values()).lower()
        ]

    # ---- smart free-text search ("GUI library" style queries) ----
    if q:
        known_tags = sorted({t.strip() for r in rows for t in str(r.get("Tags", "")).split(",") if t.strip()})
        known_professions = sorted({r["Profession"] for r in rows if r.get("Profession")})
        rows = search_mod.rank_offerings(rows, q, known_tags, known_professions)

    return rows


@app.get("/offerings/{offering_id}")
def get_offering(offering_id: int):
    row = fetch_one(OFFERINGS_DB, f"SELECT * FROM {OFFERINGS_TABLE} WHERE id = ?", (offering_id,))
    if row is None:
        return {"error": "Offering not found"}
    return row
