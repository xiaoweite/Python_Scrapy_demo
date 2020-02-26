import hashlib
import redis
import scrapy
from .. import settings


class CacheMiddleware(object):
    def __init__(self):
        self.r = redis.Redis(host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=settings.REDIS_DB, password=settings.REDIS_PASSWORD)

    def process_request(self, request, spider):
        try:
            md = hashlib.md5()
            md.update(request.url.encode('utf-8'))
            print("缓存的key%s" % md.hexdigest())
            result = self.r.get(md.hexdigest())
            if result:
                res = scrapy.http.TextResponse(url=request.url, status=200, headers=None, body=result, request=None, encoding='utf-8')
                print('从本地缓存中取数据')
                return res
        except Exception as e:
            print('cache middleware:' + str(e))
            pass