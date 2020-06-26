# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class YelpdetailsItem(scrapy.Item):
    Name = scrapy.Field()
    website_name = scrapy.Field()
    website_link = scrapy.Field()
    phone = scrapy.Field()
    Direction = scrapy.Field()
    category = scrapy.Field()
    find = scrapy.Field()
    near = scrapy.Field()
    email1 = scrapy.Field()
    email2 = scrapy.Field()
    email3 = scrapy.Field()
    email4 = scrapy.Field()
    email5 = scrapy.Field()




