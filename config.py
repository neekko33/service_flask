import pymysql

DB_CONFIG = {
    "user": "",
    "password": "",
    "port": 3306,
    "database": "",
    "host": "",
    "charset": "utf8",
}


class SQLManager(object):
    # 初始化实例方法
    def __init__(self):
        self.conn = None
        self.cursor = None
        self.connect()

    # 链接数据库
    def connect(self):
        self.conn = pymysql.connect(
            host=DB_CONFIG["host"],
            port=DB_CONFIG["port"],
            user=DB_CONFIG["user"],
            passwd=DB_CONFIG["password"],
            db=DB_CONFIG["database"],
            charset=DB_CONFIG["charset"],
        )
        self.cursor = self.conn.cursor(cursor=pymysql.cursors.DictCursor)

    # 查询多条数据
    def get_list(self, sql, args=None):
        self.cursor.execute(sql, args)
        result = self.cursor.fetchall()
        return result

    # 查询单条数据
    def get_one(self, sql, args=None):
        self.cursor.execute(sql, args)
        result = self.cursor.fetchone()
        return result

    # 执行单条sql语句
    def modify(self, sql, args=None):
        self.cursor.execute(sql, args)
        result = self.conn.commit()
        return result

    # 执行多条sql语句
    def multi_modify(self, sql, args=None):
        self.cursor.executemany(sql, args)
        result = self.conn.commit()
        return result

    # 创建单条记录
    def create(self, sql, args=None):
        self.cursor.execute(sql, args)
        self.conn.commit()
        last_id = self.cursor.lastrowid
        return last_id

    # 关闭数据库cursor和链接
    def close(self):
        self.cursor.close()
        self.conn.close()

    # 实现 with 语句的自动关闭
    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
