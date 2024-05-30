from utils.helpers.index import (
    get_proxies,
    request_with_retry,
    url_insert_bulk,
    error_slack_message,
)

COMPETITOR = "coasttocoastbreaker"
URL = "https://www.coasttocoastbreaker.com/search/ajax/suggest/?q="


def store_cosotocost(url_formed):
    try:
        outputs = []
        proxies, headers = get_proxies()
        headers["User-Agent"] = (
            "Mozilla/5.0 (Linux; Android 6.0; HTC One M9 Build/MRA58K) AppleWebKit/537.36"
        )
        response = request_with_retry(
            "get", url_formed, COMPETITOR, proxies=proxies, headers=headers
        )
        if not response:
            return
        requ = response.json()
        if len(requ) > 0:
            u = requ[0].get("link")
            if len(u) != 0:
                result = {
                    "competitor": COMPETITOR,
                    "url": u,
                    "scraper_type": "live_search",
                }
                outputs.append(result)
                if len(outputs) == 5000:
                    url_insert_bulk(outputs)
                    outputs = []
        if outputs and len(outputs):
            url_insert_bulk(outputs)
        return True
    except Exception as e:
        error_slack_message(e)


def creating_url(name):
    try:
        url_formed = URL
        url_formed += name
        store_cosotocost(url_formed)
    except Exception as e:
        error_slack_message(e)
