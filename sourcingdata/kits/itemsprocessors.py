from sourcingdata.scrapy_db.dbkits import DBKits, \
    ListItemsMapDBOperation
from sourcingdata.scrapy_db.models import ListItemsMap
from scrapy.selector import Selector
from urllib.parse import urljoin, urlsplit

class ListItemsProcessor:
    # read website item mapping data
    def read_item_parameter(self, db_connection=None, websiteID=-1):
        if db_connection is None:
            return None
        if websiteID == -1:
            return None
        list_items_map_DB_operation = ListItemsMapDBOperation(db_engine=db_connection)
        query_conditions = {ListItemsMap.website_id == websiteID}
        items_list = list_items_map_DB_operation.query_record(query_conditions=query_conditions)
        for item in items_list:
            self.item_qty += 1
            item_detail = ListItemsMap()
            item_detail.website_id = item.website_id
            item_detail.is_abstract_url = item.is_abstract_url
            item_detail.is_url = item.is_url
            item_detail.trim_space = item.trim_space
            item_detail.trim_enter = item.trim_enter
            item_detail.xpath_string = item.xpath_string
            item_detail.struct_member_name = item.struct_member_name
            item_detail.list_index = item.list_index
            item_detail.result_is_list = item.result_is_list
            self.items_detail.append(item_detail)
            pass
        pass

    # read data from match xpath
    def get_data(self, match_xpath: Selector=None, result_data=None):
        if match_xpath is not None and result_data is not None:
            for item_detail in self.items_detail:
                match_xpath_item = match_xpath.xpath(item_detail.xpath_string)
                if item_detail.result_is_list:
                    match_xpath_item = match_xpath_item[item_detail.list_index]
                match_xpath_item = match_xpath_item.extract()
                if item_detail.trim_enter:
                    match_xpath_item = match_xpath_item.replace('\n', '')
                if item_detail.trim_space:
                    match_xpath_item = match_xpath_item.replace(' ', '')
                if item_detail.is_url:
                    if not item_detail.is_abstract_url:
                        base_url = match_xpath.root.base
                        url_info = urlsplit(base_url)
                        match_xpath_item = urljoin(url_info.scheme + '://' + url_info.netloc, match_xpath_item)
                setattr(result_data, item_detail.struct_member_name, match_xpath_item)
                pass
            return result_data
        pass

    def __init__(self):
        self.item_qty = 0
        self.items_detail = []
    pass
