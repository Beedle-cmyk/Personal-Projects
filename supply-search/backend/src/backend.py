from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

import sqlite3

REACT_LINK = "http://localhost:5173"
DATABASE_PATH = r"C:\Personal-Projects\supply-search\doc_list\suppliers.db"

app = FastAPI()
app.add_middleware(CORSMiddleware, allow_origins=[REACT_LINK], allow_methods=["*"], allow_headers=["*"])

# get request via fetch from App.jsx
@app.get("/suppliers")
def get_suppliers():

    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row

    rows = conn.execute("SELECT * FROM suppliers").fetchall()
    conn.close()

    return [dict(row) for row in rows]
