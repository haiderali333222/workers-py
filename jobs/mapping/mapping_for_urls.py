# Import all the functions with siteMap
from jobs.competitors.alliedelec.fetch_store_sitemap_results import get_and_store_alliedelec_urls
from jobs.competitors.baypower.fetch_store_sitemap_results import get_and_store_baypower_urls
from jobs.competitors.breakerauthority.fetch_store_sitemap_results import get_and_store_breakerauthority_urls
from jobs.competitors.breakerhunter.fetch_store_sitemap_results import get_and_store_breakerhunters_urls
from jobs.competitors.breakeroutlet.fetch_store_sitemap_results import get_and_store_breakeroutlet_urls
from jobs.competitors.chartercont.fetch_store_sitemap_results import get_and_store_chartercontact_urls
from jobs.competitors.circuitbreakerwarehouse.fetch_store_sitemap_results import get_and_store_circuitbreakerwarehouse_urls
from jobs.competitors.controlparts.fetch_store_sitemap_results import get_and_store_controlparts_urls
from jobs.competitors.dkhardware.fetch_store_sitemap_results import get_and_store_dkhardware_urls
from jobs.competitors.gordonelectricsupply.fetch_store_sitemap_results import get_and_store_gordonelectricsupply_urls
from jobs.competitors.globaltestsupply.fetch_store_sitemap_results import get_and_store_globaltestsupply_urls
from jobs.competitors.imc_direct.fetch_store_sitemap_results import get_and_store_imcdirect_urls
from jobs.competitors.iesupply.fetch_store_sitemap_results import get_and_store_iesupplyy_urls
from jobs.competitors.kele.fetch_store_sitemap_results import get_and_store_kele_urls
from jobs.competitors.radwell.fetch_store_sitemap_results import get_and_store_radwell_urls
from jobs.competitors.relectric.fetch_store_sitemap_results import get_and_store_relectric_urls
from jobs.competitors.onlinecomponents.fetch_store_sitemap_results import get_and_store_online_components_urls
from jobs.competitors.scheider_electric.fetch_store_sitemap_results import get_and_store_scheiderElectric_urls
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
from jobs.competitors.coasttocoastbreaker.fetch_store_livesearch_results import get_and_store_coasttocoastbreaker_urls
from jobs.competitors.mouser.fetch_store_livesearch_results import get_and_store_mouser_urls
from jobs.competitors.shingle.fetch_store_livesearch_results import get_and_store_shingle_urls
from jobs.competitors.newark.fetch_store_livesearch_results import get_and_store_newark_urls
from jobs.competitors.wolfautomation.fetch_store_livesearch_results import get_and_store_wolf_automation_urls
from jobs.competitors.automationdirect.fetch_store_livesearch_results import get_and_store_automation_direct_urls
from jobs.competitors.galco.fetch_store_livesearch_results import get_and_store_galco_urls


COMPETITOR_MAPPING = {
    # With SiteMap  
    "alliedelec": get_and_store_alliedelec_urls,
    "baypower": get_and_store_baypower_urls,
    "breakerauthority": get_and_store_breakerauthority_urls,
    "breakerhunter": get_and_store_breakerhunters_urls,
    "breakeroutlet": get_and_store_breakeroutlet_urls,
    "chartercontact": get_and_store_chartercontact_urls,
    "circuitbreakerwarehouse": get_and_store_circuitbreakerwarehouse_urls,
    "controlparts": get_and_store_controlparts_urls,
    "dkhardware": get_and_store_dkhardware_urls,
    "gordonelectricsupply": get_and_store_gordonelectricsupply_urls,
    "globaltestsupply": get_and_store_globaltestsupply_urls,
    "imcdirect": get_and_store_imcdirect_urls,
    "iesupply": get_and_store_iesupplyy_urls,
    "kele": get_and_store_kele_urls,
    "radwell": get_and_store_radwell_urls,
    "relectric": get_and_store_relectric_urls,
    "scheiderelectric": get_and_store_scheiderElectric_urls,
    
    
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
    "coasttocoastbreaker": get_and_store_coasttocoastbreaker_urls,
    "galco": get_and_store_galco_urls,
    
    
    'mouser': get_and_store_mouser_urls,
    'shingle': get_and_store_shingle_urls,
    'newark': get_and_store_newark_urls,
    'wolfautomation': get_and_store_wolf_automation_urls,
    'automationdirect': get_and_store_automation_direct_urls
}
