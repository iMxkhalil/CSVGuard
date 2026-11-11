import typer
from pathlib import Path
from csvguard.reader import read_csv
from csvguard.analyzer import find_missing_headers, find_missing_values, find_duplicate_headers, find_duplicate_rows, find_inconsistent_rows 
app = typer.Typer()
   
@app.command()
def analyze(file: Path, details: bool = False):

    data = read_csv(file)

    missing_values = find_missing_values(data)
    inconsistent_rows = find_inconsistent_rows(data)
    duplicate_rows = find_duplicate_rows(data)
    duplicate_headers = find_duplicate_headers(data)
    missing_headers = find_missing_headers(data)

    total_issues = sum([
        len(missing_headers),
        len(duplicate_headers),
        len(duplicate_rows),
        len(inconsistent_rows),
        len(missing_values)
    ])

    if total_issues == 0:

        typer.secho("File is clean!", fg=typer.colors.GREEN, bold=True)

    else:
        typer.secho("Issues found in file!", fg=typer.colors.YELLOW, bold=True)

    
    print("Total issues:", total_issues)
    print("Missing headers: ", len(missing_headers))
    if details == True and len(missing_headers) != 0:
        print()
        for missing_header in missing_headers:
            print("Column number: ", missing_header["header_index"]+1, " | ", "Header name: ", missing_header["header_data"])
        print()
    print("Duplicate headers: ", len(duplicate_headers))
    if details == True and len(duplicate_headers) != 0:
        print()
        for duplicate_header in duplicate_headers:
            print("Column number: ", duplicate_header["header_index"]+1, " | ", "Header name: ", duplicate_header["header_data"])
        print()
    print("Duplicate rows: ", len(duplicate_rows))
    if details == True and len(duplicate_rows) != 0:
        print()
        for duplicate_row in duplicate_rows:
            print("Row number: ", duplicate_row["row_index"]+1, " | ", "Row data: ", duplicate_row["row_data"])
        print()
    print("Inconsistent rows: ", len(inconsistent_rows))
    if details == True and len(inconsistent_rows) != 0:
        print()
        for inconsistent_row in inconsistent_rows:
            print("Row number: ", inconsistent_row["row_index"]+1, " | ", "Row length: ", inconsistent_row["row_length"], " | ","Expected row length: ", inconsistent_row["expected_length"])
        print()
    print("Missing values: ", len(missing_values))
    if details == True and len(missing_values) != 0:
        print()
        for missing_value in missing_values:
            print("Row number: ", missing_value["row_index"]+1, " | ", "Column name: ", missing_value["col_name"], " | ", "Column number: ", missing_value["col_index"]+1)
        print()

@app.command()
def check_missing(file: Path, details: bool = False):
    data = read_csv(file)
    
    missing_values = find_missing_values(data)
    missing_headers = find_missing_headers(data)

    total_missings = sum([
        len(missing_headers),
        len(missing_values)
        ])
    if total_missings == 0:

        typer.secho("File has no missing data!", fg=typer.colors.GREEN, bold=True)

    else:
        typer.secho("Missing data detected!", fg=typer.colors.YELLOW, bold=True)

    print("Total missing: ", total_missings)
    print("Missing headers: ", len(missing_headers))
    if details == True and len(missing_headers) != 0:
        print()
        print("Missing headers:")
        print()
        for missing_header in missing_headers:
            print(
                "Column number: ", missing_header["header_index"]+1,
                " | ","Header name: ", missing_header["header_data"]
            )
        print()

    print("Missing values: ", len(missing_values))
    if details == True and len(missing_values) != 0:
        print()
        print("Missing values:")
        print()
        for missing_value in missing_values:
            print(
                "Row number:", missing_value["row_index"] + 1,
                "| Column name:", missing_value["col_name"],
                "| Column number:", missing_value["col_index"] + 1
            )
        print()
    

@app.command()
def check_duplicates(file: Path, details: bool = False):
    data = read_csv(file)

    duplicate_rows = find_duplicate_rows(data)
    duplicate_headers = find_duplicate_headers(data)

    total_duplicates = len(duplicate_rows) + len(duplicate_headers)

    if total_duplicates == 0:
        typer.secho("File has no duplicates!", fg=typer.colors.GREEN, bold=True)
    else:
        typer.secho("Duplicates detected!", fg=typer.colors.YELLOW, bold=True)

    print("Total duplicates:", total_duplicates)
    print("Duplicate headers:", len(duplicate_headers))

    if details == True and duplicate_headers:
        print("\nDuplicate headers:\n")
        for duplicate_header in duplicate_headers:
            print(
                "Column number:", duplicate_header["header_index"] + 1,
                "| Header name:", duplicate_header["header_data"]
            )

    print("Duplicate rows:", len(duplicate_rows))

    if details == True and duplicate_rows:
        print("\nDuplicate rows:\n")
        for duplicate_row in duplicate_rows:
            print(
                "Row number:", duplicate_row["row_index"] + 1,
                "| Row data:", duplicate_row["row_data"]
            )
@app.command()
def check_headers(file: Path, details: bool = False):
    data = read_csv(file)

    missing_headers = find_missing_headers(data)
    duplicate_headers = find_duplicate_headers(data)

    total_header_issues = len(missing_headers) + len(duplicate_headers)

    if total_header_issues == 0:
        typer.secho("Headers are valid!", fg=typer.colors.GREEN, bold=True)
    else:
        typer.secho("Header issues detected!", fg=typer.colors.YELLOW, bold=True)

    print("Total header issues:", total_header_issues)
    print("Missing headers:", len(missing_headers))

    if details == True and missing_headers:
        print("\nMissing headers:\n")
        for missing_header in missing_headers:
            print(
                "Column number:", missing_header["header_index"] + 1,
                "| Header name:", missing_header["header_data"]
            )

    print("Duplicate headers:", len(duplicate_headers))

    if details == True and duplicate_headers:
        print("\nDuplicate headers:\n")
        for duplicate_header in duplicate_headers:
            print(
                "Column number:", duplicate_header["header_index"] + 1,
                "| Header name:", duplicate_header["header_data"]
            )
@app.command()
def check_rows(file: Path, details: bool = False):
    data = read_csv(file)

    inconsistent_rows = find_inconsistent_rows(data)
    duplicate_rows = find_duplicate_rows(data)

    total_row_issues = len(inconsistent_rows) + len(duplicate_rows)

    if total_row_issues == 0:
        typer.secho("Rows are valid!", fg=typer.colors.GREEN, bold=True)
    else:
        typer.secho("Row issues detected!", fg=typer.colors.YELLOW, bold=True)

    print("Total row issues:", total_row_issues)
    print("Inconsistent rows:", len(inconsistent_rows))

    if details == True and inconsistent_rows:
        print("\nInconsistent rows:\n")
        for inconsistent_row in inconsistent_rows:
            print(
                "Row number:", inconsistent_row["row_index"] + 1,
                "| Row length:", inconsistent_row["row_length"],
                "| Expected row length:", inconsistent_row["expected_length"]
            )

    print("Duplicate rows:", len(duplicate_rows))

    if details == True and duplicate_rows:
        print("\nDuplicate rows:\n")
        for duplicate_row in duplicate_rows:
            print(
                "Row number:", duplicate_row["row_index"] + 1,
                "| Row data:", duplicate_row["row_data"]
            )


if __name__ == "__main__":
    app()
