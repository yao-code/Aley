import pymysql
import re

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


str_1 = "<ChJUaGVzaXNOZXdTMjAyMDEwMjgSCFkyNzkxNTQ1GghtNmp3bG52cw%3D%3D��"
str_2 = """Thesis��ghttp://new.istic.wanfangdata.com.cn/Search/IsticDeliver?datasource=DiscernDetail&db=4&uniqueId=Y2018120ISTIC"ISTIC*,fG87SiQYMrpWLtn41iccf2YcgEShplfHFqWRltk33FA=<ChJUaGVzaXNOZXdTMjAyMDEwMjgSCFkyMDE4MTIwGggyNGtkM24zMg%3D%3D��"""
pattern = r"ChJUaG[A-Za-z0-9%]+"
res1 = re.findall(pattern, str_1)
res2 = re.findall(pattern, str_2)
# print(res1)
# print(res2)

