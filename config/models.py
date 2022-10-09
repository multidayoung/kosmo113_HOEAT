import cx_Oracle as ora


class Conn_Ora:
    def myconn(self):
        conn = ora.connect('hoeat113/hoeat113@192.168.0.11/xe')
        return conn


class rankinOraMain(Conn_Ora):
    def mainRank(self):
        conn = self.myconn()
        cursor = conn.cursor()
        query = """
        select rownum, c.* from(
        select
        * from (
        select row_number() over(
        order by a.bhit desc) as ranking, 
        a.btitle, a.bimg, a.bcate, a.bnum from board a
        )
        union all
        select 
        * from (
        select row_number() over(
        partition by a.bcate
        order by a.bhit desc) as ranking, 
        a.btitle, a.bimg, a.bcate, a.bnum from board a
        )
        ) c
        where ranking <= 20
        """
        cursor.execute(query)
        res = cursor.fetchall()
        cursor.close()
        conn.close()
        return res

