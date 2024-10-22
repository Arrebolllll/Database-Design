import psycopg2 as pg
import flask
from flask import request
from flask import Flask, make_response
import jsonify
import json
import hashlib


def generate_hash(data):
    hash_object = hashlib.sha256(data.encode())
    hashed_key = hash_object.hexdigest()
    return hashed_key[0:5]


# dsn="host=localhost port=5432 dbname=数据库实验课 user=postgres password=xxxxxxx sslmode=prefer connect_timeout=10"
conn = pg.connect(host="localhost", port=5432, dbname="final", user="postgres", password="123456", sslmode="prefer",
                  connect_timeout=10)
cur = conn.cursor()

# conn.close()#注意连接的事务提交和关闭


app = Flask(__name__)


@app.route('/insertsell', methods=['POST'])
def insertsell():
    # 需要传房间号，楼号，户型，电话，客户名，剩余期数
    """
    哈希计算公式：
    hashob=roomnumber+building+type
    rid=generate_hash(hashob)#
    hashob=telephone+cname
    cid=generate_hash(hashob)#
    sid=generate_hash(cid+rid)
    """
    """
    测试样例，此处除了remain是int型其他都需套单引号，在转为sql里已有
    {
    "roomnumber":"'143'",
    "building":"'a'",
    "type":"'B'",
    "telephone":"'707322'",
    "cname":"'bkg'",
    "remain":"12"
    }
    """
    try:
        # 事务自动回退格式
        val = request.get_json()  # val.get('(key)')得到一个字符串，用f字符串解析生成sql语句
        # print(val)
        ridhash = str(val.get("roomnumber")) + str(val.get("building")) + str(val.get("type"))
        print(ridhash)
        rid = generate_hash(ridhash)
        cidhash = str(val.get("telephone")) + val.get("cname")
        print(cidhash)
        cid = generate_hash(cidhash)
        sid = generate_hash(rid + cid)
        sql = f"insert into sell_info values ('{sid}','{cid}','{rid}',{val.get('remain')})"
        print(sql)
        cur.execute(sql)
        conn.commit()
        # Return success message to the frontend
        response = {"status": "success", "message": "Data successfully inserted"}
        return json.dumps(response)
    except Exception as e:
        print(f"Error: {e}")
        # conn.rollback()

        # Return error message to the frontend
        response = {"status": "error", "message": f"Error: {e}"}
        return make_response(json.dumps(response), 500)


@app.route('/insert', methods=['POST'])
def insert():
    """
    用于向数据库插入数据的端点。
    负载示例：
    {
        "table": "room_info",
        "values": ["'e'", 6, "'61'", 98, 98, "'B'"]
    }
    """
    try:
        # 从请求中获取JSON数据
        val = request.get_json()

        # 根据表类型生成哈希对象
        hash_object = ""
        if val.get('table') == "custom_info":
            hash_object = str(val.get('values')[1]) + val.get('values')[0]  # hash_object = telephone + cname
        elif val.get('table') == "room_info":
            hash_object = str(val.get('values')[2]) + str(val.get('values')[0]) + str(
                val.get('values')[-1])  # hash_object = roomnumber + building + type
        print(hash_object)
        # 使用哈希对象生成ID
        id = generate_hash(hash_object)

        # 构建插入字符串
        insert_str = f"('{id}',"
        for value in val.get('values'):
            insert_str += str(value) + ","
        insert_str = insert_str[:-1] + ')'  # 删除尾随逗号并添加闭括号

        # 构建SQL查询
        sql = f"INSERT INTO {val.get('table')} VALUES {insert_str}"

        # 执行查询并提交更改
        cur.execute(sql)
        conn.commit()

        # 返回成功消息给前端
        response = {"status": "success", "message": "数据成功插入"}
        return json.dumps(response)

    except Exception as e:
        print(f"错误: {e}")
        conn.rollback()

        # 返回错误消息给前端
        response = {"status": "error", "message": f"错误: {e}"}
        return make_response(json.dumps(response), 500)


@app.route('/update', methods=['POST'])
def update():
    # 需要三段分为 update 后接表名，set 后面接一个两个元素的列表，where 后面接两个元素的列表，列表里两项分别为属性和值
    """
    {
        "table": "custom_info",
        "set": ["cname", "'zsr'"],
        "where": ["cid", "'1'"]
    }
    """
    try:
        val = request.get_json()  # update students set grade='2001' where sid='21307283'
        setlist = val.get('set')
        set_string = ""
        for i in range(0, len(setlist), 2):
            set_string += setlist[i]
            i += 1
            set_string += '=' + str(setlist[i]) + ','

        set_string = set_string[0:-1]  # 删除末尾逗号

        sql = f"update {val.get('table')} set {set_string} where {val.get('where')[0]}={val.get('where')[1]}"
        cur.execute(sql)
        conn.commit()
        response = {"status": "success", "message": "Data successfully updated"}
        return json.dumps(response)
    except Exception as e:
        print(f"Error: {e}")
        conn.rollback()

        # Return error message to the frontend
        response = {"status": "error", "message": f"Error: {e}"}
        return make_response(json.dumps(response), 500)



@app.route('/selectsell', methods=['GET'])
def selectsell():
    # 新加的函数，负责传回多个id对应的列表便于展示
    try:  # 顺序按sql语句所示
        sql = """select building,floor,room_number,area,total_price,type,remain,cname,telephone,sex,age,sid 
        from room_info 
        inner join sell_info on room_info.rid=sell_info.rid 
        inner join custom_info  on custom_info.cid=sell_info.cid
        """
        cur.execute(sql)
        data = cur.fetchall()
        conn.commit()
        return json.dumps(data)
    except Exception as e:
        print(f"Error: {e}")
        conn.rollback()

        # Return error message to the frontend
        response = {"status": "error", "message": f"Error: {e}"}
        return make_response(json.dumps(response), 500)


@app.route('/selectstar', methods=['POST'])
def selectstar():
    # 传回某个表的全部列
    try:  # select key1,key2* from table
        val = request.get_json()
        sql = f"select * from {val.get('table')} "
        cur.execute(sql)
        data = cur.fetchall()
        conn.commit()
        return json.dumps(data)
    except Exception as e:
        print(f"Error: {e}")
        conn.rollback()
        # Return error message to the frontend
        response = {"status": "error", "message": f"Error: {e}"}
        return make_response(json.dumps(response), 500)


@app.route('/select', methods=['POST'])
def select():
    # 传入tablename select和where参数对应两个列表{'select':['key1','key2'...],'table':'table','where':[key1,val1,key2,val2]}
    #                                                  其中key表示属性名，val表示输入的参数值，返回两层列表
    """
    {
    "table":"custom_info",
    "select":["cname","cid"],
    "where":["sex","'male'","telephon","'12'"]
    }
    """
    try:  # select key1,key2 from table where key1= val1
        val = request.get_json()
        select_string = ""
        for key in val.get('select'):
            select_string += str(key) + ','
        select_string = select_string[0:-1]
        where_string = ""
        wherelist = val.get('where')
        for i in range(0, len(wherelist), 2):
            where_string += wherelist[i]
            i += 1
            where_string += '=' + str(wherelist[i]) + ' and '
        where_string = where_string[0:-4]  # 删除末尾and
        sql = f"select {select_string} from {val.get('table')} where {where_string}"
        # print(sql)
        cur.execute(sql)
        data = cur.fetchall()
        conn.commit()
        return json.dumps(data)
    except Exception as e:
        print(f"Error: {e}")
        conn.rollback()

        # Return error message to the frontend
        response = {"status": "error", "message": f"Error: {e}"}
        return make_response(json.dumps(response), 500)


@app.route('/selectrange', methods=['POST'])
def selectrange():
    # 先小后大,传入字典对应个列表{'select':['key1','key2'...],'table':'table','where':[key1,val1,val2]}
    # where后的val1是小的参数，val2是大的参数，返回val1~val2间的属性列
    """
    {
    "table":"room_info",
    "select":["*"],
    "where":["floor",1,3]#floor这里是int型，是为了比较大小
    }
    """
    try:  # 事务自动回退格式
        val = request.get_json()  # select key1,key2 from table where key1>90 and <100
        select_string = ""
        for key in val.get('select'):
            select_string += str(key) + ','
        select_string = select_string[0:-1]
        where_string = ""
        wherelist = val.get('where')

        where_string = f"{wherelist[0]}>={wherelist[1]} and {wherelist[0]}<={wherelist[2]}"
        sql = f"select {select_string} from {val.get('table')} where {where_string}"
        print('筛选sql', sql)
        cur.execute(sql)
        data = cur.fetchall()
        conn.commit()
        return json.dumps(data)
    except Exception as e:
        print(f"Error: {e}")
        conn.rollback()
        # Return error message to the frontend
        response = {"status": "error", "message": f"Error: {e}"}
        return make_response(json.dumps(response), 500)


@app.route('/delete', methods=['POST'])
def delete():
    # 删除行，传入tablename和条件判断"where"：["cid","'1'"]
    """
    {
    "table":"custom_info",
    "where":["cid","'1'"]
    }
    """
    try:  # delete from table where key1=val1
        val = request.get_json()

        where_string = ""
        wherelist = val.get('where')

        for i in range(0, len(wherelist), 2):
            where_string += wherelist[i]
            i += 1
            where_string += '=' + wherelist[i]

        sql = f"delete from {val.get('table')} where {where_string} "

        cur.execute(sql)
        response = {"status": "success", "message": "Data successfully deleted"}
        conn.commit()
        return json.dumps(response)
    except Exception as e:
        print(f"Error: {e}")
        conn.rollback()

        # Return error message to the frontend
        response = {"status": "error", "message": f"Error: {e}"}
        return make_response(json.dumps(response), 500)


@app.route('/selled_static', methods=['POST'])
def selled_static():
    # 销售信息的统计，sum，count，max，min，avg,'where':[key1,val1,key2,val2]}
    # 这个函数只计算已经卖出的房屋的价钱，此外可以增加where条件来缩小筛查范围
    """
    {
    "method":"sum",
    "where":["floor",1]
    }
    """
    try:
        val = request.get_json()
        where_string = ""
        wherelist = val.get('where')
        for i in range(0, len(wherelist), 2):
            where_string += wherelist[i]
            where_string += '=' + str(wherelist[i + 1])
        if len(wherelist) > 0:  # 如果没条件则不加and
            where_string = 'and ' + where_string
        sql = f"select {val.get('method')}(total_price) from room_info where rid in (select rid from sell_info) {where_string}"
        print(sql)
        cur.execute(sql)
        data = cur.fetchall()
        conn.commit()
        return json.dumps(data)
    except Exception as e:
        print(f"Error: {e}")
        conn.rollback()
        # Return error message to the frontend
        response = {"status": "error", "message": f"Error: {e}"}
        return make_response(json.dumps(response), 500)


@app.route('/statistic', methods=['POST'])
def statistic():
    # 信息的统计，不止sell表  传入method：sum，count，max，min，avg, 表名，select的键值，where条件判断同前
    """
    {   
    "method":"sum",
    "table":"room_info",
    "select":"floor",#因为聚合函数只有一个参数，所以不用列表传参
    "where":["area","'1'","type","'14'"]
    }
    """
    try:
        val = request.get_json()
        where_string = ""
        wherelist = val.get('where')
        for i in range(0, len(wherelist), 2):
            where_string += wherelist[i]
            i += 1
            where_string += '=' + str(wherelist[i]) + '  and '
        where_string = where_string[0:-4]  # 删除末尾and
        sql = f"select {val.get('method')}({val.get('select')}) from {val.get('table')} where {where_string}"
        print(sql)
        cur.execute(sql)
        data = cur.fetchall()
        conn.commit()
        return json.dumps(data)
    except Exception as e:
        print(f"Error: {e}")
        conn.rollback()
        # Return error message to the frontend
        response = {"status": "error", "message": f"Error: {e}"}
        return make_response(json.dumps(response), 500)


app.run(debug=True)
