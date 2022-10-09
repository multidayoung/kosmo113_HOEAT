from django.core.paginator import Paginator
from django.shortcuts import render
from django.views import View

from ranking.models import searchData
from recipeBoard.models import Recipe_Board


class PageNSearch(View):
    def get(self, request):  # GET => page * search한 값도 연결받아야함.

        m_id = request.session.get('member_id')
        recipeBoard = Recipe_Board()
        countvvv = recipeBoard.countJim(m_id)
        countvv = "".join(str(countvvv)).strip('(,),s')
        countvv = "".join(str([('hello'),('hi')])).strip('(,)')
        print("GET*******************8vvvvvvvvvvvvv",countvv)

        recipeBoard = Recipe_Board()
        # myboardlist = recipeBoard.listBoard()
        searchValue = request.GET.get('searchValue', '')
        searchType = request.GET.get('searchType', 'btitle')
        count = "".join(str(recipeBoard.countBoard(searchType, searchValue))).strip('(,)')
        items = recipeBoard.searchBoard(searchType, searchValue)
        page = int(request.GET.get('page', '1'))

        # if 0 < len(searchValue):
        #     items = recipeBoard.searchBoard(searchValue)
        # else:
        #     items = myboardlist
        pageinator = Paginator(items, '12')

        # print("count 전체게시물 수 =>",pageinator.count)
        # print("num_pages  =>", type(pageinator.num_pages))
        print(pageinator.num_pages / 5)
        list = pageinator.get_page(page)
        # print("listnumber",list.number)
        startPage = int(((list.number - 1) / 5)) * 5 + 1
        # print("startPage",startPage)
        endPage = startPage + 5 - 1
        # print("endPage",endPage)
        npagePerBlock = list.number + 5
        # print("list.start_index", list.start_index)
        # print("list.end_index", list.end_index)
        totalPage = (pageinator.num_pages)
        # print("totalPage",totalPage)
        startplus = startPage - 1
        endplus = endPage + 1
        # print("list.paginator.page_range",list.paginator.page_range)
        return render(request, "recipeBoard/boardList.html",
                      {"list": list, "count": count, "searchValue": searchValue, "searchType": searchType,
                       "startPage": startPage, "endPage": endPage, "totalPage": totalPage,
                       "npagePerBlock": npagePerBlock, "endplus": endplus, "startplus": startplus,"countvv":countvv})

    def post(self, request):  # POST => search

        m_id = request.GET.get('member_id')
        recipeBoard = Recipe_Board()
        countvv = recipeBoard.countJim(m_id)

        print("def post")
        recipeBoard = Recipe_Board()
        searchValue = request.POST.get('searchValue','')
        searchType = request.POST.get('searchType', '')
        count = "".join(str(recipeBoard.countBoard(searchType, searchValue))).strip('(,)')
        print(f"len count : {len(count)}")
        print(f"type count : {type(count)}")
        print(f"count : {count}")
        if count != '0' :
            storeSD = searchData()
            storeSD.searchToDb(searchType, searchValue)

        items = recipeBoard.searchBoard(searchType, searchValue)
        pageinator = Paginator(items, '12')
        page = int(request.POST.get('page', '1'))
        # print("count 전체게시물 수 =>",pageinator.count)
        # print("num_pages  =>", type(pageinator.num_pages))
        print(pageinator.num_pages / 5)
        list = pageinator.get_page(page)
        # print("listnumber",list.number)
        startPage = int(((list.number - 1) / 5)) * 5 + 1
        # print("startPage",startPage)
        endPage = startPage + 5 - 1
        # print("endPage",endPage)
        npagePerBlock = list.number + 5
        # print("list.start_index", list.start_index)
        # print("list.end_index", list.end_index)
        totalPage = (pageinator.num_pages)
        # print("totalPage",totalPage)
        startplus = startPage - 5
        endplus = endPage + 1
        # print("list.paginator.page_range",list.paginator.page_range)

        return render(request, "recipeBoard/boardList.html",
                      {"list": list, "count": count, "searchValue": searchValue, "searchType": searchType,
                       "startPage": startPage, "endPage": endPage, "totalPage": totalPage,
                       "npagePerBlock": npagePerBlock, "endplus": endplus, "startplus": startplus,"countvv":countvv})