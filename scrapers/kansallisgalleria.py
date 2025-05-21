""" Module provides scraping functionality for Kansallisgalleria's museums."""

import requests
from bs4 import BeautifulSoup
from utils.scraper_helpers import parse_date_range, add_exhibition, format_exhibition_url


def scrape(museum: str, base_url: str) -> list:
    """Scrapes exhibitions from the given museum URL.
    Args:
        museum (str): The name of the museum.
        base_url (str): The base URL of the museum's website.
    Returns:
        list: A list of dictionaries containing exhibition details.
    """
    response_ongoing = requests.get(base_url + "nayttelyt", timeout=10)
    response_upcoming = requests.get(base_url + "nayttelyt/tulevat", timeout=10)
    soup_ongoing = BeautifulSoup(response_ongoing.content, "html.parser")
    soup_upcoming = BeautifulSoup(response_upcoming.content, "html.parser")
    all_sections = soup_ongoing.find_all("div", class_="cover__content") \
        + soup_upcoming.find_all("div", class_="cover__content")

    exhibitions = []
    for section in all_sections:
        name = section.find("h2").get_text(strip=True)
        dates = section.find("ul", class_="dates").get_text(strip=True)
        dates = parse_date_range(dates)

        exhibition_url = format_exhibition_url(section, base_url)
        add_exhibition(exhibitions, museum, name, dates, exhibition_url)

    return exhibitions
