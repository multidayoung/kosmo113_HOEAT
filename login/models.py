from django.db import models
from config.models import Conn_Ora

# Create your models here.
class Conn_log(Conn_Ora):
    def loginPro(self,id,pwd):
        conn = self.myconn()
        cursor = conn.cursor()
        sql = 'select mid,mpwd,mname from member where mid=:id and mpwd=:pwd'
        cursor.execute(sql,id=id,pwd=pwd)
        res = cursor.fetchone()
        cursor.close()
        conn.close()
        return res

    def forgotId(self,name,email):
        conn = self.myconn()
        cursor = conn.cursor()
        sql = 'select mid from member where mname=:name and memail=:email'
        cursor.execute(sql,name=name,email=email)
        res = cursor.fetchone()
        cursor.close()
        conn.close()
        return res

    def changePwd(self,id,pwd):
        conn = self.myconn()
        cursor = conn.cursor()
        sql = 'update member set mpwd=:pwd where mid=:id'
        cursor.execute(sql,pwd=pwd,id=id)
        cursor.close()
        conn.commit()
        conn.close()

    def checkEmail(self,id):
        conn = self.myconn()
        cursor = conn.cursor()
        sql = 'select memail from member where mid=:id'
        cursor.execute(sql,id=id)
        res = cursor.fetchone()
        cursor.close()
        conn.close()
        return res

    def genderChart(self):
        conn = self.myconn()
        cursor = conn.cursor()
        sql = 'select count(*) from member group by mgender order by mgender asc'
        cursor.execute(sql)
        res = cursor.fetchall()
        cursor.close()
        conn.close()
        return res

    def idPwdCheck(self,mid,mpwd):
        conn = self.myconn()
        cursor = conn.cursor()
        sql = 'select count(*) from member where mid=:id and mpwd=:pwd'
        cursor.execute(sql,id=mid,pwd=mpwd)
        res = cursor.fetchone()
        cursor.close()
        conn.close()
        return res