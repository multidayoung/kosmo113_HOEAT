import json
from datetime import datetime

from django.shortcuts import render

from config.models import rankinOraMain
from myPage.models import SocketClass, OraModel
from myPage.views import sessionStart


def mainHome(request):
    request = sessionStart(request)
    ref = rankinOraMain()
    res = ref.mainRank()
    totalBest = []
    korBest = []
    westBest = []
    chiBest = []
    japBest = []
    categories = ['전체','한식','양식','중식','일식']
    numbs=[1,2,3,4,5]
    cate=[]
    for e in res:
        if e[0] in range(1,21):
            totalBest.append(e)
        elif e[0] in range(21,41):
            westBest.append(e)
        elif e[0] in range(41,61):
            japBest.append(e)
        elif e[0] in range(61,81):
            chiBest.append(e)
        else:
            korBest.append(e)
    bests = [totalBest, korBest, westBest, chiBest, japBest]
    cate = zip(categories, bests, numbs)

    return render(request, "main.html", {'cate': cate, 'divOpen': [5,9,13,17], 'divClose': [4,8,12,16,20]})
#'totalBest': totalBest, 'westBest': westBest, 'japBest': japBest, 'chiBest': chiBest, 'korBest': korBest,

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