import json
from datetime import datetime

from django.shortcuts import render, redirect

# Create your views here.
from myPage.models import SocketClass, OraModel
from myPage.views import sessionStart
from ranking.models import rankinOra, SearchedData, searchData, GetChart
# pip install konlpy
from konlpy.tag import Okt  # 한국어 형태소 분석해서 명사만 추출 해준다.


def rankingmain(request):
    ref = rankinOra()
    cate = request.GET.get('cate', '')
    if len(cate) > 0:
        res = ref.mainRank(cate)
        return render(request, 'ranking/rankingmain.html', {'cateRanList': res, 'cate': cate})
    res = ref.mainRank('식')
    request = sessionStart(request)
    return render(request, 'ranking/rankingmain.html', {'cateRanList': res})


def rankingRecipe(request):
    request = sessionStart(request)
    ref = rankinOra()
    res = ref.mainRank('식')
    # , 'cate': '식'
    return render(request, 'ranking/rankingRecipeAj.html', {'cateRanList': res})


def rankingRecipeCate(request):
    cate = request.GET['cate']
    # if cate == 'total':
    #     arg = '식'
    # elif cate == 'kor':
    #     arg = '한식'
    # elif cate == 'west':
    #     arg = '양식'
    # elif cate == 'chi':
    #     arg = '중식'
    # elif cate == 'jap':
    #     arg = '일식'
    print(f"cate : {cate}")
    ref = rankinOra()
    res = ref.mainRank(cate)
    request = sessionStart(request)
    return render(request, 'ranking/rankingRecipeAjCate.html', {'cateRanList': res})


def rankingSearch(request):
    ref = searchData()
    res = ref.getSDBRank('')
    rankN = 1
    rankList = []
    for i in res:
        rankList.append(tuple([rankN, i]))
        rankN += 1
    for n, s in rankList:
        print(f"{n} : {s.snouns}")
    request = sessionStart(request)
    return render(request, 'ranking/rankingSearchAj.html', {'searchRankList': rankList})


def rankingSearchRange(request):
    sType = request.GET.get('sType', '')
    print("sType:", sType)
    ref = searchData()
    res = ref.getSDBRank(sType)
    rankN = 1
    rankList = []
    for i in res:
        rankList.append(tuple([rankN, i]))
        rankN += 1
    request = sessionStart(request)
    return render(request, 'ranking/rankingSearchAjRange.html', {'searchRankList': rankList})


def sessionEnd(request):
    print(f"세션 끝! : {datetime.now()}")
    try:
        if 'member_id' not in request.session:
            request.session['member_id'] = 'Guest' + str(SocketClass.guest)
        request.session['end'] = json.dumps(datetime.now(), default=str)
        request.session['end'] = request.session['end'].replace("\"", "")
        start = datetime.strptime(request.session['start'], '%Y-%m-%d %H:%M:%S.%f')
        end = datetime.strptime(request.session['end'], '%Y-%m-%d %H:%M:%S.%f')
        d = end - start
        res = round(d.microseconds / float(1000000)) + (d.seconds + d.days * 3600 * 24)
        OraModel().staylog(request.session['member_id'], res, datetime.now().date())
        OraModel().movepage(request.session['member_id'], request.session['pageMove'], datetime.now().date())
        request.session.clear()
    except:
        request.session.clear()
    return render(request, "myPage/msgCheck.html")


def cateHitRanking(request):
    sumOrAvg = request.GET.get('param', '')
    ref = GetChart()
    if len(sumOrAvg) > 0:
        if sumOrAvg == 'sum':
            res = ref.cateHitSumRanking()
            return render(request, 'ranking/chartRankCateAj.html', {"hitChart": res, 'sumOrAvg': 'sum'})
        elif sumOrAvg == 'avg':
            res = ref.cateHitAvgRanking()
            return render(request, 'ranking/chartRankCateAj.html', {"hitChart": res, 'sumOrAvg': 'avg'})
    res = ref.cateHitSumRanking()
    return render(request, 'ranking/chartRankCate.html', {"hitChart": res, 'sumOrAvg': 'sum'})