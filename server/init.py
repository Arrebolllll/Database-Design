import psycopg2 as pg
import random
import hashlib


# 主键的生成
def generate_hash(data):
    hash_object = hashlib.sha256(data.encode())
    hashed_key = hash_object.hexdigest()
    return hashed_key[0:5]


if __name__ == "__main__":
    # 初始化，创建表，根据表改属性类型，循环随机插入一些数据
    conn = pg.connect(host="localhost", port=5432, dbname="final", user="postgres", password="123456", sslmode="prefer",
                      connect_timeout=10)
    cur = conn.cursor()
    cur.execute("""create table  if not exists room_info(
                rid varchar(5) primary key,
                building varchar(2),
                floor int,
                room_number varchar(3) ,
                area int,
                total_price int,
                type varchar(2))""")

    cur.execute("""create table  if not exists custom_info(
                cid varchar(5) primary key,
                cname varchar(5),
                telephone varchar(15),
                sex varchar(6),
                age int)""")  # 尽量封装为函数通过模块调用

    cur.execute("""create table  if not exists sell_info(
                sid varchar(5) primary key,
                cid varchar(5) references custom_info(cid),
                rid varchar(5)  references room_info(rid),
                remain int)""")
    conn.commit()

    # 插入一些数据
    ridlist = []
    for i in range(1, 51):

        building = random.choice(['a', 'b', 'c', 'd', 'e'])
        floor = random.randint(1, 17)

        room = random.randint(1, 5)

        roomnumber = str(floor) + str(room)  # 最后一位表示该层第几户，剩余表示楼层
        area = round(random.uniform(85, 100), 1)
        single = round(random.uniform(0.85, 1), 1)
        total_price = round(area * single, 1)
        type = random.choice(['A', 'B', 'C'])
        hashob = roomnumber + building + type
        rid = generate_hash(hashob)
        if rid in ridlist:
            i -= 1
            continue
        ridlist.append(rid)
        # print(f"insert room_info values('{rid}','{building}',{floor},'{roomnumber}',{area},{total_price},'{type}')")
        cur.execute(
            f"insert into room_info values('{rid}','{building}',{floor},'{roomnumber}',{area},{total_price},'{type}')")
    conn.commit()

    cidlist = []
    for i in range(1, 51):

        cname = ""
        for j in range(3):
            cname += random.choice(['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'w', 'z', 'o', 's', 'r'])
        telephone = str(random.randint(99999, 999999))
        sex = random.choice(['male', 'female'])
        age = random.randint(20, 50)
        hashob = telephone + cname
        cid = generate_hash(hashob)
        cidlist.append(cid)
        # print(f"insert custom_info values('{cid}','{cname}','{telephone}','{sex}',{age})")
        cur.execute(f"insert into custom_info values('{cid}','{cname}','{telephone}','{sex}',{age})")
    conn.commit()

    for i in range(1, 31):
        rid = ridlist[i]
        cid = cidlist[i + 1]
        remain = random.randint(0, 36)
        sid = generate_hash(cid + rid)
        # print(f"insert sell_info values('{sid}','{cid}','{rid}',{remain})")
        cur.execute(f"insert into sell_info values('{sid}','{cid}','{rid}',{remain})")
    conn.commit()
    conn.close()
