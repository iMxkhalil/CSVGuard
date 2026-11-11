from csvguard.analyzer import find_duplicate_rows, find_inconsistent_rows, find_missing_values, find_duplicate_headers, find_missing_headers
import pytest

def test_missing_headers_no_missing():
    data = [["name", "email", "age"]]

    result = find_missing_headers(data)

    expected_result = []

    assert result == expected_result 

def test_missing_headers_multiple_missing():
    data = [["", "email", "   "]]

    result = find_missing_headers(data)
    expected_result = [{
        "header_index": 0,
        "header_data": ""
    },
    {
        "header_index": 2,
        "header_data": "   "
    }
    ]
    assert result == expected_result

def test_missing_headers_empty_data():
    data = []
    with pytest.raises(ValueError):
        find_missing_headers(data)

def test_missing_headers_empty_headers():
    data = [[]]
    with pytest.raises(ValueError):
        find_missing_headers(data)

def test_missing_values():


    data = [
    ["name", "email", "age"],
    ["Ahmed", "ahmed@gmail.com", "20"],
    ["Sami", "sami@gmail.com", "21"],
    ]


    result = find_missing_values(data)
    expected_result = []

    assert result == expected_result

def test_missing_values_with_missing_data():


    data = [
        ["name", "email", "age"],
        ["Ahmed", "ahmed@gmail.com", "20"],
        ["Sami", "", "21"],
    ]

    result = find_missing_values(data)

    expected_result = [
    {
        "row_index": 2,
        "col_index": 1,
        "col_name": "email",
        "value": "",
    }
    ]

    assert result == expected_result

def test_missing_values_with_multiple_missing_data():


    data = [
        ["name", "email", "age"],
        ["Ahmed", "", "20"],
        ["Sami", "    ", ""],
    ]

    result = find_missing_values(data)

    expected_result = [
    {
        "row_index": 1,
        "col_index": 1,
        "col_name": "email",
        "value": "",
    },
    {
        "row_index": 2,
        "col_index": 1,
        "col_name": "email",
        "value": "    ",
    },
    {
        "row_index": 2,
        "col_index": 2,
        "col_name": "age",
        "value": "",
    }
    ]

    assert result == expected_result

def test_missing_values_empty_data():

    with pytest.raises(ValueError):
        data = []
        find_missing_values(data)

def test_missing_values_headers_only():
    data = [
        ["name", "email", "age"],
    ]

    result = find_missing_values(data)

    expected_result = []

    assert result == expected_result 

def test_missing_values_no_headers():
    data = [
        ["Kim", "kim@gmail.com", "20"],
        ["Lee", "lee@gmail.com", "25"],
    ]

    result = find_missing_values(data, has_headers=False)
    expected_result = []

    assert result == expected_result

def test_missing_values_no_headers_with_missing_data():
    data = [
        ["Kim", "kim@gmail.com", "20"],
        ["lee", "", "23"],
        ["Sam", "     ", ""], 
    ]
    result = find_missing_values(data, has_headers=False)

    expected_result = [
        {
            "row_index": 1,
            "col_index": 1,
            "col_name": None,
            "value": "",
        },
        {
            "row_index": 2,
            "col_index": 1,
            "col_name": None,
            "value": "     ",
        },
        {
            "row_index": 2,
            "col_index": 2,
            "col_name": None,
            "value": "",
        }
    ]

    assert result == expected_result

def test_inconsistent_rows():
    data = [
        ["name", "email", "age"],
        ["Ahmed", "ahmed@gmail.com"],
        ["Sami", "sami@gmail.com", "21", "extra_column"],
    ]

    result = find_inconsistent_rows(data)

    expected_result = [
        {
            "row_index": 1,
            "row_length": 2,
            "expected_length": 3
        },
        {
            "row_index": 2,
            "row_length": 4,
            "expected_length": 3
        },
    ]

    assert result == expected_result

def test_inconsistent_rows_empty_data():
    with pytest.raises(ValueError):
        data = []
        find_inconsistent_rows(data)

def test_inconsistent_rows_empty_row():
    data = [
        ["name", "email", "age"],
        [],
        ["Sam", "sam@gmail.com", "56"],
    ]

    result = find_inconsistent_rows(data)

    expected_result = [
        {
            "row_index": 1,
            "row_length": 0,
            "expected_length": 3
        }
    ]   

    assert result == expected_result

def test_inconsistent_rows_headers_only():
    data = [
        ["name", "email", "age"],
    ]

    result = find_inconsistent_rows(data)

    expected_result = []

    assert result == expected_result

def test_inconsistent_rows_no_headers():
    data = [
        ["Ahmed", "ahmed@gmail.com", "20"],
        ["Sami", "sami@gmail.com", "23"],
    ]

    result = find_inconsistent_rows(data, has_headers=False)

    expected_result = []

    assert result == expected_result

def test_inconsistent_rows_no_headers_with_inconsistent_data():
    data = [
        ["Frank", "frank@gmail.com", "20"],
        ["Alice", "alice@gmail.com", "25", "extra_column"],
        ["Bob", "bob@gmail.com"],
    ]

    result = find_inconsistent_rows(data, has_headers=False)

    expected_result = [
        {
            "row_index": 1,
            "row_length": 4,
            "expected_length": 3
        },
        {
            "row_index": 2,
            "row_length": 2,
            "expected_length": 3
        },
    ]

    assert result == expected_result

def test_inconsistent_rows_no_headers_and_empty_first_row():
    with pytest.raises(ValueError):
        data = [
            [],
            ["Mark", "mark@gmail.oom", "43"],
            ["Bob", "Bob@gmail.com", "46", "extra_column"],
        ]
        find_inconsistent_rows(data, has_headers=False)

def test_inconsistent_rows_with_headers_and_empty_first_row():
    with pytest.raises(ValueError):
        data = [
            [],
            ["Mark", "mark@gmail.oom", "43"],
            ["Bob", "Bob@gmail.com", "46", "extra_column"],
        ]
        find_inconsistent_rows(data, has_headers=True)

def test_duplicate_rows_empty_data():
    with pytest.raises(ValueError):
        data = []
        find_duplicate_rows(data)

def test_duplicate_rows_single_duplicates():
    data = [
        ["name", "email", "age"],
        ["John", "john@gmail.com", "25"],
        ["Tom", "tom@gmail.com", "30"],
        ["John", "john@gmail.com", "25"],
    ]

    result = find_duplicate_rows(data)

    expected_result = [
        {"row_index": 3,
         "row_data": ["John", "john@gmail.com", "25"]
        }
    ]

    assert result == expected_result

def test_duplicate_rows_multiple_duplicates():
    data = [
        ["name", "email", "age"],
        ["Alex", "alex@gmail.com", "20"],
        ["Sami", "sami@gmail.com", "32"],
        ["Alex", "alex@gmail.com", "20"],
        ["Alex", "alex@gmail.com", "20"],
    ]

    result = find_duplicate_rows(data)

    expected_result = [
        {
            "row_index": 3,
            "row_data": ["Alex", "alex@gmail.com", "20"]
        },
        {
            "row_index": 4,
            "row_data": ["Alex", "alex@gmail.com", "20"]
        },
    ]

    assert result == expected_result

def test_duplicate_rows_no_headers():
    data = [
        ["Rey", "rey@gmail.com", "28"],
        ["Will", "will@gmail.com", "54"],
    ]

    result = find_duplicate_rows(data, has_headers=False)
    expected_result = []

    assert result == expected_result

def test_duplicate_rows_no_headers_with_duplicates():
    data = [
        ["Rey", "rey@gmail.com", "28"],
        ["Will", "will@gmail.com", "54"],
        ["Rey", "rey@gmail.com", "28"],
        
    ]
    result = find_duplicate_rows(data, has_headers=False)
    expected_result = [
        {
            "row_index": 2,
            "row_data": ["Rey", "rey@gmail.com", "28"]
        }
    ]

    assert result == expected_result

def test_missing_values_column_name_out_of_bounds():
    data = [
        ["name", "email"],
        ["Alice", "alice@gmail.com", "     "],
        ["Bob", "bob@gmail.com", ""]
    ]

    result = find_missing_values(data)

    expected_result = [
        {
            "row_index": 1,
            "col_index": 2,
            "col_name": None,
            "value": "     "
        },
        {
            "row_index": 2,
            "col_index": 2,
            "col_name": None,
            "value": ""
        }
    ]

    assert result == expected_result

def test_duplicate_rows_with_whitespace():
    data = [
        ["name", "email", "age"],
        ["John", "john@gmail.com", "43"],
        [" John ", "john@gmail.com", "43"],
    ]

    result = find_duplicate_rows(data)

    expected_result = [
        {
            "row_index": 2,
            "row_data": [" John ", "john@gmail.com", "43"]
        }
    ]

    assert result == expected_result 

def test_duplicate_rows_with_different_cases():
    data = [
        ["name", "email", "age"],
        ["john", "john@gmail.com", "43"],
        ["JOHN", "JOHN@gmail.com", "43"],
    ]

    result = find_duplicate_rows(data)

    expected_result = [
        {
            "row_index": 2,
            "row_data": ["JOHN", "JOHN@gmail.com", "43"]
        }
    ]

    assert result == expected_result 

def test_duplicate_headers_no_duplicates():
    data = [
        ["name", "email", "age"]
    ]

    result = find_duplicate_headers(data)

    expected_result = []

    assert result == expected_result 

def test_duplicate_headers_multiple_duplicates():
    data = [
        ["name", "email", "age", "EMAIL", "name "]
    ]

    result = find_duplicate_headers(data)

    expected_result = [
        {"header_index":3, "header_data": "EMAIL"},
        {"header_index":4, "header_data": "name "}
    ]


    assert result == expected_result 

def test_duplicate_headers_with_different_cases():
    data = [
        ["name", "email", "age", "Email", "nAMe"]
    ]
        
    result = find_duplicate_headers(data)
        
    expected_result = [
        {"header_index":3, "header_data": "Email"},
        {"header_index":4, "header_data": "nAMe"}
    ]
        
        
    assert result == expected_result 

def test_duplicate_headers_empty_data():
    with pytest.raises(ValueError):
        data = []
        find_duplicate_headers(data)

def test_duplicate_headers_empty_headers():
    data = [[]]
    with pytest.raises(ValueError):
        find_duplicate_headers(data)


    
