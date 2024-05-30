import requests
from bs4 import BeautifulSoup

from utils.helpers.index import url_insert_bulk, error_slack_message
from utils.slack import send_slack_message


COMPETITOR = "dkhardware"
URL = 'https://www.dkhardware.com/sitemap.xml'


def get_and_store_dkhardware_urls():
    try:
        page = requests.get(URL)
        if page.status_code != 200:
            message = "Error: "+COMPETITOR + page.text
            send_slack_message(message)
        outputs = []
        sitemap_index = BeautifulSoup(page.content, 'html.parser')
        urls = [element.text for element in sitemap_index.findAll('loc')]
        for data in urls:
            if '/products' in data:
                output = requests.get(data)
                sitemap_url = BeautifulSoup(output.content, 'html.parser')
                output_result = [o.text for o in sitemap_url.findAll('loc')]
                for i in output_result:
                    result = {
                        "competitor": COMPETITOR,
                        "url": i,
                        "scraper_type": "sitemap"
                    }

                    outputs.append(result)
                    if len(outputs) == 5000:
                        url_insert_bulk(outputs)
                        outputs = []
        if outputs and len(outputs):
            url_insert_bulk(outputs)
    except Exception as e:
        error_slack_message(e)
