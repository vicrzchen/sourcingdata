from sourcingdata.scrapy_db.dbkits import DBKits, WebsiteInfoDBOperation, ProxyInfo, ProxyInfoDBOperation
from sourcingdata.scrapy_db.models import WebsiteInfo
from datetime import datetime
from sourcingdata.scrapy_db.constvalue import START_URL_CONTRACT_INFO_TO_BE_READ
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
    database_operation.insert_record(website_info_data=website_data)

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
                                     update_data=website_data_to_update,
                                     query_conditions=query_conditions)


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
            database_operation.insert_record(proxy_info_data=proxy_info)
            proxy_info = None


# 设置合同网页信息
def make_website_info_contract():
    website_data = WebsiteInfo()
    # 设置信息
    website_data.website_name = '广东省采购中心-省直-采购合同'
    website_data.start_up_url = START_URL_CONTRACT_INFO_TO_BE_READ
    website_data.website_crawl_scope = 'gdgpo.gov.cn'
    website_data.current_page_number = 6000
    # 设置信息结束
    database_connection = DBKits()
    database_operation = WebsiteInfoDBOperation(db_engine=database_connection)
    database_operation.insert_record(website_info_data=website_data)