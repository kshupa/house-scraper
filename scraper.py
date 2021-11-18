from typing_extensions import Required
from bs4 import BeautifulSoup
import requests
import os

url = os.environ["REAL_ESTATE_URL"]
page = requests.get(url)

soup = BeautifulSoup(page.content, "html.parser")

lists = soup.find_all(div="_ngcontent-nkb-c122", class_="property-container")

for list in lists:
    price = list.find(span="_ngcontent-nkb-c158", class_="ng-star-inserted")
    # location = list.find_all("p", class_="price")
    # area = list.find_all("p", class_="price")

    print(price)
