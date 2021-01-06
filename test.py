import pymysql

CONNECT_INFO = {
    "host": "127.0.0.1",
    "user": "root",
    "password": "ale.123",
    "database": "aley",
    "port": 3306,
}

class MYSQL_CON():
    def __init__(self):
        flag = 0
        while flag <= 3:
            try:
                self.con = pymysql.Connect(**CONNECT_INFO)
                flag = 999
            except:
                flag += 1
                print("reconnect...")
            finally:
                if flag < 4:
                    print("connect failed {}".format(flag))
                else:
                    print("connect success")
        self.cursor = self.con.cursor()


    def close(self):
        self.con.commit()
        self.cursor.close()
        self.con.close()