import re
from utils.helpers.index import check_manufacturer_match
from utils.slack import detailed_error_slack_message


def is_valid_url_and_manufacturer(url):
    try:
        if "productdetail" in url:
            url_parts = url.split("/")
            if len(url_parts) > 3:
                if manufacturer := url_parts[-2]:
                    return True, manufacturer
        return False, None

    except Exception as e:
        detailed_error_slack_message(e, "masterelectronics")
        return False, None


manufacturers_match_status = {}


def is_manufacturer_match(manufacturers_dict, product_manufacturer):
    try:
        is_calculated = manufacturers_match_status.get(product_manufacturer)
        if is_calculated is not None:
            return is_calculated

        is_match = check_manufacturer_match(manufacturers_dict, product_manufacturer)
        manufacturers_match_status[product_manufacturer] = is_match

        return is_match

    except Exception as e:
        detailed_error_slack_message(e, "masterelectronics")
        return False
