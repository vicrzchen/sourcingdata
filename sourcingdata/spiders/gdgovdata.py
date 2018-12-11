# -*- coding: utf-8 -*-
import scrapy
from sourcingdata.scrapy_db.dbkits import RequirementToReadDBOperation, RequirementToRead
from sourcingdata.scrapy_db.dbkits import SourcingAnnouncementToRead, SourcingAnnouncementToReadDBOperation
from sourcingdata.scrapy_db.dbkits import ContractInfoToRead, ContractInfoToReadDBOperation
from sourcingdata.scrapy_db.dbkits import DBKits
from scrapy import Request
from urllib.parse import urljoin, urlsplit
from logging import error

from sourcingdata.scrapy_db.constvalue import \
    START_URL_REQUIREMENT_TO_BE_READ, \
    START_URL_SOURCING_ANNOUNCEMENT_TO_BE_READ, \
    START_URL_CONTRACT_INFO_TO_BE_READ


class GdgovdataSpider(scrapy.Spider):
    name = 'gdgovdata'
    # start_urls = [START_URL_REQUIREMENT_TO_BE_READ,
    # start_urls = [START_URL_SOURCING_ANNOUNCEMENT_TO_BE_READ, ]
    start_urls = [START_URL_CONTRACT_INFO_TO_BE_READ, ]
    # requirement_to_read list
    # start_urls = ['http://www.gdgpo.gov.cn/queryPrjReqList.html']
    requirement_to_read_start_url = START_URL_REQUIREMENT_TO_BE_READ
    sourcing_announcement_to_read_url = START_URL_SOURCING_ANNOUNCEMENT_TO_BE_READ
    contract_info_to_read_url = START_URL_CONTRACT_INFO_TO_BE_READ
    allowed_domains = ['gdgpo.gov.cn']
    custom_settings = {"RANDOM_DELAY": 7,
                       "COOKIES_ENABLED": False,
                       "DOWNLOADER_MIDDLEWARES": {"sourcingdata.middleware.random_delay_middleware.RandomDelayMiddleware": 999,
                                                  "sourcingdata.middlewares.SourcingdataDownloaderMiddleware": 543, },
                       "CONCURRENT_REQUESTS": 2}

    def parse(self, response):
        if response.url == self.requirement_to_read_start_url:
            return self.parse_requirement_to_read(response)
        if response.url == self.sourcing_announcement_to_read_url:
            return self.parse_sourcing_announcement_to_read(response)
        if response.url == self.contract_info_to_read_url:
            return self.parse_contract_info_to_read(response)
        # print(response.text)

        pass

    def parse_sourcing_announcement_to_read(self, response):
        stop_turn_page = False
        for match_data in response.xpath('//div[@class="m_m_cont"]/ul[@class="m_m_c_list"]/li'):
            url_data = SourcingAnnouncementToRead()
            url_data.announce_time = match_data.xpath('.//em/text()')[0].extract()
            url_data.project_name = match_data.xpath('./a/@title')[0].extract().replace(' ', '').\
                replace('\n', '').replace('\t', '')
            url_data.belong_to = match_data.xpath('.//span/a/text()')[0].extract()
            url_info = urlsplit(response.url)
            url_data.project_url = urljoin(url_info.scheme + '://' + url_info.netloc,
                                           match_data.xpath('./a/@href')[0].extract())
            query_conditions = {SourcingAnnouncementToRead.project_url == url_data.project_url}
            if self.sourcing_announcement_to_read_DB_operation.query_record(query_conditions).count() == 0:
                self.sourcing_announcement_to_read_DB_operation.insert_record(sourcing_announcement_to_read_data=
                                                                              url_data)
            else:
                stop_turn_page = False
            pass
        if not stop_turn_page:
            yield Request(response.url, callback=self.parse_sourcing_announcement_to_read, dont_filter=True)
        pass

    def parse_requirement_to_read(self, response):
        for match_data in response.xpath('.//table[@class="m_m_dljg"]/tbody/tr'):
            if len(match_data.xpath('.//td[1]/text()').extract()) > 0:
                url_data = RequirementToRead()
                url_data.list_id = match_data.xpath('.//td[1]/text()')[0].extract()
                url_data.purchasor = match_data.xpath('.//td[2]/@title')[0].extract()
                url_data.bidding_agent = match_data.xpath('.//td[3]/@title')[0].extract()
                url_data.project_name = match_data.xpath('.//td[4]/@title')[0].extract()
                url_data.items_name = match_data.xpath('.//td[5]/@title')[0].extract()
                url_data.announce_date = match_data.xpath('.//td[6]/text()')[0].\
                    extract().replace('\n', '').replace(' ', '')
                url_data.portal_name = match_data.xpath('.//td[7]/text()')[0].\
                    extract().replace('\n', '').replace(' ', '')
                url_info = urlsplit(response.url)
                url_data.url_to_read = urljoin(url_info.scheme + '://' + url_info.netloc,
                                               match_data.xpath('.//td[8]/a/@href')[0].extract())
                query_conditions = {RequirementToRead.url_to_read == url_data.url_to_read}
                if self.require_to_read_DB_operation.query_record(query_conditions).count() == 0:
                    self.require_to_read_DB_operation.insert_record(requirement_to_read_data=url_data)
        yield Request(response.url, callback=self.parse_requirement_to_read, dont_filter=True)
        pass

    def __init__(self, category=None, *args, **kwargs):
        super(GdgovdataSpider, self).__init__(*args, **kwargs)
        self.databaseConnection = DBKits()
        self.require_to_read_DB_operation = RequirementToReadDBOperation(db_engine=self.databaseConnection)
        self.sourcing_announcement_to_read_DB_operation = \
            SourcingAnnouncementToReadDBOperation(db_engine=self.databaseConnection)
        self.contract_to_read_DB_operation = ContractInfoToReadDBOperation(db_engine=self.databaseConnection)
        self.duplicate_record_qty = 0
        pass

    def parse_contract_info_to_read(self, response):
        stop_turn_page = False
        counter = 0
        for match_data in response.xpath('//div[@class="m_m_cont"]/table[@class="m_m_dljg"]/tbody/tr'):
            if counter > 0:
                try:
                    url_data = ContractInfoToRead()
                    url_data.purchasor = match_data.xpath('.//td[2]/@title')[0].extract()
                    url_data.vendor = match_data.xpath('.//td[3]/@title')[0].extract()
                    url_data.project_id = match_data.xpath('.//td[4]/@title')[0].extract()
                    url_data.contract_name = match_data.xpath('.//td[5]/@title')[0].extract()
                    url_data.contract_value = match_data.xpath('.//td[6]/text()')[0].extract().\
                        replace('\n', '').replace(' ', '')
                    url_data.contract_sign_date = match_data.xpath('.//td[7]/text()')[0].extract().\
                        replace('\n', '').replace(' ', '')
                    url_data.announce_date = match_data.xpath('.//td[8]/text()')[0].extract().\
                        replace('\n', '').replace(' ', '')
                    url_info = urlsplit(response.url)

                    url_data.url_to_read = urljoin(url_info.scheme + '://' + url_info.netloc,
                                                   match_data.xpath('.//td[9]/a/@href')[0].extract())
                    query_conditions = {ContractInfoToRead.url_to_read == url_data.url_to_read}
                    if self.contract_to_read_DB_operation.query_record(query_conditions).count() == 0:
                        self.contract_to_read_DB_operation.insert_record(contract_info_to_read_data=url_data)
                    else:
                        self.duplicate_record_qty += 1
                    if self.duplicate_record_qty > 200:
                        stop_turn_page = True
                        print('reach duplicate')
                    pass
                except Exception as exceptinfo:
                    error('Mismatch record!')
                    error(exceptinfo)
            counter += 1
        if not stop_turn_page:
            yield Request(response.url, callback=self.parse_contract_info_to_read, dont_filter=True)
        pass
