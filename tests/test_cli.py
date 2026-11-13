from pathlib import Path
from csvguard.reader import read_csv
from typer.testing import CliRunner
from csvguard.cli import app

runner = CliRunner()
EXAMPLES_DIR = Path(__file__).resolve().parents[1] / "examples"
CLEAN_FILE = EXAMPLES_DIR / "customers.csv"
DIRTY_FILE = EXAMPLES_DIR / "customers_dirty.csv"


def test_cli_help():
    result = runner.invoke(app, ["--help"])

    assert result.exit_code == 0
    assert "Usage:" in result.output


def test_analyze_clean_file():
    result = runner.invoke(app, ["analyze", str(CLEAN_FILE)])

    assert result.exit_code == 0
    assert "clean" in result.output.lower()


def test_analyze_dirty_file():
    result = runner.invoke(app, ["analyze", str(DIRTY_FILE)])

    assert result.exit_code == 0
    assert "issues found" in result.output.lower()


def test_analyze_details():
    result = runner.invoke(app, ["analyze", str(DIRTY_FILE), "--details"])

    assert result.exit_code == 0
    assert "email" in result.output.lower()
    assert "row" in result.output.lower()


def test_check_missing():
    result = runner.invoke(app, ["check-missing", str(DIRTY_FILE)])

    assert result.exit_code == 0
    assert "missing data detected" in result.output.lower()


def test_check_missing_details():
    result = runner.invoke(app, ["check-missing", str(DIRTY_FILE), "--details"])

    assert result.exit_code == 0
    assert "email" in result.output.lower()


def test_check_duplicates():
    result = runner.invoke(app, ["check-duplicates", str(DIRTY_FILE)])

    assert result.exit_code == 0
    assert "duplicates detected" in result.output.lower()


def test_check_headers():
    result = runner.invoke(app, ["check-headers", str(DIRTY_FILE)])

    assert result.exit_code == 0
    assert "header issues detected" in result.output.lower()


def test_check_rows():
    result = runner.invoke(app, ["check-rows", str(DIRTY_FILE)])

    assert result.exit_code == 0
    assert "row issues detected" in result.output.lower()


def test_invalid_file():
    non_existent = EXAMPLES_DIR / "nonexistent.csv"

    result = runner.invoke(app, ["analyze", str(non_existent)])

    assert isinstance(result.exception, SystemExit)
    assert result.exception.code == 1
    assert "Error:" in result.output


def test_analyze_empty_file(tmp_path):
    empty_file = tmp_path / "empty.csv"
    empty_file.write_text("", encoding="utf-8")

    result = runner.invoke(app, ["analyze", str(empty_file)])

    assert result.exit_code == 1
    assert "error" in result.output.lower()
    assert "empty" in result.output.lower()
    assert isinstance(result.exception, SystemExit)
    assert result.exception.code == 1

def test_analyze_headers_only_file(tmp_path):
    csv_file = tmp_path / "headers_only.csv"
    csv_file.write_text("name,email,age\n", encoding="utf-8")

    result = runner.invoke(app, ["analyze", str(csv_file)])

    assert result.exit_code == 0
    assert "clean" in result.output.lower()  

def test_check_missing_empty_file(tmp_path):
    empty_file = tmp_path/ "empty.csv"
    empty_file.write_text("", encoding="utf-8")

    result = runner.invoke(app, ["check-missing", str(empty_file)])

    assert result.exit_code == 1
    assert "error" in result.output.lower()
    assert "empty" in result.output.lower()

def test_check_duplicates_empty_file(tmp_path):
    empty_file = tmp_path / "empty.csv"
    empty_file.write_text("", encoding="utf-8")

    result = runner.invoke(app, ["check-duplicates", str(empty_file)])

    assert result.exit_code == 1
    assert "error" in result.output.lower()
    assert "empty" in result.output.lower()

def test_check_headers_empty_file(tmp_path):
    empty_file = tmp_path / "empty.csv"
    empty_file.write_text("", encoding="utf-8")

    result = runner.invoke(app, ["check-headers", str(empty_file)])

    assert result.exit_code == 1
    assert "error" in result.output.lower()
    assert "empty" in result.output.lower()

def test_check_rows_empty_file(tmp_path):
    empty_file = tmp_path / "empty.csv"
    empty_file.write_text("", encoding="utf-8")

    result = runner.invoke(app, ["check-rows", str(empty_file)])

    assert result.exit_code == 1
    assert "error" in result.output.lower()
    assert "empty" in result.output.lower()

def test_is_a_directory_error():
    result = runner.invoke(app, ["analyze", str(EXAMPLES_DIR)])

    assert result.exit_code == 1
    assert "error" in result.output.lower()
    assert "directory" in result.output.lower()

def test_invalid_encoding_error(tmp_path):
    invalid_file = tmp_path / "invalid.csv"
    invalid_file.write_bytes(b"\xff\xfe\xffa")

    result = runner.invoke(app, ["analyze", str(invalid_file)])
    
    assert result.exit_code == 1
    assert "error" in result.output.lower()
    



