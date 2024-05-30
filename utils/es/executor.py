import traceback

from services.elastic_search.connection import es
from utils.es.es_query import search_param, count_query
from utils.slack import send_slack_message


def listToString(url):
    url_formed = ""
    if url is not None:
        for f in url:
            url_formed += f
    return url_formed


def extracted_name(skip_limit_start, skip_limit_end):
    result = []
    response = None
    while response is None or response.get("hits").get("hits") is None:
        response = es.search(
            index="products_1.0",
            body=search_param,
            from_=skip_limit_start,
            size=skip_limit_end,
        )
        for data in response.get("hits").get("hits"):
            result.append(listToString(data.get("fields").get("name")))
    return result


def total_count(es_query=None):
    if es_query is None:
        response = es.count(index="products_1.0", body=count_query)
    else:
        response = es.count(index="products_1.0", body=es_query)
    total_products = response.get("count")
    return total_products


def extracted_products(skip_limit_start, skip_limit_end, es_query):
    result = []
    response = None
    while response is None or response.get("hits").get("hits") is None:
        response = es.search(
            index="products_1.0",
            body=es_query,
            from_=skip_limit_start,
            size=skip_limit_end,
        )
        for data in response.get("hits").get("hits"):
            result.append(listToString(data.get("_source").get("name")))
    return result


def extract_urls_from_es(query, skip_limit_start, skip_limit_end):
    urls = []
    response = None

    try:
        while True:
            send_slack_message(f"Fetched URLS from Elasticsearch: {skip_limit_start}")
            print("Fetched URLS from Elasticsearch: ", skip_limit_start)
            response = es.search(
                index="products_1.0",
                body=query,
                from_=skip_limit_start,
                size=skip_limit_end - 1,
            )

            hits = response.get("hits").get("hits")
            if not hits:
                break
            for data in hits:
                if data.get("_source") and data.get("_source").get("url"):
                    urls.append(
                        f"https://www.electrical.com{data.get('_source').get('url')}"
                    )

            if len(hits) < skip_limit_end:
                break

            skip_limit_start += skip_limit_end
        return urls
    except Exception as e:
        message = "Error: " + str(e) + "\n" + traceback.format_exc()
        send_slack_message(message)
