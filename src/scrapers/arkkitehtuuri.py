"""Module provides scraping functionality for the Arkkitehtuurimuseo."""

import requests
from bs4 import BeautifulSoup
from utils.scraper_helpers import parse_date_range, add_exhibition, format_exhibition_url


def scrape() -> list:
    """Scrapes exhibitions from the Arkkitehtuurimuseo website.
    Returns:
        list: A list of dictionaries containing exhibition details.
    """
    museum = "Arkkitehtuurimuseo"
    base_url = "https://www.mfa.fi/"
    response = requests.get(base_url + "nayttelyt", timeout=10)
    soup = BeautifulSoup(response.content, "html.parser")
    all_sections = soup.select(".exhibition-row") \
        + soup.select_one("#tulevatnayttelyt").select(".exhibition")

    exhibitions = []

    for section in all_sections:
        name = section.select_one(".title").get_text(strip=True)
        dates = section.find_all("time")
        if len(dates) == 2:
            start_date = dates[0].get_text(strip=True)
            end_date = dates[1].get_text(strip=True)
            dates = parse_date_range(f"{start_date}{end_date}")
        elif len(dates) == 1:
            dates = parse_date_range(dates[0].get_text(strip=True))
        else:
            dates = None, None
            print(f"Error parsing dates for exhibition: {name}")

        exhibition_url = format_exhibition_url(section, base_url)
        add_exhibition(exhibitions, museum, name, dates, exhibition_url)

    return exhibitions
