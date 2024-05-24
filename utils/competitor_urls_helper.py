# Standard library import
import random
import gzip
import traceback
import re
from time import sleep
import re
from collections import defaultdict
from bs4 import BeautifulSoup

import re
from collections import defaultdict
import pandas as pd
# Third-party library import
import requests
from pymongo import UpdateOne
from random_user_agent.user_agent import UserAgent
from random_user_agent.params import SoftwareName, OperatingSystem
import pandas as pd
from bs4 import BeautifulSoup
# local application import
from config.index import DB_NAME, PROXY_CSV_URL
from services.mongo_db.connection import mongoConnection
from utils.slack import send_slack_message
from config.index import API_KEY_SCRAPY
from datetime import datetime, date
from dateutil.parser import parse
from utils.slack import error_slack_message

db = mongoConnection()[DB_NAME]
session = requests.Session()

SCRAPPING_URLS = False
URLS_STATUS = "initial"


def get_proxies():
    try:
        software_names = [SoftwareName.CHROME.value]
        operating_systems = [OperatingSystem.WINDOWS.value,
                             OperatingSystem.LINUX.value]
        user_agent_rotator = UserAgent(
            software_names=software_names, operating_systems=operating_systems, limit=100)
        user_agent = user_agent_rotator.get_random_user_agent()
        headers = {
            'Accept': '*/*',
            'Accept-Language': 'en-GB,en-US;q=0.9,en;q=0.8',
            'User-Agent': user_agent
        }
        req = request_with_retry("get", PROXY_CSV_URL, '')
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


def request_with_retry(method, url, competitor, proxies={}, headers={}, **kwargs):
    try:
        okay = False
        retry_after = 1
        retries = 3
        response = None
        while not okay and retries:
            if method == "get":
                response = session.get(
                    url, proxies=proxies, headers=headers, **kwargs)
            elif method == "post":
                response = session.post(
                    url, proxies=proxies, headers=headers, **kwargs)
            okay = response.status_code == 200
            if not okay:
                sleep(retry_after)
            retries -= 1
            retry_after *= 2
        if response.status_code not in [200, 404]:
            filter = {
                "url": url,
                "competitor": competitor
            }
            db.faulty_urls.update_one(filter, {"$set": filter}, True)
        return response
    except Exception as e:
       error_slack_message(e)

def get_date_time():
    today = date.today()
    now = datetime.now()
    d2 = today.strftime("%B %d, %Y")
    current_time = now.strftime("%H:%M:%S")
    date_time = f"{d2} {current_time}"
    date_time = parse(date_time)
    return date_time

def url_insert_bulk(data, from_manufacturer = False):
    try:
        if type(data) is not list or len(data) == 0:
            return
        send_slack_message(f'Inserting into Mongo DB: {data[0]["competitor"]}')
        rows = []
        for item in data:
            filter = {
                "competitor": item["competitor"],
                "url": item["url"],
                "scraper_type": item["scraper_type"]
            }            
            if from_manufacturer:
                item['from_manufacturer'] = True
            item['captured_at'] = get_date_time()
            
            rows.append(UpdateOne(filter, {"$set": item}, True))
        db.competitor_url.bulk_write(rows)
    except Exception as e:
        error_slack_message(e)


def download_gz_file(competitor_name, url, count):
    scrape_api = f'https://api.scraperapi.com/?api_key={API_KEY_SCRAPY}&url={url}'
    # response = requests.get(scrape_api)
    proxies, headers = get_proxies()
    response = request_with_retry(
        "get", scrape_api, competitor_name, proxies=proxies, headers=headers)
    if competitor_name == 'us.rs-online':
        open(f"sitemap-rs{str(count)}.xml.gz", "wb").write(response.content)
    else:
        open("sitemap-" + competitor_name + str(count) + ".xml.gz", "wb").write(response.content)


def read_gz_file(url):
    f = gzip.open(url, 'rb')
    return f.read()


def url_insert(item):
    try:
        # send_slack_message("inside url_insert mongo")
        if type(item) is not dict:
            return
        filter = {
            "competitor": item["competitor"],
            "url": item["url"],
            "scraper_type": item["scraper_type"]
        }
        item['captured_at'] = get_date_time()
        db.competitor_url.update_one(filter, {"$setOnInsert": item}, True)
    except Exception as e:
        message = f"Error: {str(e)}" + "\n" + traceback.format_exc()
        print(message)
        send_slack_message(message)

def preprocess_manufacturers():
    amp_manufacturers_list = pd.read_csv('manufacturers_amplify.csv')
    manufacturers_list = amp_manufacturers_list['Manufacturer'].unique()
    manufacturers_dict = defaultdict(set)
    for manufacturer in manufacturers_list:
        clean_manufacturer = clean_string(manufacturer)
        manufacturer_words = set(clean_manufacturer.split())
        manufacturers_dict[clean_manufacturer] = manufacturer_words
    return manufacturers_dict

def check_is_whole_word(word, text):
    pattern = r'\b{}\b'.format(re.escape(word))
    return bool(re.search(pattern, text))

clean_string_pattern = re.compile(r'[^\x00-\x7F]+|[^a-zA-Z0-9\s]')

def clean_string(string, remove_company_status=False):
    clean_string_text = string.strip().lower()
    if remove_company_status:
        company_status = ['corporation', 'incorporated', 'controls', 'industrial', 'networks', 'company', 'electric', 'automation', 'switch', 'products', 'international', 'electronic','usa', 'connector', 'components', 'switzerland', 'solutions', 'tool', 'power', 'group', 'energy', 'filter', 'components', 'protection', 'devices', 'test', 'instruments', 'america', 'sensors', 'sensor' 'technologies', 'industries', 'systems', 'manufacturing','group', 'corp.', 'motors', 'inc', 'llc', 'corp', 'ltd', 'tech', 'lighting', 'technology', 'electronics']

        for status in company_status:
            if check_is_whole_word(status, clean_string_text):
                clean_string_text = clean_string_text.replace(status, '')
    clean_string_text = clean_string_pattern.sub(' ', clean_string_text)
    clean_string_text = re.sub(' +', ' ', clean_string_text)
    return clean_string_text

def get_sitemap_urls(url_to_parse, competitor):
    software_names = [SoftwareName.CHROME.value]
    operating_systems = [
            OperatingSystem.WINDOWS.value, OperatingSystem.LINUX.value]
    user_agent_rotator = UserAgent(software_names=software_names, operating_systems=operating_systems, limit=100)
    user_agent = user_agent_rotator.get_random_user_agent()
    headers = {'User-Agent': user_agent, 'Accept-Encoding': 'gzip, deflate, br', 'Accept-Language': 'en-US,en;q=0.9'}
    page = requests.get(url_to_parse, headers=headers)

    if page.status_code != 200:
        message = f"Error: {competitor} {page.text}"
        send_slack_message(message)
    sitemap_index = BeautifulSoup(page.content, 'xml')  # Use XML parser explicitly
    return [element.text for element in sitemap_index.findAll('loc')]

def check_manufacturer_match(manufacturers_dict, product_title):
    clean_product_title = clean_string(product_title, remove_company_status=True)
    product_words = {
        word for word in clean_product_title.split() if len(word) >= 2
    }

    return any(
        manufacturer_words.intersection(product_words)
        for _, manufacturer_words in manufacturers_dict.items()
    )