#!usr/bin/env python
#-*- coding:utf-8 _*-
"""
@author:andy
@time: 2019/11/26
"""

import re

from bs4 import BeautifulSoup
import requests
from pandas import DataFrame
from requests import RequestException

# requests爬取信息,BeautifulSoup解析html结构,pandas写入文件

# 获取第一个网页的内容,提供解析
def get_first_page(url):
    try:
        # 获取网页,赋值给response,设置编码格式
        response = requests.get(url)
        response.encoding = 'utf-8'
        # 请求成功的话返回网页文本
        if response.status_code == 200:
            return response.text
        return None
    except RequestException:
        return None

# 从第一个网页解析出urls,返回一个url的list
def get_urls(html):
    # 解析html
    soup = BeautifulSoup(html, 'html.parser')
    urls = []
    for data in soup.find_all(name='div',attrs={'class':'hero-list-hero Unused-Hero'}):
        #names.append(data.get('id'))
        # 获取urls
        url = data.get('onclick')
        # 正则表达式
        url_pattern = re.compile("DoNav\('(.*?)'\)",re.S)

        items = re.findall(url_pattern, str(url))[0]
        urls.append(items)

    print(urls)
    return urls

# 解析出每个英雄具体的info,返回含有属性的list
def parse_html_detailed(html):
    soup = BeautifulSoup(html_detailed, 'html.parser')
    table = soup.find(name='table')
    yx_name = table.find_all(name='span')[0].text.replace('\n','').replace(' ','')
    all_num = table.find_all(name='span')[2].text.replace(' ','').replace('使用次数:','')
    win_num = table.find_all(name='span')[3].text.replace(' ','').replace('胜率:','').replace('%','')
    print(yx_name)
    print(all_num)
    print(win_num)

    # 获得全部的tr
    wq_list = []
    wq_table_tr = soup.find(name='table',attrs={'class':'table table-hover table-striped table-list'}).find(name='tbody').find_all(name='tr')
    # 遍历tr获取td
    for td in wq_table_tr:
        # 解析td
        wq_name = td.find_all(name='td')[0].text.replace('\n', '').replace(' ', '')
        wq_use_num = td.find_all(name='td')[1].text.replace(',', '')
        wq_win_num = td.find_all(name='td')[2].text
        #print(wq_name + '/' + wq_use_num + '/' + wq_win_num)
        wq_list.append(wq_name)
        wq_list.append(wq_use_num)
        wq_list.append(wq_win_num)
        None

    print(wq_list)

    data = [yx_name,all_num,win_num,wq_list]
    print('============================')
    return data

# 将list结果输出到csv文件
def to_CSV(data):
    df = DataFrame([data])
    # header=['名字','使用次数','胜率','道具']
    df.to_csv(r'dota2_data.csv',mode='a',index=None,header=False,encoding='gbk')

if __name__ == '__main__':
    url = r'http://www.dotamax.com/hero/' #dota2
    html = get_first_page(url)
    urls = get_urls(html)
    # 遍历url,解析网页输出到文件
    for url in urls:
        url_detailed = r'http://www.dotamax.com' + url
        html_detailed = get_first_page(url_detailed)
        data=parse_html_detailed(html_detailed)
        to_CSV(data)

