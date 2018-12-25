# -*- coding: utf-8 -*-
import scrapy
from sourcingdata.scrapy_db.dbkits import RequirementToRead, RequirementToReadDBOperation
from sourcingdata.scrapy_db.dbkits import SourcingAnnouncementToRead, SourcingAnnouncementToReadDBOperation
from sourcingdata.scrapy_db.dbkits import ContractInfoToRead, ContractInfoToReadDBOperation
from sourcingdata.scrapy_db.dbkits import ListItemsMap, ListItemsMapDBOperation
from sourcingdata.scrapy_db.dbkits import SourcingPlansToRead, SourcingPlanToReadDBOperation
from sourcingdata.scrapy_db.dbkits import WebsiteInfo, WebsiteInfoDBOperation
from sourcingdata.scrapy_db.dbkits import AcceptanceToRead, AcceptanceToReadDBOperation
from sourcingdata.scrapy_db.dbkits import DBKits
from sourcingdata.kits.itemsprocessors import ListItemsProcessor
from scrapy import Request
from urllib.parse import urljoin, urlsplit
from logging import error
from sourcingdata.scrapy_db.constvalue import \
    START_URL_REQUIREMENT_TO_BE_READ, \
    START_URL_SOURCING_ANNOUNCEMENT_TO_BE_READ, \
    START_URL_CONTRACT_INFO_TO_BE_READ, \
    START_URL_SOURCING_PLAN_TO_BE_READ, \
    WEBSITE_ID_TO_CRAWL, \
    MAX_DUPLICATE_CONTINUE


class GdgovdataSpider(scrapy.Spider):
    name = 'gdgovdata'
    # start_urls = [START_URL_REQUIREMENT_TO_BE_READ,
    # start_urls = [START_URL_SOURCING_ANNOUNCEMENT_TO_BE_READ, ]
    # todo: when change type, please modify the below
    start_urls = [START_URL_SOURCING_PLAN_TO_BE_READ, ]
    # requirement_to_read list
    # start_urls = ['http://www.gdgpo.gov.cn/queryPrjReqList.html']
    requirement_to_read_start_url = START_URL_REQUIREMENT_TO_BE_READ
    sourcing_announcement_to_read_url = START_URL_SOURCING_ANNOUNCEMENT_TO_BE_READ
    contract_info_to_read_url = START_URL_CONTRACT_INFO_TO_BE_READ
    sourcing_plans_to_read_url = START_URL_SOURCING_PLAN_TO_BE_READ
    allowed_domains = ['gdgpo.gov.cn']
    custom_settings = {"RANDOM_DELAY": 7,
                       "COOKIES_ENABLED": False,
                       "DOWNLOADER_MIDDLEWARES": {"sourcingdata.middleware.random_delay_middleware.RandomDelayMiddleware": 999,
                                                  "sourcingdata.middlewares.SourcingdataDownloaderMiddleware": 543, },
                       "CONCURRENT_REQUESTS": 2}

    def parse(self, response):
        if response.url == self.requirement_to_read_start_url:
            self.DB_operation = self.require_to_read_DB_operation
        if response.url == self.sourcing_announcement_to_read_url:
            self.DB_operation = self.sourcing_announcement_to_read_DB_operation
        if response.url == self.contract_info_to_read_url:
            self.DB_operation = self.contract_to_read_DB_operation
        if response.url == self.sourcing_plans_to_read_url:
            self.DB_operation = self.sourcing_plans_to_read_DB_operation
            # return self.parse_sourcing_plan_to_read(response)
        # todo: when new type added, need assign DB operation
        return self.parse_for_list_object(response)

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
                self.sourcing_announcement_to_read_DB_operation.insert_record(url_data,
                                                                              skip_duplicated_record=False)
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
                    self.require_to_read_DB_operation.insert_record(url_data,
                                                                    skip_duplicated_record=False)
        yield Request(response.url, callback=self.parse_requirement_to_read, dont_filter=True)
        pass

    def __init__(self, category=None, *args, **kwargs):
        super(GdgovdataSpider, self).__init__(*args, **kwargs)
        self.databaseConnection = DBKits()
        self.require_to_read_DB_operation = \
            RequirementToReadDBOperation(db_engine=self.databaseConnection)
        self.sourcing_announcement_to_read_DB_operation = \
            SourcingAnnouncementToReadDBOperation(db_engine=self.databaseConnection)
        self.contract_to_read_DB_operation = \
            ContractInfoToReadDBOperation(db_engine=self.databaseConnection)
        self.list_items_map_DB_Operation = \
            ListItemsMapDBOperation(db_engine=self.databaseConnection)
        self.sourcing_plans_to_read_DB_operation = \
            SourcingPlanToReadDBOperation(db_engine=self.databaseConnection)
        self.website_info_DB_operation = \
            WebsiteInfoDBOperation(db_engine=self.databaseConnection)
        self.duplicate_record_qty = 0
        self.items_processor = ListItemsProcessor()
        self.items_processor.read_item_parameter(db_connection=self.databaseConnection, websiteID=WEBSITE_ID_TO_CRAWL)
        self.website_info = WebsiteInfo()
        self.website_info = self.website_info_DB_operation.query_record(
            {WebsiteInfo.website_id == WEBSITE_ID_TO_CRAWL}).first()
        self.duplicate_record_condition = None
        self.DB_operation = None
        pass

    def parse_contract_info_to_read(self, response):
        # self.parse_for_list_object(website_id=4)
        stop_turn_page = False
        counter = 0
        for match_data in response.xpath('//div[@class="m_m_cont"]/table[@class="m_m_dljg"]/tbody/tr'):
            if counter > 0:
                try:
                    url_data = ContractInfoToRead()
                    url_data = self.items_processor.get_data(match_xpath=match_data, result_data=url_data)
                    query_conditions = {ContractInfoToRead.url_to_read == url_data.url_to_read}
                    if self.contract_to_read_DB_operation.query_record(query_conditions).count() == 0:
                        self.contract_to_read_DB_operation.insert_record(url_data,
                                                                         skip_duplicated_record=False)
                        if self.duplicate_record_qty > 0:
                            self.duplicate_record_qty -= 1
                    else:
                        self.duplicate_record_qty += 1
                    url_data = None
                    if self.duplicate_record_qty > MAX_DUPLICATE_CONTINUE:
                        stop_turn_page = True
                        print('reach duplicate')
                    print('duplated record number is %d' % self.duplicate_record_qty)
                    pass
                except Exception as exceptinfo:
                    error('Mismatch record!')
                    error(exceptinfo)
            counter += 1
        if not stop_turn_page:
            yield Request(response.url, callback=self.parse_contract_info_to_read, dont_filter=True)
        pass

    def parse_sourcing_plan_to_read(self, response):
        # self.parse_for_list_object(website_id=4)
        stop_turn_page = False
        counter = 0
        for match_data in response.xpath('//div[@class="m_m_cont"]/table[@class="m_m_dljg"]/tbody/tr'):
            if counter > 0:
                try:
                    url_data = SourcingPlansToRead()
                    url_data = self.items_processor.get_data(match_xpath=match_data, result_data=url_data)
                    query_conditions = {SourcingPlansToRead.detail_url == url_data.detail_url}
                    if self.sourcing_plans_to_read_DB_operation.query_record(query_conditions).count() == 0:
                        self.sourcing_plans_to_read_DB_operation.insert_record(url_data,
                                                                               skip_duplicated_record=False)
                    else:
                        self.duplicate_record_qty += 1
                        print('duplicated project id is %s, url is %s' % (url_data.project_id, url_data.detail_url))
                    url_data = None
                    if self.duplicate_record_qty > MAX_DUPLICATE_CONTINUE:
                        stop_turn_page = True
                        print('reach duplicate')
                    pass
                except Exception as exceptinfo:
                    error('Mismatch record!')
                    error(exceptinfo)
            counter += 1
        if not stop_turn_page:
            yield Request(response.url, callback=self.parse_sourcing_plan_to_read, dont_filter=True)
        pass

    def parse_for_list_object(self, response):
        stop_turn_page = False
        counter = 0
        for match_data in response.xpath(self.website_info.website_match_str):
            if counter > 0:
                try:
                    list_object = globals()[self.website_info.object_name]()
                    list_object = self.items_processor.get_data(match_xpath=match_data, result_data=list_object)
                    # todo: 看是否能有更优化的做法
                    # todo: add new type website
                    # query_conditions = {SourcingPlansToRead.detail_url == list_object.detail_url}
                    query_conditions = self.DB_operation.get_duplicate_condition(list_object)
                    if self.DB_operation.query_record(query_conditions).count() == 0:
                        self.DB_operation.insert_record(list_object, skip_duplicated_record=False)
                    else:
                        self.duplicate_record_qty += 1
                    list_object = None
                    if self.duplicate_record_qty > MAX_DUPLICATE_CONTINUE:
                        stop_turn_page = True
                        print('reach duplicate')
                    pass
                except Exception as exceptinfo:
                    error('Mismatch record!')
                    error(exceptinfo)
            counter += 1
        if not stop_turn_page:
            yield Request(response.url, callback=self.parse_for_list_object, dont_filter=True)
        pass