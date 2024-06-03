import re
from utils.helpers.index import check_manufacturer_match


def extract_manufacturer_from_url(url):
    try:
        pattern = r"^https?://(?:www\.)?[a-zA-Z0-9-]+\.[a-zA-Z]{2,}/(?:en/products/detail/)?([^/]+)/"

        if match := re.match(pattern, url):
            manufacturer = match.group(1)
            return manufacturer, True
        else:
            return None, False
    except Exception as e:
        return None, False


manufacturers_match_status = {}


def is_manufacturer_match(manufacturers_dict, manufacturer_name):
    try:
        is_calculated = manufacturers_match_status.get(manufacturer_name)

        if is_calculated is not None:
            return is_calculated

        is_match = check_manufacturer_match(
            manufacturers_dict, manufacturer_name
        )

        manufacturers_match_status[manufacturer_name] = is_match

        return is_match
    except Exception as e:
        return False
