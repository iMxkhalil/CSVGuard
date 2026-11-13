def find_missing_headers(data):
    if not data or not data[0]:
        raise ValueError("Data provided is empty or first row is empty.")
    headers = data[0]
    missing_headers = []
    for header_index in range(len(headers)):
        header = headers[header_index] 
        if header.strip() == "":
            missing_headers.append({
                "header_index": header_index,
                "header_data": header,
            })
    return missing_headers

def find_duplicate_headers(data):
    if not data or not data[0]:
        raise ValueError("Data provided is empty or first row is empty.")
    headers = data[0]
    seen_headers = set()
    duplicates = []
    for header_index in range(len(headers)):
        header_data = headers[header_index]
        header = header_data.strip().casefold() 
        if header in seen_headers:
            duplicates.append({
                "header_index": header_index,
                "header_data": header_data,
            })
        else:
            seen_headers.add(header)
    return duplicates


def find_missing_values(data, has_headers=True):
    if not data: 
        raise ValueError("Data provided is empty.")
    missing_values = []
    if has_headers:
        headers = data[0]
        start_index = 1
    else:
        headers = None
        start_index = 0
    for row_index in range(start_index, len(data)):
        row = data[row_index]
        for col_index in range(len(row)):
            value = row[col_index]
            if value.strip() == "":
                missing_values.append({
                    "row_index": row_index,
                    "col_index": col_index,
                    "col_name": headers[col_index] if headers is not None and col_index < len(headers) else None,
                    "value": value,
                })
    return missing_values

def find_inconsistent_rows(data, has_headers=True):
    if not data:
        raise ValueError("Data provided is empty.")
    if not data[0]:
        raise ValueError("First row is empty. Cannot determine expected row length.")
    if has_headers:
        start_index = 1 
    else:
        start_index = 0
    inconsistent_rows = []
    for row_index in range(start_index, len(data)):
        row = data[row_index]
        if len(row) != len(data[0]):
            inconsistent_rows.append({
                "row_index": row_index,
                "row_length": len(row),
                "expected_length": len(data[0]),
            })
    return inconsistent_rows


def find_duplicate_rows(data, has_headers=True):
    if not data:
        raise ValueError("Data provided is empty.")
    seen_rows = set()
    duplicate_rows = []
    if has_headers:
        start = 1
    else:
        start = 0
    for row_index in range(start, len(data)):
        row_data = tuple(data[row_index])
        row = tuple(value.strip().casefold() for value in row_data)
        if row in seen_rows:
            duplicate_rows.append({
                "row_index": row_index,
                "row_data": list(row_data),
            })
        else:
            seen_rows.add(row)
    return duplicate_rows


