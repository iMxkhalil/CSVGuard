from pathlib import Path
from csvguard.reader import read_csv


path = Path("examples/customers.csv")

try:
    result = read_csv(path)
except FileNotFoundError as error:
    print(str(error))
except IsADirectoryError as error:
    print(str(error))   
except PermissionError as error:
    print(str(error))
except UnicodeDecodeError as error:
    print(str(error))
else:
    print(result)