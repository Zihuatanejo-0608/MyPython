#!usr/bin/env python
#-*- coding:utf-8 _*-
"""
@author:andy
@time: 2019/11/27
"""

import re

import requests
from requests import RequestException

# 获取第一个网页的内容,提供解析
def get_one_page(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.text
        return None
    except RequestException:
        return None

# 解析参数,re正则表达式,结果返回list
def parse_one_page_db(html):
    #pattern = re.compile('<tr>.*?<a.*?>(.*?)</a>.*?<a.*?>(.*?)</a>.*?<td class="bg_b">(.*?)</td>.*?</tr>',re.S)#罚球
    pattern = re.compile('<tr>.*?<a.*?>(.*?)</a>.*?<a.*?>(.*?)</a>.*?<td class="bg_b">(.*?)</td>\n<td>(.*?)</td>\n<td>(.*?)</td>.*?</tr>', re.S)#三分
    items = re.findall(pattern,html)
    return items

# 写文件,将list写入excel
def write_to_excel(parse_one_page):
    list = parse_one_page
    with open('nbaData3.xls','a',encoding='gbk') as excel:
        excel.write('name\eam\eaccuracy\n')
        for i in range(len(list)):
            for j in range(len(list[i])):
                excel.write(str(list[i][j]))#write函数不能写int类型的参数，所以使用str()转化
                excel.write('\t')#相当于Tab一下，换一个单元格
            excel.write('\n')#写完一行立马换行
        excel.close()

# 主方法
def main(num):
    # url_hp = 'https://nba.hupu.com/stats/players/ftp/%s' % (num)#罚球
    url_threePoint = 'https://nba.hupu.com/stats/players/tpp/%s' % (num)#三分
    html = get_one_page(url_threePoint)
    item = parse_one_page_db(html)
    print(item)
    write_to_excel(item)

if __name__ == '__main__':
    num = 1
    while num <= 2:
        main(num)
        num = num + 1

