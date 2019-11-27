#!usr/bin/env python
#-*- coding:utf-8 _*-
"""
@author:andy
@time: 2019/11/27
"""

import pandas as pd

# 读取数据源,遍历行内容,用json格式写入txt,每行生成一个txt,txt名用第一列数据

def one():
    data = pd.read_csv(r'D:/xx/xx/xxx/xxxx/test.csv',encoding='utf8',header=0)
    #遍历df的index
    for i in data.index:
        #取到index对应的Series
        ser=data.loc[i]
        #拼出文件名
        file_name=ser['文件名']+'.txt'
        #因为结果中不需要‘文件名’，删除
        neirong = ser.drop(['文件名'])
        #写文件
        f=open(file_name,'w')
        #series中内容转成json，写入
        f.write(neirong.to_json(force_ascii =False))
        f.close()
    print(data)

def two():
    data = pd.read_csv(r'D:/xx/xxx/xxxx/grsj.csv', encoding='gbk', header=0)
    data = data.fillna("")
    print(data)

    for i in data.index:
        ser = data.loc[i]
        file_name = ser['图片名称'] + '.txt'

        # gtgsh = ser['名称','负责人'].to_json(force_ascii=False)
        # gtgs = ser['姓名','身份证号码'].to_json(force_ascii=False)
        gtgsh = ser[['名称', '负责人']].copy()
        gtsh = ser[['姓名', '身份证号码']].copy()

        neirong = ser.drop(['图片名称', '名称', '负责人', '姓名', '身份证号码'])
        # 写入两个小json
        neirong['个体工商户'] = gtgsh
        neirong['个体商户'] = gtsh

        f = open(file_name, 'w', encoding='utf8')
        f.write(neirong.to_json(force_ascii=False))
        f.close()

if __name__ == '__main__':
    one()

