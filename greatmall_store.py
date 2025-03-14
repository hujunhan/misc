import requests
from bs4 import BeautifulSoup

# URL of the store list
url = "https://www.simon.com/mall/great-mall/stores?&filter=store_type%7CstoreType%2F1"

# Headers to mimic a real browser request
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36"
}

# Send a GET request
response = requests.get(url, headers=headers)

# Check if the request was successful
if response.status_code == 200:
    # Parse the HTML content of the page
    soup = BeautifulSoup(response.text, "html.parser")

    # Find all store entries based on observed structure
    store_list = []
    store_items = soup.select(
        "div.no-gutter-mobile.directory-store"
    )  # Adjusted selector based on provided element

    for store in store_items:
        store_name = store.get(
            "title"
        )  # Extract the 'title' attribute for the store name
        if store_name:
            store_list.append(store_name.strip())

    # Print the store names
    print("Store List:")
    for name in store_list:
        print(name)
else:
    print(f"Failed to retrieve the page. Status code: {response.status_code}")
