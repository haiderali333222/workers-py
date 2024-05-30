from bs4 import BeautifulSoup

from utils.helpers.index import url_insert_bulk, read_gz_file, error_slack_message

MAX_COUNT = 5000


def store_data(url):
    try:
        outputs = []
        file_content = read_gz_file(url)
        bs_data = BeautifulSoup(file_content, "xml")
        b_unique = bs_data.find_all("loc")
        for data in b_unique:
            data = str(data)
            if data.startswith("<loc>") and data.endswith("</loc>"):
                data = data.replace("<loc>", "")
                data = data.replace("</loc>", "")
                result = {
                    "competitor": "gordonelectricsupply",
                    "url": data,
                    "scraper_type": "sitemap",
                }
                outputs.append(result)
                if len(outputs) == MAX_COUNT:
                    url_insert_bulk(outputs)
                    outputs = []
        if outputs and len(outputs):
            url_insert_bulk(outputs)
    except Exception as e:
        error_slack_message(e)
