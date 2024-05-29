from bs4 import BeautifulSoup

from utils.helpers.index  import read_gz_file, url_insert_bulk


def store_data(url):
    outputs = []
    file_content = read_gz_file(url)
    bs_data = BeautifulSoup(file_content, 'xml')
    b_unique = bs_data.find_all('loc')
    for data in b_unique:
        data = str(data)
        if data.startswith("<loc>") and data.endswith("</loc>"):
            data = data.replace("<loc>", "")
            data = data.replace("</loc>", "")
            if "/product" in data:
                result = {
                    "competitor": "kele",
                    "url": data,
                    "scraper_type": "sitemap"
                }
                outputs.append(result)
                if len(outputs) == 5000:
                    url_insert_bulk(outputs)
                    outputs = []
    if outputs and len(outputs):
        url_insert_bulk(outputs)
