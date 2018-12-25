from sourcingdata.scrapy_db.dbkits import DBKits, \
    WebsiteInfoDBOperation,\
    ProxyInfoDBOperation, \
    ListItemsMapDBOperation
from sourcingdata.scrapy_db.models import WebsiteInfo, ProxyInfo, ListItemsMap
from datetime import datetime
from sourcingdata.scrapy_db.constvalue import \
    START_URL_CONTRACT_INFO_TO_BE_READ, \
    START_URL_SOURCING_PLAN_TO_BE_READ, \
    START_URL_ACCEPT_TO_BE_READ
from sqlalchemy import DateTime

# 设置网页信息
def make_website_info():
    website_data = WebsiteInfo()
    # 设置信息
    website_data.website_name = '广东省采购中心-省直-采购需求'
    website_data.start_up_url = 'http://www.gdgpo.gov.cn/queryMoreInfoList/channelCode/0005.html'
    website_data.website_crawl_scope = 'gdgpo.gov.cn'
    # 设置信息结束
    database_connection = DBKits()
    database_operation = WebsiteInfoDBOperation(db_engine=database_connection)
    database_operation.insert_record(website_data, skip_duplicated_record=True)

def update_website_info():
    website_data_to_update = WebsiteInfo()
    website_data_to_query = WebsiteInfo()
    # 设置信息
    website_data_to_query.start_up_url = 'http://www.gdgpo.gov.cn/queryMoreInfoList/channelCode/0005.html'
    website_data_to_query.website_crawl_scope = 'gdgpo.gov.cn'
    # 设置信息结束
    database_connection = DBKits()
    database_operation = WebsiteInfoDBOperation(db_engine=database_connection)
    website_data_to_update.current_page_number = 800
    query_conditions = {WebsiteInfo.start_up_url == website_data_to_query.start_up_url and
                        WebsiteInfo.website_crawl_scope == website_data_to_query.website_crawl_scope}
    database_operation.update_record(record_type=WebsiteInfo,
                                     update_data=website_data_to_update)


def read_proxy_info():
    database_connection = DBKits()
    database_operation = ProxyInfoDBOperation(db_engine=database_connection)

    for file_content in open('./proxy.txt', 'r').readlines():
        for proxy_string in file_content.split():
            proxy_info = ProxyInfo()
            proxy_info.proxy_ip = proxy_string.split(':')[0]
            proxy_info.proxy_port = proxy_string.split(':')[1]
            proxy_info.proxy_source = '极光免费'
            proxy_info.proxy_type = 'http'
            proxy_info.added_time = datetime.now()
            proxy_info.status = 0
            database_operation.insert_record(proxy_info, skip_duplicated_record=False)
            proxy_info = None


# 设置合同网页信息
def make_website_info_contract():
    website_data = WebsiteInfo()
    # 设置信息
    website_data.website_name = '广东省采购中心-省直-采购合同1'
    website_data.start_up_url = START_URL_CONTRACT_INFO_TO_BE_READ
    website_data.website_crawl_scope = 'gdgpo.gov.cn'
    website_data.current_page_number = 16000
    # 设置信息结束
    database_connection = DBKits()
    database_operation = WebsiteInfoDBOperation(db_engine=database_connection)
    database_operation.insert_record(website_data, skip_duplicated_record=True)


def test_db():
    conditions = {ProxyInfo.status == 1}
    database_connection = DBKits()
    proxy_operation = ProxyInfoDBOperation(db_engine=database_connection)
    print(proxy_operation.query_record(conditions).count())
    pass


# make contract to read items mapping data
def make_website_items_mapping(website_id=-1):
    filename_test = './list_items_map4sourcing_plan.txt'
    database_connection = DBKits()
    database_operation = WebsiteInfoDBOperation(db_engine=database_connection)
    line_count = 0
    for file_content in open(filename_test, 'r').readlines():
        if line_count > 0:
            list_item = ListItemsMap()
            if website_id == -1:
                list_item.website_id = int(file_content.split(',')[0])
            else:
                list_item.website_id = website_id
            if file_content.split(',')[1] == 'True':
                list_item.result_is_list = True
            else:
                list_item.result_is_list = False
            list_item.list_index = int(file_content.split(',')[2])
            list_item.struct_member_name = file_content.split(',')[3]
            list_item.xpath_string = file_content.split(',')[4]
            if file_content.split(',')[5] == 'True':
                list_item.trim_enter = True
            else:
                list_item.trim_enter = False
            if file_content.split(',')[6] == 'True':
                list_item.trim_space = True
            else:
                list_item.trim_space = False
            if file_content.split(',')[7] == 'True':
                list_item.is_url = True
            else:
                list_item.is_url = False
            if file_content.split(',')[8] == 'True':
                list_item.is_abstract_url = True
            else:
                list_item.is_abstract_url = False
            database_operation.insert_record(record_data=list_item, skip_duplicated_record=False)
            list_item = None
        line_count += 1

def make_website_info_sourcing_plan():
    website_data = WebsiteInfo()
    # 设置信息
    website_data.website_name = '广东省采购中心-省直-采购计划'
    website_data.start_up_url = START_URL_SOURCING_PLAN_TO_BE_READ
    website_data.website_crawl_scope = 'gdgpo.gov.cn'
    website_data.current_page_number = 1
    website_data.website_next_page_str = '//a[@class="aborder2"]/span[contains(.,"下一页")]'
    website_data.website_goto_page_str = '//input[@id="pointPageIndexId"]'
    # 设置信息结束
    database_connection = DBKits()
    database_operation = WebsiteInfoDBOperation(db_engine=database_connection)
    database_operation.insert_record(website_data, skip_duplicated_record=True)


def make_website_info_accept():
    website_data = WebsiteInfo()
    # 设置信息
    website_data.website_name = '广东省采购中心-省直-履约验收'
    website_data.start_up_url = START_URL_ACCEPT_TO_BE_READ
    website_data.website_crawl_scope = 'gdgpo.gov.cn'
    website_data.current_page_number = 1
    website_data.website_next_page_str = '//a[@class="aborder2"]/span[contains(.,"下一页")]'
    website_data.website_goto_page_str = '//input[@id="pointPageIndexId"]'
    # 设置信息结束
    database_connection = DBKits()
    database_operation = WebsiteInfoDBOperation(db_engine=database_connection)
    database_operation.insert_record(website_data, skip_duplicated_record=True)
