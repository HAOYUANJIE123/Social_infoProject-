#conding=utf-8
import os
import random
import subprocess
from subprocess import Popen, PIPE
import platform
from flask import Flask, redirect, url_for, request, render_template
import pymysql
from mailmerge import MailMerge
app = Flask(__name__)
@app.route('/')
def query_UI():
    return render_template('login.html')

@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        print("aa")
        user_name = str(request.form["user_name"])
        user_password = str(request.form["user_password"])
        user_cls = str(request.form["user_cls"])
        if user_cls == "个人用户":
            check = login_check(user_name, user_password, table_name="user_person")
        else:
            check = login_check(user_name, user_password, table_name="user_company")
        print(check)
        if check == 1:
            if user_cls == "个人用户":
                return render_template('index1.html',user_name=user_name)
            else:
                return render_template('index2.html',user_name=user_name)
        else:
            return render_template('login.html')

def login_check(user_name, password, table_name):
    check = 0
    # 打开数据库连接
    # db = pymysql.Connect(host='localhost', port=3306, user='root', passwd='123456', db='company', charset='utf8')
    db = pymysql.Connect(host='47.97.117.208', port=3306, user='root', passwd='haoyuanjie', db='mysql', charset='utf8')
    # 使用cursor()方法获取操作游标
    cursor = db.cursor()
    # SQL 查询语句
    sql = "SELECT * FROM " + table_name
    try:
        # 执行SQL语句
        cursor.execute(sql)
        # 获取所有记录列表
        results = cursor.fetchall()
        if table_name == "user_person":
            for row in results:
                sql_name = row[1]
                sql_password = row[-2]
                print(sql_name, user_name, password, sql_password)
                if sql_name == user_name and password == sql_password:
                    check = 1
                    break
        else:
            for row in results:
                sql_name = row[1]
                sql_password = row[-2]
                print(sql_name, sql_password)
                print(sql_name, user_name, password, sql_password)
                if sql_name == user_name and password == sql_password:
                    check = 1
                    break
    except:
        print("Error: unable to fecth data")
    # 关闭数据库连接
    db.close()
    return check

# 个人用户注册
@app.route('/registered_person', methods=['POST', 'GET'])
def registered_person():
    print("用户注册")
    if request.method == 'POST':
        args = []
        user_name = str(request.values["user_name"])
        person_name = str(request.values["person_name"])
        money = str(request.values["money"])
        industry_cls = str(request.values["industry_cls"])
        xym = str(request.values["xym"])
        province = str(request.values["province"])
        city = str(request.values["city"])
        address = str(request.values["address"])
        lng_lon = str(request.values["lng_lon"])
        phone = str(request.values["phone"])
        email = str(request.values["email"])
        user_password = str(request.values["user_password"])

        args.append(user_name)
        args.append(user_name)
        args.append(person_name)
        args.append(money)
        args.append(industry_cls)
        args.append(xym)
        args.append(province)
        args.append(city)
        args.append(address)
        args.append(lng_lon)
        args.append(phone)
        args.append(email)
        args.append(user_password)
        args.append("person")

        print(args)
        registered_person_insert(args)
        results = "注册成功"
        a={"results": results}
        return a

def registered_person_insert(args):
    # db = pymysql.Connect(host='localhost', port=3306, user='root', passwd='123456', db='company', charset='utf8')
    db = pymysql.Connect(host='47.97.117.208', port=3306, user='root', passwd='haoyuanjie', db='mysql', charset='utf8')
    # 使用cursor()方法获取操作游标
    cursor = db.cursor()
    sql = "INSERT INTO user_person (userID, user_name, person_name, money, industry_cls, xym, province, city," \
          "address, lng_lon, phone, email, password, user_cls) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, " \
          "%s, %s, %s, %s)"

    try:
        # 执行sql语句
        cursor.execute(sql, args)
        # 提交到数据库执行
        db.commit()
    except:
        # 如果发生错误则回滚
        db.rollback()
    # 关闭数据库连接
    db.close()


# 企业用户注册
@app.route('/registered_company', methods=['POST', 'GET'])
def registered_company():
    if request.method == 'POST':
        args = []
        company_name = str(request.values["company_name"])
        person_name = str(request.values["person_name"])
        money = float(request.values["money"])
        data = str(request.values["data"])
        state = str(request.values["state"])
        province = str(request.values["province"])
        city = str(request.values["city"])
        company_cls = str(request.values["company_cls"])
        xym = str(request.values["xym"])
        phone = str(request.values["phone"])
        industry = str(request.values["industry"])
        goodstype = str(request.values["goodstype"])
        address = str(request.values["address"])
        lng_lon = str(request.values["lng_lon"])
        email = str(request.values["email"])
        user_password = str(request.values["user_password"])

        args.append(company_name)
        args.append(company_name)
        args.append(person_name)
        args.append(money)
        args.append(data)
        args.append(state)
        args.append(province)
        args.append(city)
        args.append(company_cls)
        args.append(xym)
        args.append(phone)
        args.append(industry)
        args.append(goodstype)
        args.append(address)
        args.append(lng_lon)
        args.append(email)
        args.append(user_password)
        args.append("company")
        # print(args)
        registered_company_insert(args)
        results = "注册成功"
        a={"results": results}
        return a

def userid(table_naem):
    num = 0
    # 打开数据库连接
    # db = pymysql.Connect(host='localhost', port=3306, user='root', passwd='123456', db='company', charset='utf8')
    db = pymysql.Connect(host='47.97.117.208', port=3306, user='root', passwd='haoyuanjie', db='mysql', charset='utf8')
    # 使用cursor()方法获取操作游标
    cursor = db.cursor()
    # SQL 查询语句
    sql = "SELECT COUNT(*) FROM " + table_naem
    try:
        # 执行SQL语句
        cursor.execute(sql)
        # 获取所有记录列表
        print(cursor)
        results = cursor.fetchall()
        num = results[0][0]
    except:
        print("Error: unable to fecth data")
    # 关闭数据库连接
    db.close()
    print(num)
    return num

def registered_company_insert(args):
    # db = pymysql.Connect(host='localhost', port=3306, user='root', passwd='123456', db='company', charset='utf8')
    db = pymysql.Connect(host='47.97.117.208', port=3306, user='root', passwd='haoyuanjie', db='mysql', charset='utf8')
    # 使用cursor()方法获取操作游标
    cursor = db.cursor()
    sql = "INSERT INTO user_company (userID, companyName, person_name, money, data, state, province, city, company_cls," \
          "xym, phone, industry, my_goodstype, address, lng_lon, email, password, user_cls) " \
          "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"

    try:
        # 执行sql语句
        cursor.execute(sql, args)
        # 提交到数据库执行
        db.commit()
    except:
        # 如果发生错误则回滚
        db.rollback()
    # 关闭数据库连接
    db.close()


# ***************************************后端系统的代码*******************************************************************
# *********************************************************************************************************************
# @app.route('/')
# def query_UI():
#     # return render_template('Query.html')
#     return render_template('index.html')


# 接收前端信息
@app.route('/attribute_query', methods=['POST', 'GET'])
def recevie_AttributeQueryInfo_from_html():
    if request.method == 'POST':
        # citystring = request.form['citytext']
        # industrystring = request.form['industrytext']
        citystring = request.values['citytext']
        industrystring = request.values['industrytext']
        citylist = citystring.split(',')
        citylist.remove('')
        industrylist = industrystring.split(',')
        industrylist.remove('')
        print(citylist)
        results = select(city=citylist, company_class=industrylist)
        # return render_template("Query.html", rows=results)
        a={"results": results}
        return a


@app.route('/spaital_query', methods=['POST', 'GET'])
def recevie_SpaitalQueryInfo_from_html():
    if request.method == 'POST':
        # Recinfo = request.form['Rec_info']
        Recinfo = request.values['Rec_info']
        min_lng = Recinfo.split(',')[0].split('-')[0]
        max_lng = Recinfo.split(',')[0].split('-')[1]
        min_lat = Recinfo.split(',')[1].split('-')[0]
        max_lat = Recinfo.split(',')[1].split('-')[1]
        results = select1(min_lng, max_lng, min_lat, max_lat)
        # return render_template("Query.html", rows=results)
        a={"results": results}
        return a


@app.route('/spaital_query1', methods=['POST', 'GET'])
def recevie_SpaitalQueryInfo_from_html1():
    goods2company_dic = {

        '救生防护衣物': '纺织服装、服饰业',
        '应急食品': '食品制造业',
        '医药物资': '医药制造业',
        '医疗防护': '卫生',
        '户外纺织用品': '纺织业',
        '小型救援工具': '批发业',
        '土木相关': '土木工程建筑业',
        '临时板房': '房屋建筑业',
        '农副食品': '农副食品加工业',
        '五金设备': '金属制造业',
        '汽车零件': '汽车制造业',
        '饮用水': '酒、饮料和精制茶制造业',
        '肉类产品': '畜牧业',
        '运输车': '道路运输业',
        '': ''
    }
    if request.method == 'POST':
        jiuyuanPos = request.values['jiuyuanPos']
        goodsNum = request.values['goodsNum']
        companyNum = request.values['companyNum']
        Recinfo = request.values['Rec_info']
        goods = request.values['goodstype']
        resource = goods2company_dic[goods]
        print(resource)
        min_lng = Recinfo.split(',')[0].split('-')[0]
        max_lng = Recinfo.split(',')[0].split('-')[1]
        min_lat = Recinfo.split(',')[1].split('-')[0]
        max_lat = Recinfo.split(',')[1].split('-')[1]
        results = select2(min_lng, max_lng, min_lat, max_lat, resource)
        m = int(companyNum.split('/')[1])
        if len(results) > m:
            random.shuffle(results)
            results = results[:m]
        _, num, lon_list, lat_list, end_city, shipments = \
            quota(des_lat=jiuyuanPos.split(',')[1], des_lng=jiuyuanPos.split(',')[0], M=int(companyNum.split('/')[0]),
                  goodsNum=int(goodsNum), spaital_results=results)
        a={"company_num": num, "company_lon": lon_list, "company_lat": lat_list, "end_company_lon_lat": end_city,
                "shipments": shipments}
        return a
        # return render_template("find_road.html", rows=results, company_num=num, company_lon=lon_list,
        #                        company_lat=lat_list, end_company_lon_lat=end_city, shipments=shipments)


# 数据库select
def select(city, company_class):
    # sql = "INSERT INTO company (企业名称, 法定代表人, 注册资本, 成立日期, 经营状态, 所属省份, 所属市区, 所属区县," \
    #       "公司类型, 统一社会信用代码, 纳税人识别号, 工商注册号, 组织机构代码, 联系电话, 所属行业, 地址, 网址, 邮箱," \
    #       "经营范围, money, poi_name, lon, lat)
    # 打开数据库连接
    db = pymysql.Connect(host='47.97.117.208', port=3306, user='root', passwd='haoyuanjie', db='mysql', charset='utf8')
    # 使用cursor()方法获取操作游标
    cursor = db.cursor()
    # SQL 查询语句
    # sql = "SELECT 企业名称,lon,lat FROM company WHERE 所属市区 in "+str(city)+" and 所属行业 in "+str(company_class)
    sql = "SELECT 企业名称,所属市区,联系电话,所属行业,地址,money,lon,lat FROM company WHERE 所属市区 in " + str(city) + " and 所属行业 in " + str(company_class)
    sql = sql.replace('[', '(').replace(']', ')')
    # sql = "SELECT * FROM company WHERE 所属市区 = '武汉市' and 所属行业='房地产业'"
    print(sql)
    try:
        # 执行SQL语句
        cursor.execute(sql)
        # 获取所有记录列表
        results = cursor.fetchall()
    except:
        print("Error: unable to fecth data")
    # 关闭数据库连接
    db.close()
    results = list(results)
    print(results)
    return results


def select1(min_lng, max_lng, min_lat, max_lat):
    # sql = "INSERT INTO company (企业名称, 法定代表人, 注册资本, 成立日期, 经营状态, 所属省份, 所属市区, 所属区县," \
    #       "公司类型, 统一社会信用代码, 纳税人识别号, 工商注册号, 组织机构代码, 联系电话, 所属行业, 地址, 网址, 邮箱," \
    #       "经营范围, money, poi_name, lon, lat)
    # 打开数据库连接
    db = pymysql.Connect(host='47.97.117.208', port=3306, user='root', passwd='haoyuanjie', db='mysql', charset='utf8')
    # 使用cursor()方法获取操作游标
    cursor = db.cursor()
    # SQL 查询语句
    # sql = "SELECT 企业名称,lon,lat FROM company WHERE 所属市区 in "+str(city)+" and 所属行业 in "+str(company_class)
    sql = "SELECT 企业名称,所属市区,联系电话,所属行业,地址,money,lon,lat FROM company" \
          " WHERE lon >=" + min_lng + " and lon <= " + max_lng + " and lat >= " + min_lat + " and lat <= " + max_lat
    # sql = "SELECT 企业名称,所属市区,联系电话,所属行业,地址,money,lon,lat FROM company" \
    #       " WHERE lon >=" + min_lng + " and lon <= " + max_lng+ " and lat >= " + min_lat+ " and lat <= " +max_lat
    sql = sql.replace('[', '(').replace(']', ')')
    # sql = "SELECT * FROM company WHERE 所属市区 = '武汉市' and 所属行业='房地产业'"
    print(sql)
    try:
        # 执行SQL语句
        cursor.execute(sql)
        # 获取所有记录列表
        results = cursor.fetchall()
    except:
        print("Error: unable to fecth data")
    # 关闭数据库连接
    db.close()
    results = list(results)
    print(results)
    return results


def select2(min_lng, max_lng, min_lat, max_lat, resource):
    # sql = "INSERT INTO company (企业名称, 法定代表人, 注册资本, 成立日期, 经营状态, 所属省份, 所属市区, 所属区县," \
    #       "公司类型, 统一社会信用代码, 纳税人识别号, 工商注册号, 组织机构代码, 联系电话, 所属行业, 地址, 网址, 邮箱," \
    #       "经营范围, money, poi_name, lon, lat)
    # 打开数据库连接
    db = pymysql.Connect(host='47.97.117.208', port=3306, user='root', passwd='haoyuanjie', db='mysql', charset='utf8')
    # 使用cursor()方法获取操作游标
    cursor = db.cursor()
    # SQL 查询语句
    # sql = "SELECT 企业名称,lon,lat FROM company WHERE 所属市区 in "+str(city)+" and 所属行业 in "+str(company_class)
    sql = "SELECT 企业名称,所属市区,联系电话,所属行业,地址,money,lon,lat FROM company" \
          " WHERE lon >=" + min_lng + " and lon <= " + max_lng + " and lat >= " + min_lat + " and lat <= " + max_lat + " and 所属行业 like " + "'%" + resource + "%'"
    # sql = "SELECT 企业名称,所属市区,联系电话,所属行业,地址,money,lon,lat FROM company" \
    #       " WHERE lon >=" + min_lng + " and lon <= " + max_lng+ " and lat >= " + min_lat+ " and lat <= " +max_lat
    sql = sql.replace('[', '(').replace(']', ')')
    # sql = "SELECT * FROM company WHERE 所属市区 = '武汉市' and 所属行业='房地产业'"
    print(sql)
    try:
        # 执行SQL语句
        cursor.execute(sql)
        # 获取所有记录列表
        results = cursor.fetchall()
    except:
        print("Error: unable to fecth data")
    # 关闭数据库连接
    db.close()
    results = list(results)
    print(results)
    return results


# ***************** 路径规划相关函数**************************
import pandas as pd
import json
from urllib.request import urlopen
import time
import numpy as np
import math


def time_and_distance(lat, lng, des_lat, des_lng, ak):
    # "http: // api.map.baidu.com / direction / v2 / driving?origin = 40.01116, 116.339303 & destination = 39.936404, 116.452562 & ak = a43urGu5pblMlqdO4yA08z5vde376RwW"
    url_drive = "http://api.map.baidu.com/direction/v2/driving?origin=%s&destination=%s&output=json&ak=%s" \
                % (str(lat) + "," + str(lng), str(des_lat) + "," + str(des_lng), ak)
    print(url_drive)
    result_drive = json.loads(urlopen(url_drive).read())  # json转dict
    status_drive = result_drive['status']
    print('ak秘钥：{0}  获取驾车路线状态码status：{1}'.format(ak, status_drive))
    if status_drive == 0:  # 状态码为0：无异常
        distance_drive = result_drive['result']['routes'][0]['distance']  # 里程(米)
        timesec_drive = result_drive['result']['routes'][0]['duration']  # 耗时(秒)
    elif status_drive == 302 or status_drive == 210 or status_drive == 201:  # 302:额度不足;210:IP验证未通过
        distance_drive = timesec_drive = 'AK错误'
    else:
        distance_drive = timesec_drive = '请求错误'
    return distance_drive, timesec_drive


def get_all_message(des_lat, des_lng, spaital_results):
    ak = "5E5EE28a7615536d1ffe2ce2a3667859"
    # print(pf)
    names = []
    moneys = []
    lats = []
    lngs = []
    for i in spaital_results:
        names.append(i[0])
        moneys.append(i[5])
        lats.append(float(i[7]))
        lngs.append(float(i[6]))

    distance_drive_list = []
    timesec_drive_list = []

    for lat, lng in zip(lats, lngs):
        time.sleep(1)
        # 114.309043, 30.550317 黄鹤楼

        distance_drive, timesec_drive = time_and_distance(lat, lng, des_lat, des_lng, ak)
        print(distance_drive, timesec_drive)
        distance_drive_list.append(distance_drive)
        timesec_drive_list.append(timesec_drive)
        goal_city_position = [float(des_lng), float(des_lat)]
    return names, lats, lngs, moneys, distance_drive_list, timesec_drive_list, goal_city_position


def quota(des_lat, des_lng, M, goodsNum, spaital_results):
    _, _, _, money_list, distance_list, time_list, _ = get_all_message(des_lat, des_lng, spaital_results)

    def Normalization(x, Max, Min):
        x = (x - Min) / (Max - Min)
        return x

    money_list_Normalization = Normalization(money_list, Max=np.max(money_list), Min=np.min(money_list))
    time_list_Normalization = Normalization(time_list, Max=np.max(time_list), Min=np.min(time_list))
    score = 0.7 * time_list_Normalization + 0.3 * money_list_Normalization
    print(score)
    # score1 = sorted(score, reverse=True)
    # print(score1)
    score_index = score.argsort()[::-1]
    # 选取topM

    top_M = score_index[:M]
    print(top_M)

    # 计算配额

    name_list, lat_list, lng_list, _, _, _, end_city = get_all_message(des_lat, des_lng, spaital_results)

    top_M_name = np.array([])
    top_M_money = np.array([])
    top_M_lat = np.array([])
    top_M_lng = np.array([])
    for i in top_M:
        top_M_name = np.append(top_M_name, name_list[i])
        top_M_money = np.append(top_M_money, money_list[i])
        top_M_lat = np.append(top_M_lat, float(lat_list[i]))
        top_M_lng = np.append(top_M_lng, float(lng_list[i]))

    def Shipments(money, number):
        money_sum = money.sum()
        shipments = np.ceil(money / money_sum * number)
        return shipments

    print(top_M_money)
    shipments = Shipments(top_M_money, number=goodsNum)
    print(shipments)
    print(top_M_name, top_M_money, top_M_lat, top_M_lng)
    return top_M_name, M, top_M_lng.tolist(), top_M_lat.tolist(), end_city, shipments.tolist()


# 888888888888888888888888888888888888888申请人界面的相关函数88888888888888888888888888888888888888888888888888888888888888888888888888888
# 任务发布请求相关后端函数*****************************************************************************************************************
@app.route('/add_require', methods=['POST', 'GET'])
def add_require2mysql():
    if request.method == 'POST':
        disasterName = request.values['disasterName']
        disasterDescription = request.values['disasterDescription']
        jiuyuanPos = request.values['jiuyuanPos'].replace(',', '_')
        goodsNum = request.values['goodsNum']
        companyNum = request.values['companyNum']
        goodstype = request.values['goodstype']
        requireMan = request.values['requireMan']
        midresponseList = ''
        finalresponseList = ''
        requirestate = '0'
        signAgreement = ''
        insert_require(disasterName, disasterDescription, jiuyuanPos, goodsNum, companyNum, goodstype, requireMan,
                       midresponseList, finalresponseList, requirestate, signAgreement)
        return ''


def insert_require(disasterName, disasterDescription, jiuyuanPos, goodsNum, companyNum, goodstype, requireMan,
                   midresponseList, finalresponseList, requirestate, signAgreement):
    db = pymysql.Connect(host='47.97.117.208', port=3306, user='root', passwd='haoyuanjie', db='mysql', charset='utf8')
    # 使用cursor()方法获取操作游标
    cursor = db.cursor()
    sql = '''INSERT INTO goodsrequire (disasterName, disasterDescription, jiuyuanPos, goodsNum, companyNum, goodstype, requireMan, midresponseList,finalresponseList,requirestate,signAgreement \
          ) VALUES ('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s')'''
    sql = sql % (
        disasterName, disasterDescription, jiuyuanPos, goodsNum, companyNum, goodstype, requireMan, midresponseList,
        finalresponseList, requirestate, signAgreement)
    try:
        # 执行sql语句
        cursor.execute(sql)
        # 提交到数据库执行
        db.commit()
    except:
        # 如果发生错误则回滚
        db.rollback()
    # 关闭数据库连接
    db.close()


# 为申请任务用户查询可申请的物资需求任务******************************************************************************************************************
@app.route('/selectForme', methods=['POST', 'GET'])
def select_goodsrequireTask_Forme():
    if request.method == 'POST':
        # 根据用户名，查找自己可以提供什么物资
        userID = request.values['userID'].split(":")[1]
        my_goodstype = selectSQL_userInfoByUserID(userID)
        # 根据自己可以提供的物资以及物资需求状态去goodsrequire表遍
        requirestate = '0'
        # my_goodstype='3'
        goodsrequireTask = selectSQL_goodsrequireTask(userID, my_goodstype, requirestate)
        disasterName = [i[0] for i in goodsrequireTask]
        disasterDescription = [i[1] for i in goodsrequireTask]
        goodstype = [i[5] for i in goodsrequireTask]
        goodsNum = [i[3] for i in goodsrequireTask]
        a={"disasterName": disasterName, "disasterDescription": disasterDescription, "goodstype": goodstype,
                "goodsNum": goodsNum}
        return a


def selectSQL_userInfoByUserID(userID):
    db = pymysql.Connect(host='47.97.117.208', port=3306, user='root', passwd='haoyuanjie', db='mysql', charset='utf8')
    # 使用cursor()方法获取操作游标
    cursor = db.cursor()
    sql = "select my_goodstype from user_company where userID='{}'".format(userID)
    print(sql)
    # 执行SQL语句
    cursor.execute(sql)
    # 获取所有记录列表
    results = cursor.fetchall()
    # 关闭数据库连接
    db.close()
    results = list(results)[0][0]
    return results


def selectSQL_goodsrequireTask(userID, my_goodstype, requirestate):
    db = pymysql.Connect(host='47.97.117.208', port=3306, user='root', passwd='haoyuanjie', db='mysql', charset='utf8')
    # 使用cursor()方法获取操作游标
    cursor = db.cursor()
    sql = "select * from goodsrequire where goodstype='{}' and requirestate='{}' and midresponseList not like '%{}%' ".format(
        my_goodstype, requirestate, userID)
    print(sql)
    # results=[]
    try:
        # 执行SQL语句
        cursor.execute(sql)
        # 获取所有记录列表
        results = cursor.fetchall()
        print('')
    except:
        print("Error: unable to fecth data")
    # 关闭数据库连接
    db.close()
    results = list(results)
    # disasterName=[i[0] for i in results ]
    # disasterDescription=[i[1] for i in results ]
    # goodstype=[i[5] for i in results ]
    # goodsNum=[i[3] for i in results ]
    return results


# 为申请任务用户查询已经申请的物资需求任务******************************************************************************************************************
@app.route('/haveapply_selectForme', methods=['POST', 'GET'])
def haveapply_selectForme():
    if request.method == 'POST':
        # 根据用户名，查找自己可以提供什么物资
        userID = request.values['userID'].split(":")[1]
        requirestate = '0'
        goodsrequireTask = selectSQL_haveapply_goodsrequireTask(userID, requirestate)
        disasterName = [i[0] for i in goodsrequireTask]
        disasterDescription = [i[1] for i in goodsrequireTask]
        goodstype = [i[5] for i in goodsrequireTask]
        goodsNum = [i[3] for i in goodsrequireTask]
        a={"disasterName": disasterName, "disasterDescription": disasterDescription, "goodstype": goodstype,
                "goodsNum": goodsNum}
        return a


def selectSQL_haveapply_goodsrequireTask(userID, requirestate):
    db = pymysql.Connect(host='47.97.117.208', port=3306, user='root', passwd='haoyuanjie', db='mysql', charset='utf8')
    # 使用cursor()方法获取操作游标
    cursor = db.cursor()
    sql = "select * from goodsrequire where requirestate='{}' and midresponseList like '%{}%' ".format(requirestate,
                                                                                                       userID)
    print(sql)
    try:
        # 执行SQL语句
        cursor.execute(sql)
        # 获取所有记录列表
        results = cursor.fetchall()
        print('')
    except:
        print("Error: unable to fecth data")
    # 关闭数据库连接
    db.close()
    results = list(results)
    return results


# 申请按钮的物资需求任务*******************************************************************************************************
@app.route('/applyrequireTask', methods=['POST', 'GET'])
def applyrequireTask():
    if request.method == 'POST':
        # 根据申请人用户名，任务名将申请人用户名写入任务表中的midresponseList
        userID = request.values['userID'].split(":")[1]
        disasterName = request.values['disasterName']
        updateSQL_midresponseList(userID, disasterName)
        return ''


def updateSQL_midresponseList(userID, disasterName):
    db = pymysql.Connect(host='47.97.117.208', port=3306, user='root', passwd='haoyuanjie', db='mysql', charset='utf8')
    # 使用cursor()方法获取操作游标
    cursor = db.cursor()
    # 先获取该任务的中间回复人列表记录
    sql = "select midresponseList from goodsrequire where disasterName ='{}'".format(disasterName)
    cursor.execute(sql)
    result = cursor.fetchall()
    oldmidresponseList = list(result)[0]
    oldmidresponseList = oldmidresponseList[0]
    if userID not in oldmidresponseList:
        newmidresponseList = oldmidresponseList + '$' + userID
        sql = "update goodsrequire set midresponseList='{}' where disasterName='{}'".format(newmidresponseList,
                                                                                            disasterName)
        print(sql)
        cursor.execute(sql)
        db.commit()
        # 关闭数据库连接
        db.close()


# 为申请任务用户查询绘制按钮自己到救援点的路线*******************************************************************************************************
@app.route('/twoPointRoad', methods=['POST', 'GET'])
def twoPointRoad():
    if request.method == 'POST':
        # 根据申请人用户名，任务名将申请人用户名写入任务表中的midresponseList
        userID = request.values['userID'].split(":")[1]
        disasterName = request.values['disasterName']
        companyPos, jiuyuanPos = selectSQL_twoPointPosition(userID, disasterName)
        a={"companyPos": companyPos, "jiuyuanPos": jiuyuanPos}
        return a


def selectSQL_twoPointPosition(userID, disasterName):
    db = pymysql.Connect(host='47.97.117.208', port=3306, user='root', passwd='haoyuanjie', db='mysql', charset='utf8')
    # 使用cursor()方法获取操作游标
    cursor = db.cursor()
    # 先获取自己点的经纬度坐标
    sql = "select lon,lat from company where 企业名称 =(select companyName from user_company where userID ='{}')".format(
        userID)
    cursor.execute(sql)
    result = cursor.fetchall()
    result = list(result)
    company_lon = [i[0] for i in result][0]
    company_lat = [i[1] for i in result][0]
    companyPos = [float(company_lon), float(company_lat)]
    sql = "select jiuyuanPos from goodsrequire where disasterName ='{}'".format(disasterName)
    print(sql)
    cursor.execute(sql)
    result = cursor.fetchall()
    result = list(result)[0][0]
    jiuyuan_lon = result.split('_')[0]
    jiuyuan_lat = result.split('_')[1]
    jiuyuanPos = [float(jiuyuan_lon), float(jiuyuan_lat)]
    # 关闭数据库连接
    db.close()
    return companyPos, jiuyuanPos


# 查询需要执行的物资需求任务*******************************************************************************************************
@app.route('/needtodo_selectForme', methods=['POST', 'GET'])
def needtodo_selectForme():
    if request.method == 'POST':
        if request.method == 'POST':
            # 根据用户名，查找任务表，自己需要执行的任务
            userID = request.values['userID'].split(":")[1]
            requirestate = '1'

            needtodo_taskResult = selectSQL_needtode_goodsrequireTask(userID, requirestate)

            disasterName = [i[0] for i in needtodo_taskResult]
            disasterDescription = [i[1] for i in needtodo_taskResult]
            goodstype = [i[5] for i in needtodo_taskResult]
            goodsNum = [i[3] for i in needtodo_taskResult]
            requireman = [i[6] for i in needtodo_taskResult]
            signAgreement = [i[10] for i in needtodo_taskResult]
            requiremanEmail = [selectSQL_requiremanEmail(i) for i in requireman]
            a={"disasterName": disasterName, "disasterDescription": disasterDescription, "goodstype": goodstype,
                    "goodsNum": goodsNum, "requireman": requireman, "requiremanEmail": requiremanEmail,
                    "signAgreement": signAgreement}
            return a


def selectSQL_needtode_goodsrequireTask(userID, requirestate):
    db = pymysql.Connect(host='47.97.117.208', port=3306, user='root', passwd='haoyuanjie', db='mysql', charset='utf8')
    # 使用cursor()方法获取操作游标
    cursor = db.cursor()
    sql = "select * from goodsrequire where finalresponseList like '%{}%' and requirestate='{}' ".format(userID,
                                                                                                         requirestate)
    print(sql)
    try:
        # 执行SQL语句
        cursor.execute(sql)
        # 获取所有记录列表
        results = cursor.fetchall()
        print('')
    except:
        print("Error: unable to fecth data")
    # 关闭数据库连接
    db.close()
    results = list(results)
    # disasterName=[i[0] for i in results ]
    # disasterDescription=[i[1] for i in results ]
    # goodstype=[i[5] for i in results ]
    # goodsNum=[i[3] for i in results ]
    return results


def selectSQL_requiremanEmail(requireman):
    db = pymysql.Connect(host='47.97.117.208', port=3306, user='root', passwd='haoyuanjie', db='mysql', charset='utf8')
    # 使用cursor()方法获取操作游标
    cursor = db.cursor()
    sql = "select email from user_person where user_name='{}' ".format(requireman)
    print(sql)
    try:
        # 执行SQL语句
        cursor.execute(sql)
        # 获取所有记录列表
        results = cursor.fetchall()
        print('')
    except:
        print("Error: unable to fecth data")
    # 关闭数据库连接
    db.close()
    requiremanEmail = list(results)[0][0]
    return requiremanEmail
    # *****签订协议******************************


@app.route('/signAgreement', methods=['POST', 'GET'])
def signAgreement():
    if request.method == 'POST':
        # 根据申请人用户名，任务名将申请人用户名写入任务表中的midresponseList
        userID = request.values['userID'].split(":")[1]
        disasterName = request.values['disasterName']
        requirestate = '1'
        if request.values['userID'].split(":")[0]=='公司名称':
            updateSQL_signAgreement(userID, disasterName, requirestate)
            create_Agreement_myresponse(userID, disasterName, requirestate)
        else:
            updateSQL_signAgreement(userID, disasterName, requirestate)
            create_Agreement_myrequire(disasterName, requirestate)
        return ''


def updateSQL_signAgreement(userID, disasterName, requirestate):
    db = pymysql.Connect(host='47.97.117.208', port=3306, user='root', passwd='haoyuanjie', db='mysql', charset='utf8')
    # 使用cursor()方法获取操作游标
    cursor = db.cursor()
    # 先获取该任务的中间回复人列表记录
    sql = "select signAgreement from goodsrequire where disasterName ='{}' and requirestate='{}'".format(disasterName,
                                                                                                         requirestate)
    cursor.execute(sql)
    result = cursor.fetchall()
    oldsignAgreement = list(result)[0]
    oldsignAgreement = oldsignAgreement[0]
    if userID not in oldsignAgreement:
        newsignAgreement = oldsignAgreement + '$' + userID
        sql = "update goodsrequire set signAgreement='{}' where disasterName='{}' and  requirestate='{}' ".format(
            newsignAgreement, disasterName, requirestate)
        print(sql)
        cursor.execute(sql)
        db.commit()
        # 关闭数据库连接
        db.close()


def create_Agreement_myresponse(userID, disasterName, requirestate):
    db = pymysql.Connect(host='47.97.117.208', port=3306, user='root', passwd='haoyuanjie', db='mysql', charset='utf8')
    # 使用cursor()方法获取操作游标
    cursor = db.cursor()
    sql = "select companyName from user_company where userID='{}'".format(userID)
    print(sql)
    # 执行SQL语句
    cursor.execute(sql)
    # 获取所有记录列表
    results = cursor.fetchall()
    companyName = list(results)[0][0]
    # 先获取该任务的中间回复人列表记录
    sql = "select disasterDescription, requireMan,goodsNum,goodstype,companyNum from goodsrequire where disasterName ='{}' and requirestate='{}'".format(
        disasterName, requirestate)
    cursor.execute(sql)
    result = cursor.fetchall()
    # 关闭数据库连接
    db.close()
    result = list(result)[0]
    reason = result[0]
    requireName = result[1]
    responseName = companyName
    goodstype = result[3]
    goodsNum = result[2]
    companyNum = int(result[4])
    seed = random.randint(1, companyNum)
    goodsNum = int(int(goodsNum) * (seed / companyNum))
    create_pdf_Agreement(disasterName=disasterName, requireName=requireName, responseName=responseName, reason=reason,
                         goodstype=goodstype, goodsNum=str(goodsNum), is_myrequire=False)


# 888888888888888888888888888888888888888发布人界面的相关函数88888888888888888888888888888888888888888888888888888888888888888888888888888
# 查询自己发布的相关后端函数*****************************************************************************************************************
@app.route('/selectMyrequireTask', methods=['POST', 'GET'])
def selectMyrequireTask():
    if request.method == 'POST':
        # 根据用户名，查找自己可以提供什么物资
        userID = request.values['userID'].split(":")[1]
        # requirestate='0'
        goodsrequireTask = selectSQL_haverequire_state0_goodsrequireTask(userID)
        disasterName = [i[0] for i in goodsrequireTask]
        goodstype = [i[5] for i in goodsrequireTask]
        goodsNum = [i[3] for i in goodsrequireTask]
        midresponseList = [i[7] for i in goodsrequireTask]
        companyNum = [i[4] for i in goodsrequireTask]
        finalresponseList = [i[8] for i in goodsrequireTask]
        a={"disasterName": disasterName, "midresponseList": midresponseList, "goodstype": goodstype,
                "goodsNum": goodsNum, "companyNum": companyNum, "finalresponseList": finalresponseList}
        return a


def selectSQL_haverequire_state0_goodsrequireTask(userID):
    db = pymysql.Connect(host='47.97.117.208', port=3306, user='root', passwd='haoyuanjie', db='mysql', charset='utf8')
    # 使用cursor()方法获取操作游标
    cursor = db.cursor()
    # sql = "select * from goodsrequire where requirestate='{}' and requireMan ='{}' ".format(requirestate,userID)
    sql = "select * from goodsrequire where requireMan ='{}' ".format(userID)
    print(sql)
    try:
        # 执行SQL语句
        cursor.execute(sql)
        # 获取所有记录列表
        results = cursor.fetchall()
        print('')
    except:
        print("Error: unable to fecth data")
    # 关闭数据库连接
    db.close()
    results = list(results)
    return results


# 发布人根据候选人列表计算最终*****************************************************************************************************************
@app.route('/caculate', methods=['POST', 'GET'])
def caculate():
    if request.method == 'POST':
        midresponse = request.values['midresponse']
        disasterName = request.values['disasterName']
        companyNum = int(request.values['companyNum'])
        goodsNum = int(request.values['goodsNum'])
        # 根据灾害名获取救援点的经纬坐标
        jiuyuanPos = selectSQL_jiuyuanPos(disasterName)
        # 获取候选公司的经纬度以及资产
        companyList = midresponse.split('$')
        if '' in companyList:
            companyList.remove('')

        spaital_resultsList = []
        for userID in companyList:
            spaital_result = selectSQL_companyinfo(userID)
            spaital_resultsList.append(spaital_result)
        Topcmopanynamelist, num, lon_list, lat_list, end_city, shipments = quota(jiuyuanPos[1], jiuyuanPos[0],
                                                                                 companyNum, goodsNum,
                                                                                 spaital_resultsList)
        # 将Topcmopanyname公司对应的userID写入finalresponseList,并修改状态为'1'
        updateSQL_goodsrequire_finalresponseList(Topcmopanynamelist, disasterName)
        a={"company_num": num, "company_lon": lon_list, "company_lat": lat_list, "end_company_lon_lat": end_city,
                "shipments": shipments}
        return a


def selectSQL_jiuyuanPos(disasterName):
    db = pymysql.Connect(host='47.97.117.208', port=3306, user='root', passwd='haoyuanjie', db='mysql', charset='utf8')
    # 使用cursor()方法获取操作游标
    cursor = db.cursor()
    # 先获取自己点的经纬度坐标
    sql = "select jiuyuanPos from goodsrequire where disasterName ='{}'".format(disasterName)
    print(sql)
    cursor.execute(sql)
    result = cursor.fetchall()
    result = list(result)[0][0]
    jiuyuan_lon = result.split('_')[0]
    jiuyuan_lat = result.split('_')[1]
    jiuyuanPos = [float(jiuyuan_lon), float(jiuyuan_lat)]
    # 关闭数据库连接
    db.close()
    return jiuyuanPos


def selectSQL_companyinfo(userID):
    db = pymysql.Connect(host='47.97.117.208', port=3306, user='root', passwd='haoyuanjie', db='mysql', charset='utf8')
    # 使用cursor()方法获取操作游标
    cursor = db.cursor()
    # 先获取自己点的经纬度坐标
    sql = "select 企业名称,所属市区,联系电话,所属行业,地址,money,lon,lat from company where 企业名称 =(select companyName from user_company where userID ='{}')".format(
        userID)
    cursor.execute(sql)
    results = cursor.fetchall()
    results = list(results)[0]
    results = list(results)
    print(results)
    return results


def selectSQL_companyName2userID(companyName):
    db = pymysql.Connect(host='47.97.117.208', port=3306, user='root', passwd='haoyuanjie', db='mysql', charset='utf8')
    # 使用cursor()方法获取操作游标
    cursor = db.cursor()
    # 先获取自己点的经纬度坐标
    sql = "select userID from user_company where companyName ='{}'".format(companyName)
    cursor.execute(sql)
    results = cursor.fetchall()
    results = list(results)[0][0]
    return results


def updateSQL_goodsrequire_finalresponseList(Topcmopanynamelist, disasterName):
    finalresponseList = ''
    for companyName in Topcmopanynamelist:
        finalresponseList += selectSQL_companyName2userID(companyName) + '*'
    print(finalresponseList)
    db = pymysql.Connect(host='47.97.117.208', port=3306, user='root', passwd='haoyuanjie', db='mysql', charset='utf8')
    # 使用cursor()方法获取操作游标
    cursor = db.cursor()
    sql = "update goodsrequire set finalresponseList='{}' where disasterName='{}'".format('', disasterName)

    print(sql)
    cursor.execute(sql)
    db.commit()

    sql = "update goodsrequire set finalresponseList='{}' where disasterName='{}'".format(finalresponseList,
                                                                                          disasterName)

    print(sql)
    cursor.execute(sql)
    db.commit()

    sql = "update goodsrequire set requirestate='{}' where disasterName='{}'".format('1', disasterName)

    print(sql)
    cursor.execute(sql)
    db.commit()
    # 关闭数据库连接
    db.close()


# 发布人选择待签订*****************************************************************************************************************
@app.route('/needtoSign_ForRequireman', methods=['POST', 'GET'])
def needtoSign_ForRequireman():
    if request.method == 'POST':
            # 根据用户名，查找任务表，自己需要执行的任务
        userID = request.values['userID'].split(":")[1]
        requirestate = '1'
        needtodo_taskResult = selectSQL_needtoSign_ForRequireman_goodsrequireTask(userID, requirestate)

        disasterName = [i[0] for i in needtodo_taskResult]
        disasterDescription = [i[1] for i in needtodo_taskResult]
        goodstype = [i[5] for i in needtodo_taskResult]
        goodsNum = [i[3] for i in needtodo_taskResult]
        requireman = [i[6] for i in needtodo_taskResult]
        signAgreement = [i[10] for i in needtodo_taskResult]
        # create_Agreement_myrequire(disasterName[0], requirestate)
        a={"disasterName": disasterName, "disasterDescription": disasterDescription, "goodstype": goodstype,
                "goodsNum": goodsNum, "requireman": requireman, "signAgreement": signAgreement}
        return a


def selectSQL_needtoSign_ForRequireman_goodsrequireTask(userID, requirestate):
    db = pymysql.Connect(host='47.97.117.208', port=3306, user='root', passwd='haoyuanjie', db='mysql', charset='utf8')
    # 使用cursor()方法获取操作游标
    cursor = db.cursor()
    sql = "select * from goodsrequire where requireMan ='{}' and requirestate='{}' ".format(userID, requirestate)
    print(sql)
    try:
        # 执行SQL语句
        cursor.execute(sql)
        # 获取所有记录列表
        results = cursor.fetchall()
        print('')
    except:
        print("Error: unable to fecth data")
    # 关闭数据库连接
    db.close()
    results = list(results)
    return results


def create_Agreement_myrequire(disasterName, requirestate):
    db = pymysql.Connect(host='47.97.117.208', port=3306, user='root', passwd='haoyuanjie', db='mysql', charset='utf8')
    # 使用cursor()方法获取操作游标
    cursor = db.cursor()
    sql = "select disasterDescription, requireMan,goodsNum,goodstype from goodsrequire where disasterName ='{}' and requirestate='{}'".format(
        disasterName, requirestate)
    cursor.execute(sql)
    result = cursor.fetchall()
    # 关闭数据库连接
    db.close()
    result = list(result)[0]
    reason = result[0]
    requireName = result[1]
    goodstype = result[3]
    goodsNum = result[2]
    create_pdf_Agreement(disasterName=disasterName, requireName=requireName, responseName='*****', reason=reason,
                         goodstype=goodstype, goodsNum='*****', is_myrequire=True)


# 协议生成部分*********************************************************************************************
def create_pdf_Agreement(disasterName, requireName, responseName, reason, goodstype, goodsNum, is_myrequire=True):
    motherpath = os.path.abspath(".")
    if is_myrequire:
        template = os.path.join(motherpath, 'static/Agreement/FirstAgreement.docx')  # 模版位置
    else:
        template = os.path.join(motherpath, 'static/Agreement/SecondAgreement.docx')  # 模版位置
    document = MailMerge(template)
    document.merge(
        disasterName=disasterName,  # 第三列到域1
        requireName=requireName,  # 第四列到域2
        responseName=responseName,  # 第五列到域3
        reason=reason,  # 第六列到域4
        goodstype=goodstype,  # 第七列到域5
        goodsNum=goodsNum,  # 第八列到域6
        danjia='***',  # 商品单价
        howmuch='***'
    )
    wordname = template.replace('Agreement.', 'newAgreement.')  # 甲方作为文件名
    if os.path.exists(wordname):
        os.remove(wordname)
    document.write(wordname)  # 创建新文件
    document.close()
    covert_word2pdf(wordname)


def covert_word2pdf(word_path):
    system = platform.system()
    if system == 'Windows':
        covert_word2pdf_win(word_path)

    else:
        covert_word2pdf_Linux(word_path)


def covert_word2pdf_win(word_path):
    from win32com.client import Dispatch, constants, gencache
    import pythoncom
    pythoncom.CoInitialize()
    wd=Dispatch('Word.Application')
    pdf_path=word_path.replace('.docx','.pdf')
    if os.path.exists(pdf_path):
        os.remove(pdf_path)
    try:
        doc=wd.Documents.Open(word_path,ReadOnly=1)
        doc.SaveAs(pdf_path,FileFormat=17)
        print('{}转换完毕！'.format(word_path))
        wd.Quit()
    except Exception as e:
        print('转换异常，异常值是{}'.format(e))
    finally:
        print('')



def covert_word2pdf_Linux(word_path):
    """将word 转换为pdf
    函数说明:将路径为infile的word文件转换为pdf,保存进路径为outfile的pdf文件.
    参数: outfile(str):保存文件pdf 的路径.
    参数: infile(str):word文件的路径.
    参数: timeout:转换文件时的时间延迟.
    """
    pdf_path=os.path.abspath(os.path.join(word_path, os.path.pardir))
    pdffile=os.path.join(pdf_path,word_path.split('/')[-1].replace('.docx','.pdf'))
    if os.path.exists(pdffile):
        os.remove(pdffile)
    args = ['libreoffice', '--headless', '--convert-to', 'pdf', '--outdir', pdf_path, word_path]
    process = subprocess.run(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=None)


#*****************************************案例库*********************************************************************
@app.route('/example', methods=['POST', 'GET'])
def example():
    # rows = accident_select("无", "无", "无")
    # print(rows)
    rows = []
    return render_template('example1.html',
                           rows=rows)

@app.route('/example_select', methods=['POST', 'GET'])
def example_select():
    story_name = str(request.values["story_name"])
    condition_province = str(request.values["condition_province"])
    condition_cls = str(request.values["condition_cls"])
    condition_degree = str(request.values["condition_degree"])
    # if story_name == "" and condition_province == "" and condition_cls == "" and condition_degree == "":
    #     rows = []
    # else:
    #     rows = accident_select(story_name, condition_province, condition_cls, condition_degree)
    # return render_template('example1.html',
    #                        rows=rows)
    results=accident_select(story_name, condition_province, condition_cls, condition_degree)
    results = list(results)
    cls1 =[i[1] for i in results]
    cls2 =[i[2] for i in results]
    cls3 =[i[3] for i in results]
    cls6 = [i[6] for i in results]
    cls7 = [i[7] for i in results]
    cls8 = [i[8] for i in results]
    cls9 = [i[9] for i in results]
    cls10 = [i[10] for i in results]
    cls11 = [i[11] for i in results]
    cls12 = [i[12] for i in results]
    a={"cls1":cls1,"cls2":cls2,"cls3":cls3,"cls6":cls6,"cls7":cls7,"cls8":cls8,"cls9":cls9,"cls10":cls10,"cls11":cls11,"cls12":cls12}
    return a

def accident_select(story_name, condition_province, condition_cls, condition_degree):
    args0 = []
    # 打开数据库连接
    # db = pymysql.Connect(host='localhost', port=3306, user='root', passwd='123456', db='company', charset='utf8')
    db = pymysql.Connect(host='47.97.117.208', port=3306, user='root', passwd='haoyuanjie', db='mysql', charset='utf8')
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
            args.append("../static/example/"+id+".pdf")
            args.append(i+1)

            args0.append(args)
    except:
        print("Error: unable to fecth data")
    # 关闭数据库连接
    db.close()
    return args0


if __name__ == '__main__':
    app.run( host='0.0.0.0',port= 5000,debug=True)
    # app.run(host='47.97.117.208', port=5000, debug=True)
    # select_goodsrequireTask_Forme()
