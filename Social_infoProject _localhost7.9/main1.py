import random
import pandas as pd

from flask import Flask, redirect, url_for, request, render_template, flash
import pymysql

app = Flask(__name__)
@app.route('/')
def query_UI():
    return render_template('button.html')

@app.route('/example', methods=['POST', 'GET'])
def example():
    # rows = accident_select("无", "无", "无")
    # print(rows)
    rows = []
    return render_template('example1.html',
                           rows=rows)

@app.route('/example_select', methods=['POST', 'GET'])
def example_select():
    story_name = str(request.form["story_name"])
    condition_province = str(request.form["condition_province"])
    condition_cls = str(request.form["condition_cls"])
    condition_degree = str(request.form["condition_degree"])
    if story_name == "" and condition_province == "" and condition_cls == "" and condition_degree == "":
        rows = []
    else:
        rows = accident_select(story_name, condition_province, condition_cls, condition_degree)
    return render_template('example1.html',
                           rows=rows)

# 事故建表
def accident_creat_table():
    # 打开数据库连接
    db = pymysql.Connect(host='localhost', port=3306, user='root', passwd='123456', db='company', charset='utf8')
    # db = pymysql.Connect(host='47.97.117.208', port=3306, user='root', passwd='haoyuanjie', db='mysql', charset='utf8')
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
    db = pymysql.Connect(host='localhost', port=3306, user='root', passwd='123456', db='company', charset='utf8')
    # db = pymysql.Connect(host='47.97.117.208', port=3306, user='root', passwd='haoyuanjie', db='mysql', charset='utf8')
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

def read_excel():
    path = r"C:\Users\33294\PycharmProjects\flaskProject _localhost1\汇总表.xls"
    result = pd.read_excel(path, header=0)
    name_list = result.drop_duplicates('事发省份')
    name_list = name_list.sort_values('事发省份')
    print(name_list["事发省份"].to_list())
    print(len(name_list["事发省份"].to_list()))
    print(len(name_list))

    # a = result.values.tolist()
    # print(a)
    # accident_insert(a)

def accident_select(story_name, condition_province, condition_cls, condition_degree):
    args0 = []
    # 打开数据库连接
    db = pymysql.Connect(host='localhost', port=3306, user='root', passwd='123456', db='company', charset='utf8')
    # db = pymysql.Connect(host='47.97.117.208', port=3306, user='root', passwd='haoyuanjie', db='mysql', charset='utf8')
    # 使用cursor()方法获取操作游标
    cursor = db.cursor()
    # SQL 查询语句
    if story_name == "":
        sql = "SELECT * FROM accident"
        if condition_province == "":
            if condition_cls == "":
                if condition_degree == "":
                    sql1 = sql
                else:
                    sql1 = sql + " WHERE 灾害事故等级='%s'" % condition_degree
            else:
                if condition_degree == "":
                    sql1 = sql + " WHERE 事故类型='%s'" % condition_cls
                else:
                    sql1 = sql + " WHERE 事故类型='%s' and 灾害事故等级='%s'" % (condition_cls, condition_degree)
        else:
            if condition_cls == "":
                if condition_degree == "":
                    sql1 = sql + " WHERE 事发省份='%s'" % condition_province
                else:
                    sql1 = sql + " WHERE 事发省份='%s' and 灾害事故等级='%s'" % (condition_province, condition_degree)
            else:
                if condition_degree == "":
                    sql1 = sql + " WHERE 事发省份='%s' and 事故类型='%s'" % (condition_province, condition_cls)
                else:
                    sql1 = sql + " WHERE 事发省份='%s' and 事故类型='%s' and 灾害事故等级='%s'" % \
                           (condition_province, condition_cls, condition_degree)
    else:
        sql1 = "SELECT * FROM accident where 灾害事故名称 like '%{}%'".format(story_name)
    try:
        # 执行SQL语句
        cursor.execute(sql1)
        # 获取所有记录列表
        results = cursor.fetchall()
        for i, row in enumerate(results):
            args = []
            id = row[0]
            name = row[1]
            time = row[2]
            province = row[3]
            address = row[4]
            lonlat = row[5]
            cls = row[6]
            Harmful_substances = row[7]
            degree = row[8]
            loss = row[9]
            Supplies = row[10]

            args.append(id)
            args.append(name)
            args.append(time)
            args.append(province)
            args.append(address)
            args.append(lonlat)
            args.append(cls)
            args.append(Harmful_substances)
            args.append(degree)
            args.append(loss)
            args.append(Supplies)
            args.append("../static/example/"+name+".pdf")
            args.append(i+1)

            args0.append(args)
    except:
        print("Error: unable to fecth data")
    # 关闭数据库连接
    db.close()
    return args0

if __name__ == '__main__':
    # accident_select(condition_province='广东省', condition_cls='危化品—有毒品事故', condition_degree='特')
    # accident_creat_table()
    # read_excel()
    app.run(host='127.0.0.1', port=5000, debug=True)