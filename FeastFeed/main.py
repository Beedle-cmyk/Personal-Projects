from bs4 import BeautifulSoup
import requests

# Option 1: read from saved file
with open("temp.xml", "r", encoding="utf-8") as f:
    doc = BeautifulSoup(f.read(), "xml")

# Option 2: fetch live feed (uncomment if you want fresh data)
# url = "https://www.washington.edu/calendar/feed"
# resp = requests.get(url)
# doc = BeautifulSoup(resp.text, "xml")

for item in doc.find_all("item"):
    title = item.title.text if item.title else None
    link = item.link.text if item.link else None
    date = item.pubDate.text if item.pubDate else None
    print(title, link, date)
