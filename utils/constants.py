URLS_BY_MANUFACTURER = [
    "galco",
    "shingle",
    "mouser",
    "zoro",
    "onlinecomponents",
    "walkerindustrial",
    "masterelectronics",
    "wolfautomation" "digikey",
    "us.rs-online",
    "automationdirect",
    "newark",
]

SCRAPER_CRASHED_EMAIL_BODY = "Crawler stopped unexpectedly! Please consult the developer."

UNABLE_TO_SCRAPE_EMAIL_BODY = """
<p>Crawler is unable to scrape. The reason could be one of the following:</p>
<ul>
<li>Website your are trying to scrape is currently down.</li>
<li>Website your are trying to scrape is blocking this request.</li>
</ul>
"""

SEND_SCRAPERS_STATUS_EMAIL_RECIPIENT_TO = ["amna.mubashar@pursue.today", "alishan@pursue.today", "haider@pursue.today"]
SEND_SCRAPERS_STATUS_EMAIL_RECIPIENT_CC = ["ramzan@pursue.today"]
SEND_SCRAPERS_STATUS_EMAIL_SUBJECT = "Amplify Scraper Status"


def scraper_started_email_body_template(competitors):
    list_of_competitors = "<ul>"
    for competitor in competitors:
        list_of_competitors += f"<li>{competitor}</li>"
    list_of_competitors += "</ul>"

    return f"""
        <p>Crawler has been initiated for the following scraper(s):</p>
        {list_of_competitors}
        <p><strong>Note:</strong>Please note that it will take some time to complete, and the scraper's operation is not guaranteed as it depends on the availability of data on competitors' websites.</p>
    """


def scraper_completed_email_body_template(competitors, es_query):
    list_of_competitors = "<ul>"
    for competitor in competitors:
        list_of_competitors += f"<li>{competitor}</li>"
    list_of_competitors += "</ul>"

    return f"""
        <p>Crawler has been completed for the following scraper(s):</p>
        {list_of_competitors}
        <p>The scraper is currently operational with these filters.</p>
        <p><strong>Filter:  </strong>{es_query}</p>
        <p><strong>Note:</strong> The scraper's operation is not guaranteed as it depends on the availability of data on competitors' websites.</p>
    """


def scraper_status_email_body_template(working_scraper, not_working_scraper):
    list_of_working_scraper = "<ul>"
    for key, value in working_scraper.items():
        list_of_working_scraper += f"<li><strong>{key}:</strong> <span style='color: green'> success: {value['success']}</span>, <span style='color: red'>error:  {value['error']}</span></li>"
    list_of_working_scraper += "</ul>"

    list_of_not_working_scraper = "<ul>"
    for key, value in not_working_scraper.items():
        list_of_not_working_scraper += f"<li><strong>{key}:</strong> <span style='color: green'> success: {value['success']}</span>, <span style='color: red'>error:  {value['error']}</span></li>"
    list_of_not_working_scraper += "</ul>"

    return f"""
        <p>Working Scrappers:</p>
        {list_of_working_scraper}
        <p>Not Working Scrappers:</p>
        {list_of_not_working_scraper}
    """
