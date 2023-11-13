import scrapy
import json
import base64


class ProxyCzSpider(scrapy.Spider):
    name = "proxyczscraper"
    # allowed_domains = ["free-proxy.cz"]

    # the file is run from root/poxy
    file_path = "proxy/country_codes.json"

    # Open and load the JSON file as a Python dictionary
    with open(file_path, "r", encoding="utf-8") as json_file:
        country_codes = json.load(json_file)

    codes = [country_code["code"] for country_code in country_codes]
    # codes = {'US', 'PL', 'DE'} for debugging purposes
    start_urls = [f"http://www.free-proxy.cz/en/proxylist/country/{code}/https/ping/all" for code in codes]

    def parse(self, response):
        table = response.xpath('//table[@id="proxy_list"]/tbody/tr')
        for row in table:
            ip_script = row.xpath('.//td[1]/script/text()').get()
            if ip_script:
                # Split safely
                split_script = ip_script.split('"')
                if len(split_script) > 1:
                    ip_encoded = split_script[1]
                    ip_address = base64.b64decode(ip_encoded).decode('utf-8')
                else:
                    # Handle the case where the script doesn't contain the expected format
                    self.logger.warning(f"Unexpected script format: {ip_script}")
                    continue
            else:
                # Direct text extraction for IP address
                ip_address = row.xpath('.//td[1]/text()').get()

            port = row.xpath('.//td[2]/span/text()').get()
            country = row.xpath('.//td[4]/a/text()').get()
            # added for debug reasons since the scrapper grabs only US proxies even tho we provided other country codes

            yield {'IP Address': ip_address, 'Port': port, 'Country': country}
