import pydash
import pandas as pd

from utils.helpers.index import url_insert_bulk, error_slack_message

from .helper import get_categories_id, get_Item_names, COMPETITOR, URL, MAX_COUNT


def get_and_store_automation_direct_urls():
    try:
        df = pd.read_csv("data/manufacturers_amplify.csv")
        manufacturers = df["Manufacturer"].unique()
        outputs = []

        for manf in manufacturers:
            result = get_categories_id(manf)

            if not result:
                continue
            if categories := pydash.get(result, "categoryStructure", []):
                for cat in categories:
                    if subCategories := pydash.get(cat, "subCategories", []):
                        for subcat in subCategories:
                            if node_id := pydash.get(subcat, "nodeId"):
                                if items := get_Item_names(manf, node_id):
                                    if not items:
                                        continue
                                    results = pydash.get(
                                        items, "solrResult.response.docs", []
                                    )

                                    for docs in results:
                                        item_code = pydash.get(docs, "item_code")
                                        new_url = URL + item_code
                                        result = {
                                            "competitor": COMPETITOR,
                                            "url": new_url,
                                            "scraper_type": "live_search",
                                            "from_manufacturer": True,
                                        }

                                        outputs.append(result)
                                if len(outputs) >= MAX_COUNT:
                                    url_insert_bulk(outputs)
                                    outputs = []

        if outputs and len(outputs):
            url_insert_bulk(outputs)

    except Exception as e:
        error_slack_message(e)
