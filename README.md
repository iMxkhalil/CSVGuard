# CSVGuard

**CSVGuard** is a lightweight Python command-line tool for CSV data quality analysis.

CSV files used in data workflows can contain subtle structural and content issues, such as missing values, duplicate rows, duplicate headers, and inconsistent row lengths. These problems can cause pipeline failures or unexpected results during data processing.

CSVGuard helps identify these issues directly from the terminal, providing a quick summary of data quality and detailed information about where problems occur.

## Features

CSVGuard performs the following checks:

- **Missing Values:** Detects empty and whitespace-only cells, reporting their row and column positions.
- **Missing Headers:** Identifies blank or whitespace-only column names.
- **Duplicate Headers:** Detects repeated column names, ignoring case and surrounding whitespace.
- **Duplicate Rows:** Identifies duplicate data rows, using case-insensitive comparison and whitespace normalization.
- **Inconsistent Rows:** Detects rows whose number of columns differs from the expected row length.
- **Two Inspection Modes:**
  - **Summary mode (default):** Displays the overall status and issue counts.
  - **Detailed mode (`--details`):** Displays the locations and relevant information for detected issues.

## Installation

### Prerequisites

- Python 3.10 or higher
- Git

### 1. Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/CSVGuard.git
cd CSVGuard
```

Replace `YOUR_USERNAME` with your GitHub username.

### 2. Create a virtual environment

**Windows (PowerShell):**

```powershell
py -m venv .venv
.venv\Scripts\Activate.ps1
```

**Linux/macOS:**

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install CSVGuard

From the project root directory, run:

```bash
py -m pip install -e .
```

This installs CSVGuard in editable mode along with its declared dependencies.

To install the testing dependency:

```bash
py -m pip install pytest
```

After installation, the `csvguard` command is available in your terminal.

## Usage

### General Syntax

```bash
csvguard COMMAND FILE [OPTIONS]
```

To display the available commands:

```bash
csvguard --help
```

To display help for a specific command:

```bash
csvguard analyze --help
```

### Available Commands

#### 1. `analyze`

Performs a complete CSV data quality analysis, checking for all supported issues.

```bash
csvguard analyze examples/customers.csv
```

To display detailed results:

```bash
csvguard analyze examples/customers_dirty.csv --details
```

#### 2. `check-missing`

Checks for missing headers and missing cell values.

```bash
csvguard check-missing examples/customers_dirty.csv
```

Detailed results:

```bash
csvguard check-missing examples/customers_dirty.csv --details
```

#### 3. `check-duplicates`

Checks for duplicate headers and duplicate data rows.

```bash
csvguard check-duplicates examples/customers_dirty.csv
```

Detailed results:

```bash
csvguard check-duplicates examples/customers_dirty.csv --details
```

#### 4. `check-headers`

Checks the header row for missing and duplicate column names.

```bash
csvguard check-headers examples/customers_t1.csv
```

Detailed results:

```bash
csvguard check-headers examples/customers_t1.csv --details
```

#### 5. `check-rows`

Checks for duplicate rows and inconsistent row lengths.

```bash
csvguard check-rows examples/customers_dirty.csv
```

Detailed results:

```bash
csvguard check-rows examples/customers_dirty.csv --details
```

**Note:** All commands display a summary by default. Use `--details` to see the locations of detected issues.

## Example Output

### Clean CSV

Running CSVGuard against a clean CSV file:

```text
$ csvguard analyze examples/customers.csv

File is clean!
Total issues: 0
Missing headers: 0
Duplicate headers: 0
Duplicate rows: 0
Inconsistent rows: 0
Missing values: 0
```

### CSV Containing Issues — Summary Mode

```text
$ csvguard analyze examples/customers_dirty.csv

Issues found in file!
Total issues: 7
Missing headers: 0
Duplicate headers: 1
Duplicate rows: 1
Inconsistent rows: 0
Missing values: 5
```

### CSV Containing Issues — Detailed Mode

Using the `--details` option displays the locations of detected problems:

```text
$ csvguard analyze examples/customers_dirty.csv --details

Issues found in file!
Total issues: 7
Missing headers: 0
Duplicate headers: 1

Column number: 4 | Header name: age

Duplicate rows: 1

Row number: 5 | Row data: ['Ali', 'ali@example.com', '21', '21']

Inconsistent rows: 0
Missing values: 5

Row number: 3 | Column name: email | Column number: 2
Row number: 6 | Column name: name | Column number: 1
Row number: 6 | Column name: email | Column number: 2
Row number: 6 | Column name: age | Column number: 3
Row number: 6 | Column name: age | Column number: 4
```

## Project Structure

```text
CSVGuard/
├── examples/
│   ├── customers.csv
│   ├── customers_dirty.csv
│   ├── customers_t1.csv
│   └── invalid_encoding.csv
├── src/
│   └── csvguard/
│       ├── __init__.py
│       ├── analyzer.py
│       ├── cli.py
│       └── reader.py
├── tests/
│   ├── test_analyzer.py
│   ├── test_cli.py
│   └── test_reader.py
├── pyproject.toml
└── README.md
```

## Running Tests

CSVGuard uses [pytest](https://docs.pytest.org/) for its test suite.

Run all tests:

```bash
py -m pytest
```

Run tests with verbose output:

```bash
py -m pytest -v
```

Run a specific test file:

```bash
py -m pytest tests/test_cli.py
```

## Technologies

- **Python 3.10+:** Main programming language.
- **Typer:** Command-line application framework.
- **CSV (Python Standard Library):** CSV file parsing.
- **Pathlib (Python Standard Library):** File and path handling.
- **pytest:** Testing framework.

## License

The project currently has no license specified.