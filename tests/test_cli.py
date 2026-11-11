import csv
from pathlib import Path

from typer.testing import CliRunner
from csvguard.cli import app

runner = CliRunner()
EXAMPLES_DIR = Path(__file__).resolve().parents[1] / "examples"


def _example_csv(predicate):
    for csv_file in sorted(EXAMPLES_DIR.iterdir()):
        if csv_file.suffix.lower() != ".csv":
            continue
        try:
            with csv_file.open(newline="", encoding="utf-8-sig") as source:
                rows = list(csv.reader(source))
        except UnicodeDecodeError:
            continue
        if predicate(rows):
            return csv_file
    raise AssertionError(f"No matching CSV example found in {EXAMPLES_DIR}")


def _has_missing_value(rows):
    return len(rows) > 1 and any(not value.strip() for row in rows[1:] for value in row)


def _has_missing_email(rows):
    if not rows or "email" not in [header.strip().lower() for header in rows[0]]:
        return False
    email_index = [header.strip().lower() for header in rows[0]].index("email")
    return any(len(row) <= email_index or not row[email_index].strip() for row in rows[1:])


def _has_duplicate_rows(rows):
    data_rows = [tuple(row) for row in rows[1:]]
    return len(data_rows) != len(set(data_rows))


def _has_header_issues(rows):
    if not rows or not rows[0]:
        return False
    headers = [h.strip().lower() for h in rows[0]]
    has_missing = any(not h for h in headers)
    has_duplicate = len(headers) != len(set(headers))
    return has_missing or has_duplicate


def _has_row_issues(rows):
    if not rows or len(rows) <= 1:
        return False
    expected_len = len(rows[0])
    has_inconsistent = any(len(row) != expected_len for row in rows[1:])
    data_rows = [tuple(v.strip().lower() for v in row) for row in rows[1:]]
    has_duplicate = len(data_rows) != len(set(data_rows))
    return has_inconsistent or has_duplicate


def test_cli_help():
    result = runner.invoke(app, ["--help"])

    assert result.exit_code == 0
    assert "Usage:" in result.output


def test_analyze_clean_file():
    csv_file = _example_csv(
        lambda rows: len(rows) > 1
        and bool(rows[0])
        and all(header.strip() for header in rows[0])
        and all(len(row) == len(rows[0]) and all(value.strip() for value in row) for row in rows[1:])
        and len({tuple(row) for row in rows[1:]}) == len(rows[1:])
    )

    result = runner.invoke(app, ["analyze", str(csv_file)])

    assert result.exit_code == 0
    assert "clean" in result.output.lower() or "no issues" in result.output.lower()


def test_analyze_dirty_file():
    csv_file = _example_csv(_has_missing_value)

    result = runner.invoke(app, ["analyze", str(csv_file)])

    assert result.exit_code == 0
    assert any(term in result.output.lower() for term in ("issue", "missing"))


def test_analyze_details():
    csv_file = _example_csv(_has_missing_email)

    result = runner.invoke(app, ["analyze", str(csv_file), "--details"])

    assert result.exit_code == 0
    assert "email" in result.output.lower()


def test_check_missing():
    csv_file = _example_csv(_has_missing_value)

    result = runner.invoke(app, ["check-missing", str(csv_file)])

    assert result.exit_code == 0
    assert "missing" in result.output.lower()


def test_check_duplicates():
    csv_file = _example_csv(_has_duplicate_rows)

    result = runner.invoke(app, ["check-duplicates", str(csv_file)])

    assert result.exit_code == 0
    assert "duplicate" in result.output.lower()


def test_check_headers():
    csv_file = _example_csv(_has_header_issues)

    result = runner.invoke(app, ["check-headers", str(csv_file)])

    assert result.exit_code == 0
    assert "header" in result.output.lower()


def test_check_rows():
    csv_file = _example_csv(_has_row_issues)

    result = runner.invoke(app, ["check-rows", str(csv_file)])

    assert result.exit_code == 0
    assert "row" in result.output.lower()


def test_invalid_file():
    non_existent = Path("nonexistent.csv")

    result = runner.invoke(app, ["analyze", str(non_existent)])

    assert result.exit_code != 0
    assert isinstance(result.exception, FileNotFoundError)
