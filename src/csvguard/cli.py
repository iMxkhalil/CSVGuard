import typer
from pathlib import Path
from csvguard.reader import read_csv
from csvguard.analyzer import (
    find_missing_headers,
    find_missing_values,
    find_duplicate_headers,
    find_duplicate_rows,
    find_inconsistent_rows,
)

app=typer.Typer() 


def handle_error(error):
    typer.secho(
        f"Error: {error}",
        fg=typer.colors.RED,
        bold=True
    )
    raise typer.Exit(code=1)


@app.command()
def analyze(file: Path, details: bool = False):
    try:
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

    
        typer.echo(f"Total issues: {total_issues}")
        typer.echo(f"Missing headers: {len(missing_headers)}")
        if details and missing_headers:
            typer.echo()
            for missing_header in missing_headers:
                typer.echo(f"Column number: {missing_header['header_index'] + 1} | Header name: {missing_header['header_data']}")
            typer.echo()
        typer.echo(f"Duplicate headers: {len(duplicate_headers)}")
        if details and duplicate_headers:
            typer.echo()
            for duplicate_header in duplicate_headers:
                typer.echo(f"Column number: {duplicate_header['header_index'] + 1} | Header name: {duplicate_header['header_data']}")
            typer.echo()
        typer.echo(f"Duplicate rows: {len(duplicate_rows)}")
        if details and duplicate_rows:
            typer.echo()
            for duplicate_row in duplicate_rows:
                typer.echo(f"Row number: {duplicate_row['row_index'] + 1} | Row data: {duplicate_row['row_data']}")
            typer.echo()
        typer.echo(f"Inconsistent rows: {len(inconsistent_rows)}")
        if details and inconsistent_rows:
            typer.echo()
            for inconsistent_row in inconsistent_rows:
                typer.echo(f"Row number: {inconsistent_row['row_index'] + 1} | Row length: {inconsistent_row['row_length']} | Expected row length: {inconsistent_row['expected_length']}")
            typer.echo()
        typer.echo(f"Missing values: {len(missing_values)}")
        if details and missing_values:
            typer.echo()
            for missing_value in missing_values:
                typer.echo(f"Row number: {missing_value['row_index'] + 1} | Column name: {missing_value['col_name']} | Column number: {missing_value['col_index'] + 1}")
            typer.echo()

    except (ValueError, OSError, UnicodeError) as error:
        handle_error(error)


@app.command()
def check_missing(file: Path, details: bool = False):
    try:
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

        typer.echo(f"Total missing: {total_missings}")
        typer.echo(f"Missing headers: {len(missing_headers)}")
        if details and missing_headers:
            typer.echo()
            typer.echo("Missing headers:")
            typer.echo()
            for missing_header in missing_headers:
                typer.echo(
                    f"Column number: {missing_header['header_index'] + 1} | Header name: {missing_header['header_data']}"
                )
            typer.echo()

        typer.echo(f"Missing values: {len(missing_values)}")
        if details and missing_values:
            typer.echo()
            typer.echo("Missing values:")
            typer.echo()
            for missing_value in missing_values:
                typer.echo(
                    f"Row number: {missing_value['row_index'] + 1} | Column name: {missing_value['col_name']} | Column number: {missing_value['col_index'] + 1}"
                )
            typer.echo()

    except (ValueError, OSError, UnicodeError) as error:
        handle_error(error)
    

@app.command()
def check_duplicates(file: Path, details: bool = False):
    try:
        data = read_csv(file)

        duplicate_rows = find_duplicate_rows(data)
        duplicate_headers = find_duplicate_headers(data)

        total_duplicates = len(duplicate_rows) + len(duplicate_headers)

        if total_duplicates == 0:
            typer.secho("File has no duplicates!", fg=typer.colors.GREEN, bold=True)
        else:
            typer.secho("Duplicates detected!", fg=typer.colors.YELLOW, bold=True)

        typer.echo(f"Total duplicates: {total_duplicates}")
        typer.echo(f"Duplicate headers: {len(duplicate_headers)}")

        if details and duplicate_headers:
            typer.echo("\nDuplicate headers:\n")
            for duplicate_header in duplicate_headers:
                typer.echo(
                    f"Column number: {duplicate_header['header_index'] + 1} "
                    f"| Header name: {duplicate_header['header_data']}"
                )

        typer.echo(f"Duplicate rows: {len(duplicate_rows)}")

        if details and duplicate_rows:
            typer.echo("\nDuplicate rows:\n")
            for duplicate_row in duplicate_rows:
                typer.echo(
                    f"Row number: {duplicate_row['row_index'] + 1} "
                    f"| Row data: {duplicate_row['row_data']}"
                )

    except (ValueError, OSError, UnicodeError) as error:
        handle_error(error)


@app.command()
def check_headers(file: Path, details: bool = False):
    try:
        data = read_csv(file)

        missing_headers = find_missing_headers(data)
        duplicate_headers = find_duplicate_headers(data)

        total_header_issues = len(missing_headers) + len(duplicate_headers)

        if total_header_issues == 0:
            typer.secho("Headers are valid!", fg=typer.colors.GREEN, bold=True)
        else:
            typer.secho("Header issues detected!", fg=typer.colors.YELLOW, bold=True)

        typer.echo(f"Total header issues: {total_header_issues}")
        typer.echo(f"Missing headers: {len(missing_headers)}")

        if details and missing_headers:
            typer.echo("\nMissing headers:\n")
            for missing_header in missing_headers:
                typer.echo(
                    f"Column number: {missing_header['header_index'] + 1} "
                    f"| Header name: {missing_header['header_data']}"
                )

        typer.echo(f"Duplicate headers: {len(duplicate_headers)}")

        if details and duplicate_headers:
            typer.echo("\nDuplicate headers:\n")
            for duplicate_header in duplicate_headers:
                typer.echo(
                    f"Column number: {duplicate_header['header_index'] + 1} "
                    f"| Header name: {duplicate_header['header_data']}"
                )

    except (ValueError, OSError, UnicodeError) as error:
        handle_error(error)


@app.command()
def check_rows(file: Path, details: bool = False):
    try:
        data = read_csv(file)

        inconsistent_rows = find_inconsistent_rows(data)
        duplicate_rows = find_duplicate_rows(data)

        total_row_issues = len(inconsistent_rows) + len(duplicate_rows)

        if total_row_issues == 0:
            typer.secho("Rows are valid!", fg=typer.colors.GREEN, bold=True)
        else:
            typer.secho("Row issues detected!", fg=typer.colors.YELLOW, bold=True)

        typer.echo(f"Total row issues: {total_row_issues}")
        typer.echo(f"Inconsistent rows: {len(inconsistent_rows)}")

        if details and inconsistent_rows:
            typer.echo("\nInconsistent rows:\n")
            for inconsistent_row in inconsistent_rows:
                typer.echo(
                    f"Row number: {inconsistent_row['row_index'] + 1} "
                    f"| Row length: {inconsistent_row['row_length']} "
                    f"| Expected row length: {inconsistent_row['expected_length']}"
                )

        typer.echo(f"Duplicate rows: {len(duplicate_rows)}")

        if details and duplicate_rows:
            typer.echo("\nDuplicate rows:\n")
            for duplicate_row in duplicate_rows:
                typer.echo(
                    f"Row number: {duplicate_row['row_index'] + 1} "
                    f"| Row data: {duplicate_row['row_data']}"
                )
    except (ValueError, OSError, UnicodeError) as error:
        handle_error(error)


if __name__ == "__main__":
    app()
