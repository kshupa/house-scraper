# from selenium import webdriver
# from bs4 import BeautifulSoup
# from time import sleep
# import requests
# import os

# # url = os.environ["REAL_ESTATE_URL"]
# # print(url)
# url = "https://www.zillow.com/homes/Wylie,-TX_rb/"
# # print(url)
# page = requests.get(url)
# # driver = webdriver.Chrome()
# # page.get(url)
# # sleep(10)

# soup = BeautifulSoup(page.content, "html.parser")

# # lists = driver.find_elements_by_css_selector("div.item ng-star-inserted").text

# # lists = soup.find_all("div", {'class': "list-card-info"})

# # for l in lists:
# #     price = l.find("div", class_="list-card-price").text
# #     address = l.find("address", class_="list-card-addr").text
# #     # area = list.find_all("p", class_="price")

# #     print(price, address)


# properties = soup.find("ul", {"class": "photo-cards photo-cards_wow photo-cards_short photo-cards_extra-attribution"}).find_all("li")
# for e in properties:
#     price = e.find("article").find("div", {"class": "list-card-price"}).text
#     address = e.find("article").find("div", {"class": "list-card-addr"}).text
#     properties.append([price, address])
#     print(properties)


import json
import requests
from bs4 import BeautifulSoup


# url = "https://www.zillow.com/homes/Wylie,-TX_rb/"
url = "https://www.zillow.com/homes/for_sale/?searchQueryState=%7B%22pagination%22%3A%7B%7D%2C%22usersSearchTerm%22%3A%22Wylie%2C%20TX%22%2C%22mapBounds%22%3A%7B%22west%22%3A-97.14777711964818%2C%22east%22%3A-96.25651125050756%2C%22south%22%3A32.834439575661484%2C%22north%22%3A33.323487247721886%7D%2C%22isMapVisible%22%3Atrue%2C%22filterState%22%3A%7B%22price%22%3A%7B%22min%22%3A200000%2C%22max%22%3A400000%7D%2C%22mp%22%3A%7B%22min%22%3A663%2C%22max%22%3A1326%7D%2C%22ah%22%3A%7B%22value%22%3Atrue%7D%2C%22con%22%3A%7B%22value%22%3Afalse%7D%2C%22mf%22%3A%7B%22value%22%3Afalse%7D%2C%22manu%22%3A%7B%22value%22%3Afalse%7D%2C%22tow%22%3A%7B%22value%22%3Afalse%7D%2C%22apa%22%3A%7B%22value%22%3Afalse%7D%2C%22apco%22%3A%7B%22value%22%3Afalse%7D%7D%2C%22isListVisible%22%3Atrue%2C%22mapZoom%22%3A11%7D"
headers = {
    "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:91.0) Gecko/20100101 Firefox/91.0"
}

soup = BeautifulSoup(requests.get(url, headers=headers).content, "html.parser")

data = json.loads(
    soup.select_one("script[data-zrr-shared-data-key]").contents[0].strip("!<>-")
)

# uncomment this to print all data:
# print(json.dumps(data, indent=4))

for result in data["cat1"]["searchResults"]["listResults"]:
    print(
        "{:<15} {:<50} {:<15}".format(
            result["statusText"], result["address"], result["price"]
        )
    )
