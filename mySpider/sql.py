from datetime import datetime

import time
import pymysql
import pytz

from . import settings

db = pymysql.connect(settings.MYSQL_HOST, settings.MYSQL_USER, settings.MYSQL_PASSWORD, settings.MYSQL_DB,
                     settings.MYSQL_PORT, charset=settings.MYSQL_CHARSET,cursorclass=pymysql.cursors.DictCursor)
cursor = db.cursor()

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
            cls.fp = open('sql.log', 'w+', encoding='utf-8')
            text = str(e) + "\n"
            cls.fp.write(text)

            # with open('./log/sql.log', 'r+') as i:
            #     i.write('profile sql error![error]:' + str(e))
            print(e)
            cursor.rollback()
            cls.fp.close()
        pass







