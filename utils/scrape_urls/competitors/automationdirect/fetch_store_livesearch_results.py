import pandas as pd
import pydash

from utils.helpers.index import url_insert_bulk
from utils.slack import detailed_error_slack_message

from .helper import COMPETITOR, MAX_COUNT, URL, get_categories_id, get_Item_names


def get_and_store_automation_direct_urls():
    outputs = []
    try:
        df = pd.read_csv("data/manufacturers_amplify.csv")
        manufacturers = df["Manufacturer"].unique()

        for manf in manufacturers:
            try:
                result = get_categories_id(manf)

                if not result:
                    continue
                if categories := pydash.get(result, "categoryStructure", []):
                    for cat in categories:
                        if subCategories := pydash.get(cat, "subCategories", []):
                            for subcat in subCategories:
                                if node_id := pydash.get(subcat, "nodeId"):
                                    try:
                                        if items := get_Item_names(manf, node_id):
                                            if not items:
                                                continue
                                            results = pydash.get(
                                                items,
                                                "solrResult.response.docs",
                                                [],
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
                                    except Exception as e:
                                        detailed_error_slack_message(e, COMPETITOR)
                                        continue
            except Exception as e:
                detailed_error_slack_message(e, COMPETITOR)
                continue

        if outputs and len(outputs):
            url_insert_bulk(outputs)

    except Exception as e:
        detailed_error_slack_message(e, COMPETITOR)

    if outputs and len(outputs):
        url_insert_bulk(outputs)
