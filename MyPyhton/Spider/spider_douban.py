#!usr/bin/env python
#-*- coding:utf-8 _*-
"""
@author:andy
@time: 2019/11/27
"""

import re

import requests
from requests import RequestException

# 早期爬虫,爬取建议将 request 替换成 selenium,解析用 BeautifulSoup 替换 re,写文件用pandas

# 获取第一个网页的内容,提供解析
def get_one_page(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.text
        return None
    except RequestException:
        return None

# 解析参数,re正则表达式
def parse_one_page_imdb(html):
    # <p class="bb">(.*?)</p>,电影名称
    pattern = re.compile('<a href="/title/.*?">.*?"bb">(.*?)</p>.*?<i>(.*?)</i>.*?<p>英文名：(.*?)</p>.*?导演：（ <span>(.*?)</span>.*?年代：<i>(.*?)</i>.*?</a>',re.S)
    # 解析结构返回list
    items = re.findall(pattern,html)
    return items

# 写文件,将list写入excel
def write_to_excel(parse_one_page):
    list = parse_one_page
    with open('imdb250.xls','a',encoding='gbk') as excel:
        excel.write('fileName\score\EnglishName\director\years\n')
        for i in range(len(list)):
            for j in range(len(list[i])):
                excel.write(str(list[i][j]))#write函数不能写int类型的参数，所以使用str()转化
                excel.write('\t')#相当于Tab一下，换一个单元格
            excel.write('\n')#写完一行立马换行
        excel.close()

# 写文件,将list写入txt
def write_to_txt(parse_one_page):
    list = parse_one_page
    with open('imdb250.txt','a',encoding='utf-8') as txt:
        txt.write('fileName,score,EnglishName,director,years\n')
        for row in list:
            rowtxt = '{},{},{},{},{}'.format(row[0],row[1],row[2],row[3],row[4])
            txt.write(rowtxt)
            txt.write('\n')
        txt.close()

# 主方法
def main(num):
    url_imdb = 'http://www.imdb.cn/imdb250/%s' % (num)
    html = get_one_page(url_imdb)
    item = parse_one_page_imdb(html)
    print(item)
    write_to_excel(item)
    #write_to_txt(item)

if __name__ == '__main__':
    num = 1
    while num <= 9:
        main(num)
        num = num + 1

