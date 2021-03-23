# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class TianyaItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    post_url = scrapy.Field()
    post_title = scrapy.Field()  # 标题
    post_time = scrapy.Field()  # 发表时间
    reply_num = scrapy.Field()  # 楼数
    content = scrapy.Field()  # 内容
    author = scrapy.Field()  # 楼主
    author_id = scrapy.Field()


