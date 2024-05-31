from bs4 import BeautifulSoup
from utils.helpers.index import (
    read_gz_file,
    url_insert_bulk,
    check_manufacturer_match,
)
from utils.slack import detailed_error_slack_message

COMPETITOR = "zoro"


def store_data(url, manufacturers_dict):
    try:
        file_content = read_gz_file(url)
        bs_data = BeautifulSoup(file_content, "xml")
        b_unique = bs_data.find_all("loc")
        outputs = []
        for data in b_unique:
            data = str(data)
            if data.startswith("<loc>") and data.endswith("</loc>"):
                data = data.replace("<loc>", "")
                if url_data := data.replace("</loc>", ""):
                    if manufacturer := url_data.replace("https://www.zoro.com/", ""):
                        manufacturer_arr = manufacturer.split("-")
                        manufacturer = " ".join(manufacturer_arr[:4])

                        if manufacturer and check_manufacturer_match(
                            manufacturers_dict, manufacturer
                        ):
                            result = {
                                "competitor": "zoro",
                                "url": url_data,
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
