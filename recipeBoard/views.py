import json
from collections import Counter
from datetime import datetime

import konlpy
from dateutil.relativedelta import relativedelta
from django.http import HttpResponse
from django.shortcuts import render, redirect

from myPage.models import SocketClass, OraModel
from myPage.views import sessionStart
from ranking.models import searchData
from recipeBoard.models import RecipeBoard, Recipe_Board, RecipeBoardDao
from recipeBoard.page_search import PageNSearch


def boardHome(request):
    return render(request, 'recipeBoard/recipeBoard.html')

def boardWrite(request):
    return render(request, 'recipeBoard/boardWrite.html')

UPLOAD_DIR = '/home/kosmo113/python/workspace/HoEat/recipeBoard/static/foodImg/'
def boardInsert(request):
    request = sessionStart(request)
    # enctype="multipart/form-data" 일 때는 request.FILES['file1']
    # file의 name, file size 함께 전송되어 온다.
    # product_name = request.POST['product_name']
    # file = request.FILES['file1']
    # print('file type => {}, pname=>{}'.format(file,product_name))
    # print('file name =>',file._name)
    # print('file size =>', file.size)
    # print('request.FILES =>', request.FILES)
    # request.FILES안에서 딕셔너리의 키 값인 file1 즉 파라미터 변수명
    # upload가 되었나 안되었나
    if 'bimg' in request.FILES:
        file = request.FILES['bimg']
        file_name = file._name
        # 바이너리 파일을 읽기 위해서는 파일모드를 rb 로, 쓰기 위해서는 wb 로 지정
        fp = open(UPLOAD_DIR + file_name, 'wb')
        # chunks() : 1byte 단위로 읽어 들이는 함수, java로 치면 bufferedInputStream, spring은 transferto
        for chunk in file.chunks():
            fp.write(chunk)
        fp.close()
    else:
        file_name = '-'
    dict = {'btitle':request.POST['btitle'],'mid': request.session.get('member_id'), 'bcont':request.POST['bcont'], 'bimg' : file_name,
             'bingredient' : request.POST['bingredient'], 'bcate' : request.POST['bcate']}
    recipeBoard = Recipe_Board()
    recipeBoard.writeBoard(**dict)
    return redirect("/recipeBoard/boardList")

def boardList(request):
    request = sessionStart(request)

    if request.method == 'GET':  # page * search한 값도 연결받아야함.
        re = PageNSearch().get(request)
        return re
    else:  # POST => search
        re = PageNSearch().post(request)
        return re

def boardDetail(request):
    request = sessionStart(request)
    bnum = request.GET['bnum']
    recipeBoard = Recipe_Board()
    recipeBoard.upHitBoard(bnum)
    board = recipeBoard.detailBoard(bnum)

    print(type(board))
    print(board)
    return render(request, "recipeBoard/boardDetail.html", {'board': board})

def boardUpdate(request):
    request = sessionStart(request)
    bnum = request.GET['bnum']
    recipeBoard = Recipe_Board()
    board = recipeBoard.detailBoard(bnum)
    return render(request, "recipeBoard/boardUpdate.html", {'board': board})

def boardUpdateGo(request):
    request = sessionStart(request)
    bnum = request.POST['bnum']
    print(bnum)
    if 'bimg' in request.FILES:
        file = request.FILES['bimg']
        file_name = file._name
        # 바이너리 파일을 읽기 위해서는 파일모드를 rb 로, 쓰기 위해서는 wb 로 지정
        fp = open(UPLOAD_DIR + file_name, 'wb')
        # chunks() : 1byte 단위로 읽어 들이는 함수, java로 치면 bufferedInputStream, spring은 transferto
        for chunk in file.chunks():
            fp.write(chunk)
        fp.close()
    else:
        file_name = '-'
    dict = {'btitle': request.POST['btitle'], 'bcont': request.POST['bcont'], 'bimg': file_name,
            'bingredient': request.POST['bingredient'], 'bcate': request.POST['bcate'], 'bnum': bnum}
    print(request.POST['btitle'])
    print(request.POST['bcont'])
    print(file_name)
    print(request.POST['bingredient'])
    print(request.POST['bcate'])

    recipeBoard = Recipe_Board()
    recipeBoard.updateBoard(**dict)
    return redirect("/recipeBoard/boardList")

def boardDelete(request):
    request = sessionStart(request)
    bnum = request.GET['bnum']
    recipeBoard = Recipe_Board()
    recipeBoard.deleteBoard(bnum)
    return redirect("/recipeBoard/boardList")

def boardChart(request):
    now = datetime.now()
    if request.method == 'GET':
        before_one_year = (now - relativedelta(years=1)).date()
        print(type(before_one_year),":",before_one_year)
        bdate = request.GET.get('bdate',before_one_year)
        edate = request.GET.get('edate', now.date())
    else:
        bdate = request.POST['bdate']
        edate = request.POST['edate']

    print(type(bdate),":",bdate)
    print(type(edate), ":", edate)
    recipeBoard = Recipe_Board()
    datelist = recipeBoard.dateList(bdate,edate)
    stop_word = ["레시피", "실기", "동영상", "시간", "시험", "조리", "만들기", "기능사", "요리", "방법", "일식집"]
    wordtotal = []
    for e in datelist:
        noun= konlpy.tag.Okt().nouns(e[2]) # 명사 반환
        for j in noun:
            if j not in stop_word and len(j) > 1: # 불용어 처리
                wordtotal.append(j)
    word_cnt = Counter(wordtotal)
    wordv_cnt_totalList = word_cnt.most_common(10)
    print(f'most_common() =>{word_cnt.most_common(10)}')
    return render(request, "recipeBoard/chartDemo.html", {'wordv_cnt_totalList': wordv_cnt_totalList})

def insertJim(request):
    m_id = request.session.get('member_id')
    b_num = request.GET['bnum']
    recipeBoard = Recipe_Board()
    kwargs = {"m_id":m_id,"b_num":b_num}
    recipeBoard.insertJim(**kwargs);
    return redirect("/recipeBoard/boardList")

def deleteJim(request):
    m_id = request.session.get('member_id')
    b_num = request.GET['bnum']
    recipeBoard = Recipe_Board()
    kwargs = {"m_id":m_id,"b_num":b_num}
    recipeBoard.deleteJim(**kwargs)
    return redirect("/recipeBoard/boardList")

def countAllJim(request):
    b_num = request.GET['bnum']
    recipeBoard = Recipe_Board()
    countAllv = recipeBoard.countAllJim(b_num)
    return render(request, "recipeBoard/boardList.html", {'countAllv':countAllv})

def countJim(request):
    m_id = request.GET.get('member_id')
    recipeBoard = Recipe_Board()
    countv = recipeBoard.countJim(m_id)
    return render(request, "recipeBoard/boardList.html", {'countv':countv})


def jjim(request):
    m_id = request.session.get('member_id')
    b_num = request.GET['bnum']
    print("m_id",m_id)
    print("b_num",b_num)
    recipeBoard = Recipe_Board()
    execList = recipeBoard.jjimSetting(m_id,b_num)
    print("*찜"*30)
    print(execList[0],":",execList[1])
    return render(request, "recipeBoard/jjim.html",{"execList":execList})


def commentWrite(request):
    request = sessionStart(request)
    return render(request, 'recipeBoard/form.html')


def commDetail(request):
    request = sessionStart(request)
    # bnum = request.GET['bnum']
    recipeBoardDao = RecipeBoardDao()

    # 원래 상세보기
    # myDetail = recipeBoardDao.listDetail()

    if request.method == 'POST':
        # rnum = request.POST['rnum']
        # mid = request.POST['mid']
        bnum = request.POST['bnum']

        # 댓글
        mycommentList = recipeBoardDao.listComment(bnum)
        # print(myDetail)
        print('===============================', bnum)
        rscore = request.POST['rscore']
        rcont = request.POST['rcont']
        dcDetail = { 'mid': request.session['member_id'], 'bnum':bnum, 'rscore':rscore, 'rcont':rcont}
        recipeBoardDao.commInsert(**dcDetail)
        return redirect("/recipeBoard/commDetail?bnum="+bnum)
    else:
        bnum = request.GET['bnum']
        recipeBoard = Recipe_Board()
        recipeBoard.upHitBoard(bnum)
        recipeBoard = Recipe_Board()
        board = recipeBoard.detailBoard(bnum)
        mycommentList = recipeBoardDao.listComment(bnum)

        return render(request, "recipeBoard/boardDetail.html",{"board": board, "cvo":mycommentList})

def commUpdate(request):
    request = sessionStart(request)
    bnum = request.POST['bnum']
    recipeBoardDao = RecipeBoardDao()
    items= {'rscore':request.POST['rscore'], 'rcont': request.POST['rcont'],
            'rnum': request.POST['rnum']}
    recipeBoardDao.updateComm(**items)
    return redirect("/recipeBoard/commDetail?bnum="+bnum)

def commDelete(request):
    request = sessionStart(request)
    rnum = request.GET['rnum']
    bnum = request.GET['bnum']
    recipeBoardDao = RecipeBoardDao()
    recipeBoardDao.deleteBoard(rnum)
    return redirect("/recipeBoard/commDetail?bnum="+bnum)

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
