from datetime import datetime


from django.db import models

# Create your models here.
from django.db.models import Count, Window
from django.db.models.functions import RowNumber

from config.models import Conn_Ora
from konlpy.tag import Okt # 한국어 형태소 분석해서 명사만 추출 해준다.

class SearchedData(models.Model):
    sidx = models.AutoField(primary_key=True)
    sType = models.CharField(max_length=100, blank=True, null=False)
    snouns = models.CharField(max_length=100, blank=True, null=False)
    sdate = models.DateTimeField('date published')

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
        bimg, bcate, bnum 
        from board where bcate like :value order by bhit desc) a where rownum <= 100
        """
        cursor.execute(query, value='%' + cate + '%')
        res = cursor.fetchall()
        cursor.close()
        conn.close()
        return res

class searchData:
    def searchToDb(self, sType, sValue):
        if len(sValue) > 0:
            okt = Okt()
            nouns = okt.nouns(sValue)
            print(f"nouns.count: {len(nouns)}")
            if len(nouns) < 1:
                noun = sValue
                print(f"noun: {noun}")
                sdb = SearchedData(sType=sType, snouns=noun, sdate=datetime.now())
                sdb.save()
            else:
                print(f"nouns: {nouns}")
                for i in nouns:
                    sdb = SearchedData(sType=sType, snouns=i, sdate=datetime.now())
                    sdb.save()
        # getIn = []
        # for i in nouns:
        #     getIn = zip(sType,i)
        # for i in getIn:
        # print(f"getIn : {i}") # raw로 넣으려 했다가 포기함 위에가 더 깔끔하고 반복하는 거는 똑같아서
        # SearchedData.objects.raw("""
        # insert into ranking_searcheddata (sType, snouns, sdate) values(:1, :2, datetime('now','localtime'));
        # """, getIn)
    def getSDBRank(self, sType):
        sType = '%'+sType+'%'
        print("sType:", sType)
        sValues = SearchedData.objects.raw(f"""
        select snouns, sType, count(*) as cnt, sidx from ranking_searcheddata where sType like \'{sType}\' group by snouns order by cnt desc
        """)
        # sValues = (SearchedData.objects.annotate(total_counts=Count('snouns')).order_by('total_counts').annotate(rank = Window(expression=RowNumber())))
        # for i in sValues:
        #     print(i.snouns, ' : ', i.cnt)
        return sValues

class GetChart(Conn_Ora):
    def cateHitAvgRanking(self):
        sql = """
        SELECT bcate, round(avg(bhit),2) AS avg_hit FROM board GROUP by bcate order by avg_hit desc
        """
        conn = self.myconn()
        cursor = conn.cursor()
        cursor.execute(sql)
        res = cursor.fetchall()
        cursor.close()
        conn.close()
        return res

    def cateHitSumRanking(self):
        sql = """
        SELECT bcate, sum(bhit) AS total_hit FROM board GROUP by bcate order by total_hit desc
        """
        conn = self.myconn()
        cursor = conn.cursor()
        cursor.execute(sql)
        res = cursor.fetchall()
        cursor.close()
        conn.close()
        return res


# def getMainRank(cate):
#     print(f"first cate => {cate}")
#     if cate == 'total':
#         arg = '식'
#     elif cate == 'kor':
#         arg = '한식'
#     elif cate == 'west':
#         arg = '양식'
#     elif cate == 'chi':
#         arg = '중식'
#     elif cate == 'jap':
#         arg = '일식'
#     ref = rankinOra()
#     res = ref.mainRank(arg)
#     # for i in res:
#     #     print(type(i))
#     #     print(i[0])
#     #     print(i[1])
#     #     print(i[2])
#     #     print(i[2])
#     #     print(i[3])
#     #     print(i[4])
#     #     print("*"*30)