"""Scraper helper functions for extracting and formatting data from HTML content."""

import re
from datetime import datetime


def parse_date_range(dates):
    """Parses the date range from the exhibition dates string.
    Args:
        dates (str): The date range string to parse.
    Returns:
        tuple: A tuple containing the start and end dates in 'YYYY-MM-DD' format.
        If the exhibition is permanent or parsing the dates fails, returns (None, None).
    """
    dates = dates.strip().lower().replace("–", "-")

    if "pysyvä" in dates:
        return None, None

    try:
        range_parts = dates.split("-")

        if len(range_parts) == 2:
            start_raw = range_parts[0].strip()
            end_raw = range_parts[1].strip()

            end_date = datetime.strptime(end_raw, '%d.%m.%Y')

            if re.match(r'^\d{1,2}\.\d{1,2}\.$', start_raw):
                start_raw += str(end_date.year)

            start_date = datetime.strptime(start_raw, '%d.%m.%Y')

        else:
            single_date_str = range_parts[0].strip()
            start_date = datetime.strptime(single_date_str, '%d.%m.%Y')
            return start_date.strftime('%d.%m.%Y'), None

    except ValueError:
        # Handle cases where the date format is not as expected
        print(f"Error parsing date: {dates}")
        return None, None

    return start_date.strftime('%d.%m.%Y'), end_date.strftime('%d.%m.%Y')


def add_exhibition(exhibitions: str, museum: str, name: str, dates: tuple, url: str) -> None:
    """Adds an exhibition to the list of exhibitions.
    Args:
        exhibitions (list): The list of exhibitions to add to.
        museum (str): The name of the museum.
        name (str): The name of the exhibition.
        dates (tuple): A tuple containing the start and end dates.
        url (str): The URL of the exhibition page.
    """
    exhibitions.append({
        "museum": museum,
        "name": name,
        "start_date": dates[0],
        "end_date": dates[1],
        "url": url,
    })


def format_exhibition_url(section: str, base_url: str) -> str:
    """Formats the exhibition URL to ensure it is absolute.
    Args:
        section (str): The section containing the exhibition URL.
        base_url (str): The base URL of the museum's website.
    Returns:
        str: The formatted exhibition URL.
    """
    try:
        exhibition_url = section.select_one("a")["href"]
        if base_url not in exhibition_url:
            exhibition_url = base_url + exhibition_url
        return exhibition_url
    except (KeyError, TypeError):
        # Handle cases where the exhibition URL is not found
        print("Error formatting exhibition URL")
        return None
