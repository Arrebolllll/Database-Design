import psycopg2 as pg
import flask
from flask import request
from flask import Flask
import jsonify
import json
# dsn="host=localhost port=5432 dbname=数据库实验课 user=postgres password=xxxxxxx sslmode=prefer connect_timeout=10"
conn=pg.connect(host="localhost",port=5432,dbname="final",user="postgres",password="123",sslmode="prefer", connect_timeout=10 )
cur=conn.cursor()
cur.execute("create table  if not exists room_info(rid varchar(5) primary key,floor int ,area varchar(10),type varchar(2),price_single varchar(10),total_price varchar(10),locate varchar(10))")
cur.execute("create table  if not exists custom_info(cid varchar(5) primary key,cname varchar(5),telephon varchar(15),sex varchar(6),card_id varchar(20))")#尽量封装为函数通过模块调用

cur.execute("create table  if not exists sell_info(rid varchar(5) primary key references room_info(rid),cid varchar(5) references custom_info(cid),loan_month int,if_full varchar(3))")#尽量封装为函数通过模块调用

conn.commit()
# conn.close()#注意连接的事务提交和关闭


app=Flask(__name__)

@app.route('/insert',methods=['POST'])
def insert():#传{"table":'table'}
    """
    {
    "table":"custom_info",
    "1":"1",
    "2":"2",
    "3":12,
    "4":"'yes'",#传字符串进来要两个引号
    "5":"12"
}"""
    try:#事务自动回退格式
        val=request.get_json()#val.get('(key)')得到一个字符串，用f字符串解析生成sql语句
        print(val)
        insertstr="("
        for key,value in val.items():
            if key!="table":
                insertstr+=str(value)+","
        insertstr=insertstr[:-1]+')'#删逗号加括号，便于插入
        sql=f"insert into {val.get('table')} values {insertstr}"
        cur.execute(sql)
        conn.commit()
        # Return success message to the frontend
        response = {"status": "success", "message": "Data successfully inserted"}
        return json.dumps(response)


    except Exception as e:
        print(f"Error: {e}")
        conn.rollback()

        # Return error message to the frontend
        response = {"status": "error", "message": f"Error: {e}"}
        return json.dumps(response)




@app.route('/update',methods=['POST'])
def update():#需要三段分为update后接表名，set后面接一个两个元素的列表，where后面接两个元素的列表，分别为属性和值
    """
    {
    "table":"custom_info",
    "set":["cname","'zsr'"],
    "where":["cid","'1'"]
    }
    """
    try:
        val=request.get_json()#update students set grade='2001' where sid='21307283'
        sql=f"update {val.get('table')} set {val.get('set')[0]}={val.get('set')[1]} where {val.get('where')[0]}={val.get('where')[1]}"
        cur.execute(sql)
        conn.commit()
        response = {"status": "success", "message": "Data successfully updated"}
        return json.dumps(response)
    except Exception as e:
        print(f"Error: {e}")
        conn.rollback()

        # Return error message to the frontend
        response = {"status": "error", "message": f"Error: {e}"}
        return json.dumps(response)

@app.route('/selectstar',methods=['POST'])
def selectstar():#
    try:#select key1,key2* from table 
        val=request.get_json()
        sql=f"select * from {val.get('table')} "
        cur.execute(sql)
        data=cur.fetchall()
        conn.commit()
        return json.dumps(data)
        
    except Exception as e:
        print(f"Error: {e}")
        conn.rollback()

        # Return error message to the frontend
        response = {"status": "error", "message": f"Error: {e}"}
        return json.dumps(response)

@app.route('/select',methods=['POST'])
def select():#多属性同时查则靠循环增加字符串,传入字典对应个列表{'select':['key1','key2'...],'table':'table','where':[key1,val1,key2,val2]}
    """
    {
    "table":"custom_info",
    "select":["cname","cid"],
    "where":["sex","'male'","telephon","'12'"]
    }
    """
    try:#select key1,key2 from table where key1=
            

        val=request.get_json()
        select_string=""
        for key in val.get('select'):
            select_string+=str(key)+','
        select_string=select_string[0:-1]
        where_string=""
        wherelist=val.get('where')
        for i in range(0,len(wherelist),2):
            where_string+=wherelist[i]
            i+=1
            where_string+='='+str(wherelist[i])+' and '
        where_string=where_string[0:-4]    #删除末尾and
        sql=f"select {select_string} from {val.get('table')} where {where_string}"
        # print(sql)
        cur.execute(sql)
        data=cur.fetchall()
        conn.commit()
        return json.dumps(data)


    except Exception as e:
        print(f"Error: {e}")
        conn.rollback()

        # Return error message to the frontend
        response = {"status": "error", "message": f"Error: {e}"}
        return json.dumps(response)


@app.route('/selectrange',methods=['POST'])
def selectrange():#先小后大,传入字典对应个列表{'select':['key1','key2'...],'table':'table','where':[key1,val1,val2]}
    """
    {
    "table":"room_info",
    "select":["*"],
    "where":["floor",1,3]#floor这里是int型，是为了比较大小
    }
    """
    try:#事务自动回退格式
        val=request.get_json()#select key1,key2 from table where key1>90 and <100
        select_string=""
        for key in val.get('select'):
            select_string+=str(key)+','
        select_string=select_string[0:-1]
        where_string=""
        wherelist=val.get('where')
        
        where_string=f"{wherelist[0]}>={wherelist[1]} and {wherelist[0]}<={wherelist[2]}"
        sql=f"select {select_string} from {val.get('table')} where {where_string}"
        cur.execute(sql)
        data=cur.fetchall()
        conn.commit()
        return json.dumps(data)
    except Exception as e:
        print(f"Error: {e}")
        conn.rollback()

        # Return error message to the frontend
        response = {"status": "error", "message": f"Error: {e}"}
        return json.dumps(response)



@app.route('/delete',methods=['POST'])
def delete():
    """
    {
    "table":"custom_info",
    "where":["cid","'1'"]
    }
    """
    try:#delete from table where key1=val1
        val=request.get_json()

        where_string=""
        wherelist=val.get('where')
        for i in range(0,len(wherelist),2):
            where_string+=wherelist[i]
            i+=1
            where_string+='='+wherelist[i]
        sql=f"delete from {val.get('table')} where {where_string} "
        # print(sql)
        cur.execute(sql)
        response = {"status": "success", "message": "Data successfully deleted"}
        conn.commit()
        return json.dumps(response)
    except Exception as e:
        print(f"Error: {e}")
        conn.rollback()

        # Return error message to the frontend
        response = {"status": "error", "message": f"Error: {e}"}
        return json.dumps(response)
    

@app.route('/selled_static',methods=['POST'])#这个函数只计算已经卖出的房屋的价钱，此外可以增加where条件来缩小筛查范围
def selled_static():#销售信息的统计，sum，count，max，min，avg,'where':[key1,val1,key2,val2]}
    """
    {
    "method":"sum",
    "where":["floor",1]
    }
    """
    try:
        val=request.get_json()
        where_string=""
        wherelist=val.get('where')
        for i in range(0,len(wherelist),2):
            where_string+=wherelist[i]
            where_string+='='+str(wherelist[i+1])
        if len(wherelist)>0:#如果没条件则不加and
            where_string='and '+where_string
        sql=f"select {val.get('method')}(floor) from room_info where rid in (select rid from sell_info) {where_string}"#floor记得改为total_price
        print(sql)
        cur.execute(sql)
        data=cur.fetchall()
        conn.commit()
        return json.dumps(data)


    except Exception as e:
        print(f"Error: {e}")
        conn.rollback()
        # Return error message to the frontend
        response = {"status": "error", "message": f"Error: {e}"}
        return json.dumps(response)



@app.route('/statistic',methods=['POST'])
def statistic():#销售信息的统计，sum，count，max，min，avg
    """
    {   
    "method":"sum",
    "table":"room_info",
    "select":"floor",#因为聚合函数只有一个参数，所以不用列表传参
    "where":["area","'1'","type","'14'"]
    }
    """
    try:
        val=request.get_json()
        where_string=""
        wherelist=val.get('where')
        for i in range(0,len(wherelist),2):
            where_string+=wherelist[i]
            i+=1
            where_string+='='+str(wherelist[i])+'  and '
        where_string=where_string[0:-4]    #删除末尾and
        sql=f"select {val.get('method')}({val.get('select')}) from {val.get('table')} where {where_string}"
        print(sql)
        cur.execute(sql)
        data=cur.fetchall()
        conn.commit()
        return json.dumps(data)


    except Exception as e:
        print(f"Error: {e}")
        conn.rollback()

        # Return error message to the frontend
        response = {"status": "error", "message": f"Error: {e}"}
        return json.dumps(response)

app.run(debug=True)
