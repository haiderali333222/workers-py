from jobs.competitors.alliedelec.fetch_store_sitemap_results import get_and_store_alliedelec_urls
from jobs.competitors.baypower.fetch_store_sitemap_results import get_and_store_baypower_urls
from jobs.competitors.breakerauthority.fetch_store_sitemap_results import get_and_store_breakerauthority_urls
from jobs.competitors.breakerhunter.fetch_store_sitemap_results import get_and_store_breakerhunters_urls
from jobs.competitors.breakeroutlet.fetch_store_sitemap_results import get_and_store_breakeroutlet_urls
from jobs.competitors.chartercont.fetch_store_sitemap_results import get_and_store_chartercontact_urls
from jobs.competitors.circuitbreakerwarehouse.fetch_store_sitemap_results import get_and_store_circuitbreakerwarehouse_urls
from jobs.competitors.coasttocoastbreaker.fetch_store_sitemap_results import get_and_store_coasttocoastbreaker_urls
from jobs.competitors.controlparts.fetch_store_sitemap_results import get_and_store_controlparts_urls
from jobs.competitors.dkhardware.fetch_store_sitemap_results import get_and_store_dkhardware_urls
from jobs.competitors.galco.fetch_store_sitemap_results import get_and_store_galco_urls
from jobs.competitors.gordonelectricsupply.fetch_store_sitemap_results import get_and_store_gordonelectricsupply_urls
from jobs.competitors.globaltestsupply.fetch_store_sitemap_results import get_and_store_globaltestsupply_urls
from jobs.competitors.imc_direct.fetch_store_sitemap_results import get_and_store_imcdirect_urls
from jobs.competitors.iesupply.fetch_store_sitemap_results import get_and_store_iesupplyy_urls
from jobs.competitors.kele.fetch_store_sitemap_results import get_and_store_kele_urls
from jobs.competitors.radwell.fetch_store_sitemap_results import get_and_store_radwell_urls
from jobs.competitors.relectric.fetch_store_sitemap_results import get_and_store_relectric_urls
from jobs.competitors.onlinecomponents.fetch_store_sitemap_results import get_and_store_online_components_urls
from jobs.competitors.scheider_electric.fetch_store_sitemap_results import get_and_store_scheiderElectric_urls



COMPETITOR_MAPPING = {
    "alliedelec": get_and_store_alliedelec_urls,
    "baypower": get_and_store_baypower_urls,
    "breakerauthority": get_and_store_breakerauthority_urls,
    "breakerhunter": get_and_store_breakerhunters_urls,
    "breakeroutlet": get_and_store_breakeroutlet_urls,
    "chartercontact": get_and_store_chartercontact_urls,
    "circuitbreakerwarehouse": get_and_store_circuitbreakerwarehouse_urls,
    "coasttocoastbreaker": get_and_store_coasttocoastbreaker_urls,
    "controlparts": get_and_store_controlparts_urls,
    "dkhardware": get_and_store_dkhardware_urls,
    "galco": get_and_store_galco_urls,
    "gordonelectricsupply": get_and_store_gordonelectricsupply_urls,
    "globaltestsupply": get_and_store_globaltestsupply_urls,
    "imcdirect": get_and_store_imcdirect_urls,
    "iesupply": get_and_store_iesupplyy_urls,
    "kele": get_and_store_kele_urls,
    "radwell": get_and_store_radwell_urls,
    "relectric": get_and_store_relectric_urls,
    "scheiderelectric": get_and_store_scheiderElectric_urls,
    "onlinecomponents": get_and_store_online_components_urls,
}
