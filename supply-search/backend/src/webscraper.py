from utils import converter
from pathlib import Path
from bs4 import BeautifulSoup

import sqlite3
import requests

KEYWORDS = [
    "product",
    "products",
    "service",
    "services",
    "solution",
    "solutions",
    "materials",
    "about"
]

class Webscraper:

    def __init__(self, xlsx_file : Path | str):
        """ 
        Initializes a webscraper object. Converts the provided xlsx file (without replacement) into a
        sqlLite compatible db file

        Args:
            xlsx_file : path to xlsx file
        
        Returns:
            None
        """

        self.data_base = converter.convert_to_db(xlsx_file)
        self.con = sqlite3.connect(Path(self.data_base).parent / "suppliers.db")
        cursor = self.con.execute(
            "SELECT [Supplier Name] FROM suppliers"
        )
        self.supplier_list = [row[0] for row in cursor.fetchall()]



    def close_connection(self) -> bool:
        """
        Closes the sqlite3 connection
        
        Args:
            None
        
        Returns:
            bool indicating if connection closed successfully
        """
        return self.con.close()

        
    def update(self):
        
        pass