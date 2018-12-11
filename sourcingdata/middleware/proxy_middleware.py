import urllib3
import logging
from logging import error
from sourcingdata.scrapy_db.dbkits import DBKits, ProxyInfoDBOperation, ProxyInfo
from datetime import datetime


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
        r = http.request('GET', 'http://d.jghttp.golangapi.com/getip?num=1&type=3&pro=&city=0&yys=0&port=1&pack=2945&ts=0&ys=0&cs=0&lb=1&sb=0&pb=4&mr=1&regions=')
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
                    database_operation.insert_record(proxy_info_data=proxy_info)
                    proxy_info = None
        else:
            return None
    except Exception as excepinfo:
        error(excepinfo)
        return -1
    return None

def remove_all_proxy():
    pass