"""Main script to scrape exhibitions from all the museums."""

from scrapers import kansallisgalleria, amos_rex, arkkitehtuuri, designmuseo
from utils import storage


def main():
    """Main function to scrape exhibitions from all museums and save to CSV."""
    all_exhibitions = []

    kansallisgalleria_museums = {"Sinebrychoff": "https://sinebrychoffintaidemuseo.fi/",
                                 "Kiasma": "https://kiasma.fi/",
                                 "Ateneum": "https://ateneum.fi/"}

    for museum, url in kansallisgalleria_museums.items():
        all_exhibitions.extend(kansallisgalleria.scrape(museum, url))

    all_exhibitions.extend(amos_rex.scrape())
    all_exhibitions.extend(arkkitehtuuri.scrape())
    all_exhibitions.extend(designmuseo.scrape())

    storage.save_csv(all_exhibitions, "data/exhibitions.csv")


if __name__ == "__main__":
    main()
