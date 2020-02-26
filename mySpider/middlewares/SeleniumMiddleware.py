from selenium import webdriver
from selenium.common import exceptions
from .. import settings
from ..helper import Helper
import re
import redis
import time
import json

#chrome_options = Options()
#chrome_options.add_argument('--headless')  # 使用无头谷歌浏览器模式
#chrome_options.add_argument('--disable-gpu')
#chrome_options.add_argument('--no-sandbox')
# 指定谷歌浏览器路径
#webdriver.Chrome(chrome_options=chrome_options,executable_path='/root/zx/spider/driver/chromedriver')

r = Helper.redis()
# 检测是否是机器人
is_robot = r.get(settings.IS_ROBOT)

if is_robot:
    options = webdriver.ChromeOptions()
    proxy_ip = Helper.get_proxy()
    print("selenium使用的代理IP为：%s" % proxy_ip)
    options.add_argument("--accept-language=zh-CN,zh;q=0.9,en;q=0.8")
    options.add_argument("--proxy-server=http://{}".format(proxy_ip))

    driver = webdriver.Chrome(executable_path='C:\Program Files (x86)\Google\Chrome\Application\chromedriver',
                              chrome_options=options)  # 创建Chrome对象.


class SeleniumMiddleware(object):

    @classmethod
    def process_request(cls, request, spider):
        if is_robot:
            driver.get('https://www.amazon.com')
            time.sleep(2)

            # 判断是否需要验证码
            img_src = driver.find_element_by_xpath("//div[@class='a-row a-text-center']/img").get_attribute('src')
            if re.match(r'https://images-na.ssl-images-amazon.com/captcha/*', img_src):
                print("需要验证码")

                # 手动填写验证码
                verify_code = input("请填写验证码：")
                input_box = driver.find_element_by_xpath("//input[@id='captchacharacters']")
                input_box.send_keys(verify_code)
                print("验证码填写完成请等待")

            print('selenium提交表单...')
            one_click = driver.find_element_by_xpath("//button[@class='a-button-text']")
            one_click.click()
            time.sleep(2)

            cookies_list = driver.get_cookies()
            json_cookies = json.dumps(cookies_list)  # 通过json将cookies写入文件

            with open('cookies.json', 'w') as f:
                f.write(json_cookies)
                Helper.redis().delete(settings.IS_ROBOT)

            driver.quit()  # 使用完, 记得关闭浏览器, 不然chromedriver.exe进程为一直在内存中.
        else:
            pass
