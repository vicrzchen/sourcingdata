import urllib3
import logging
from logging import error
from sourcingdata.scrapy_db.dbkits import DBKits, ProxyInfoDBOperation, ProxyInfo
from datetime import datetime
from random import randint

def get_random_http_proxy():
    database_connection = DBKits()
    database_operation = ProxyInfoDBOperation(db_engine=database_connection)
    get_all_available_proxy = {ProxyInfo.status == 0 and ProxyInfo.proxy_type == 'http'}
    record_sets = database_operation.query_record(query_conditions=get_all_available_proxy).\
        order_by(ProxyInfo.added_time.desc(),
                 ProxyInfo.last_used_time.asc())
    if record_sets.count() > 0:
        return_proxy_info:ProxyInfo = record_sets.first()
        mark_used_proxy(return_proxy_info.proxy_id)
        return return_proxy_info
    return None


def mark_used_proxy(proxy_id=None):
    database_connection = DBKits()
    database_operation = ProxyInfoDBOperation(db_engine=database_connection)
    query_conditions = {ProxyInfo.proxy_id == proxy_id}
    proxy_data_for_update = ProxyInfo()
    proxy_data_for_update.last_used_time = datetime.now()
    database_operation.update_record(query_conditions=query_conditions,
                                     update_data=proxy_data_for_update)
    pass


def mark_unavailable_proxy(proxy_id=None):
    database_connection = DBKits()
    database_operation = ProxyInfoDBOperation(db_engine=database_connection)
    query_conditions = {ProxyInfo.proxy_id == proxy_id}
    proxy_data_for_update = ProxyInfo()
    proxy_data_for_update.status = 1
    database_operation.update_record(query_conditions=query_conditions,
                                     update_data=proxy_data_for_update)
    pass


def reget_proxy():
    http = urllib3.PoolManager()
    try:
        r = http.request('GET', 'http://d.jghttp.golangapi.com/getip?num=1&type=3&pro=&city=0&yys=0&port=1&pack=3283&ts=0&ys=0&cs=0&lb=1&sb=0&pb=4&mr=1&regions=')
        if r.status == 200:
            database_connection = DBKits()
            database_operation = ProxyInfoDBOperation(db_engine=database_connection)
            for file_content in r.data.decode('utf-8').splitlines():
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
        else:
            return None
    except Exception as excepinfo:
        error(excepinfo)
        return -1
    return None


def get_random_user_agent():
    user_agents=['Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.71 Safari/537.1 LBBROWSER',
                 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36 OPR/26.0.1656.60',
                 'Opera/8.0 (Windows NT 5.1; U; en)',
                 'Mozilla/5.0 (Windows NT 5.1; U; en; rv:1.8.1) Gecko/20061208 Firefox/2.0.0 Opera 9.50',
                 'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; en) Opera 9.50',
                 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:34.0) Gecko/20100101 Firefox/34.0',
                 'Mozilla/5.0 (X11; U; Linux x86_64; zh-CN; rv:1.9.2.10) Gecko/20100922 Ubuntu/10.10 (maverick) Firefox/3.6.10',
                 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/534.57.2 (KHTML, like Gecko) Version/5.1.7 Safari/534.57.2',
                 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.71 Safari/537.36',
                 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
                 'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/534.16 (KHTML, like Gecko) Chrome/10.0.648.133 Safari/534.16',
                 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/30.0.1599.101 Safari/537.36',
                 'Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko',
                 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.11 TaoBrowser/2.0 Safari/536.11',
                 'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E; LBBROWSER)',
                 'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; QQDownload 732; .NET4.0C; .NET4.0E; LBBROWSER)',
                 'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E; QQBrowser/7.0.3698.400)',
                 'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; QQDownload 732; .NET4.0C; .NET4.0E)',
                 'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.84 Safari/535.11 SE 2.X MetaSr 1.0',
                 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0; SV1; QQDownload 732; .NET4.0C; .NET4.0E; SE 2.X MetaSr 1.0)',
                 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Maxthon/4.4.3.4000 Chrome/30.0.1599.101 Safari/537.36',
                 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.122 UBrowser/4.0.3214.0 Safari/537.36'
                 ]
    return user_agents[randint(0, len(user_agents))]


def remove_all_proxy():
    pass