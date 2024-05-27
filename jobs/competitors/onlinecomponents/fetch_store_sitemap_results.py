import re
from utils.helpers.index import error_slack_message, check_manufacturer_match, url_insert_bulk,preprocess_manufacturers, get_sitemap_urls

COMPETITOR = 'onlinecomponents'
STARTING_URL = 'https://www.onlinecomponents.com/sitemaps.xml'

def is_valid_url_and_manufacturer(url):
    try:
        pattern = r'^https://www\.onlinecomponents\.com/en/([^/]+)/([^/]+)(?:\.([^/]+))?/?$'    
        return (True, match[1]) if (match := re.match(pattern, url)) else (False, None)
    except Exception as e:
        error_slack_message(e)
        return False, None

manufacturers_match_status = {}

def is_manufacturer_match(manufacturers_dict, product_manufacture):
    try: 
        is_calculated = manufacturers_match_status.get(product_manufacture)
        
        if is_calculated is not None:
            return is_calculated

        is_match = check_manufacturer_match(manufacturers_dict, product_manufacture)

        manufacturers_match_status[product_manufacture] = is_match

        return is_match
    except Exception as e:
        error_slack_message(e)
        return False

def get_and_store_online_components_urls():
    try:
        manufacturers_dict = preprocess_manufacturers()
        count = 0
        outputs = []

        sitemap_urls = get_sitemap_urls(STARTING_URL, COMPETITOR)
        
        print(f'Found {len(sitemap_urls)} sitemap urls')
        
        for sitemap_url in sitemap_urls:
            website_urls = get_sitemap_urls(sitemap_url, COMPETITOR)

            for url in website_urls:
                is_valid, manufacturer = is_valid_url_and_manufacturer(url)

                if is_valid and manufacturer and is_manufacturer_match(manufacturers_dict, manufacturer):
                    count += 1
                    result = {
                        "competitor": COMPETITOR,
                        "url": url,
                        "scraper_type": "sitemap",
                        'from_manufacturer': True
                    }
                    print(f'inserting, {count}')
                    outputs.append(result)

                if count >= 10:
                    url_insert_bulk(outputs)
                    count = 0
                    outputs = []
        if outputs and len(outputs):
            url_insert_bulk(outputs)
            outputs = []
        
    except Exception as e:
        error_slack_message(e)