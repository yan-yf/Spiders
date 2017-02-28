# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class DoubanbookItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    bookname = scrapy.Field()         #书名
    author = scrapy.Field()           #作者
    publisher = scrapy.Field()        #出版社
    translator = scrapy.Field()       #译者
    publishyear = scrapy.Field()      #出版年
    price = scrapy.Field()            #定价
    stars = scrapy.Field()            #豆瓣评分
    quote = scrapy.Field()
    num = scrapy.Field()