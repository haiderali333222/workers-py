from utils.helpers.index import (
    clean_string,
    check_is_whole_word,
    get_page_from_url,
)
from utils.slack import detailed_error_slack_message

COMPETITOR = "shingle"
COMPETITOR_MANUFACTURERS = [
    "Banner Engineering Corp",
    "Turck Inc.",
    "Siemens Industry Inc.",
    "SMC",
    "ABB, Inc",
    "ABB T&B Installation Products",
    "ADVANTECH",
    "Allied Moulded Products Inc.",
    "Acme Electric",
    "Ametek US Gauge Division",
    "APPLIED MOTION PRODUCTS",
    "WATER ANALYTICS",
    "Baldor",
    "Baumer Ltd",
    "Bodine Electric Company",
    "DART CONTROLS, INC.",
    "Contrex Incorporated",
    "Dodge",
    "Dynapar Corporation",
    "Edwards Signaling/Walter Kidde Portable",
    "Electrical & Electronic Controls Inc.",
    "Emka Inc",
    "Encoder Products Co",
    "ENERDOOR",
    "EXOR ELECTRONIC R&D, INC.",
    "FEDERAL SIGNAL CORP SSG",
    "Fireye",
    "Formsprag",
    "Fuji Electric Corp. of America",
    "Gates Rubber Company",
    "Hammond Manufacturing",
    "HMS Industrial Networks",
    "HTM Sensors Inc.",
    "IDEC",
    "Invertek Drives USA LLC",
    "KB Electronics Inc.",
    "Lenze Americas Corporation",
    "LITTLEFUSE, INC.",
    "Lovato Electric",
    "Lovejoy",
    "Macromatic Industrial Controls Inc.",
    "Maxcess International",
    "MELTRIC",
    "Mencom Corporation",
    "Migatron Corp",
    "Midland Industries",
    "Molex LLC",
    "Moxa Technologies",
    "Mulhern Belting Inc",
    "Nexen Group, Inc.",
    "Nidec Industrial Automation",
    "NK Technologies",
    "Oriental Motors",
    "Panduit Sales Corp.",
    "Patlite Corp",
    "PULS, L.P.",
    "Red Lion Controls",
    "Rittal North America, LLC",
    "Setra Systems, Inc.",
    "Sew-Eurodrive, Inc.",
    "Sola HD",
    "Sprecher & Schuh Inc",
    "TECO Westinghouse",
    "Tri-Tronics",
    "Wago Corporation",
    "Warner Elec Brake & Clutch",
    "Weg Electric Motors Corp.",
    "Weidmuller Inc.",
    "Yaskawa Electric America Inc.",
    "Zero-Max Inc",
]
MAX_LIMIT = 5000


def form_url(manufacturer):
    try:
        found_manufacturer = (
            manufacturer.strip().replace(" ", "%20").replace(",", "%2C")
        )
        return f"https://shingle.com/c?PageSize=50&Manufacturer={found_manufacturer}"
    except Exception as e:
        detailed_error_slack_message(e, COMPETITOR)
        return None


def get_manufacturer_url(manufacturer):
    try:
        clean_manufacturer = clean_string(manufacturer)
        clean_manufacturer_parts = clean_manufacturer.split(" ")
        sub_list = []

        for part in clean_manufacturer_parts:
            for comp_manu in COMPETITOR_MANUFACTURERS:
                url = clean_string(comp_manu, remove_company_status=True)

                is_whole_word = check_is_whole_word(part, url)
                if is_whole_word and len(part) > 1:
                    is_exact_match = part == url

                    if is_exact_match:
                        return form_url(comp_manu)
                    formed_url = form_url(comp_manu)

                    if formed_url not in sub_list:
                        sub_list.append(formed_url)

        return sub_list[0] if sub_list else None
    except Exception as e:
        detailed_error_slack_message(e, COMPETITOR)
        return None


def fetch_and_store_all_search_results(url, is_first_page=False):
    next_pages = []
    store_outputs = []

    print(f"fetching url: {url}")

    try:
        page = get_page_from_url(url, COMPETITOR, stream=True, verify=False)

        if not page:
            return store_outputs, next_pages

        if is_first_page:
            if links_wrapper := page.find("div", class_="CurrentPage"):
                links = links_wrapper.find_all("a", class_="page-link")
                for link in links:
                    if link["href"] == "#":
                        continue

                    url = f"https://shingle.com{link['href']}"
                    next_pages.append(url)

        if products_wrapper := page.findAll("div", class_="ItemData"):
            for product in products_wrapper:
                if product_link := product.find("a"):
                    url = f"https://shingle.com{product_link['href']}"
                    store_outputs.append(
                        {
                            "competitor": COMPETITOR,
                            "url": url,
                            "scraper_type": "live_search",
                            "from_manufacturer": True,
                        }
                    )

    except Exception as e:
        detailed_error_slack_message(e, COMPETITOR)

    return store_outputs, next_pages
