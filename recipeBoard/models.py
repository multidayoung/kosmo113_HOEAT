# from ckeditor.fields import RichTextField
import cx_Oracle
from django.db import models

# Create your models here.

from django.db import models

# Create your models here.
from config.models import Conn_Ora


class RecipeBoard(models.Model):
    bnum = models.AutoField(primary_key=True)
    mid = models.CharField(max_length=100,blank=True,null=False)
    btitle = models.CharField(max_length=255,blank=True,null=False)
    bcont = models.TextField(blank=True, null=False)
    bimg = models.CharField(max_length=255,blank=True,null=False)
    bingredient = models.TextField(blank=True, null=False)  # 길이 제한 없는 문자열
    bhit = models.IntegerField()
    bcate = models.CharField(max_length=100, blank=True, null=False)
    bdate = models.DateTimeField('date published') # p.120

class Recipe_Board(Conn_Ora):
    def listBoard(self):
        conn = Conn_Ora().myconn()
        cursor = conn.cursor()
        sql = "select bnum, btitle, mid, bimg, bhit from board order by 1 desc"
        cursor.execute(sql)
        listv = cursor.fetchall()
        cursor.close()
        conn.close()
        return listv

    def searchBoard(self, type, value):
        conn = Conn_Ora().myconn()
        cursor = conn.cursor()
        value = '%' + value + '%'
        sql = f"select bnum, btitle, mid, bimg, bhit from board where {type} like \'{value}\' order by 1 desc"
        cursor.execute(sql)
        print('-------------------------', value)
        searchv = cursor.fetchall()
        cursor.close()
        conn.close()
        return searchv

    # query = """
    #         select rownum, a.* from (
    #         select btitle, mid,
    #         case when bhit >= 10000 then round(bhit/10000,1)||'만'
    #         else to_char(bhit) end as bhit2,
    #         bimg, bcate, bnum
    #         from board where bcate like :value order by bhit desc) a where rownum <= 100
    #         """
    # cursor.execute(query, value='%' + cate + '%')

    def countBoard(self, type, value):
        conn = Conn_Ora().myconn()
        cursor = conn.cursor()
        value = '%'+value+'%'
        print(f"type : {type}")
        print(f"value : {value}")
        #values = (type, '%'+value+'%')
        sql = f"select count(*) from board where {type} like \'{value}\' order by 1 desc"
        cursor.execute(sql)
        countv = cursor.fetchone()
        print(f'countv : {countv}')
        cursor.close()
        conn.close()
        return countv

    def writeBoard(self, **kwargs):
        conn = Conn_Ora().myconn()
        cursor = conn.cursor()
        sql = "insert into board values(board_seq.nextVal, :mid, :btitle, :bcont, :bimg, :bingredient, 0, :bcate, sysdate)"
        cursor.execute(sql, **kwargs)
        cursor.close()
        conn.commit()
        conn.close()

    def detailBoard(self, bnum):
        conn = Conn_Ora().myconn()
        cursor = conn.cursor()
        sql = "select bnum, mid, btitle, bcont, bimg, bingredient, bhit, bcate, bdate from board where bnum=:bnum"
        cursor.execute(sql, bnum=bnum)
        detailv = cursor.fetchone()
        # cursor.close()
        # conn.close()
        return detailv

    def updateBoard(self, **kwargs):
        conn = Conn_Ora().myconn()
        cursor = conn.cursor()
        sql = "update board set btitle=:btitle, bcont=:bcont, bimg=:bimg, bingredient=:bingredient, bcate=:bcate where bnum=:bnum"
        cursor.execute(sql, **kwargs)
        cursor.close()
        conn.commit()
        conn.close()

    def deleteBoard(self, bnum):
        conn = Conn_Ora().myconn()
        cursor = conn.cursor()
        sql = "delete from board where bnum=:bnum"
        cursor.execute(sql, bnum=bnum)
        cursor.close()
        conn.commit()
        conn.close()

    def upHitBoard(self, bnum):
        conn = Conn_Ora().myconn()
        cursor = conn.cursor()
        sql = "update board set bhit = bhit+1 where bnum=:bnum"
        cursor.execute(sql, bnum=bnum)
        cursor.close()
        conn.commit()
        conn.close()

    def dateList(self,bdate,edate):
        conn = Conn_Ora().myconn()
        cursor = conn.cursor()
        sql = f"select * from board where bdate between to_date(\'{bdate}\','YYYY-MM-DD') and to_date(\'{edate}\','YYYY-MM-DD')"
        cursor.execute(sql)
        datelist = cursor.fetchall()
        cursor.close()
        conn.close()
        return datelist

    def insertJim(self, **kwargs):
        conn = Conn_Ora().myconn()
        cursor = conn.cursor()
        sql = "insert into jjim values(jjim_seq.nextVal, :m_id, :b_num)"
        cursor.execute(sql, **kwargs)
        cursor.close()
        conn.commit()
        conn.close()

    def deleteJim(self, **kwargs):
        conn = Conn_Ora().myconn()
        cursor = conn.cursor()
        sql = "delete from jjim where mid = :m_id and bnum = :b_num"
        cursor.execute(sql, **kwargs)
        cursor.close()
        conn.commit()
        conn.close()

    def countAllJim(self, b_num):
        conn = Conn_Ora().myconn()
        cursor = conn.cursor()
        sql = "select count(*) from jjim where bnum = :b_num"
        cursor.execute(sql, b_num=b_num)
        countAllv = cursor.fetchone()
        cursor.close()
        conn.close()
        return countAllv

    def countJim(self, m_id):
        conn = Conn_Ora().myconn()
        cursor = conn.cursor()
        print("m_id++===================+>",m_id)
        sql = "select bnum from jjim where mid = :m_id"
        cursor.execute(sql, m_id=m_id)
        countvv = cursor.fetchall()
        print("countvvvvvvvvvvvvvvvvvvv",countvv)
        cursor.close()
        conn.close()
        return countvv







    def jjimSetting(self,m_id,b_num):
        conn = Conn_Ora().myconn()
        cursor = conn.cursor()
        out_ck = cursor.var(cx_Oracle.NUMBER)
        out_countl = cursor.var(cx_Oracle.NUMBER)
        cursor.callproc('pro_jjim1',[m_id,b_num,out_countl,out_ck])
        #sql = "BEGIN PRO_JJIM1(:1,:2,:3,:4); END;"
        #cursor.execute(sql,[m_id,b_num,out_countl,out_ck])
        execList = [out_countl.getvalue(),out_ck.getvalue()]
        print("out_countl=>",out_countl.getvalue())
        print("out_ck=>", out_ck.getvalue())
        cursor.close()
        conn.close()
        return execList



class RecipeBoardDao(Conn_Ora):
    # insert 메서드
    def commInsert(self, **kwargs):
        # insert
        # mid = request.POST['mid']
        # mid = 'xman1'
        # rscore = request.POST['rscore']
        # rcont = request.POST['rcont']
        sql_insert = "insert into review values(review_seq.nextVal, :mid, :bnum, :rscore, :rcont, sysdate)"
        # 입력받은 값과 sql 바인딩 처리
        # execute(sql, bind)
        conn = Conn_Ora().myconn()
        cursor = conn.cursor()  # 자바의 preparedstatement같은 느낌
        # cursor.execute(sql_insert, pwd=pwdv, writer=writerv, subject=subjectv, content=contentv)
        cursor.execute(sql_insert, **kwargs)  # executeUpdate()
        cursor.close()
        conn.commit()
        conn.close()

     # 댓글 출력 메서드
    def listComment(self, bnum):
        conn = self.myconn()
        cursor = conn.cursor()
        #print(cursor)
        sql_select = 'select rnum, mid, bnum, rscore, rcont, to_char(rdate, \'yyyy-mm-dd\') rdate from review where bnum=:bnum order by 1 desc'
        cursor.execute(sql_select, bnum=bnum)
        listv = cursor.fetchall()
        # cursor.close()
        # conn.close()
        return listv

    def updateComm(self, **kwargs):
        conn = Conn_Ora().myconn()
        cursor = conn.cursor()
        sql = "update review set rscore=:rscore, rcont=:rcont where rnum=:rnum"
        cursor.execute(sql, **kwargs)
        cursor.close()
        conn.commit()
        conn.close()

    def deleteBoard(self, rnum):
        conn = Conn_Ora().myconn()
        cursor = conn.cursor()
        sql = "delete from review where rnum=:rnum"
        cursor.execute(sql, rnum=rnum)
        cursor.close()
        conn.commit()
        conn.close()
