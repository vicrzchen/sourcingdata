# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy import Field


class SourcingdataItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()

    collection = 'requirement'
    purchaser_name = Field()
    agent_name = Field()
    project_id = Field()
    announce_time = Field()
    belong_to = Field()
    project_name = Field()
    contact_person = Field()
    contact_phone = Field()

    pass
