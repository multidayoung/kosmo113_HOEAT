import json
import time
from datetime import datetime
import random
import string

from django.core.paginator import Paginator
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
import smtplib
from email.mime.text import MIMEText
from email.message import EmailMessage

from django.views.decorators.csrf import csrf_exempt

# Create your views here.
from myPage.models import OraModel, SocketClass


def mainIndex(request):
    request = sessionStart(request)
    return render(request, "myPage/myPage_main.html")


def detail(request):
    request = sessionStart(request)
    detail = OraModel().detail(request.session['member_id'])
    if detail is None:
        pass
    else:
        detail = list(detail)
    print(type(detail))

    return render(request, "myPage/myPage_memberDetail.html", {"detail": detail})


@csrf_exempt
def jjimList(request):

    request = sessionStart(request)
    request.session['pageMove'] += 1
    page = int(request.GET.get('page', '1'))
    if request.method =='GET':
        searchValue = request.GET.get('searchValue',None)
        if searchValue is not None:
            jjimDic = {"mid": request.session['member_id'], "searchValue": "%"+searchValue+"%"}
        else:
            jjimDic = {"mid": request.session['member_id'], "searchValue": searchValue}
    else:
        searchValue = request.POST['searchValue']
        jjimDic = {"mid": request.session['member_id'], "searchValue": "%"+searchValue+"%"}
    items = OraModel().jjimList(**jjimDic)
    jjimCount = len(items)
    pageinator = Paginator(items, '10')
    List = pageinator.get_page(page)
    if searchValue is None:
        searchValue = ''
    if len(items) == 0:
        List = None
    return render(request,"myPage/myPage_jjim.html",{"List":List,'jjimCount':jjimCount,'searchValue':searchValue})

@csrf_exempt
def reviewList(request):

    request = sessionStart(request)
    request.session['pageMove'] += 1
    page = int(request.GET.get('page', '1'))

    if request.method == 'GET':
        select = request.GET.get('select', 'myreview')  # 내가받은 댓글인지 작성한 댓글인지의 구분,최초로 해당 페이지에 들어갈땐 myreview로 설정
        searchValue = request.GET.get('searchValue', None)
        if searchValue is not None:
            reviewDic = {"mid": request.session['member_id'], "searchValue": "%"+searchValue+"%"}
        else:
            reviewDic = {"mid": request.session['member_id'], "searchValue": searchValue}
    else:
        select = request.POST['selectReview']
        searchValue = request.POST['searchValue']
        reviewDic = {"mid": request.session['member_id'], "searchValue": "%" + searchValue + "%"}
    items = OraModel().review(select,**reviewDic)
    reviewCount = len(items)
    pageinator = Paginator(items, '10')
    List = pageinator.get_page(page)
    if searchValue is None:
        searchValue = ''
    if len(items) == 0:
        List = None
    return render(request, "myPage/myPage_review.html",{"select":select,"List":List,'reviewCount':reviewCount,'searchValue':searchValue})


@csrf_exempt
def recipeList(request):

    request = sessionStart(request)
    request.session['pageMove'] += 1
    page = int(request.GET.get('page', '1'))
    if request.method =='GET':
        searchValue = request.GET.get('searchValue',None)
        if searchValue is not None:
            recipeDic = {"mid": request.session['member_id'], "searchValue": "%"+searchValue+"%"}
        else:
            recipeDic = {"mid": request.session['member_id'], "searchValue": searchValue}
    else:
        searchValue = request.POST['searchValue']
        recipeDic = {"mid": request.session['member_id'], "searchValue": "%"+searchValue+"%"}
    items = OraModel().recipe(**recipeDic)
    recipeCount = len(items)
    pageinator = Paginator(items, '10')
    List = pageinator.get_page(page)
    if searchValue is None:
        searchValue = ''
    if len(items) == 0:
        List = None
    return render(request,"myPage/myPage_recipe.html",{"List":List,'reviewCount':recipeCount,'searchValue':searchValue})

def msgTest(request):
    request = sessionStart(request)
    return render(request, "myPage/MsgTest.html")


def msgCheck(request):
    request = sessionStart(request)
    sendEmail = request.GET.get('sendEmail')

    s = smtplib.SMTP('smtp.gmail.com', 587)
    s.ehlo()
    s.starttls()
    s.login('you12zin34@gmail.com', 'gwhuzdqqdedflanj')
    msg = EmailMessage()
    msg['Subject'] = "이메일 인증 확인 부탁드립니다"
    bunho = ""
    sp = string.ascii_letters.join(string.digits)
    rang = 8
    result = ''
    for i in range(rang):
        bunho += random.choice(sp)
    print(bunho)
    msg.set_content("인증번호는 " + bunho + "입니다")
    msg['From'] = "you12zin34@gmail.com"
    msg['To'] = sendEmail
    s.send_message(msg)
    s.quit()
    return render(request, "myPage/msgCheck.html", {"bunho": bunho})


def sessionStart(request):
    print(f"세션 시작! : {datetime.now()}")

    if 'start' not in request.session:
        request.session['start'] = json.dumps(datetime.now(), default=str)
        request.session['start'] = request.session['start'].replace("\"", "")
        # SocketClass.socketList.append(request)
    if 'pageMove' not in request.session:
        request.session['pageMove'] = 0
    else:
        request.session['pageMove'] += 1
    return request

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


def chart(request):
    arr1 = []  # 날짜
    # ====================
    arrList = []
    # ===================
    res = OraModel().staylogDate()
    res2 = list(OraModel().movelogList())
    for item in res:
        arr1.append(datetime.strftime(item[1], '%Y-%m-%d'))
    count = 0
    for rownum, sdate in res:
        days = datetime.strftime(sdate, '%Y-%m-%d')
        arrList.append(OraModel().stayList(str(days)))
    for i in res2:
        imsi = list(arrList[count][0]) + list([res2[count][0]])
        arrList[count] = imsi
        count += 1
    print(arrList)
    chart = zip(arr1, arrList)

    return render(request, "myPage/myPage_Chart.html", {"chart": chart})


def dropMember(request):
    member_id = request.GET.get('member_id')
    mpwd = OraModel().getPwd(member_id)
    return render(request, "myPage/myPage_DropMember.html", {"member_id": member_id, "mpwd": mpwd})


def emailCheck(request):
    return render(request, "myPage/myPage_emailCheck.html")


def confirm(request):
    member_id = request.session.get('member_id')
    OraModel().dropMember(member_id)
    request.session.clear()
    # return render(request,"myPage/myPage_confirm.html")
    return redirect("/")

def pwdCheck(request):
    pwd = OraModel().getPwd(request.session['member_id'])
    print(f"sessionmid : {request.session['member_id']}")
    print(f"pwd : {pwd} : {pwd[0]}")
    return render(request, "myPage/myPage_pwdCheck.html", {"member_id": request.session['member_id'], "pwd": pwd})


def memberUpdate(request):
    member = {"mname": request.POST.get('mname'), "mbirth": request.POST.get('mbirth').replace("-", ""),
              "memail": request.POST.get('memail'), "mid": request.POST.get('member_id')}
    for k, v in member.items():
        print(f'{k} : {v}')
    OraModel().updateMember(**member)
    request.session['member_name']=request.POST.get('mname')
    return detail(request)
