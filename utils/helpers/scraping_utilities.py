# Standard library import
import random
import gzip
from time import sleep

# Third-party library import
import requests
from random_user_agent.user_agent import UserAgent
from random_user_agent.params import SoftwareName, OperatingSystem
from bs4 import BeautifulSoup

# local application import
from config.index import PROXY_CSV_URL
from utils.slack import send_slack_message
from config.index import API_KEY_SCRAPY
from utils.slack import error_slack_message
import os

session = requests.Session()


def get_proxies():
    try:
        software_names = [SoftwareName.CHROME.value]
        operating_systems = [
            OperatingSystem.WINDOWS.value,
            OperatingSystem.LINUX.value,
        ]
        user_agent_rotator = UserAgent(
            software_names=software_names,
            operating_systems=operating_systems,
            limit=100,
        )
        user_agent = user_agent_rotator.get_random_user_agent()
        headers = {
            "Accept": "*/*",
            "Accept-Language": "en-GB,en-US;q=0.9,en;q=0.8",
            "User-Agent": user_agent,
        }
        req = request_with_retry("get", PROXY_CSV_URL, "")
        url_content = req.content
        url_content = url_content.decode()
        urls = url_content.split("\n")
        random_url = random.choice(urls)
        random_url = random_url.split(":")
        proxy_url = f"http://{random_url[2]}:{random_url[3]}@{random_url[0]}:{random_url[1]}"
        proxies = {"http": proxy_url, "https": proxy_url}
        return proxies, headers
    except Exception as e:
        error_slack_message(e)
        return {}, {}


def request_with_retry(
    method, url, proxies={}, headers={}, retries=3, **kwargs
):
    try:
        okay = False
        retry_after = 1
        response = None
        while not okay and retries:
            if method == "get":
                response = session.get(
                    url, proxies=proxies, headers=headers, **kwargs
                )
            elif method == "post":
                response = session.post(
                    url, proxies=proxies, headers=headers, **kwargs
                )
            okay = response.status_code == 200
            if not okay:
                sleep(retry_after)
            retries -= 1
            retry_after *= 2
        return response
    except Exception as e:
        error_slack_message(e)


def download_gz_file(
    competitor_name,
    url,
    count,
    ultra_premium=False,
    premium=False,
    render=False,
):
    try:
        scrape_api = (
            f"https://api.scraperapi.com/?api_key={API_KEY_SCRAPY}&url={url}"
        )

        if ultra_premium:
            scrape_api = f"{scrape_api}&ultra_premium=true"
        elif premium:
            scrape_api = f"{scrape_api}&premium=true"
        if render:
            scrape_api = f"{scrape_api}&render=true"

        # response = requests.get(scrape_api)
        proxies, headers = get_proxies()
        response = request_with_retry(
            "get", scrape_api, proxies=proxies, headers=headers
        )
        if competitor_name == "us.rs-online":
            file_name = f"sitemap-rs{str(count)}.xml.gz"
        else:
            file_name = f"sitemap-{competitor_name}{str(count)}.xml.gz"
        file_path = os.path.join("trash", file_name)
        with open(file_path, "wb") as file:
            file.write(response.content)
        return file_path
    except Exception as e:
        error_slack_message(e)
        return None


def read_gz_file(url):
    try:
        f = gzip.open(url, "rb")
        return f.read()
    except Exception as e:
        error_slack_message(e)
        return None


def get_sitemap_urls(url_to_parse, competitor):
    try:
        proxies, headers = get_proxies()
        page = requests.get(url_to_parse, headers=headers, proxies=proxies)

        if page.status_code != 200:
            message = f"Error: {competitor} {page.text}"
            error_slack_message(message, "error")
        sitemap_index = BeautifulSoup(
            page.content, "xml"
        )  # Use XML parser explicitly
        found_urls = [element.text for element in sitemap_index.findAll("loc")]

        print(f"Total URLs: {len(found_urls)} for {url_to_parse}")

        return found_urls
    except Exception as e:
        error_slack_message(e)
        return []


def get_page_with_scraperapi_from_url(
    url, competitor, is_premium=False, is_ultra_premium=False, is_render=False
):
    try:
        scrape_api = (
            f"https://api.scraperapi.com/?api_key={API_KEY_SCRAPY}&url={url}"
        )

        if is_ultra_premium:
            scrape_api = f"{scrape_api}&ultra_premium=true"
        elif is_premium:
            scrape_api = f"{scrape_api}&premium=true"

        if is_render:
            scrape_api = f"{scrape_api}&render=true"

        proxies, headers = get_proxies()
        page = None
        try:
            page = request_with_retry(
                "get", scrape_api, proxies=proxies, headers=headers
            )
        except Exception as e:
            error_slack_message(e)
            return

        if page.status_code != 200:
            message = f"Error: {competitor} {page.text}"
            send_slack_message(message, "error")
            return

        return BeautifulSoup(page.content, "html.parser")
    except Exception as e:
        error_slack_message(e)


def get_page_from_url(url, competitor, stream=False, verify=True):
    try:
        proxies, headers = get_proxies()
        page = None
        try:
            page = requests.get(
                url,
                proxies=proxies,
                headers=headers,
                stream=stream,
                verify=verify,
            )
        except Exception as e:
            error_slack_message(e)

        if page.status_code != 200:
            message = f"Error: {competitor}{page.text}"
            send_slack_message(message, "error")

        return BeautifulSoup(page.text, "html.parser")
    except Exception as e:
        error_slack_message(e)
