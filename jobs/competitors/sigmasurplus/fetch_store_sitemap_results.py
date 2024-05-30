import requests

from bs4 import BeautifulSoup

from utils.helpers.index import url_insert_bulk, remove_outdated_urls
from utils.slack import send_slack_message, error_slack_message

COMPETITOR = "sigmasurplus"
MAX_COUNT = 5000


def get_and_store_sigmasurplus_urls():
    try:
        remove_outdated_urls(COMPETITOR)
        url = "https://sigmasurplus.com/xmlsitemap.php"
        page = requests.get(url, stream=True)

        outputs = []
        if page.status_code != 200:
            message = f"Error: sigmasurplus {page.text}"
            send_slack_message(message)

        sitemap_index = BeautifulSoup(page.content, "html.parser")
        urls = [element.text for element in sitemap_index.findAll("loc")]
        for data in urls:
            if "product" in data:
                print(data)
                sitemap = requests.get(data)
                result_index = BeautifulSoup(sitemap.content, "html.parser")
                try:
                    for element in result_index.findAll("loc"):
                        result = {
                            "competitor": "sigmasurplus",
                            "url": element.text,
                            "scraper_type": "sitemap",
                        }
                        outputs.append(result)
                        if len(outputs) == 5000:
                            url_insert_bulk(outputs)
                            outputs = []
                except Exception as e:
                    message = "Loop breaking"
                    send_slack_message(message)
        if outputs and len(outputs):
            url_insert_bulk(outputs)
    except Exception as e:
        error_slack_message(e)
