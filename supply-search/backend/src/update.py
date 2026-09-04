import xml.etree.ElementTree as ET
from urllib.parse import urlparse
import pandas as pd

SUPPLIER_NAME = "3D Systems"

excel_file = r"C:\Personal-Projects\supply-search\doc_list\offerings.xlsx"
sitemap_file = r"C:\Personal-Projects\supply-search\doc_list\sitemap-product-1.xml"

def product_name_from_url(url: str) -> str:
    """
    Converts:
    https://shop.3dsystems.com/s/product/epm-filter-pleated/01t34000004ANunAAG?language=en_US

    Into:
    Epm Filter Pleated
    """
    parts = urlparse(url).path.split("/")

    try:
        product_index = parts.index("product")
        slug = parts[product_index + 1]
        return slug.replace("-", " ").title()
    except (ValueError, IndexError):
        return "Unknown Product"


# Load spreadsheet
df = pd.read_excel(excel_file)

# Find supplier row
matches = df.index[df["Supplier Name"].astype(str).str.strip() == SUPPLIER_NAME]

if len(matches) == 0:
    print(f"Supplier '{SUPPLIER_NAME}' not found.")
    raise SystemExit()

supplier_row = matches[0]

print(f"Found supplier at row {supplier_row}")

# Parse sitemap XML
tree = ET.parse(sitemap_file)
root = tree.getroot()

namespace = {
    "sm": "http://www.sitemaps.org/schemas/sitemap/0.9"
}

urls = []

for url_tag in root.findall("sm:url", namespace):
    loc = url_tag.find("sm:loc", namespace)

    if loc is not None and loc.text:
        urls.append(loc.text)

print(f"Found {len(urls)} URLs")

# Build new rows
new_rows = []

for url in urls:
    product_name = product_name_from_url(url)

    new_rows.append({
        "Supplier Name": "",
        "Type": "Product",
        "Offering Name": product_name,
        "URL": url
    })

# Insert rows directly below supplier
top = df.iloc[:supplier_row + 1]
bottom = df.iloc[supplier_row + 1:]

insert_df = pd.DataFrame(new_rows)

result = pd.concat(
    [top, insert_df, bottom],
    ignore_index=True
)

output_file = r"C:\Personal-Projects\supply-search\doc_list\offerings_updated.xlsx"

result.to_excel(output_file, index=False)

print(f"Done. Saved to: {output_file}")