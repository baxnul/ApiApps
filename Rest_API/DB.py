import psycopg2


def get_db_connection():
    conn = psycopg2.connect(
        host='localhost',
        database='postgres',
        user='postgres',
        password='admin',
        port="5432"
    )
    return conn


def get_usr_list(active=True):
    conn = get_db_connection()
    cur = conn.cursor()
    if active:
        cur.execute("SELECT * FROM users_1 where active=True")
    else:
        cur.execute("SELECT * FROM users_1")
    users = cur.fetchall()
    cur.close()
    conn.close()
    res = []
    dic = {}
    for i in users:
        dic['id'] = i[0]
        dic['login'] = i[1]
        dic['password'] = i[2]
        dic['active'] = i[3]
        res.append(dic)
        dic = {}
    newlist = sorted(res, key=lambda d: d['id'])
    return newlist
