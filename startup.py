from scrapy import cmdline

cmdline.execute('scrapy crawl gdgovdata'.split())
# cmdline.execute('scrapy crawl gdgovdata_detail'.split())

from makedata import make_website_info, update_website_info, read_proxy_info, make_website_info_contract, test_db, make_website_items
from sourcingdata.middleware.proxy_middleware import mark_used_proxy, mark_unavailable_proxy, get_random_http_proxy, \
    reget_proxy
from sourcingdata.scrapy_db.dbkits import DBKits
from sourcingdata.kits.itemsprocessors import ListItemsProcessor
# make_website_info()
# update_website_info()
# read_proxy_info()
# reget_proxy()
# make_website_info_contract()
# print(get_random_http_proxy())
# test_db()
# make_website_items()
# databaseConnection = DBKits()
#
# a = ListItemsProcessor()
# a.read_item_parameter(db_connection=databaseConnection, websiteID=4)
#
