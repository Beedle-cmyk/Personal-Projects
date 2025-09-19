from bs4 import BeautifulSoup 
import requests

url = "https://huskylink.washington.edu/event/11411956"
result = requests.get(url)
doc = BeautifulSoup(result.text, 'html.parser')
print(doc.prettify())