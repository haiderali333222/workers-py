# Standard library import
import re
from collections import defaultdict

# Third-party library import
import pandas as pd

# local application import
from utils.slack import error_slack_message


def preprocess_manufacturers():
    amp_manufacturers_list = pd.read_csv("data/manufacturers_amplify.csv")
    print("list", amp_manufacturers_list)
    manufacturers_list = amp_manufacturers_list["Manufacturer"].unique()
    manufacturers_dict = defaultdict(set)
    for manufacturer in manufacturers_list:
        clean_manufacturer = clean_string(manufacturer)
        manufacturer_words = set(clean_manufacturer.split())
        manufacturers_dict[clean_manufacturer] = manufacturer_words
    return manufacturers_dict


def check_is_whole_word(
    word, text
):  # sourcery skip: use-fstring-for-formatting
    try:
        pattern = r"\b{}\b".format(re.escape(word))
        return bool(re.search(pattern, text))
    except Exception as e:
        error_slack_message(e)
        return False


clean_string_pattern = re.compile(r"[^\x00-\x7F]+|[^a-zA-Z0-9\s]")


def clean_string(string, remove_company_status=False):
    try:
        clean_string_text = string.strip().lower()
        if remove_company_status:
            company_status = [
                "corporation",
                "incorporated",
                "controls",
                "industrial",
                "networks",
                "company",
                "electric",
                "automation",
                "switch",
                "products",
                "international",
                "electronic",
                "usa",
                "connector",
                "components",
                "switzerland",
                "solutions",
                "tool",
                "power",
                "group",
                "energy",
                "filter",
                "components",
                "protection",
                "devices",
                "test",
                "instruments",
                "america",
                "sensors",
                "sensor" "technologies",
                "industries",
                "systems",
                "manufacturing",
                "group",
                "corp.",
                "motors",
                "inc",
                "llc",
                "corp",
                "ltd",
                "tech",
                "lighting",
                "technology",
                "electronics",
            ]

            for status in company_status:
                if check_is_whole_word(status, clean_string_text):
                    clean_string_text = clean_string_text.replace(status, "")
        clean_string_text = clean_string_pattern.sub(" ", clean_string_text)
        clean_string_text = re.sub(" +", " ", clean_string_text)
        return clean_string_text
    except Exception as e:
        error_slack_message(e)
        return ""


def check_manufacturer_match(manufacturers_dict, product_title):
    clean_product_title = clean_string(
        product_title, remove_company_status=True
    )
    product_words = {
        word for word in clean_product_title.split() if len(word) >= 2
    }

    return any(
        manufacturer_words.intersection(product_words)
        for _, manufacturer_words in manufacturers_dict.items()
    )


def listToString(url):
    return "".join(url)
