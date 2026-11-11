from pathlib import Path


def test_path():
    file_path = Path(input("Enter the file path: "))
    if file_path.exists():
        if file_path.is_file():
            print(file_path, "is a file.")
        else:
            print(file_path, "is not a file.")
    else:
        print(file_path, "does not exist.")


if __name__ == "__main__":
    test_path()
