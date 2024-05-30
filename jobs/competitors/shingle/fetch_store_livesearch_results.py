import pandas as pd

from utils.helpers.index import url_insert_bulk
from utils.slack import error_slack_message

from .helper import MAX_LIMIT, fetch_and_store_all_search_results, get_manufacturer_url


def get_and_store_shingle_urls():
    try:
        urls = []
        outputs = []
        count = 0

        df = pd.read_csv("data/manufacturers_amplify.csv")
        manufacturers = df["Manufacturer"].unique()

        for manufacturer in manufacturers:
            if url := get_manufacturer_url(manufacturer):
                urls.append(url)

        urls = list(set(urls))

        print(f"started fetching urls: {len(urls)}")
        for url in urls:
            first_page_outputs, next_pages = fetch_and_store_all_search_results(
                url, is_first_page=True
            )

            print(
                f"first_page_outputs: {len(first_page_outputs)} next_pages: {len(next_pages)} for url: {url}"
            )
            if first_page_outputs:
                outputs.extend(first_page_outputs)

            if next_pages:
                for next_page in next_pages:
                    next_page_outputs, _ = fetch_and_store_all_search_results(next_page)

                    print(
                        f"next_page_outputs: {len(next_page_outputs)} for next_page: {next_page}"
                    )

                    if next_page_outputs:
                        outputs.extend(next_page_outputs)
                        count += len(next_page_outputs)

                    if count >= MAX_LIMIT:
                        url_insert_bulk(outputs)
                        outputs = []
                        count = 0

            if count >= MAX_LIMIT:
                url_insert_bulk(outputs)
                outputs = []
                count = 0

        if outputs:
            url_insert_bulk(outputs)
            outputs = []

    except Exception as e:
        error_slack_message(e)
