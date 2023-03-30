import os
import re
import time
from random import random

import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from log import logger

output_dir = 'output'
start_date = '20220214'
today = '20230330'


class Crawl:
    def __init__(self, open_browser=True):
        chrome_options = Options()
        if not open_browser:
            # 增加无头（不打开浏览器）
            chrome_options.add_argument('--headless')
            chrome_options.add_argument('--disable-gpu')

        # 防止被网站识别（伪装）
        chrome_options.add_experimental_option('excludeSwitches', ['enable-automation'])

        # 打开网页不加载图片
        prefs = {
            'profile.default_content_setting_values': {
                'images': 2
            }
        }
        chrome_options.add_experimental_option('prefs', prefs)
        self.browser = webdriver.Chrome(options=chrome_options)
        self.browser.implicitly_wait(5)
        logger.info("初始化成功！")

        # 如果输出文件夹不存在，则创建
        if not os.path.exists(output_dir):
            logger.info(f'{output_dir}文件夹不存在，自动创建{output_dir}文件夹')
            os.mkdir(output_dir)
        else:
            logger.info(f'{output_dir}文件夹已存在')

    @staticmethod
    def _rand_wait(min_wait=0.5, max_wait=2):
        """
        随机等待
        :param min_wait: 最小等待时间
        :param max_wait: 最大等待时间
        """
        time.sleep(min_wait + (max_wait - min_wait) * random())

    def get_url(self, url):
        self._rand_wait()
        self.browser.get(url)

    def _get_code(self):
        return self.browser.page_source

    def get_contents(self):
        return re.findall("<content>(.*?)</content>", self._get_code(), re.S)

    def quit(self):
        self._rand_wait()  # 等待
        self.browser.close()  # 关闭当前网页
        self.browser.quit()  # 完全退出浏览器
        logger.info('浏览器已关闭！')


def crawl():
    page_size = 100
    page_num = 1

    date_list = pd.date_range(start=start_date, end=today).strftime("%Y-%m-%d").tolist()
    date_list.reverse()
    logger.debug(date_list)

    crawl = Crawl(False)
    for date in date_list:
        try:
            url = f'https://api-treehole.xmwishtone.com/dev-api/wx/home/tabView_v1.0?pageNum={page_num}&pageSize={page_size}&tabType=%E4%BB%8A%E6%97%A5%E4%B8%8A%E5%B1%8F&applyUp=2&status=1&createTime={date}'
            crawl.get_url(url)
            contents = crawl.get_contents()

            # 打开data.txt文件，如果文件不存在则创建
            if len(contents) > 0:
                with open(f'{output_dir}/{date}.txt', 'w', encoding='utf-8') as f:
                    # 逐行写入数据
                    for content in contents:
                        logger.debug(content)
                        f.write(content + '\n\n')
                logger.info(f'已爬取{date}的数据，共{len(contents)}条')
            else:
                logger.warning(f'{date}没有数据，跳过')
        except Exception as e:
            logger.error(f'{date}爬取失败！')

    crawl.quit()


if __name__ == '__main__':
    crawl()
