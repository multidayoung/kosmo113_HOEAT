from django.db import models
from config.models import Conn_Ora

class MemberDao(Conn_Ora):
    def memberinsert(self, memberlist):
        conn = self.myconn()
        cursor = conn.cursor()
        sql = "insert into member values(:1,:2,:3,:4,:5,:6,:7)"
        cursor.execute(sql, memberlist)
        cursor.close()
        conn.commit()
        conn.close()

    def idcheck(self, idx):
        conn = self.myconn()
        cursor = conn.cursor()
        if(idx == ''):
            return '2'
        else:
            sql = "select count(*) from member where mid=:mid"
            cursor.execute(sql,mid=idx)
            res = cursor.fetchone()
            cursor.close()
            conn.close()
            return res

    def joinLog(self):
        conn = self.myconn()
        cursor = conn.cursor()
        sql = "select mdate, count(*) from member group by mdate order by mdate"
        cursor.execute(sql)
        res = cursor.fetchall()
        cursor.close()
        conn.close()
        return res
