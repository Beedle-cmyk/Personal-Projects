"""
Central configuration for the supply-search backend.

Edit the paths below (or set the matching environment variables) to point
at your actual .xlsx source files and the .db files produced by
scripts/converter.py.
"""

import os
from pathlib import Path

BASE_DIR = Path(r"C:\Personal-Projects\supply-search\data")

# ---- SQLite databases (produced by scripts/converter.py) ----
SUPPLIERS_DB = os.environ.get("SUPPLIERS_DB", str(BASE_DIR / "suppliers.db"))
OFFERINGS_DB = os.environ.get("OFFERINGS_DB", str(BASE_DIR / "data.db"))
TAGS_DB = os.environ.get("TAGS_DB", str(BASE_DIR / "tags.db"))

# ---- Source spreadsheets (used by the pipeline scripts) ----
SUPPLIERS_XLSX = os.environ.get("SUPPLIERS_XLSX", str(BASE_DIR / "suppliers.xlsx"))
OFFERINGS_XLSX = os.environ.get("OFFERINGS_XLSX", str(BASE_DIR / "data.xlsx"))
TAGS_XLSX = os.environ.get("TAGS_XLSX", str(BASE_DIR / "tags.xlsx"))

# ---- Table names inside each db ----
SUPPLIERS_TABLE = "suppliers"
OFFERINGS_TABLE = "offerings"
TAGS_TABLE = "tags"

# ---- CORS ----
REACT_ORIGIN = os.environ.get("REACT_ORIGIN", "http://localhost:5173")

# ---- Anthropic (used by scripts/tag_offerings.py and search.py) ----
ANTHROPIC_MODEL = os.environ.get("ANTHROPIC_MODEL", "claude-sonnet-4-6")
# The API key is read from the ANTHROPIC_API_KEY environment variable
# automatically by the anthropic SDK - do not hardcode it here.

# ---- Misc ----
# Shown on the Home page. Update this whenever you re-run the pipeline,
# or leave as None to have the backend report the newest db file's
# modified-time instead (see /meta/last-updated in main.py).
LAST_UPDATED_OVERRIDE = os.environ.get("LAST_UPDATED_OVERRIDE")  # e.g. "2026-09-04"
