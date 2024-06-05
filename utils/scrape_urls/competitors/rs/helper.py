import re

from bs4 import BeautifulSoup

from utils.helpers.index import (
    clean_string,
    preprocess_manufacturers,
    read_gz_file,
    url_insert_bulk,
)
from utils.slack import detailed_error_slack_message

COMPETITOR = "us.rs-online"


def extract_manufacturer_from_url(url):
    try:
        pattern = r"https?://[a-zA-Z0-9.-]+/product/([^/]+)/"
        if match := re.match(pattern, url):
            manufacturer = match.group(1).split("/")[0]
            return manufacturer, True
        else:
            return None, False
    except Exception as e:
        detailed_error_slack_message(e, COMPETITOR)
        return None, False


manufacturers_match_status = {}


def is_manufacturer_match(manufacturers_dict, manufacturer_name):
    try:
        is_calculated = manufacturers_match_status.get(manufacturer_name)

        if is_calculated is not None:
            return is_calculated

        clean_product_title = clean_string(manufacturer_name, remove_company_status=True)
        product_words = {word for word in clean_product_title.split() if len(word) >= 2}

        is_match = any(manufacturer_words.intersection(product_words) for _, manufacturer_words in manufacturers_dict.items())

        manufacturers_match_status[manufacturer_name] = is_match

        return is_match
    except Exception as e:
        detailed_error_slack_message(e, COMPETITOR)
        return False


def store_data(url):
    try:
        outputs = []
        manufacturers_dict = preprocess_manufacturers()
        file_content = read_gz_file(url)
        bs_data = BeautifulSoup(file_content, "xml")
        b_unique = bs_data.find_all("loc")
        for data in b_unique:
            data = str(data)
            if data.startswith("<loc>") and data.endswith("</loc>"):
                data = data.replace("<loc>", "")
                data = data.replace("</loc>", "")
                manufacturer, is_valid = extract_manufacturer_from_url(data)
                if is_valid and manufacturer and is_manufacturer_match(manufacturers_dict, manufacturer):
                    result = {
                        "competitor": "us.rs-online",
                        "url": data,
                        "scraper_type": "sitemap",
                        "from_manufacturer": True,
                    }
                    outputs.append(result)
                    if len(outputs) == 5000:
                        url_insert_bulk(outputs)
                        outputs = []

        if outputs and len(outputs):
            url_insert_bulk(outputs)

    except Exception as e:
        detailed_error_slack_message(e, COMPETITOR)
