# coding: utf-8
from sqlalchemy import Column, Date, DateTime, String, text
from sqlalchemy.dialects.mysql import INTEGER, TINYINT
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata


class ContractInfoToRead(Base):
    __tablename__ = 'contract_info_to_read'

    contract_info_id = Column(INTEGER(64), primary_key=True, unique=True)
    purchasor = Column(String(200))
    vendor = Column(String(200))
    project_id = Column(String(200))
    contract_name = Column(String(1000))
    contract_value = Column(String(100))
    contract_sign_date = Column(String(20))
    announce_date = Column(String(20))
    url_to_read = Column(String(1000))


class ProxyInfo(Base):
    __tablename__ = 'proxy_info'

    proxy_id = Column(INTEGER(64), primary_key=True, unique=True)
    proxy_type = Column(String(10), server_default=text("'http'"))
    proxy_ip = Column(String(18))
    proxy_port = Column(String(5))
    proxy_source = Column(String(200))
    added_time = Column(DateTime)
    status = Column(INTEGER(11), server_default=text("'0'"))
    last_used_time = Column(DateTime)


class Requirement(Base):
    __tablename__ = 'requirement'

    requirement_id = Column(INTEGER(64), primary_key=True, unique=True)
    purchaser_name = Column(String(1000))
    agent_name = Column(String(1000))
    project_id = Column(String(1000))
    announce_time = Column(DateTime)
    belong_to = Column(String(1000))
    project_name = Column(String(1000))
    contact_person = Column(String(1000))
    contact_phone = Column(String(1000))


class RequirementToRead(Base):
    __tablename__ = 'requirement_to_read'

    requirement_to_read_id = Column(INTEGER(64), primary_key=True, unique=True)
    list_id = Column(INTEGER(64))
    purchasor = Column(String(200))
    bidding_agent = Column(String(200))
    project_name = Column(String(400))
    items_name = Column(String(400))
    announce_date = Column(String(20))
    portal_name = Column(String(100))
    url_to_read = Column(String(1000))
    read_status = Column(INTEGER(11), server_default=text("'0'"))


class SourcingAnnouncementToRead(Base):
    __tablename__ = 'sourcing_announcement_to_read'

    sourcing_announcement_to_read_id = Column(INTEGER(64), primary_key=True)
    belong_to = Column(String(100))
    project_name = Column(String(1000))
    announce_time = Column(String(100))
    project_url = Column(String(1000))
    read_flag = Column(TINYINT(1), server_default=text("'0'"))


class Vendor(Base):
    __tablename__ = 'vendor'

    vendorID = Column(INTEGER(11), primary_key=True, unique=True)
    name = Column(String(1000), nullable=False)
    address = Column(String(1000))
    phone = Column(String(50))
    description = Column(String(2000))


class WebsiteInfo(Base):
    __tablename__ = 'website_info'

    website_id = Column(INTEGER(64), primary_key=True, unique=True)
    website_name = Column(String(200))
    start_up_url = Column(String(1000))
    current_page_number = Column(INTEGER(11))
    website_struct_type = Column(INTEGER(11), server_default=text("'0'"))
    website_crawl_scope = Column(String(1000))
    website_group_id = Column(INTEGER(64))
