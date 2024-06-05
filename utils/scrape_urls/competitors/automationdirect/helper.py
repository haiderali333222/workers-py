import requests

from utils.helpers.index import get_proxies
from utils.slack import detailed_error_slack_message, send_slack_message

COMPETITOR = "automationdirect"
URL = "https://www.automationdirect.com/adc/shopping/catalog/"
MAX_COUNT = 5000


def get_categories_id(manf):
    manf = manf.strip()
    url = "https://www.automationdirect.com/ajax?"

    proxies, headers = get_proxies()

    data = {
        "spellcheck": "null",
        "fctype": "adc.falcon.search.SearchFormCtrl",
        "cmd": "AjaxSearch",
        "searchquery": manf,
        "rawSearchquery": manf,
        "pageRefresh": "true",
        "solrQueryString": {f"q={manf}&rows=50&facet=true"},
        "productType": "",
        "controllingWidgetName": "Item_Type_ms",
        "categoryId": "0",
    }
    try:
        response = requests.post(url, headers=headers, data=data, proxies=proxies)
        return response.json()
    except ValueError:
        detailed_error_slack_message(ValueError, COMPETITOR)
        return


def get_Item_names(manf, id):
    manf = manf.strip()
    url = "https://www.automationdirect.com/ajax?"

    proxies, headers = get_proxies()

    if not proxies or not headers:
        send_slack_message("No proxies or headers found", "error")
        return

    data = {
        "spellcheck": "null",
        "fctype": "adc.falcon.search.SearchFormCtrl",
        "cmd": "AjaxSearch",
        "searchquery": manf,
        "rawSearchquery": manf,
        "pageRefresh": "true",
        "solrQueryString": {f"q={manf}&rows=50&facet=true"},
        "productType": "",
        "controllingWidgetName": "Item_Type_ms",
        "categoryId": id,
    }
    try:
        response = requests.post(url, headers=headers, data=data, proxies=proxies)
        return response.json()
    except ValueError:
        detailed_error_slack_message(ValueError, COMPETITOR)
        return
