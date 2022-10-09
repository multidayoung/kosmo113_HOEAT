import datetime
import json
import random
import string

from django.shortcuts import render
from member.models import MemberDao

import smtplib
from email.mime.text import MIMEText
from email.message import EmailMessage

from myPage.models import SocketClass, OraModel
from myPage.views import sessionStart


def memberJoin(request):
    request = sessionStart(request)
    return render(request, "member/join.html")


def memberInsert(request):
    request = sessionStart(request)
    memberDao = MemberDao()
    now = datetime.datetime.now()
    now = datetime.datetime.strftime(now, '%Y-%m-%d')
    now = datetime.datetime.strptime(now, '%Y-%m-%d')
    member = (request.POST['mid'], request.POST['mpwd'],
              request.POST['mname'], request.POST['mbirth'].replace('-', ''),
              request.POST['mgender'], request.POST['memail'], now)
    memberDao.memberinsert(member)
    return render(request, "member/success.html", {'mname': request.POST['mname']})


def memberIdchk(request):
    request = sessionStart(request)
    memberDao = MemberDao()
    idx = request.GET['mid']
    res = memberDao.idcheck(idx)
    return render(request, 'member/idchk.html', {'res': res[0]})


def memberEmailchk(request):
    request = sessionStart(request)
    sendEmail = request.GET.get('sendEmail')
    s = smtplib.SMTP('smtp.gmail.com', 587)
    s.ehlo()
    s.starttls()
    s.login('gjh13531@gmail.com', 'lgczewbvqkmpsbaa')
    msg = EmailMessage()
    msg['Subject'] = "회원가입 인증메일입니다."
    bunho = ""
    sp = string.ascii_letters.join(string.digits)
    rang = 8
    for i in range(rang):
        bunho += random.choice(sp)
    msg.set_content("인증번호는 " + bunho + " 입니다")
    msg['From'] = "gjh13531@gmail.com"
    msg['To'] = sendEmail
    s.send_message(msg)
    s.quit()
    return render(request, "member/emailchk.html", {"bunho": bunho})


def joinChart(request):
    request = sessionStart(request)
    arr1 = []
    arr2 = []
    memberDao = MemberDao()
    res = dict(memberDao.joinLog())
    for dic, cnt in res.items():
        days = datetime.datetime.strftime(dic, '%Y-%m-%d')
        arr1.append(days)
        arr2.append(cnt)
    chart = zip(arr1, arr2)
    return render(request, "member/joinChart.html", {"chart": chart})

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
