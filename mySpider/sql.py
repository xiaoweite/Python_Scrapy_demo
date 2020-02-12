from datetime import datetime

import time
import pymysql
import pytz

from . import settings

db = pymysql.connect(settings.MYSQL_HOST, settings.MYSQL_USER, settings.MYSQL_PASSWORD, settings.MYSQL_DB,
                     settings.MYSQL_PORT, charset=settings.MYSQL_CHARSET)
cursor = db.cursor()

class TeacherSql(object):
    @classmethod
    def insert_teccher_item(cls, item):
        sql = "INSERT INTO `teacher`" \
              "(`name`, `title`, `info`)" \
              "VALUES ('%s', %s, %s)" % \
              (item['name'], db.escape(item['title']), db.escape(item['info']))
        try:
            cursor.execute(sql)
            db.commit()
            print('add_teacher--[name]:', item['name'])
        except pymysql.MySQLError as e:
            # with open('./log/sql.log', 'r+') as i:
            #     i.write('profile sql error![error]:' + str(e))
            print(e)
            cursor.rollback()
        pass

class ReviewSql(object):

    @classmethod
    def insert_profile_item(cls, item):
        sql = "INSERT INTO `py_review_profile`" \
              "(`asin`, `product`, `brand`, `seller`, `image`," \
              "`review_total`, `review_rate`, `pct_five`, `pct_four`, `pct_three`, " \
              "`pct_two`, `pct_one`, `latest_total`, `create_time`, `update_time`) " \
              "VALUES ('%s', %s, %s, %s, '%s', '%s', " \
              "'%s', '%s', '%s', '%s', '%s', '%s', 0, '%s', '%s')" %\
              (item['asin'], db.escape(item['product']), db.escape(item['brand']), db.escape(item['seller']), item['image'],
               item['review_total'], item['review_rate'], item['pct_five'], item['pct_four'],
               item['pct_three'], item['pct_two'], item['pct_one'], item['create_time'], item['update_time'])
        try:
            if cls.check_exist_profile(item['asin']):
                cls.update_profile_item(item)
                print('update review profile--[asin]:', item['asin'])
            else:
                cursor.execute(sql)
                db.commit()
                print('save review profile--[asin]:', item['asin'])
        except pymysql.MySQLError as e:
            with open('./log/sql.log', 'r+') as i:
                i.write('profile sql error![error]:' + str(e))
            print(e)
            cursor.rollback()
        pass

    @classmethod
    def update_profile_item(cls, item):
        now_time = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
        sql = "UPDATE `py_review_profile` SET `latest_total`=`review_total`,`product`=%s, `brand`=%s, `seller`=%s, `image`=%s, `review_total`='%s', `review_rate`='%s'," \
              "`pct_five`='%s', `pct_four`='%s', `pct_three`='%s', `pct_two`='%s', `pct_one`='%s', `update_time`='%s' " \
              "WHERE `asin`='%s'" % \
              (db.escape(item['product']), db.escape(item['brand']), db.escape(item['seller']), db.escape(item['image']),
               item['review_total'], item['review_rate'],item['pct_five'], item['pct_four'], item['pct_three'], item['pct_two'], item['pct_one'],
               now_time, item['asin'])
        try:
            cursor.execute(sql)
            db.commit()
        except pymysql.MySQLError as e:
            print(e)
            cursor.rollback()

    @classmethod
    def check_exist_profile(cls, asin):
        sql = "SELECT * FROM `py_review_profile` WHERE (`asin` = '%s')" % (asin)
        result = cursor.execute(sql)
        if result:
            return True
        else:
            return False

    @classmethod
    def insert_detail_item(cls, item):
        sql = "INSERT INTO `py_review_detail`(`asin`, `review_id`, `reviewer`, `review_url`, `star`, `date`, `title`, `content`) " \
              "VALUES ('%s', '%s', %s, '%s', '%s', '%s', %s, %s)" % \
              (item['asin'], item['review_id'], db.escape(item['reviewer']), item['review_url'], item['star'],
               item['date'], db.escape(item['title']), db.escape(item['content']))
        try:
            if cls.check_exist_detail(item['asin'], item['review_id']) is not True:
                print('save review detail--[asin]:', item['asin'], '[reviewID]:', item['review_id'])
                cursor.execute(sql)
                db.commit()
        except pymysql.MySQLError as e:
            print(e)
            cursor.rollback()
        pass

    @classmethod
    def check_exist_detail(cls, asin, review_id):
        sql = "SELECT * FROM `py_review_detail` WHERE `asin` = '%s' AND `review_id`='%s'" % (asin, review_id)
        result = cursor.execute(sql)
        if result:
            return True
        else:
            return False

    @classmethod
    def get_last_review_total(cls, asin):
        sql = "SELECT `review_total`, `latest_total` FROM `py_review_profile` WHERE `asin`='%s'" % asin
        cursor.execute(sql)
        item = cursor.fetchone()
        if item:
            return item['latest_total']
        else:
            return False

    @classmethod
    def update_profile_self(cls, asin):
        sql = "UPDATE `py_review_profile` SET `latest_total` = `review_total` WHERE `asin`='%s'" % asin
        cursor.execute(sql)
        db.commit()


class RankingSql(object):
    expire_rank = 500
    py_keyword_table = 'py_salesranking_keywords'  # 爬虫抓
    py_sales_table = 'py_salesrankings'
    keyword_table = 'salesranking_keywords'
    sales_table = 'salesrankings'
    tz = pytz.timezone(settings.TIMEZONE)

    @classmethod
    def insert_sales_ranking(cls, item):
        now = datetime.now(cls.tz).strftime('%Y-%m-%d %H:%M:%S')
        sql = "INSERT INTO `%s`(`asin`, `rank`, `classify`, `date`) VALUES ('%s', '%s', %s, '%s')" % \
              (cls.py_sales_table, item['asin'], item['rank'], db.escape(item['classify']), now)
        update_sql = "UPDATE `%s` SET `last_rank`=`rank`, `status`=1, `classify`=%s, `rank`='%s', `updated_at`='%s' WHERE `asin` = '%s'"  % \
                     (cls.sales_table, db.escape(item['classify']), item['rank'], now, item['asin'])
        try:
            cursor.execute(sql)
            cursor.execute(update_sql)
            db.commit()
            print('save sales_rank:', item)
        except pymysql.DatabaseError as error:
            print(error)
            cursor.rollback()

    @classmethod
    def insert_keyword_ranking(cls, item):
        sql = "INSERT INTO `%s`(`skwd_id`, `rank`, `date`) VALUES ('%s', '%s', '%s')" % \
              (cls.py_keyword_table, item['skwd_id'], item['rank'], item['date'])
        update_sql = "UPDATE `%s` SET `last_rank`=`rank`, `rank`='%s', `status`=1, `updated_at`='%s' WHERE `id`='%s'" % \
                     (cls.keyword_table, item['rank'], item['date'], item['skwd_id'])
        try:
            cursor.execute(sql)
            cursor.execute(update_sql)
            db.commit()
            print('save keyword_rank:', item)
        except pymysql.DatabaseError as error:
            print(error)
            cursor.rollback()

    @classmethod
    def fetch_sales_ranking(cls):
        sql = "SELECT `id`, `asin` FROM `%s`WHERE `status` =1 AND `deleted_at` is NULL" % cls.sales_table
        cursor.execute(sql)
        item = cursor.fetchall()
        return item

    @classmethod
    def fetch_keywords_ranking(cls):
        sql = "SELECT `a`.`id`, `a`.`keyword`, `a`.`rank` as `rank`, `b`.`asin` as `asin` FROM `%s` as `a` " \
              "LEFT JOIN `%s` as `b` ON `b`.`id`=`a`.`sk_id` WHERE `b`.`deleted_at` is NULL AND `a`.`deleted_at` is NULL " % \
              (cls.keyword_table, cls.sales_table)
        cursor.execute(sql)
        item = cursor.fetchall()
        return item

    @classmethod
    def update_keywords_expire_rank(cls, skwd_id):
        now = datetime.now(cls.tz).strftime('%Y-%m-%d %H:%M:%S')
        sql = "UPDATE `%s` SET `last_rank`=`rank`, `rank`='%s', `updated_at`='%s', `status`=1 WHERE `id`='%s'" % (cls.keyword_table, cls.expire_rank, now, skwd_id)
        py_sql = "INSERT INTO `%s`(`skwd_id`, `rank`, `date`) VALUES ('%s', '%s', '%s')" % (cls.py_keyword_table, skwd_id, cls.expire_rank, now)
        try:
            cursor.execute(sql)
            cursor.execute(py_sql)
            db.commit()
            print('update keyword_rank: [', skwd_id, '] expired')
        except pymysql.DataError as error:
            print(error)
            cursor.rollback()

    @classmethod
    def update_keywords_none_rank(cls, skwd_id):
        now = datetime.now(cls.tz).strftime('%Y-%m-%d %H:%M:%S')
        sql = "UPDATE `%s` SET `updated_at`='%s', `status`=2 WHERE `id`='%s'" % (cls.keyword_table, now, skwd_id)
        try:
            cursor.execute(sql)
            print('update keyword_rank: [', skwd_id, '] none')
        except pymysql.DataError as error:
            print(error)
            cursor.rollback()





