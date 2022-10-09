import cx_Oracle

from config.models import Conn_Ora

class SocketClass:
    guest=1987654

class OraModel(Conn_Ora):
    def __init__(self):
        pass
    def detail(self,mid):
        conn = self.myconn()
        cursor = conn.cursor()
        sql = "select * from member where mid=:mid"
        cursor.execute(sql,mid=mid)
        res = cursor.fetchone()
        cursor.close()
        conn.close()
        return res
    def jjimList(self,**kwargs):
        conn = self.myconn()
        cursor = conn.cursor()
        conn = self.myconn()
        cursor = conn.cursor()
        for key, val in kwargs.items():
            if key == 'mid':
                sql = "select b.*,r.* from board b,(select avg(nvl(rscore,0)) avg,jji.bnum from review r,(select bnum from jjim where mid=:mid) jji where r.bnum(+)=jji.bnum group by jji.bnum) r where b.bnum=r.bnum and b.btitle like :searchValue"
                mid = val
            elif val is None:
                sql = "select b.*,r.* from board b,(select avg(nvl(rscore,0)) avg,jji.bnum from review r,(select bnum from jjim where mid=:mid) jji where r.bnum(+)=jji.bnum group by jji.bnum) r where b.bnum=r.bnum"
                cursor.execute(sql, mid=mid)
            elif key == 'searchValue' and val is not None:
                cursor.execute(sql, **kwargs)
        res = cursor.fetchall()
        res2 = list()
        count=0
        for i in res:
            check=list()
            for j in i:
                if isinstance(j,cx_Oracle.LOB):
                    check.append(j.read())
                else:
                    check.append(j)
            res2.append(check)
            count+=1
        cursor.close()
        conn.close()
        return res2

    def review(self,select,**kwargs):
        conn = self.myconn()
        cursor = conn.cursor()
        if select=='myreview':
            for key, val in kwargs.items():
                if key == 'mid':
                    sql = "select rnum,mid,bnum,rscore,rcont,rdate from review where mid=:mid and rcont like :searchValue"
                    mid = val
                elif val is None:
                    sql = "select rnum,mid,bnum,rscore,rcont,rdate from review where mid=:mid"
                    cursor.execute(sql, mid=mid)
                elif key == 'searchValue' and val is not None:
                    cursor.execute(sql, **kwargs)
        else :
            for key, val in kwargs.items():
                if key == 'mid':
                    sql = "select mid,rnum,rscore,rcont,rdate from review where bnum in (select bnum from board where mid=:mid) and rcont like : searchValue"
                    mid = val
                elif val is None:
                    sql = "select mid,rnum,rscore,rcont,rdate from review where bnum in (select bnum from board where mid=:mid)"
                    cursor.execute(sql, mid=mid)
                elif key == 'searchValue' and val is not None:
                    cursor.execute(sql, **kwargs)
        res = cursor.fetchall()
        res2 = list()
        count=0

        for i in res:
            check=list()
            for j in i:
                if isinstance(j,cx_Oracle.LOB):
                    check.append(j.read())
                else:
                    check.append(j)
            res2.append(check)
            count+=1
        cursor.close()
        conn.close()
        return res2
    def recipe(self,**kwargs):
        conn = self.myconn()
        cursor = conn.cursor()
        for key,val in kwargs.items():
            if key=='mid':
                sql = "select * from board where mid=:mid and btitle like :searchValue"
                mid=val
            elif val is None:
                sql = "select * from board where mid=:mid"
                cursor.execute(sql,mid=mid)
            elif key=='searchValue' and val is not None:
                cursor.execute(sql, **kwargs)
        res = cursor.fetchall()
        cursor.close()
        conn.close()
        return res
    def staylog(self,member,time,sdate):
        conn = self.myconn()
        cursor = conn.cursor()
        sql = "insert into staylog values(staylog_seq.nextVal,:member,:time,:sdate)"
        cursor.execute(sql, member=member,time=time,sdate=sdate)
        conn.commit()
        cursor.close()
        conn.close()
        pass
    def movepage(self,member,movetime,sdate):
        conn = self.myconn()
        cursor = conn.cursor()
        sql = "insert into movelog values(movelog_seq.nextVal,:member,:movetime,:sdate)"
        cursor.execute(sql, member=member,movetime=movetime,sdate=sdate)
        conn.commit()
        cursor.close()
        conn.close()
        pass
    def stayList(self,sdate):
        conn = self.myconn()
        cursor = conn.cursor()
        sql = "select count(case when staytime>1 and staytime<11 then 1 end) a,count(case when staytime>10 and staytime<31 then 1 end) b, count(case when staytime>30 and staytime<61 then 1 end) c,count(case when staytime>60 then 1 end) d from staylog where sdate=to_date(:sdate,'yy-mm-dd')"
        cursor.execute(sql,sdate=sdate)
        res = cursor.fetchall()
        cursor.close()
        conn.close()
        return res
    def staylogDate(self):
        conn = self.myconn()
        cursor = conn.cursor()
        sql = "select rownum,sdate from (select distinct(sdate) from staylog order by 1 asc) where rownum<5 "
        cursor.execute(sql)
        res = cursor.fetchall()
        cursor.close()
        conn.close()
        return res
    def movelogList(self):
        conn = self.myconn()
        cursor = conn.cursor()
        sql = "select ceil(avg(movetime)) avg from movelog group by mdate"
        cursor.execute(sql)
        res = cursor.fetchall()
        cursor.close()
        conn.close()
        return res
    def getPwd(self,mid):
        conn = self.myconn()
        cursor = conn.cursor()
        sql = "select mpwd from member where mid=:mid"
        cursor.execute(sql,mid=mid)
        res = cursor.fetchone()
        cursor.close()
        conn.close()
        return res
    def dropMember(self,mid):
        conn = self.myconn()
        cursor = conn.cursor()
        sql = "delete from member where mid=:mid"
        cursor.execute(sql,mid=mid)
        conn.commit()
        cursor.close()
        conn.close()
        pass
    def updateMember(self,**kwargs):
        conn = self.myconn()
        cursor = conn.cursor()
        sql = "update member set mname=:mname,mbirth=:mbirth,memail=:memail where mid=:mid"
        cursor.execute(sql,**kwargs)
        conn.commit()
        cursor.close()
        conn.close()
        pass