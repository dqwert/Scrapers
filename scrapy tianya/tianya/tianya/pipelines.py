# -*- coding: utf-8 -*-
# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

# title = scrapy.Field()  # 标题
# author = scrapy.Field()  # 楼主
# post_time = scrapy.Field()  # 发表时间
# floor = scrapy.Field()  # 楼数
# content = scrapy.Field()  # 内容


# 爬取到的数据写入到SQLite数据库
import sqlite3


class SQLitePipeline(object):

    # 打开数据库
    def open_spider(self, spider):
        self.f = open('tianya.txt', 'w')

        db_name = spider.settings.get('SQLITE_DB_NAME', 'scrapy.db')

        self.db_conn = sqlite3.connect(db_name)
        self.db_cur = self.db_conn.cursor()
        sql_drop = 'DROP TABLE if EXISTS postData'
        sql_create = 'Create TABLE postData ' \
                     '(post_url TEXT, post_title TEXT, post_time TEXT, reply_num TEXT, content TEXT, author TEXT, author_id TEXT)'
        self.db_cur.execute(sql_drop)
        self.db_cur.execute(sql_create)

    # 关闭数据库
    def close_spider(self, spider):
        self.db_conn.commit()
        self.db_conn.close()
        self.f.close()

    # 对数据进行处理
    def process_item(self, item, spider):
        self.insert_db(item)
        self.f.write(item['content'])
        self.f.write("\n")
        return item

    # 插入数据
    def insert_db(self, item):
        values = (
            item['post_url'],
            item['post_title'],
            item['post_time'],
            item['reply_num'],
            item['content'],
            item['author'],
            item['author_id'],
        )

        sql = 'INSERT INTO postData VALUES(?,?,?,?,?,?,?)'
        self.db_cur.execute(sql, values)
