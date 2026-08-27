import sqlite3
import pandas as pd

from pathlib import Path

EXCEL_FILE = r"C:\Personal-Projects\supply-search\doc_list\TEST.xlsx"

def convert_to_db(excel_file) -> str | Path:
    """
    Converts the provided excel file into a separate database file
    This is stored in the same directory as the excel file location

    Args:
        excel_file : the excel file to convert
    
    Returns:
        Path to excel database file

    """
    df = pd.read_excel(excel_file)
    db_path = Path(excel_file).parent / "suppliers.db"

    con = sqlite3.connect(db_path)
    df.to_sql("suppliers", con, if_exists="replace", index=False)
    print(f"Imported {len(df)} suppliers")

    df = pd.read_sql_query(
        "SELECT * FROM suppliers LIMIT 10", con
    )
    print(df)
    con.close()
    return db_path



if __name__ == '__main__':
    convert_to_db(EXCEL_FILE)