# Python script to get the lowest price of a shopping list from Amazon
# Input: link to the shopping list
# Output: lowest price of the shopping list of each item
from wishlist.core import Wishlist
import requests
from bs4 import BeautifulSoup
import time
from selenium import webdriver

options = webdriver.ChromeOptions()
options.add_argument("--headless")
options.add_argument("--ignore-certificate-errors")
options.add_argument("--incognito")
driver = webdriver.Chrome("./chromedriver", options=options)

# https://www.amazon.com/hz/wishlist/ls/3DGKBIQCC090M/ref=nav_wishlist_lists_1
# make it public
# Get the url list of the items
LIST_NAME = "3DGKBIQCC090M"
url_list = []
title_list = []
# w = Wishlist(LIST_NAME)
# for item in w:
#     title_list.append(item.title)
#     url_list.append(item.url)
# print(url_list)


def get_lowest_price(span_list):
    price_list = []
    for span in span_list:
        price = span.text
        try:
            if price[0] == "$":
                price_list.append(float(price[1:].replace(",", "")))
        except:
            pass
    if len(price_list) == 0:
        print("No price data")
        return 0
    else:
        return min(price_list)


def check_price(url):
    driver.get(url)
    page_source = driver.page_source
    soup = BeautifulSoup(page_source, "html.parser")
    # find all 'a-offscreen' class
    price_data = soup.find_all("span", {"class": "a-offscreen"})

    if len(price_data) == 0:
        print("No price data")
        return
    lowest_p = get_lowest_price(price_data)
    print(lowest_p)


# Get the lowest price of each item
# in used or new condition
# for i in range(len(url_list)):
#     print(title_list[i])
#     time.sleep(1)
#     check_price(url_list[i])
check_price(
    "https://www.amazon.com/dp/B07VPQV7BY/?coliid=I3FMVSIPZ0S399&colid=3DGKBIQCC090M&psc=1&ref_=lv_ov_lig_dp_it"
)
