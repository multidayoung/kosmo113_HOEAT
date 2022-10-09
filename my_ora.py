from django.db import models

# Create your models here.
from config.models import Conn_Ora


class rankinOra(Conn_Ora):
    def mainRank(self, cate):
        print(f"cate => {cate}")
        conn = self.myconn()
        cursor = conn.cursor()
        query = """
        select rownum, a.* from (
        select btitle, mid, 
        case when bhit >= 10000 then round(bhit/10000,1)||'만' 
        else to_char(bhit) end as bhit2, 
        bimg, bcate 
        from board where bcate like :value order by bhit desc) a where rownum <= 100
        """
        cursor.execute(query, value='%' + cate + '%')
        res = cursor.fetchall()
        cursor.close()
        conn.close()
        return res

def getMainRank(cate):
    print(f"first cate => {cate}")
    if cate == 'total':
        arg = '식'
    elif cate == 'kor':
        arg = '한식'
    elif cate == 'west':
        arg = '양식'
    elif cate == 'chi':
        arg = '중식'
    elif cate == 'jap':
        arg = '일식'
    ref = rankinOra()
    res = ref.mainRank(arg)
    print('haha')
    for i in res:
        print(type(i))
        print(i[0])
        print(i[1])
        print(i[2])
        print(i[3])
        print(i[4])
        print("*"*30)

# plz = input('골라 => ')
# getMainRank(plz)