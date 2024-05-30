from bs4 import BeautifulSoup
from random_user_agent.user_agent import UserAgent
from random_user_agent.params import SoftwareName, OperatingSystem

from services.slack.slack_message import send_slack_message
from utils.helpers.index import url_insert_bulk, request_with_retry, get_proxies, error_slack_message

COMPETITOR = "chartercontact"
URL = 'http://www.chartercontact.com/sitemap.xml'


def get_and_store_chartercontact_urls():
    try:
        outputs = []
        software_names = [SoftwareName.CHROME.value]
        operating_systems = [
            OperatingSystem.WINDOWS.value, OperatingSystem.LINUX.value]
        user_agent_rotator = UserAgent(
            software_names=software_names, operating_systems=operating_systems, limit=100)
        user_agent = user_agent_rotator.get_random_user_agent()
        headers = {
            'Accept': '*/*',
            'Accept-Language': 'en-GB,en-US;q=0.9,en;q=0.8',
            'User-Agent': user_agent,
            'X-Requested-With': 'XMLHttpRequest'
        }
        proxies, headers = get_proxies()
        page = request_with_retry(
            "get", URL, COMPETITOR, proxies=proxies, headers=headers)

        if page.status_code != 200:
            message = f"Error: {COMPETITOR}{page.text}"
            send_slack_message(message)
        sitemap_index = BeautifulSoup(page.content, 'html.parser')
        urls = [element.text for element in sitemap_index.findAll('loc')]
        for i in urls:
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
