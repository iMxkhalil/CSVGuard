from pathlib import Path
from csvguard.reader import read_csv
import pytest
import textwrap

def test_read_csv():
     
    file_path = Path(__file__).parent.parent / "examples" / "customers.csv"

    result = read_csv(file_path)

    expected_result = [
            ['name', 'email', 'age'], 
            ['Ali', 'ali@example.com', '21'], 
            ['Sara', 'sara@example.com', '19'], 
            ['Ahmed', 'ahmed@example.com', '24']
        ]
    
    assert result == expected_result

def test_read_csv_file_not_found():
    file_path = Path("nonexistent.csv")

    with pytest.raises(FileNotFoundError):
        read_csv(file_path)

def test_read_csv_directory():
    file_path = Path(__file__).parent.parent / "examples"

    with pytest.raises(IsADirectoryError):
        read_csv(file_path)

def test_read_csv_invalid_encoding():
    file_path = Path(__file__).parent.parent / "examples" / "invalid_encoding.csv"

    with pytest.raises(UnicodeDecodeError):
        read_csv(file_path)

def test_read_csv_with_utf8_bom(tmp_path):
    csv_file = tmp_path / "bom.csv"
    csv_file.write_text(
        "name,email\nAli,ali@example.com\n",
        encoding="utf-8-sig"
    )

    result = read_csv(csv_file)

    expected = [
        ["name", "email"],
        ["Ali", "ali@example.com"]
    ]

    assert result == expected

def test_read_csv_with_special_characters(tmp_path):
    csv_file = tmp_path / "special.csv"
    csv_file.write_text(
        "name,city\nElodie,miami\nأحمد,صفاقس\n",
        encoding="utf-8"
    )

    result = read_csv(csv_file)

    expected = [
        ["name", "city"],
        ["Elodie", "miami"],
        ["أحمد", "صفاقس"],
    ]

    assert result == expected

def test_read_csv_with_quoted_fields(tmp_path):
    quoted_file = tmp_path / "quoted_file.csv"
    quoted_file.write_text(
    """\
name,description
Ali,"Python, Java and SQL"
Sara,"First line
Second line"
""",
    encoding="utf-8"
)
    result = read_csv(quoted_file)

    expected = [
        ["name", "description"],
        ["Ali", "Python, Java and SQL"],
        ["Sara", "First line\r\nSecond line"]
    ]
    assert result == expected

def test_read_csv_with_escaped_quotes(tmp_path):
    quoted_file = tmp_path / "escaped_quotes_file.csv"
    quoted_file.write_text('name,description\nAli,"He said ""Hello"" to me', encoding="utf-8")

    result = read_csv(quoted_file)
    expected = [
        ["name", "description"],
        ['Ali', 'He said "Hello" to me']
    ]

    assert result == expected