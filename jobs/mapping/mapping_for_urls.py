# Import all the functions with siteMap
from jobs.competitors.onlinecomponents.fetch_store_sitemap_results import get_and_store_online_components_urls
from jobs.competitors.digikey.fetch_store_sitemap_results import get_and_store_digikey_urls
from jobs.competitors.masterelectronics.fetch_store_sitemap_results import get_and_store_master_electronics_urls
from jobs.competitors.mc_mc.fetch_store_sitemap_results import get_and_store_mc_mc_urls
from jobs.competitors.plchardware.fetch_store_sitemap_results import get_and_store_plchardware_urls
from jobs.competitors.sigmasurplus.fetch_store_sitemap_results import get_and_store_sigmasurplus_urls
from jobs.competitors.classicautomation.fetch_store_sitemap_results import get_and_store_classic_automation_urls
from jobs.competitors.zoro.fetch_store_sitemap_results import get_and_store_zoro_urls
from jobs.competitors.walkerindustrial.fetch_store_sitemap_results import get_and_store_walker_industrial_urls
from jobs.competitors.unisgroup.fetch_store_sitemap_results import get_and_store_unisgroup_urls
from jobs.competitors.rs.fetch_store_sitemap_results import get_and_store_rs_urls
from jobs.competitors.swgr.fetch_store_sitemap_results import get_and_store_swgr_urls
from jobs.competitors.super_breaker.fetch_store_sitemap_results import get_and_store_superbreakers_urls

# Import all the functions with LiveSearch
from jobs.competitors.mouser.fetch_store_livesearch_results import get_and_store_mouser_urls
from jobs.competitors.shingle.fetch_store_livesearch_results import get_and_store_shingle_urls
from jobs.competitors.newark.fetch_store_livesearch_results import get_and_store_newark_urls
from jobs.competitors.wolfautomation.fetch_store_livesearch_results import get_and_store_wolf_automation_urls
from jobs.competitors.automationdirect.fetch_store_livesearch_results import get_and_store_automation_direct_urls


COMPETITOR_MAPPING = {
    # With SiteMap  
    "onlinecomponents": get_and_store_online_components_urls,
    'digikey': get_and_store_digikey_urls,
    'masterelectronics': get_and_store_master_electronics_urls,
    "mc_mc": get_and_store_mc_mc_urls,
    'plchardware': get_and_store_plchardware_urls,
    'sigmasurplus': get_and_store_sigmasurplus_urls,
    'classicautomation': get_and_store_classic_automation_urls,
    'zoro': get_and_store_zoro_urls,
    'walkerindustrial': get_and_store_walker_industrial_urls,
    'unisgroup': get_and_store_unisgroup_urls,
    "us.rs-online": get_and_store_rs_urls,
    'swgr': get_and_store_swgr_urls,
    "superbreakers": get_and_store_superbreakers_urls,
    
    # With LiveSearch
    'mouser': get_and_store_mouser_urls,
    'shingle': get_and_store_shingle_urls,
    'newark': get_and_store_newark_urls,
    'wolfautomation': get_and_store_wolf_automation_urls,
    'automationdirect': get_and_store_automation_direct_urls
}
