# Supply Search

## Layout

```
backend/
  config.py              <- edit paths here (xlsx sources + db outputs)
  db.py                  <- sqlite helpers
  search.py              <- "search by description" query expansion
  main.py                <- FastAPI app (run this)
  requirements.txt
  scripts/
    converter.py         <- xlsx -> sqlite, for all three sheets
    fetch_supplier_urls.py  <- Step 1 (suppliers.xlsx URL column)
    crawl_offerings.py      <- Step 2/3 (data.xlsx from sitemaps)
    tag_offerings.py        <- Step 4 (data.xlsx Tags column via Claude)
frontend/
  src/
    App.jsx              <- routes
    Home.jsx              <- landing page, last-updated badge
    SupplierInfo.jsx       <- suppliers.xlsx browser (was SupplierTable.jsx)
    SupplierSearch.jsx     <- data.xlsx offerings search + filters
    SupplierDetails.jsx    <- one supplier's full record
    config.js               <- API_BASE URL
```

## One-time setup

```
cd backend
pip install -r requirements.txt
setx ANTHROPIC_API_KEY "sk-ant-..."     # or export on macOS/Linux
```

Edit `backend/config.py` if your xlsx files or output folder differ from
`C:\Personal-Projects\supply-search\data\`.

## Data pipeline (run in this order, whenever source data changes)

```
cd backend/scripts

# 1. suppliers.xlsx: fill in missing URLs
python fetch_supplier_urls.py
python converter.py suppliers

# 2. tags.xlsx -> tags.db (no generation needed, just convert)
python converter.py tags

# 3. data.xlsx: discover offerings from each supplier's sitemap
python crawl_offerings.py

# 4. data.xlsx: assign tags to each offering via Claude
python tag_offerings.py
python converter.py data
```

Rows the crawler couldn't classify are written with `Type = "NEEDS REVIEW"`
in data.xlsx - filter on that column to find suppliers whose site needs a
manual look (no sitemap, blocked robots.txt, etc).

## Run the app

```
# terminal 1
cd backend
uvicorn main:app --reload --port 8000

# terminal 2
cd frontend
npm install
npm run dev
```

Open http://localhost:5173 - Home page links to Supplier Search (offerings,
smart search + filters) and Supplier Info (full supplier directory).
