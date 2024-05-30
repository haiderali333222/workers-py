import re
from utils.helpers.index import check_manufacturer_match

COMPETITOR = 'walkerindustrial'
STARTING_URL = 'https://www.walkerindustrial.com/sitemap.xml'
MAX_COUNT = 5000

def is_valid_url_and_manufacturer(url):
    pattern = r'^https://www\.walkerindustrial\.com/([^/]+)/([^/]+)(?:\.([^/]+))?/?$'
    return (True, match[1]) if (match := re.match(pattern, url)) else (False, None)
    
manufacturers_match_status = {}

def is_manufacturer_match(manufacturers_dict, product_title):
    is_calculated = manufacturers_match_status.get(product_title)
    
    if is_calculated is not None:
        return is_calculated

    is_match = check_manufacturer_match(manufacturers_dict, product_title)
    
    manufacturers_match_status[product_title] = is_match

    return is_match