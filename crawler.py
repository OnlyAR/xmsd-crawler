import os
import time
from random import random

import pandas as pd
import requests

from log.logger import logger

start_date = '2022-02-01'
end_date = '2023-03-31'

# 将当前工作目录切换到当前文件所在目录
os.chdir(os.path.dirname(os.path.abspath(__file__)))

out_path = 'output'
filename = 'origin-data.csv'


class Crawler:
    def __init__(self, date_list, page_size=100, page_num=1):
        self.date_list = date_list
        self.page_size = page_size
        self.page_num = page_num
        self.df = pd.DataFrame(columns=['id', '发布日期', '发布时间', '正文', '用户名', '用户id', '年龄', '性别', '点赞数', '评论数', '主题'])

    @staticmethod
    def _rand_pause(min_limit=0.5, max_limit=2):
        # 在指定范围内随机暂停
        t = random() * (max_limit - min_limit) + min_limit
        # 保留两位小数
        logger.debug('暂停{}秒'.format(round(t, 2)))
        time.sleep(t)

    def get_json(self, date):
        self._rand_pause()
        url = f'https://api-treehole.xmwishtone.com/dev-api/wx/home/tabView_v1.0?pageNum={self.page_num}&pageSize={self.page_size}&tabType=%E4%BB%8A%E6%97%A5%E4%B8%8A%E5%B1%8F&applyUp=2&status=1&createTime={date}'
        response = requests.get(url)
        return response.json()

    def parse(self, json_obj):
        ids = []  # 留言id
        dates = []  # 发布日期
        created_times = []  # 发布时间
        messages = []  # 留言内容
        user_names = []  # 用户名
        user_ids = []  # 用户id
        user_ages = []  # 用户年龄
        user_genders = []  # 用户性别
        like_nums = []  # 点赞数
        comments_nums = []  # 评论数
        topics = []  # 主题

        cnt = 0
        for row in json_obj['page']['rows']:
            if row['deleted'] == 0:
                cnt += 1

                ids.append(str(row['id']))
                dates.append(row['createTime'][:10])
                created_times.append(row['createTime'][11:])
                messages.append(row['content'])
                user_names.append(row['nickname'])
                user_ids.append(str(row['createUser']))
                user_ages.append(str(row['userInfo']['age']) if row['userInfo']['age'] is not None else None)
                user_genders.append('男' if row['userInfo']['gender'] == 0 else '女')
                like_nums.append(int(row['likeNum']))
                comments_nums.append(int(row['commentNum']))

                if row['topic'] is None:
                    topics.append(None)
                else:
                    topics.append(row['topic']['content'])

        self.df = pd.concat(
            [self.df,
             pd.DataFrame({
                 'id': ids,
                 '发布日期': dates,
                 '发布时间': created_times,
                 '正文': messages,
                 '用户名': user_names,
                 '用户id': user_ids,
                 '年龄': user_ages,
                 '性别': user_genders,
                 '点赞数': like_nums,
                 '评论数': comments_nums,
                 '主题': topics,
             })], ignore_index=True
        )
        return cnt

    def run(self):
        for date in self.date_list:
            try:
                logger.info(f'正在爬取{date}的数据...')
                json_obj = self.get_json(date)
                cnt = self.parse(json_obj)
                logger.info(f'爬取{date}的数据成功，共{cnt}条')
            except Exception as e:
                logger.error(f'爬取{date}的数据失败')
                logger.error(e)

        # 以'|'分隔，保存到csv文件
        self.df.to_csv(os.path.join(out_path, filename), index=False, encoding='utf-8-sig', sep='|')


if __name__ == '__main__':
    # 生成日期列表
    date_list = pd.date_range(start=start_date, end=end_date).strftime("%Y-%m-%d").tolist()
    logger.debug(date_list)
    # 逆序
    date_list.reverse()
    crawler = Crawler(date_list)
    crawler.run()
