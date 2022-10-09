import json
import random
import smtplib
import string
from datetime import datetime
from email.message import EmailMessage

from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt

from login.models import Conn_log

from myPage.models import SocketClass, OraModel
from myPage.views import sessionStart


def loginform(request):
    request = sessionStart(request)
    # 로그인 상태일때 url로 로그인 들어가면 다시 로그인 못하게 하기
    if 'member_id' in request.session:
        print('뭐야 이거')
        del request.session['member_id']
        # del request.session['member_name']
        return redirect('/')
    # 폼에서 submit으로 전송 되어온 POST
    if request.method == 'POST':
        member_id = request.POST['id']
        member_pwd = request.POST['pwd']
        connlog = Conn_log()
        res = connlog.loginPro(member_id,member_pwd)
        print('res =>',res)
        if res is not None:
            if member_id == res[0] and member_pwd == res[1]:
                print("Login Success!")
                # session 등록하기
                request.session['member_id']=res[0]
                request.session['member_name']=res[2]
                return redirect("/")
            else:
                print("다시 로그인")
        else:
            print("아이디 비밀번호가 올바르지 않습니다.")

    return render(request, 'login/login.html')

def logout(request):
    request = sessionStart(request)
    del request.session['member_id']
    del request.session['member_name']
    return redirect('/')

@csrf_exempt
def forgotId(request):
    request = sessionStart(request)
    if request.method == 'POST':
        member_name = request.POST['member_name']
        member_email = request.POST['member_email']
        print(member_name)
        print(member_email)
        conn = Conn_log()
        res = conn.forgotId(member_name,member_email)
        if res is not None:
            res = ''.join(res)
            print(type(res))
            return render(request,'login/discoverId.html',{'res':res})
        else:
            return render(request,'login/discoverId.html',{'res':res})
    return render(request, 'login/forgotId.html')

def forgotPwd(request):
    request = sessionStart(request)
    return render(request,"login/findPwd.html")

def msgCheck(request):
    request = sessionStart(request)
    member_id=request.GET.get('member_id')
    sendEmail=request.GET.get('sendEmail')
    conn = Conn_log()
    res = conn.checkEmail(member_id)
    dbEmail = ''.join(res)
    print(sendEmail)
    print(dbEmail)
    if sendEmail==dbEmail:
        s = smtplib.SMTP('smtp.gmail.com',587)
        s.ehlo()
        s.starttls()
        s.login('qudfuf0331@gmail.com','dspvsccfvojwutwh')
        msg=EmailMessage()
        msg['Subject']="이메일 인증 확인 부탁드립니다"
        bunho = ""
        sp = string.ascii_letters.join(string.digits)
        rang = 8
        for i in range(rang):
            bunho += random.choice(sp)
        print(bunho)
        msg.set_content("인증번호는 "+bunho+"입니다")
        msg['From']="qudfuf0331@gmail.com"
        msg['To']=sendEmail
        s.send_message(msg)
        s.quit()
        return render(request,"login/msgCheck.html",{"bunho":bunho})
    else:
        bunho = 'fail'
        return render(request,"login/msgCheck.html",{"bunho":bunho})

def changePwdForm(request):
    request = sessionStart(request)
    member_id = request.GET.get('id')
    return render(request, "login/changePwdForm.html",{"member_id":member_id})

def changePwd(request):
    request = sessionStart(request)
    member_id = request.POST['id']
    newPwd = request.POST['newPwd']
    conn = Conn_log()
    conn.changePwd(member_id,newPwd)
    return redirect("/login/loginform")

def genderChart(request):
    request = sessionStart(request)
    conn = Conn_log()
    res = conn.genderChart()
    print(res)
    reslist = []
    for e in res:
        reslist.append(int(''.join(str(e)).strip('()').replace(",","")))
    print(reslist)
    return render(request, "login/genderChart.html",{'reslist':reslist})

@csrf_exempt
def loginCheck(request):
    request = sessionStart(request)
    mid = request.POST['mid']
    mpwd = request.POST['mpwd']
    conn = Conn_log()
    res = "".join(str(conn.idPwdCheck(mid,mpwd))).strip('(,)')
    print(res)
    return render(request,"login/idPwdCheck.html",{"res":res})

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