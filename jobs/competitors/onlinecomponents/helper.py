import re
from utils.helpers.index import error_slack_message, check_manufacturer_match


def is_valid_url_and_manufacturer(url):
    try:
        pattern = r'^https://www\.onlinecomponents\.com/en/([^/]+)/([^/]+)(?:\.([^/]+))?/?$'    
        return (True, match[1]) if (match := re.match(pattern, url)) else (False, None)
    except Exception as e:
        error_slack_message(e)
        return False, None

manufacturers_match_status = {}

def is_manufacturer_match(manufacturers_dict, product_manufacture):
    try: 
        is_calculated = manufacturers_match_status.get(product_manufacture)
        
        if is_calculated is not None:
            return is_calculated

        is_match = check_manufacturer_match(manufacturers_dict, product_manufacture)

        manufacturers_match_status[product_manufacture] = is_match

        return is_match
    except Exception as e:
        error_slack_message(e)
        return False
