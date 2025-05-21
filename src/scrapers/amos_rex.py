""" Module provides scraping functionality for Amos Rex museum."""

import requests
from bs4 import BeautifulSoup
from utils.scraper_helpers import parse_date_range, add_exhibition, format_exhibition_url


def scrape():
    """Scrapes exhibitions from the Amos Rex museum website.
    Returns:
        list: A list of dictionaries containing exhibition details.
    """
    museum = "Amos Rex"
    base_url = "https://amosrex.fi/"

    response_ongoing = requests.get(base_url + "nayttelyt", timeout=10)
    response_upcoming = requests.get(base_url + "nayttelyt/tulevat-nayttelyt", timeout=10)
    soup_ongoing = BeautifulSoup(response_ongoing.content, "html.parser")
    soup_upcoming = BeautifulSoup(response_upcoming.content, "html.parser")
    all_sections = soup_ongoing.select(".lifts-2-columns_item") \
        + soup_upcoming.select(".lifts-2-columns_item")

    exhibitions = []

    for section in all_sections:
        name = section.select_one(".lifts-2-columns_item__title").get_text(strip=True)
        info_texts = section.select_one(".lifts-2-columns_item__text").find_all("p")
        if len(info_texts) == 2:
            dates_text = info_texts[-1].get_text(strip=True)
            dates = parse_date_range(dates_text)
        else:
            dates = None, None

        exhibition_url = format_exhibition_url(section, base_url)
        add_exhibition(exhibitions, museum, name, dates, exhibition_url)

    return exhibitions
