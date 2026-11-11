from pathlib import Path
from csvguard.reader import read_csv
import pytest


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
    