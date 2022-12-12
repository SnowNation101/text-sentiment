# -*- coding: utf-8 -*-
# @Time    : 19-3-28 上午10:56
# @Author  : Redtree
# @File    : main.py
# @Desc :

import emotion_eng
import emotion_cn
import pymysql

# 创建连接MYSQL的类
class TestMysql:
    # 初始化变量
    def __init__(self, username, host, passwd, database):
        self.username = username
        self.host = host
        self.passwd = passwd
        self.database = database

    # 创建数据库连接
    def conn_mysql(self):
        conn = pymysql.connect(user=self.username, host=self.host, password=self.passwd, db=self.database)
        return conn

    # 关闭数据库的提示信息
    def close_mysql(self):
        # print("MySQL is Closed")
        pass

    # 查询数据
    def get_data(self,sql):
        self.conn = self.conn_mysql()
        cur = self.conn.cursor()

        # while True:
        #sql = input('输入SQL语句:') #通过这里进行链接
        #print('Received Message: ', sql)  # 这里发过来的data需要是sql语言，直接用于操作数据库
        cur.execute(sql)
        self.conn.commit()
        results = cur.fetchall()

        cur.close()
        self.close_mysql()
        return results

if __name__ == '__main__':
    # 定义变量
    username = 'root'
    host = '127.0.0.1'
    passwd = '123456'
    database = 'text_sentiment'

    # 使用try--except
    try:
        # 创建TestMysql的实例
        mysql = TestMysql(username, host, passwd, database)
        mysql.conn_mysql()
        # sql = ""
        # mysql.get_data(sql)
    except pymysql.err.ProgrammingError as e:
        print("Exception Error is %s" % (e))
    except pymysql.err.OperationalError as e:
        print("Exception Error is %s" % (e))

    sql = "select text from tmp where id = 1 ;"
    data = mysql.get_data(sql)
    data = data[0][0]


    sql = "select language from tmp where id = 1 ;"
    language = mysql.get_data(sql)
    language = language[0][0]


    if language == 0:
        out_put = emotion_cn.getMoodValue(data)
        sql = "update tmp set value=" + str(out_put) + "where id = 1;"
        mysql.get_data(sql)


    if language == 1:
        out_put = emotion_eng.getMoodValue(data)
        sql = "update tmp set value=" + str(out_put) + "where id = 1;"
        mysql.get_data(sql)

