from utils.helpers.index import check_manufacturer_match
from utils.slack import detailed_error_slack_message


def is_valid_url_and_manufacturer(url):
    try:
        if "productdetail" in url:
            url_parts = url.split("/")

            if len(url_parts) < 5:
                return False, None

            if product_manufacture := url_parts[-2]:
                return True, product_manufacture

        return False, None
    except Exception as e:
        detailed_error_slack_message(e, "onlinecomponents")
        return False, None


manufacturers_match_status = {}


def is_manufacturer_match(manufacturers_dict, product_manufacture):
    try:
        is_calculated = manufacturers_match_status.get(product_manufacture)

        if is_calculated is not None:
            return is_calculated

        is_match = check_manufacturer_match(
            manufacturers_dict, product_manufacture
        )

        manufacturers_match_status[product_manufacture] = is_match

        return is_match
    except Exception as e:
        detailed_error_slack_message(e, "onlinecomponents")
        return False
