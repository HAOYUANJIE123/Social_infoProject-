import pandas as pd
import os
import pymysql
from app import selectSQL_goodsrequireTask



def creat_company_table():
    # 打开数据库连接
    db = pymysql.Connect(host='47.97.117.208', port=3306, user='root', passwd='haoyuanjie', db='mysql', charset='utf8')
    # 使用 cursor() 方法创建一个游标对象 cursor
    cursor = db.cursor()
    # 使用 execute() 方法执行 SQL，如果表存在则删除
    # cursor.execute("DROP TABLE IF EXISTS EMPLOYEE")
    # 使用预处理语句创建表
    sql = """CREATE TABLE company (
             企业名称  CHAR(50) NOT NULL,
             法定代表人  CHAR(30),
             注册资本 CHAR(30),  
             成立日期 CHAR(30),
             经营状态 CHAR(30),
             所属省份 CHAR(30),
             所属市区 CHAR(30),
             所属区县 CHAR(30),
             公司类型 CHAR(30),
             统一社会信用代码 CHAR(30),
             纳税人识别号 CHAR(30),
             工商注册号 CHAR(30),
             组织机构代码 CHAR(30),
             联系电话 CHAR(30),
             所属行业 CHAR(30),
             地址 CHAR(100),
             网址  CHAR(30),
             邮箱 CHAR(30),
             经营范围  TEXT,
             money  FLOAT,
             poi_name  CHAR(50),
             lon CHAR(15),
             lat CHAR(15)
             )"""
    cursor.execute(sql)
    # 关闭数据库连接
    db.close()


def read_excel(path=r"temp_company\食品制造业.xls"):
    data = pd.read_excel(path, sheet_name=0, index_col=0)
    data = data[data["lon"] != "-"]
    return data.values.tolist()


def insert(args):
    db = pymysql.Connect(host='47.97.117.208', port=3306, user='root', passwd='haoyuanjie', db='mysql', charset='utf8')
    # 使用cursor()方法获取操作游标
    cursor = db.cursor()
    sql = "INSERT INTO company (企业名称, 法定代表人, 注册资本, 成立日期, 经营状态, 所属省份, 所属市区, 所属区县," \
          "公司类型, 统一社会信用代码, 纳税人识别号, 工商注册号, 组织机构代码, 联系电话, 所属行业, 地址, 网址, 邮箱," \
          "经营范围, money, poi_name, lon, lat) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, " \
          "%s, %s, %s, %s, %s, %s, %s, %s)"

    try:
        # 执行sql语句
        cursor.executemany(sql, args)
        # 提交到数据库执行
        db.commit()
    except:
        # 如果发生错误则回滚
        db.rollback()
    # 关闭数据库连接
    db.close()


def get_all_excel():
    file_path = r"C:\Users\32430\Desktop\Social_infoProject _localhost7.9\数据20210629"
    file_path = r"./"
    path_list = [os.path.join(file_path, i) for i in os.listdir(file_path) if i.endswith('hefei.xls')]
    # path_list = [os.path.join(file_path, i) for i in os.listdir(file_path) if i.endswith('test.xls')]
    if len(path_list) == 0:
        print("temp文件夹为空")
    else:
        for path in path_list:
            args = read_excel(path)
            print(args)
            insert(args)




def creat_require_table():
    # 打开数据库连接
    db = pymysql.Connect(host='47.97.117.208', port=3306, user='root', passwd='haoyuanjie', db='mysql', charset='utf8')
    # 使用 cursor() 方法创建一个游标对象 cursor
    cursor = db.cursor()
    # 使用 execute() 方法执行 SQL，如果表存在则删除
    cursor.execute("DROP TABLE IF EXISTS goodsrequire")
    # 使用预处理语句创建表
    sql = """CREATE TABLE goodsrequire (
             disasterName  CHAR(50) NOT NULL,
             disasterDescription  CHAR(100),
             jiuyuanPos CHAR(30),
             goodsNum CHAR(30),
             companyNum CHAR(30),
             goodstype CHAR(30),
             requireMan CHAR(30),
             midresponseList CHAR(100),
             finalresponseList CHAR(100),
             requirestate CHAR(30),
             signAgreement CHAR(100)
             )"""
    print(sql)
             

    cursor.execute(sql)
    # 关闭数据库连接
    db.close()


# 事故建表
def accident_creat_table():
    # 打开数据库连接
    # db = pymysql.Connect(host='localhost', port=3306, user='root', passwd='123456', db='company', charset='utf8')
    db = pymysql.Connect(host='47.97.117.208', port=3306, user='root', passwd='haoyuanjie', db='mysql', charset='utf8')
    # 使用 cursor() 方法创建一个游标对象 cursor
    cursor = db.cursor()
    # 使用 execute() 方法执行 SQL，如果表存在则删除
    # cursor.execute("DROP TABLE IF EXISTS accident")
    # 使用预处理语句创建表
    sql = """CREATE TABLE accident (
             灾害事故编码 CHAR(100),
             灾害事故名称  TEXT,
             事发时间 TEXT,
             事发省份 TEXT,
             事发地点 TEXT,
             事发地坐标 TEXT,
             事故类型 TEXT,
             主要致灾物质 TEXT,
             灾害事故等级 TEXT,
             损失情况 TEXT,
             主要应急资源 TEXT
             )"""
    cursor.execute(sql)
    # 关闭数据库连接
    db.close()
def accident_insert(args):
    # db = pymysql.Connect(host='localhost', port=3306, user='root', passwd='123456', db='company', charset='utf8')
    db = pymysql.Connect(host='47.97.117.208', port=3306, user='root', passwd='haoyuanjie', db='mysql', charset='utf8')
    # 使用cursor()方法获取操作游标
    cursor = db.cursor()
    sql = "INSERT INTO accident " \
          "(灾害事故编码, 灾害事故名称, 事发时间, 事发省份, 事发地点, 事发地坐标, 事故类型, 主要致灾物质, 灾害事故等级, 损失情况, 主要应急资源) " \
          "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
    try:
        # 执行sql语句
        cursor.executemany(sql, args)
        # 提交到数据库执行
        db.commit()
    except:
        # 如果发生错误则回滚
        db.rollback()
    # 关闭数据库连接
    db.close()
def read_accident_excel():
    path = r"C:\Users\32430\Desktop\Social_infoProject _localhost7.9\汇总表.xls"
    result = pd.read_excel(path, header=0)
    name_list = result.drop_duplicates('事发省份')
    name_list = name_list.sort_values('事发省份')
    print(name_list["事发省份"].to_list())
    print(len(name_list["事发省份"].to_list()))
    print(len(name_list))

    a = result.values.tolist()
    print(a)
    accident_insert(a)
# 个人用户建表
def person_creat_table():
    # 打开数据库连接
    # db = pymysql.Connect(host='localhost', port=3306, user='root', passwd='123456', db='company', charset='utf8')
    db = pymysql.Connect(host='47.97.117.208', port=3306, user='root', passwd='haoyuanjie', db='mysql', charset='utf8')
    # 使用 cursor() 方法创建一个游标对象 cursor
    cursor = db.cursor()
    # 使用 execute() 方法执行 SQL，如果表存在则删除
    cursor.execute("DROP TABLE IF EXISTS user_person")
    # 使用预处理语句创建表
    sql = """CREATE TABLE user_person (
             userID  CHAR(50) NOT NULL,
             user_name  TEXT,
             person_name TEXT,
             money FLOAT,
             industry_cls TEXT,
             xym TEXT,
             province TEXT,
             city TEXT,
             address TEXT,
             lng_lon TEXT,
             phone TEXT,
             email TEXT,
             password TEXT,
             user_cls TEXT
             )"""
    cursor.execute(sql)
    # 关闭数据库连接
    db.close()

# 企业用户建表
def company_creat_table():
    # 打开数据库连接
    # db = pymysql.Connect(host='localhost', port=3306, user='root', passwd='123456', db='company', charset='utf8')
    db = pymysql.Connect(host='47.97.117.208', port=3306, user='root', passwd='haoyuanjie', db='mysql', charset='utf8')
    # 使用 cursor() 方法创建一个游标对象 cursor
    cursor = db.cursor()
    # 使用 execute() 方法执行 SQL，如果表存在则删除
    cursor.execute("DROP TABLE IF EXISTS user_company")
    # 使用预处理语句创建表
    sql = """CREATE TABLE user_company (
             userID  CHAR(50) NOT NULL,
             companyName  CHAR(50),
             person_name TEXT,
             money FLOAT,
             data TEXT,
             state TEXT,
             province TEXT,
             city TEXT,
             company_cls TEXT,
             xym TEXT,
             phone TEXT,
             industry TEXT,
             my_goodstype TEXT,
             address TEXT,
             lng_lon TEXT,
             email CHAR(30),
             password CHAR(30),
             user_cls CHAR(20)
             )"""
    cursor.execute(sql)
    # 关闭数据库连接
    db.close()
if __name__ == '__main__':
    # selectSQL_goodsrequireTask('3','0')
    # print(os.path.abspath("."))

    #以下为MySQL数据库建表
    # person_creat_table()
    # company_creat_table()
    # creat_require_table()
    #建accident表，并写入数据
    # accident_creat_table()
    # read_accident_excel()
    ####公司信息表建表
    # creat_company_table()
    get_all_excel()
