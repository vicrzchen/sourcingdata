from sqlalchemy import create_engine
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sourcingdata.scrapy_db.constvalue import DB_NAME, \
    DB_PASSWORD, \
    DB_USER, \
    SERVER_ADDRESS, \
    SERVER_PORT, \
    MAX_DB_OPERATION_CATCH
from sourcingdata.scrapy_db.models import RequirementToRead, \
    SourcingAnnouncementToRead, \
    WebsiteInfo, \
    ProxyInfo, \
    ContractInfoToRead, \
    ListItemsMap

import logging


class DBKits:
    engine = None
    __sessions = []

    def __init__(self):
        try:
            self.engine = create_engine(
                'mysql+pymysql://' + DB_USER + ':' +
                DB_PASSWORD + '@' +
                SERVER_ADDRESS + ':' +
                SERVER_PORT + '/' + DB_NAME)
            self.Base = automap_base()
            self.Base.prepare(self.engine, reflect=True)
        except Exception as exce_info:
            logging.error(exce_info)
            self.engine = None

    def __del__(self):
        pass


class DBOperationBase:

    # table_type_name = table name in DB
    # data_struct_name = data struct var for data storage
    def __init__(self, db_engine: DBKits=None, table_type_name: str= None, data_struct_name: str=None):
        if not(DBKits is None):
            setattr(self, data_struct_name, getattr(db_engine.Base.classes, table_type_name))
            self.__data_struct_name = data_struct_name
            self._db_session = Session(db_engine.engine)
            self._db_engine = db_engine
            self._row_data = None
            self._operateion_times = 0
            pass
        pass

    def _commit_to_db(self):
        if self._operateion_times >= MAX_DB_OPERATION_CATCH:
            self._db_session.commit()
            self._operateion_times = 0
        else:
            self._operateion_times += 1
        pass

    def insert_record(self, record_data=None, skip_duplicated_record=False):

        is_duplicated_record = False
        if skip_duplicated_record:
            # TODO: 需要判重
            is_duplicated_record = False
            pass
        if not(record_data is None) and not is_duplicated_record:
            try:
                new_row_data = self.map_record_to_row_data(record_data)
                self._db_session.add(new_row_data)
                # self._db_session.commit()
                self._commit_to_db()
            except Exception as exce_info:
                logging.error(exce_info)
        pass

    def update_record(self, query_conditions=None, update_data=None):
        if not(query_conditions is None or update_data is None):
            record_set = self.get_all_records(record_type=self.record_type)
            for i in query_conditions:
                record_set = record_set.filter(i)
            if record_set.count() > 0:
                try:
                    record_dict = self.map_record_to_dict(update_data)
                    # 去掉无用变量_sa_instance_state
                    record_dict.pop('_sa_instance_state', None)
                    record_set.update(record_dict)
                    # self._db_session.commit()
                    self._commit_to_db()
                except Exception as exce_info:
                    logging.error(exce_info)
                pass
            pass
        pass

    #map a record data into dict
    def map_record_to_dict(self, record_data=None):
        record_dict = dict()
        for key, value in vars(record_data).items():
                if value is not None:
                    record_dict[key] = value
        return record_dict

    # map a record data into _row_data member
    def map_record_to_row_data(self, record_data=None):
        row_data = eval('self.' + self.__data_struct_name)()
        for key, value in vars(record_data).items():
            setattr(row_data, key, value)
        return row_data
    pass

    def get_all_records(self, record_type=None):
        all_records = None
        try:
            all_records = self._db_session.query(record_type)
        except Exception as exec_info:
            logging.error(exec_info)
        return all_records

    def query_record(self, query_conditions=None):
        all_record = self.get_all_records(record_type=self.record_type)
        if all_record and query_conditions is not None:
            for i in query_conditions:
                all_record = all_record.filter(i)
        return all_record
        pass

    def __del__(self):
        self._db_session.commit()


class RequirementToReadDBOperation(DBOperationBase):
    def __init__(self, db_engine: DBKits=None):
        super(RequirementToReadDBOperation, self).__init__(db_engine,
                                                           table_type_name='requirement_to_read',
                                                           data_struct_name='_RequirementToReadData')
        self.record_type = RequirementToRead
        pass


class SourcingAnnouncementToReadDBOperation(DBOperationBase):
    def __init__(self, db_engine: DBKits=None):
        super(SourcingAnnouncementToReadDBOperation, self).__init__(db_engine,
                                                                    table_type_name='sourcing_announcement_to_read',
                                                                    data_struct_name='_SourcingAnnouncementToRead')
        self.record_type = SourcingAnnouncementToRead
        pass


class WebsiteInfoDBOperation(DBOperationBase):
    def __init__(self, db_engine: DBKits=None):
        super(WebsiteInfoDBOperation, self).__init__(db_engine,
                                                     table_type_name='website_info',
                                                     data_struct_name='_WebsiteInfo')
        self.record_type = WebsiteInfo
        pass


class ProxyInfoDBOperation(DBOperationBase):
    def __init__(self, db_engine: DBKits=None):
        super(ProxyInfoDBOperation, self).__init__(db_engine,
                                                   table_type_name='proxy_info',
                                                   data_struct_name='_ProxyInfo')
        self.record_type = ProxyInfo
        pass


class ContractInfoToReadDBOperation(DBOperationBase):
    def __init__(self, db_engine: DBKits=None):
        super(ContractInfoToReadDBOperation, self).__init__(db_engine,
                                                            table_type_name='contract_info_to_read',
                                                            data_struct_name='_ContractInfoToRead')
        self.record_type = ContractInfoToRead
        pass


class ListItemsMapDBOperation(DBOperationBase):
    def __init__(self, db_engine: DBKits=None):
        super(ListItemsMapDBOperation, self).__init__(db_engine,
                                                      table_type_name='list_items_maps',
                                                      data_struct_name='_ListItemsMaps')
        self.record_type = ListItemsMap
        pass
