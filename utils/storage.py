"""Module provides functionality to save data to CSV files."""

import csv
import os


def save_csv(data, path):
    """Saves a list of dictionaries to a CSV file.
    Args:
        data (list): A list of dictionaries to save.
        path (str): The file path where the CSV will be saved.
    """
    if not data:
        return
    keys = data[0].keys()
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=keys)
        writer.writeheader()
        writer.writerows(data)
