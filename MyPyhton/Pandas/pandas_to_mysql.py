#!usr/bin/env python
#-*- coding:utf-8 _*-
"""
@author:andy
@time: 2019/11/27
"""

import pandas as pd
from sqlalchemy import create_engine

#链接mysql,数据库类型+驱动库,数据库链接地址端口,库名
engine = create_engine('mysql+pymysql://root:xxxxxx@127.0.0.1:3306/testdemo')
# 读取数据源,excel
df = pd.read_csv(r'D:\work\xxxx\xx\xxxx\xxxx\aaa.csv',encoding='gbk')
# 给数据源设置列名
df.columns=['名字','稀有程度','花费','种族','职业','生命值','攻击力','护甲','攻击速度','魔法抗性','攻击范围','技能']
print(df)
# 写入mysql,name=表名, replace=全部清除,再写入
df.to_sql(name='hero',con=engine,index=True,if_exists='replace')



