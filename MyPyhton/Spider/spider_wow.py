#!usr/bin/env python
#-*- coding:utf-8 _*-
"""
@author:andy
@time: 2019/11/27
"""
import re
from bs4 import BeautifulSoup
import requests
from pandas import DataFrame
from requests import RequestException


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

def get_urls(html):
    urls = []
    # 解析html
    soup = BeautifulSoup(html, 'html.parser')
    # 编辑div标签,缩小范围,不套两层循环会查询出2次数据
    for div in soup.find_all(name='div',attrs={'class':'iconname'}):
        # 遍历div中的a标签,class_='item_info'的数据（全部）,recursive=循环
        for url in div.find_all(name='a',attrs={'class':'item_info'},recursive=True):
            # urls数组添加href元素
            urls.append(url.get('href'))
    print(urls)
    return urls

def parse_html_detailed(html_detailed):
    soup = BeautifulSoup(html_detailed, 'html.parser')
    # 定位到表单,武器本身就是个表单
    table = soup.find(name='div',attrs={'class':'item_board item'})
    # 遍历获取物品id
    for id in table.find(name='span'):
        print(id.string)
    #武器名称是td标签的第一项
    name = table.find_all(name='td')[0]
    english_name = table.find_all(name='td')[2]
    # 武器类型
    wqlx = table.find_all(name='td')[6]
    # 武器伤害
    wqsh = table.find_all(name='td')[7]
    # 武器速度
    wqsd = table.find_all(name='td')[8]
    # 秒伤
    ms = table.find_all(name='td')[9]
    # 需要等级
    lv_num = re.compile('需要等级 \d+')
    need_lv_list = re.findall(lv_num,str(table))
    #长度>0,给值,反之设置空字符串
    if len(need_lv_list)>0:
        need_lv = need_lv_list[0]
    else:
        need_lv = ''
    # 武器等级
    wq_lv = table.find(name='td',attrs={'class':'item_level'}).text

    print(name.string)
    print(english_name.string)
    print(wqlx.string)
    print(wqsh.string)
    print(wqsd.string)
    print(ms.string)
    print(need_lv)
    print(wq_lv)

    # 装备效果
    all_zb = table.find_all(name='td',attrs={'class':'item_spell'})
    str_lits = []
    for zb in all_zb:
        zbA = zb.find(name='a').text
        str_lits.append(zbA)
    str_zb='@'.join(i for i in str_lits)
    print(str_zb)


    zone_name = ''
    percent = ''
    npc_name = ''
    # 掉落信息表
    table_dl = soup.find(name='div',attrs={'class':'grid'})
    # 判断属于哪种掉落,npc,任务,制造
    if table_dl.find(name='td',attrs={'class':'npcs-title'}) != None:
        npc = table_dl.find(name='td', attrs={'class': 'npcs-title'})
        npc_name = npc.find(name='a').text
        # 掉落概率
        percent = table_dl.find_all(name='td')[6].string.replace('\n','')
        zone = table_dl.find(name='td', attrs={'class': 'normal-link'})
        # 掉落地址
        if zone.find(name='a') != None:
            zone_name = zone.find(name='a').text
    # 任务掉落
    elif table_dl.find(name='td', attrs={'class': 'quest-title'}) != None:
        npc = table_dl.find(name='td', attrs={'class': 'quest-title'})
        npc_name = npc.find(name='a').text
        # 掉落概率
        percent = '任务'
        zone = table_dl.find(name='td', attrs={'class': 'normal-link'})
        # 掉落地址
        if zone.find(name='a') != None:
            zone_name = zone.find(name='a').text
    # 制造
    elif table_dl.find(name='td', attrs={'class': 'table-icon'}) != None:
        npc = table_dl.find(name='td', attrs={'class': 'table-icon'})
        npc_name = npc.find(name='a').text
        # 掉落概率
        percent = '制造'

    print(npc_name)
    print(zone_name)
    print(percent)

    data = [name.string, english_name.string, wqlx.string, wqsh.string, wqsd.string, ms.string, need_lv, wq_lv, str_zb,npc_name,zone_name,percent]
    print('===========================')
    return data

def to_CSV(data):
    df = DataFrame([data])
    df.to_csv(r'wq1.csv',mode='a',header=False,index=None,encoding='gbk')

if __name__ == '__main__':
    # url = r'http://cn.60wdb.com/items/c/2/19/page/1'#魔杖
    # url = 'http://cn.60wdb.com/items/c/2/5'#双手锤
    url = r'http://cn.60wdb.com/items/c/2/1'  # 双手斧
    html = get_first_page(url)
    urls = get_urls(html)
    for url_detailed in urls:
        html_detailed = get_first_page(url_detailed)
        data = parse_html_detailed(html_detailed)
        to_CSV(data)





