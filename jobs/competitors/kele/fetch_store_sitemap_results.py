from .helper import BeautifulSoup,store_data
from utils.helpers.index  import request_with_retry, get_proxies, download_gz_file, error_slack_message
from services.slack.slack_message import send_slack_message


COMPETITOR = 'kele'
URL = 'https://www.kele.com/sitemap-index.xml'


def get_and_store_kele_urls():
    try:
        message = "start getting url for "+COMPETITOR
        send_slack_message(message)
        proxies, headers = get_proxies()
        page = request_with_retry(
            "get", URL, COMPETITOR, proxies=proxies, headers=headers)
        if page.status_code != 200:
            message = "Error: "+COMPETITOR + page.text
            send_slack_message(message)
        sitemap_index = BeautifulSoup(page.content, 'html.parser')
        sitemap_url = [
            element.text for element in sitemap_index.findAll('loc')]
        count = 0
        for data in sitemap_url:
            if '.gz' in data:
                count += 1
                download_gz_file(COMPETITOR, data, count)
                store_data("sitemap-"+COMPETITOR+str(count)+".xml.gz")
    except Exception as e:
        error_slack_message(e)
