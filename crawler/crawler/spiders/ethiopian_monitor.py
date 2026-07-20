import scrapy


class EthiopianMonitorSpider(scrapy.Spider):
    name = "ethiopian_monitor"
    allowed_domains = ["ethiopianmonitor.com"]
    start_urls = ["https://ethiopianmonitor.com"]

    def parse(self, response):
        pass
