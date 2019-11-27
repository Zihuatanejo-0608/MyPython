#!usr/bin/env python
#-*- coding:utf-8 _*-
"""
@author:andy
@time: 2019/11/27
"""

import pandas as pd

# 读取excel1,excel2的数据,处理和合并,生成excel3

# 取第一个excel的数据
def one(file,sheet):
    # 读取成为一个矩阵,放到缓存
    data = pd.read_excel(io=file, sheet_name=sheet,header=11,index=False)
    #打印选取范围的列名
    #print(data.head(0))
    #选取第11行开始到第76行结束(76行是从第11行往后算)
    #need_data = data[10:76]

    d1 = data.loc[10:75,['合同号','开票金额','外部其他','外部主营','内部其他']]
    #合同号列,字符串替换
    d1['合同号'] = d1['合同号'].str.replace('\n', '/')
    #剔除‘合同号’为空的行
    d1 = d1.dropna(subset=['合同号'])
    #print(d1)
    return d1

# 取第二个excel的数据
def two(file,sheet):
    data = pd.read_excel(io=file, sheet_name=sheet,header=0,index=False)
    d2 = data.loc[:,['项目编号','合同编号']]
    #重命名列名
    d2.columns = ['项目编号','合同号']
    #print(d2)
    return d2

# 根据d1,d2生成第三张表（终表）
def three(path,d1,d2):
    data = d1.merge(d2, on='合同号',how='left')
    print(data)
    # 将缓存中的矩阵写入csv
    data.to_csv(path + 'data1.csv',encoding='gbk',index=False)

if __name__ == '__main__':
    path = r'D:/XX/XXXX/xxxxx/xxxx/'
    file_one = path + '201x年各月收入预算-按财务报表口径-201xxx.xlsx'
    file_two = path + '软件三部台帐201x.xlsx'

    d1 = one(file_one,'10月')
    d2 = two(file_two,'合同总台帐')
    three(path,d1,d2)



