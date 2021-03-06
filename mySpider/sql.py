from datetime import datetime

import time
import pymysql
import pytz

from . import settings

db = pymysql.connect(settings.MYSQL_HOST, settings.MYSQL_USER, settings.MYSQL_PASSWORD, settings.MYSQL_DB,
                     settings.MYSQL_PORT, charset=settings.MYSQL_CHARSET,cursorclass=pymysql.cursors.DictCursor)
cursor = db.cursor()

db2 = pymysql.connect(settings.MYSQL_HOST, settings.MYSQL_USER, settings.MYSQL_PASSWORD, settings.ZBLOG_MYSQL_DB,
                     settings.MYSQL_PORT, charset=settings.ZBLOG_MYSQL_CHARSET,cursorclass=pymysql.cursors.DictCursor)
cursor2 = db2.cursor()

class TeacherSql(object):
    @classmethod
    def insert_teccher_item(cls, item):

        sql = "INSERT INTO `teacher`" \
              "(`name`, `title`, `info`,`create_time`)" \
              "VALUES ('%s', %s, %s, %s)" % \
              (item['name'], db.escape(item['title']), db.escape(item['info']),db.escape(item['create_time']))
        try:
            cursor.execute(sql)
            db.commit()
            print('add_teacher--[name]:', item['name'])
        except pymysql.MySQLError as e:
            cls.fp = open('sql.log', 'a+', encoding='utf-8')
            text = str(e) + "\n"
            cls.fp.write(text)

            # with open('./log/sql.log', 'r+') as i:
            #     i.write('profile sql error![error]:' + str(e))
            print(e)
            cursor.rollback()
            cls.fp.close()
        pass

    @classmethod
    def insert_blog_item(cls,item):
        sql = "INSERT INTO `zbp_post`" \
              "(`log_CateID`, `log_AuthorID`, `log_Title`,`log_Intro`,`log_Content`,`log_Meta`,`log_PostTime`)" \
              "VALUES (%s,%s,%s,%s,%s,%s,%s)" % \
              (db2.escape(item['log_CateID']),db2.escape(item['log_AuthorID']), db2.escape(item['log_Title']), db2.escape(item['log_Intro']), db2.escape(item['log_Content']), db2.escape(item['log_Meta']), db2.escape(item['log_PostTime']))
        try:
            print(sql)
            cursor2.execute(sql)
            db2.commit()
            print('add_Title--[name]:', item['log_Title'])
        except pymysql.MySQLError as e:
            cls.fp = open('sql.log', 'a+', encoding='utf-8')
            text = str(e) + "\n"
            cls.fp.write(text)

            # with open('./log/sql.log', 'r+') as i:
            #     i.write('profile sql error![error]:' + str(e))
            print(e)
            db2.rollback()
            cls.fp.close()
        pass
        pass

    @classmethod
    def insert_amazon_product_item(cls,item):
        sql = "INSERT INTO `amazon_product`" \
              "(`product_title`, `product_tags`, `product_price`,`stock_status`,`sales`,`technical_details`,`create_time`)" \
              "VALUES (%s,%s, %s,%s,%s,%s,%s)" % \
              (item['product_title'], db.escape(item['product_tags']), db.escape(item['product_price']), db.escape(item['stock_status']), db.escape(item['sales']), db.escape(item['technical_details']), db.escape(item['create_time']))
        try:
            cursor.execute(sql)
            db.commit()
            print('add_amazon_product--[amazon_product]:', item['product_title'])
        except pymysql.MySQLError as e:
            cls.fp = open('sql.log', 'a+', encoding='utf-8')
            text = str(e) + "\n"
            cls.fp.write(text)

            # with open('./log/sql.log', 'r+') as i:
            #     i.write('profile sql error![error]:' + str(e))
            print(e)
            cursor.rollback()
            cls.fp.close()
        pass









