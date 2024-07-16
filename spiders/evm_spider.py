import scrapy
from typing import Any
from scrapy.http import Response


class EvmSpider(scrapy.Spider):
    name = "evmSpider"
    allowed_domains = ["evm.ink"]
    start_urls = ["https://evm.ink/address/0xf6372ef94026f71e5e48f0ff2ff5ceb06fdff303"]

    def start_requests(self):
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/58.0.3029.110 Safari/537.3'}
        for url in self.start_urls:
            yield scrapy.Request(url, headers=headers)

    def parse(self, response: Response, **kwargs: Any):
        print("网页内容:", response.text)
        pass
