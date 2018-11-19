import pymysql
from queue import Queue

class ConnPool:

    __instance = None

    def __init__(self,host=None,port=None,user=None,passwd=None,db=None,charset=None,maxconn=5):
        self.host,self.port,self.user,self.passwd,self.db,self.charset=host,port,user,passwd,db,charset
        self.maxconn = maxconn
        self.pool = Queue(maxconn)
        for i in range(maxconn):
            try:
                conn = pymysql.connect(host=self.host, port=self.port, user=self.user, passwd=self.passwd, db=self.db, charset=self.charset)
                conn.autocommit(True)
                self.pool.put(conn)
            except Exception as e:
                raise IOError(e)

    @classmethod
    def get_instance(cls, *args, **kwargs):
        if cls.__instance:
            return cls.__instance
        else:
            cls.__instance = ConnPool(*args, **kwargs)
            return cls.__instance

    def exec_sql(self, sql, operation=None):
        '''
        执行没有返回结果的sql
        '''
        try:
            conn = self.pool.get()
            cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
            response = cursor.execute(sql,operation) if operation else cursor.execute(sql)
        except Exception as e:
            print(e)
            cursor.close()
            self.pool.put(conn)
            return None
        else:
            cursor.close()
            self.pool.put(conn)
            return response

    def exec_sql_feach(self, sql, operation=None):
        '''
        执行有返回结果的sql,select
        '''
        try:
            conn=self.pool.get()
            cursor=conn.cursor(cursor=pymysql.cursors.DictCursor)
            response=cursor.execute(sql,operation) if operation else cursor.execute(sql)
        except Exception as e:
            print(e)
            cursor.close()
            self.pool.put(conn)
            return None,None
        else:
            result = cursor.fetchall()
            cursor.close()
            self.pool.put(conn)
            return response,result

    def check(self):
        for i in range(self.maxconn):
            try:
                conn = self.pool.get()
                if conn.ping():
                    self.pool.put(conn)
                else:
                    conn = pymysql.connect(host=self.host, port=self.port, user=self.user, passwd=self.passwd, db=self.db, charset=self.charset)
                    conn.autocommit(True)
                    self.pool.put(conn)
            except Exception as e:
                print(e)
                return None
            else:
                return True

    def close(self):
        for i in range(self.maxconn):
            self.pool.get().close()

sqlconn = ConnPool.get_instance(host='123.206.95.123', port=3306, user='root', passwd='Nkx.29083X', db='blog', charset='utf8', maxconn=10)