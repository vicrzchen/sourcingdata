# -*- coding: utf-8 -*-
import scrapy
from sourcingdata.scrapy_db.dbkits import \
    SourcingAnnouncementToReadDBOperation, \
    SourcingAnnouncementToRead, \
    DBKits
from scrapy import Request


class GdgovdataDetailSpider(scrapy.Spider):
    name = 'gdgovdata_detail'
    allowed_domains = ['www.gdgpo.gov.cn']
    start_urls = ['http://www.gdgpo.gov.cn/']
    custom_settings = {"RANDOM_DELAY": 0, "COOKIES_ENABLED": False, "DOWNLOADER_MIDDLEWARES": {
        "sourcingdata.middleware.random_delay_middleware.RandomDelayMiddleware": 999,
        "sourcingdata.middleware.gdgovdata_detail_middleware.GDGovDataDetailDownloaderMiddleware": 543, }, "CONCURRENT_REQUESTS": 2}

    def parse(self, response):
        result:SourcingAnnouncementToRead = \
            self.sourcing_message_to_read_DB_operation.query_record(
                {SourcingAnnouncementToRead.read_flag is False}).get(ident=2)
        pass

    def __init__(self):
        self.databaseConnection = DBKits()
        self.sourcing_message_to_read_DB_operation = SourcingAnnouncementToReadDBOperation(db_engine=self.databaseConnection)
