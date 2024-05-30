import requests

from random_user_agent.user_agent import UserAgent
from random_user_agent.params import SoftwareName, OperatingSystem
from bs4 import BeautifulSoup

from utils.helpers.index import (
    download_gz_file,
    error_slack_message,
    preprocess_manufacturers,
    get_sitemap_urls,
)
from utils.slack import send_slack_message

from .helper import store_data

COMPETITOR = "zoro"
URL = "https://www.zoro.com/sitemaps/usa/sitemap-index.xml"


def get_and_store_zoro_urls():
    try:
        count = 0

        sitemap_url = get_sitemap_urls(URL, COMPETITOR)
        manufacturers_dict = preprocess_manufacturers()

        for data in sitemap_url:
            if "product-" in data:
                count += 1
                path = download_gz_file(COMPETITOR, data, count)
                store_data(path, manufacturers_dict)
    except Exception as e:
        error_slack_message(e)
