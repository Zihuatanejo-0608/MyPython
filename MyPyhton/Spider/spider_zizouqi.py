#!usr/bin/env python
#-*- coding:utf-8 _*-
"""
@author:andy
@time: 2019/11/27
"""

from time import sleep

from bs4 import BeautifulSoup
from pandas import DataFrame
from selenium import webdriver

# selenium爬取网页内容,BeautifulSoup解析html

# 获取网页html转化为str
def get_web(driver,url):
    #打开网页
    driver.get(url)
    #返回网页内容text
    return driver.page_source

# 解析第一个网页得到英雄名字,返回一个名字的list
def get_names(html):
    # 解析html
    soup = BeautifulSoup(html, 'html.parser')
    fw = soup.find(name='ul', attrs={'class': 'charactor-head-ul'})
    names = []
    for data in fw.find_all(name='p'):
        name = data.text
        names.append(name)
    print(names)
    return names

# 解析英雄基本信息,返回一个含有基本属性的list
def get_hero_info(url_info):
    soup = BeautifulSoup(url_info, 'html.parser')
    basic_info = soup.find(name='div', attrs={'class': 'charactor-box charactor-box-zh-cn'}).find(name='div', attrs={'class': 'name'})
    name = basic_info.find_all(name='span')[0].text
    lvl = basic_info.find_all(name='span')[1].text
    spend = basic_info.find_all(name='span')[2].text
    print('名字:' + name)
    print('稀有程度:' + lvl)
    print('花费:' + spend)
    race = soup.find(name='div', attrs={'class': 'charactor-box charactor-box-zh-cn'}).find(name='li', attrs={'class': 'race'}).find(name='span').text
    print('种族:' + race)
    career = soup.find(name='div', attrs={'class': 'charactor-box charactor-box-zh-cn'}).find(name='li', attrs={'class': 'career'}).find(name='span').text
    print('职业:' + career)

    nature = soup.find(name='div', attrs={'class': 'charactor-box charactor-box-zh-cn'}).find(name='ul', attrs={'class': 'nature'})
    sm = nature.find(name='li', attrs={'title': '生命值'}).find(name='div').text
    gj = nature.find(name='li', attrs={'title': '攻击力'}).find(name='div').text
    hj = nature.find(name='li', attrs={'title': '护甲'}).find(name='div').text
    gs = nature.find(name='li', attrs={'title': '攻击速度'}).find(name='div').text
    mk = nature.find(name='li', attrs={'title': '魔法抗性'}).find(name='div').text
    fw = nature.find(name='li', attrs={'title': '攻击范围'}).find(name='div').text
    print('生命值:' + sm)
    print('攻击力:' + gj)
    print('护甲:' + hj)
    print('攻击速度:' + gs)
    print('魔法抗性:' + mk)
    print('攻击范围:' + fw)

    skill_name = soup.find(name='div', attrs={'class': 'charactor-box charactor-box-zh-cn'}).find(name='p',attrs={'class': 'skill-name'}).text
    skill_text = soup.find(name='div', attrs={'class': 'charactor-box charactor-box-zh-cn'}).find(name='p',attrs={'class': 'skill-text'}).text
    skill = skill_name + ':' + skill_text
    print(skill)
    print('********************')

    data = [name,lvl,spend,race,career,sm,gj,hj,gs,mk,fw,skill]
    return data

# 二星数据
def star2(driver,url_info):
    star2 = driver.find_element_by_xpath('/html/body/div[1]/div/div[2]/div/div[4]/div/div/div[2]/p')
    star2.click()
    sleep(2)
    soup = BeautifulSoup(url_info, 'html.parser')
    nature = soup.find(name='div', attrs={'class': 'charactor-box charactor-box-zh-cn'}).find(name='ul', attrs={'class': 'nature'})
    sm = nature.find(name='li', attrs={'title': '生命值'}).find(name='div').text
    gj = nature.find(name='li', attrs={'title': '攻击力'}).find(name='div').text
    print('生命值:' + sm)
    print('攻击力:' + gj)
    print('********************')

# 三星数据
def star3(driver,url_info):
    star3 = driver.find_element_by_xpath('/html/body/div[1]/div/div[2]/div/div[4]/div/div/div[3]/p')
    star3.click()
    sleep(5)
    soup = BeautifulSoup(url_info, 'html.parser')
    nature = soup.find(name='div', attrs={'class': 'charactor-box charactor-box-zh-cn'}).find(name='ul', attrs={'class': 'nature'})
    sm = nature.find(name='li', attrs={'title': '生命值'}).find(name='div').text
    gj = nature.find(name='li', attrs={'title': '攻击力'}).find(name='div').text
    print('生命值:' + sm)
    print('攻击力:' + gj)
    print('===================')

# 写文件,写入csv
def to_CSV(data):
    df = DataFrame([data])
    df.to_csv(r'zzq5.csv',mode='a',index=None,header=False,encoding='gbk')

# 关闭浏览器
def close_browser(driver):
    driver.close()
    driver.quit()

# 主方法
def mian():
    # firefox设置,无需打开浏览器运行
    firefox_options = webdriver.FirefoxOptions()
    firefox_options.add_argument('--headless')
    # 设置 firefox 驱动
    driver = webdriver.Firefox(executable_path='geckodriver', options=firefox_options)

    url = r'https://ddzzq.qq.com/web201909/charactor.shtml'  # 自走棋
    html = get_web(driver, url)
    names = get_names(html)

    for name in names:
        url_details = 'https://ddzzq.qq.com/web201909/charactor-detail.shtml?id=' + name
        url_info = get_web(driver, url_details)
        data = get_hero_info(url_info)
        # star2(driver, url_info)
        # star3(driver, url_info)
        to_CSV(data)

    close_browser(driver)

if __name__ == '__main__':
    mian()
