# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from scrapy.http import HtmlResponse
from logging import getLogger, error
from time import sleep
from sourcingdata.scrapy_db.dbkits import DBKits, WebsiteInfoDBOperation, WebsiteInfo, ProxyInfo
from sourcingdata.scrapy_db.constvalue import \
    NEXT_PAGE_OF_REQUIREMENT_TO_BE_READ,\
    NEXT_PAGE_OF_SOURCING_ANNOUNCEMENT_TO_BE_READ, \
    NEXT_PAGE_OF_CONTRACT_INFO_TO_BE_READ,\
    START_URL_REQUIREMENT_TO_BE_READ, \
    START_URL_SOURCING_ANNOUNCEMENT_TO_BE_READ, \
    START_URL_CONTRACT_INFO_TO_BE_READ,\
    TIME_INTERVAL_MIN_SECOND_SOURCING_ANNOUNCEMENT_TO_BE_READ, \
    TIME_INTERVAL_MAX_SECOND_SOURCING_ANNOUNCEMENT_TO_BE_READ
from random import randint
from sourcingdata.middleware.proxy_middleware import get_random_http_proxy, mark_unavailable_proxy, reget_proxy

class SourcingdataSpiderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, dict or Item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Response, dict
        # or Item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


class SourcingdataDownloaderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request, spider):
        # Called for each request that goes through the downloader
        # middleware.

        # Must either:
        # - return None: continue processing this request
        # - or return a Response object
        # - or return a Request object
        # - or raise IgnoreRequest: process_exception() methods of
        #   installed downloader middleware will be called
        next_page_string = ''
        # 以指定首页作为判断依据
        # 设置此次处理的是“采购需求”栏目
        if request.url == START_URL_REQUIREMENT_TO_BE_READ:
            next_page_string = NEXT_PAGE_OF_REQUIREMENT_TO_BE_READ
        # 设置此次处理的是“采购公告”栏目
        if request.url == START_URL_SOURCING_ANNOUNCEMENT_TO_BE_READ:
            next_page_string = NEXT_PAGE_OF_SOURCING_ANNOUNCEMENT_TO_BE_READ
            self.go_to_page_string = '//input[@name="pageIndex"]'
        # 设置此次处理的是“采购合同”栏目
        if request.url == START_URL_CONTRACT_INFO_TO_BE_READ:
            next_page_string = NEXT_PAGE_OF_CONTRACT_INFO_TO_BE_READ
            self.go_to_page_string = '//input[@id="pointPageIndexId"]'

        if self.current_session_access_counter == self.reset_session_pages:
            try:
                self.close_browser(is_error=False)
                self.new_browser()
            except Exception as exceptinfo:
                error(exceptinfo)
                return None

        if len(request.url) > 0:
            got_right_page = False
            try_times = 0
            max_retry_time = 10
            while not got_right_page and try_times < max_retry_time:
                try_times += 1
                try:
                    print('current page is: %s , data is collected' % self.current_page)
                    try:
                        print('before click')
                        self.browser.find_element_by_xpath(next_page_string).click()
                        print('after click')
                    except Exception as exceptinfo:
                        print(exceptinfo)
                        print('Can not find next to click.')
                        self.close_browser(is_error=True)
                        self.new_browser()
                    sleep_time = randint(TIME_INTERVAL_MIN_SECOND_SOURCING_ANNOUNCEMENT_TO_BE_READ,
                                         TIME_INTERVAL_MAX_SECOND_SOURCING_ANNOUNCEMENT_TO_BE_READ)
                    try:
                        self.current_page = int(self.browser.
                                                find_element_by_xpath(self.go_to_page_string).
                                                get_property('value'))
                    except Exception as excepts:
                        print(excepts)
                        # TODO: 考虑处理异常后如何再继续（Done）
                        print('can not open the url')
                        self.close_browser(is_error=True)
                        self.new_browser()
                        # return HtmlResponse(url=request.url, status=500, request=request)
                    print('sleeping......, sleep time is %d' % sleep_time)
                    sleep(sleep_time)
                    page_to_update = WebsiteInfo()
                    page_to_update.current_page_number = self.current_page
                    self.website_info_DB_operation.update_record(query_conditions=self.query_condition,
                                                                 update_data=page_to_update)
                    self.current_session_access_counter += 1
                    got_right_page = True
                except Exception as excepinfo:
                    error(excepinfo)
                    self.first_time_browse = False
                    self.close_browser(is_error=True)
                    self.new_browser()
                    # return HtmlResponse(url=request.url, status=500, request=request)
            if got_right_page:
                return HtmlResponse(url=request.url,
                                    body=self.browser.page_source,
                                    request=request,
                                    encoding='utf-8',
                                    status=200)
            else:
                return HtmlResponse(url=request.url, status=500, request=request)

        else:
            return None

    def process_response(self, request, response, spider):
        # Called with the response returned from the downloader.
        # Must either;
        # - return a Response object
        # - return a Request object
        # - or raise IgnoreRequest
        return response

    def process_exception(self, request, exception, spider):
        # Called when a download handler or a process_request()
        # (from other downloader middleware) raises an exception.

        # Must either:
        # - return None: continue processing this exception
        # - return a Response object: stops process_exception() chain
        # - return a Request object: stops process_exception() chain
        pass

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)

    def __init__(self, timeout=None, service_args=[]):
        # TODO: START_URL 如何按照不同类型的爬虫赋予不同类型的值
        self.START_URL = START_URL_CONTRACT_INFO_TO_BE_READ
        self.go_to_page_string = ''
        self.go_to_page_string = '//input[@id="pointPageIndexId"]'
        # TODO: 结束
        self.logger = getLogger(__name__)
        self.chrome_options = None
        self.first_time_browse = True
        self.timeout = timeout
        self.browser = True
        # current_page = 当前翻到第几页
        self.current_session_access_counter = 0
        self.reset_session_pages = 0
        # 以下处理当前应该跳到第几页
        self.databaseConnection = DBKits()
        self.website_info_DB_operation = WebsiteInfoDBOperation(db_engine=self.databaseConnection)
        self.query_condition = {WebsiteInfo.website_id == 4}
        # self.query_condition = {WebsiteInfo.start_up_url == self.START_URL}
        self.query_result = self.website_info_DB_operation.query_record(query_conditions=self.query_condition)
        self.current_proxy: ProxyInfo = None
        if self.query_result.count() == 1:
            self.current_page = self.query_result.first().current_page_number
        else:
            self.current_page = 1
        self.new_browser()

    def new_browser(self):
        got_right_browser = False
        try_times = 0
        while not got_right_browser and try_times <= 10:
            try_times += 1
            got_right_browser = True
            try:
                self.chrome_options = webdriver.ChromeOptions()
                self.chrome_options.add_argument('disable-infobars')
                prefs = {"profile.managed_default_content_settings.images": 2}
                self.current_proxy = get_random_http_proxy()
                proxy_address = 'http://%s:%s' %(self.current_proxy.proxy_ip, self.current_proxy.proxy_port)
                if self.current_proxy is not None:
                    proxy_str = "--proxy-server=%s" % proxy_address
                    self.chrome_options.add_argument(proxy_str)
                self.chrome_options.add_experimental_option("prefs", prefs)
                self.first_time_browse = True
                self.browser = webdriver.Chrome(executable_path=
                                                'C:\\Users\\vichen-h\Desktop\\chromedriver.exe',
                                                chrome_options=self.chrome_options)
                self.current_session_access_counter = 0
                # 设定浏览器一次性看多少个网页然后关闭
                self.reset_session_pages = randint(100, 125)
            except Exception as expt:
                error(expt)
            try:
                self.browser.get(self.START_URL)
                self.browser.find_element_by_xpath(self.go_to_page_string)
                turn_page_script = 'turnOverPage(' + str(self.current_page) + ')'
                self.browser.execute_script(turn_page_script)
                # if self.browser.find_element_by_class_name():
                #     print('need to call use another proxy')
                self.current_page = self.browser.\
                    find_element_by_xpath(self.go_to_page_string). \
                    get_property('value')
                self.first_time_browse = False
            except Exception as excep:
                error(excep)
                print('can not go at line 249')
                self.close_browser(is_error=True)
                got_right_browser = False

    # 如果因为出错则将代理标记为无效代理，is_error为出错标志
    def close_browser(self, is_error=False):
        self.browser.close()
        self.browser = None
        # TODO: 改回来
        # if self.current_proxy is not None and is_error:
        if self.current_proxy is not None:
            mark_unavailable_proxy(proxy_id=self.current_proxy.proxy_id)
            reget_proxy()

            self.current_proxy = None
        self.chrome_options = None

    def __del__(self):
        self.close_browser(is_error=False)

    def spider_closed(self, spider):
        self.close_browser(is_error=False)
