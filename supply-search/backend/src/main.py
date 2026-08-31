from webscraper import Webscraper

EXCEL_FILE = r"C:\Personal-Projects\supply-search\doc_list\TEST.xlsx"

def main():
    wb = Webscraper(EXCEL_FILE)
    wb.update(
    wb.generate_links()
    )

if __name__ == '__main__':
    main()