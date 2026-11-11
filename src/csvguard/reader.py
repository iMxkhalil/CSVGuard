import csv

from pathlib import Path

def read_csv(path: Path) -> list[list[str]]:

    """Read a CSV file and return its rows as a list of lists of strings."""

    if not path.exists(): 
        raise FileNotFoundError(f"File not found: {path}")
    
    if path.is_dir():
        raise IsADirectoryError(f"The provided path {path} is a directory, not a file.")
    
    with open(path, mode="r", newline="", encoding="utf-8") as csvfile:
        reader = csv.reader(csvfile)
        rows = []

        for row in reader:
            rows.append(row)

    return rows
