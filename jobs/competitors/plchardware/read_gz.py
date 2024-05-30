import gzip
from bs4 import BeautifulSoup
from utils.helpers.index import url_insert_bulk

MAX_COUNT = 5000

def store_data(url):
    outputs = []
    f = gzip.open(url, 'rb')
    file_content = f.read()
    bs_data = BeautifulSoup(file_content, 'xml')
    b_unique = bs_data.find_all('loc')
    for data in b_unique:
        data = str(data)
        if data.startswith("<loc>") and data.endswith("</loc>"):
            data = data.replace("<loc>", "")
            data = data.replace("</loc>", "")
            if "/Product" in data:
                result = {
                    "competitor": "plchardware",
                    "url": data,
                    "scraper_type": "sitemap"
                }
                outputs.append(result)
                if len(outputs) >= MAX_COUNT:
                    url_insert_bulk(outputs)
                    outputs = []
    if outputs and len(outputs):
        url_insert_bulk(outputs)