import requests
from bs4 import BeautifulSoup
from utils.helpers.index import error_slack_message, url_insert_bulk
from utils.slack import send_slack_message

from config.index import API_KEY_SCRAPY


COMPETITOR = "breakerauthority"
URL = 'https://breakerauthority.com/sitemap.xml'


def get_and_store_breakerauthority_urls():
    try:
        scrape_api = f'https://api.scraperapi.com/?api_key={API_KEY_SCRAPY}&url={URL}&render=true'
        page = requests.get(scrape_api)
        if page.status_code != 200:
            message = f"Error:  {COMPETITOR} {page.text}"
            send_slack_message(message)
        sitemap_index = BeautifulSoup(page.content, 'html.parser')
        sitemap_url = [
            element.text for element in sitemap_index.findAll('loc')]
        outputs = []
        for data in sitemap_url:
            if '/product-s' in data:
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
