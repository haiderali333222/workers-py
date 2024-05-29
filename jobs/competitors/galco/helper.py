from utils.helpers.index import request_with_retry, url_insert_bulk, get_proxies, error_slack_message, check_manufacturer_match, preprocess_manufacturers
from services.slack.slack_message import send_slack_message
from bs4 import BeautifulSoup



COMPETITOR = 'galco'
MANUFACTURERS_URL = 'https://www.galco.com/manufacturers'
BASE_URL = 'https://www.galco.com'
PAGE_LIMIT = 25


def get_data_from_url(url):
    proxies, headers  = get_proxies()
    page = None
    try:
        page = request_with_retry("get", url, COMPETITOR, proxies=proxies, headers=headers)
    except Exception as e:
        message = f"Error: {COMPETITOR}{e}"
        send_slack_message(message)
        return 

    if page.status_code != 200:
        message = f"Error: {COMPETITOR}{page.text}"
        send_slack_message(message)
        return 

    return BeautifulSoup(page.content, 'html.parser')

manufacturers_match_status = {}

def is_manufacturer_match(manufacturers_dict, product_title):
    is_calculated = manufacturers_match_status.get(product_title)
    
    if is_calculated is not None:
        return is_calculated

    is_match = check_manufacturer_match(manufacturers_dict, product_title)
    
    manufacturers_match_status[product_title] = is_match

    return is_match

def get_manufacturer_page_links():
    manufacturer_page_links = []
    
    manufacturers_dict = preprocess_manufacturers()
    if manufacturer_page := get_data_from_url(MANUFACTURERS_URL):
            mfr_groups = manufacturer_page.find_all('li', class_='ambrands-brand-item')

            for mfr_group in mfr_groups:
                if a := mfr_group.find('a'):
                    href = a['href']

                    if href and '/manufacturer' in href:
                        if manf_name := href.replace(
                            '/manufacturer/', ''    
                        ):
                            if is_manufacturer_match(manufacturers_dict, manf_name):
                                matched_manufacturer_link = f'{BASE_URL}{href}?product_list_limit={PAGE_LIMIT}'
                                
                                manufacturer_page_links.append(matched_manufacturer_link)
    
    
    return manufacturer_page_links


def get_product_links_from_plp(plp_link, is_first_page=False):
    product_links = []
    next_page_links = []

    plp_page = get_data_from_url(plp_link)

    if product_link_tags := plp_page.find_all('a', class_='product-item-link'):
        for product_link_tag in product_link_tags:
            if 'href' in product_link_tag.attrs:
                product_href = product_link_tag['href']
                product_links.append(product_href)

    if is_first_page:
        if total_results := plp_page.find('p', class_='toolbar-amount'):
            total_results = total_results.text.strip()
            if 'of' in total_results:
                total_results = total_results.split('of')[-1].strip()
                total_results = int(total_results)
                
                if total_results > PAGE_LIMIT:
                    total_pages = total_results // PAGE_LIMIT
                    for i in range(2, total_pages + 2):
                        next_page_link = f"{plp_link}&p={i}"
                        next_page_links.append(next_page_link)        

    return product_links, next_page_links

def get_products_urls_and_store(product_list_page_link):
    products_links_outputs = []
    max_count = 5000
    product_links, next_pages = get_product_links_from_plp(product_list_page_link, is_first_page=True)
    

    if product_links:
        first_page_links = add_product_links_to_outputs(product_links)
        products_links_outputs.extend(first_page_links)

    for next_page in next_pages:
        next_page_product_links, _ = get_product_links_from_plp(next_page)
        

        if next_page_product_links:
            found_links =  add_product_links_to_outputs(next_page_product_links)
            products_links_outputs.extend(found_links)
                
        if len(products_links_outputs) >= max_count:
            url_insert_bulk(products_links_outputs)
            products_links_outputs = []

    if len(products_links_outputs) > 0:
        url_insert_bulk(products_links_outputs)
        products_links_outputs = []

def add_product_links_to_outputs(product_links):
    product_links_outputs = []
    
    if product_links:
        for product_link in product_links:
            result = {
                "competitor": COMPETITOR,
                "url": product_link,
                "scraper_type": "live_search",
                'from_manufacturer': True
            }
            product_links_outputs.append(result)
                
    return product_links_outputs
