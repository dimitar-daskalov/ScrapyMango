import scrapy
import json


class MangoSpider(scrapy.Spider):
    name = "mango"

    # providing the url for the product
    start_urls = [
        'https://shop.mango.com/gb/women/skirts-midi/midi-satin-skirt_17042020.html?c=99'
    ]

    headers = {
        ':authority': 'shop.mango.com',
        ':method': 'GET',
        ':path': '/services/garments/1704202099',
        ':scheme': 'https',
        'accept': 'application/json, text/plain, */*',
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'bg-BG,bg;q=0.9',
        'cache-control': 'no-cache',
        'pragma': 'no-cache',
        'referer': 'https://shop.mango.com/gb/women/skirts-midi/midi-satin-skirt_17042020.html?c=99',
        'sec-ch-ua': '"Chromium";v="94", "Google Chrome";v="94", ";Not A Brand";v="99"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': 'Windows',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'stock-id': '006.IN.0.false.false.v3',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36'
    }

    def parse(self, response):
        url = 'https://shop.mango.com/services/garments/1704202099'

        # simulating a request, so we can get the data from the response
        yield scrapy.Request(
            url,
            callback=self.parse_api,
            headers=self.headers
        )

    def parse_api(self, response):
        # extracting the raw data from the JSON response
        raw_data = response.body
        data = json.loads(raw_data)

        # providing the default color of the product
        default_color = ""
        for el in data["colors"]["colors"]:
            if el["default"]:
                default_color = el
                break

        # extracting the sizes with list comprehension
        sizes = [el["value"] for el in default_color["sizes"] if not el["value"] == "0"]

        # providing the product info and returning it
        product_info = {
            "name": data["name"],
            "price": data["price"]["price"],
            "color": default_color["label"],
            "size": sizes
        }

        yield product_info
