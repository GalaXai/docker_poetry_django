import scrapy, json


class ProxyListSpider(scrapy.Spider):
    name = "proxylistscraper"
    allowed_domains = ["www.proxy-list.download"]

    # the file is run from root/poxy
    file_path = "proxy/country_codes.json"

    # Open and load the JSON file as a Python dictionary
    with open(file_path, "r", encoding="utf-8") as json_file:
        country_codes = json.load(json_file)

    codes = [country_code["code"] for country_code in country_codes]
    start_urls = [f"https://www.proxy-list.download/api/v1/get?type=http&country={code}" for code in codes]

    def parse(self, response):
        page = response.body.decode("utf-8").split("\r\n")
        for proxy in page:
            yield ({f"{proxy.split(':')[0]}": f"{proxy.split(':')[-1]}"})
