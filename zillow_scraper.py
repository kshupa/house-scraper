import csv
import json
import requests
from bs4 import BeautifulSoup


class ZillowScraper:
    final_results = []
    headers = {
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        "accept-encoding": "gzip, deflate, br",
        "accept-language": "en-US,en;q=0.9",
        "cache-control": "max-age=0",
        "cookie": "zguid=23|%24bca19a7a-8e22-4461-82f8-f11c82199f28; zgsession=1|8bfede42-5d6a-4678-84bd-0bec5dd3fa59; _ga=GA1.2.939108706.1637283491; zjs_user_id=null; zjs_anonymous_id=%22bca19a7a-8e22-4461-82f8-f11c82199f28%22; _pxvid=c4a00909-48d3-11ec-a8ac-58666665424a; _gcl_au=1.1.790680264.1637283495; KruxPixel=true; DoubleClickSession=true; _fbp=fb.1.1637283495551.723233755; __pdst=1883e6bcf1534c7c84d1724a12ecfb6e; __gads=ID=8ea890cabca54f75:T=1637283495:S=ALNI_MaBfXLyVoWvtFwsHZLglUeAzo51xQ; KruxAddition=true; G_ENABLED_IDPS=google; _pin_unauth=dWlkPVl6ZGhZakprTXpZdE9UWmhZUzAwWlRjMkxXRmxPVFl0WXpVelpEZGxZamd4TjJGaw; utag_main=v_id:017d35b381ab0005ce8e41be4cd505078018307000c9e$_sn:2$_se:1$_ss:1$_st:1637364488575$dc_visit:2$ses_id:1637362688575%3Bexp-session$_pn:1%3Bexp-session$dcsyncran:1%3Bexp-session$tdsyncran:1%3Bexp-session$dc_event:1%3Bexp-session$dc_region:us-east-1%3Bexp-session$ttd_uuid:e398ba4c-00c4-45fc-86c3-c00c0a3e378d%3Bexp-session; _uetvid=c777b86048d311ec9c408d9122dddc96; JSESSIONID=957C4B609D01C72DDF805821CE2F167F; _gid=GA1.2.690201787.1637529144; _px3=7b455ec9a60a42c29958383a421fa874956aa5723a07dd7e39d71ba191697d1c:x4FrxpCcZitKSuclgwPtH7Q73xUmstnZv41s8rnR9q0UATclA2uGIURtZ9EWqEchkae9bB5PF6tTAUZFhaKNBg==:1000:+DuBValPVd+VJIPNpq/e2HFwWyQUjmGbivnSjTC4KgrnMSuK+Sa0tTO6CcGv1dLefObt9anKHZa+tcWuaJJu7qUjc6teI3sCRsI+/kPLV19visKSl84p9eJUOYsMPq826VLZ99w43SJyIfCkWDCmy/4QGsMsrOZXsPr6bB4lHWuJfiuHsyYWjucyvDxWkUXjpu2Xomq5PP67r9B31NyMSA==; AWSALB=KOYWnUPKJwAgdLKPOVQmZabP9+0FFbdSquu3zBPHspTC5l/Ch2gF0ex8Iuopp96J9IhKf5zl3m6OvGjdE/yAaJ4x74ekYsWW9wIZFHrjI0PeympGWaXFmO+P+mfy; AWSALBCORS=KOYWnUPKJwAgdLKPOVQmZabP9+0FFbdSquu3zBPHspTC5l/Ch2gF0ex8Iuopp96J9IhKf5zl3m6OvGjdE/yAaJ4x74ekYsWW9wIZFHrjI0PeympGWaXFmO+P+mfy; search=6|1640121859086%7Crect%3D33.3445103853356%252C-96.39771053271484%252C33.10038515758498%252C-96.84334346728515%26rid%3D32783%26disp%3Dmap%26mdm%3Dauto%26p%3D1%26sort%3Ddays%26z%3D1%26type%3Dhouse%252Cland%26price%3D250000-360000%26mp%3D825-1188%26fs%3D1%26fr%3D0%26mmm%3D0%26rs%3D0%26ah%3D0%26singlestory%3D0%26housing-connector%3D0%26abo%3D0%26garage%3D0%26pool%3D0%26ac%3D0%26waterfront%3D0%26finished%3D0%26unfinished%3D0%26cityview%3D0%26mountainview%3D0%26parkview%3D0%26waterview%3D0%26hoadata%3D1%26zillow-owned%3D0%263dhome%3D0%26featuredMultiFamilyBuilding%3D0%09%0932783%09%09%09%09%09%09",
        "referer": "https://www.zillow.com/homes/for_sale/?searchQueryState=%7B%22pagination%22%3A%7B%7D%2C%22usersSearchTerm%22%3A%22McKinney%2C%20TX%22%2C%22mapBounds%22%3A%7B%22west%22%3A-96.84334346728515%2C%22east%22%3A-96.39771053271484%2C%22south%22%3A33.10038515758498%2C%22north%22%3A33.3445103853356%7D%2C%22isMapVisible%22%3Atrue%2C%22filterState%22%3A%7B%22price%22%3A%7B%22min%22%3A250000%2C%22max%22%3A360000%7D%2C%22mp%22%3A%7B%22min%22%3A825%2C%22max%22%3A1188%7D%2C%22ah%22%3A%7B%22value%22%3Atrue%7D%2C%22con%22%3A%7B%22value%22%3Afalse%7D%2C%22mf%22%3A%7B%22value%22%3Afalse%7D%2C%22manu%22%3A%7B%22value%22%3Afalse%7D%2C%22tow%22%3A%7B%22value%22%3Afalse%7D%2C%22apa%22%3A%7B%22value%22%3Afalse%7D%2C%22apco%22%3A%7B%22value%22%3Afalse%7D%7D%2C%22isListVisible%22%3Atrue%2C%22mapZoom%22%3A12%7D",
        "sec-ch-ua": '" Not A;Brand";v="99", "Chromium";v="96", "Google Chrome";v="96"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "macOS",
        "sec-fetch-dest": "document",
        "sec-fetch-mode": "navigate",
        "sec-fetch-site": "same-origin",
        "sec-fetch-user": "?1",
        "upgrade-insecure-requests": "1",
        "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.55 Safari/537.36",
    }

    def fetch(self, url, params):
        response = requests.get(url, headers=self.headers, params=params)
        print(response)
        return response

    def parse(self, response):
        soup = BeautifulSoup(response, features="html.parser")
        listings = soup.find(
            "ul",
            {
                "class": "photo-cards photo-cards_wow photo-cards_short photo-cards_extra-attribution"
            },
        )
        for listing in listings.contents:
            script = listing.find("script", {"type": "application/ld+json"})
            if script:
                json_script = json.loads(script.contents[0])
                self.final_results.append(
                    {
                        "name": json_script["name"],
                        "url": json_script["url"],
                        "floor_size": json_script["floorSize"]["value"],
                        "price": listing.find("div", {"class": "list-card-price"}).text,
                    }
                )
        print(self.final_results)

    def write_to_csv(self):
        with open("zillow.csv", "w") as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=self.final_results[0].keys())
            writer.writeheader

            for row in self.final_results:
                writer.writerow(row)

    def run(self):
        url = "https://www.zillow.com/homes/McKinney,-TX_rb/"
        params = {
            "pagination": {"currentPage": 1},
            "usersSearchTerm": "McKinney, TX",
            "mapBounds": {
                "west": -96.84334346728515,
                "east": -96.39771053271484,
                "south": 33.10038515758498,
                "north": 33.3445103853356,
            },
            "regionSelection": [{"regionId": 32783, "regionType": 6}],
            "isMapVisible": "false",
            "filterState": {
                "price": {"min": 0, "max": 360000},
                "mp": {"min": 825, "max": 1188},
                "ah": {"value": "true"},
                "con": {"value": "false"},
                "mf": {"value": "false"},
                "manu": {"value": "false"},
                "tow": {"value": "false"},
                "apa": {"value": "false"},
                "apco": {"value": "false"},
            },
            "isListVisible": "true",
            "mapZoom": 12,
        }

        fethced_response = self.fetch(url, params)
        self.parse(fethced_response.text)
        # if need to parse more than one page
        # time.sleep(2)


if __name__ == "__main__":
    scraper = ZillowScraper()
    scraper.run()
    scraper.write_to_csv()
