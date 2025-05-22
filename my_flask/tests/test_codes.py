import requests
from collections import Counter


def test_unique_codes():
    codes = []
    for _ in range(3):
        response = requests.get('http://localhost:5000/codes')
        codes.extend(response.text.split())

    duplicates = [item for item, count in Counter(codes).items() if count > 1]
    print(f"重复码数量: {len(duplicates)}")


if __name__ == '__main__':
    test_unique_codes()