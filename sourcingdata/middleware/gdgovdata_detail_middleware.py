from scrapy import signals
from scrapy.http import HtmlResponse
from logging import getLogger, error


class GDGovDataDetailDownloaderMiddleware:
    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request, spider):

        return None

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)