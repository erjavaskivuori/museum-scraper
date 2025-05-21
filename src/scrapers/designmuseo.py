"""Module provides scraping functionality for the Designmuseo."""

import requests
from bs4 import BeautifulSoup
from utils.scraper_helpers import parse_date_range, add_exhibition, format_exhibition_url


def scrape() -> list:
    """Scrapes exhibitions from the Designmuseo website.
    Returns:
        list: A list of dictionaries containing exhibition details.
    """
    museum = "Designmuseo"
    base_url = "https://www.designmuseum.fi/fi/"
    response = requests.get(base_url + "nayttelyt", timeout=10)
    soup = BeautifulSoup(response.content, "html.parser")
    current = soup.select_one("ul.columns-3")
    upcoming = soup.select("ul.columns-3")[1]
    all_sections = current.select(".has-link") + upcoming.select(".has-link")

    exhibitions = []

    for section in all_sections:
        name = section.select_one("h3").get_text(strip=True)
        dates = section.select_one("div > p > span > strong")
        if dates is not None:
            dates = parse_date_range(dates.get_text(strip=True))
        else:
            dates = None, None
            print(f"Error parsing dates for exhibition: {name}")

        exhibition_url = format_exhibition_url(section, base_url)
        add_exhibition(exhibitions, museum, name, dates, exhibition_url)

    return exhibitions
