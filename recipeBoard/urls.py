from django.urls import path

from recipeBoard import views

urlpatterns = [
    path('boardHome', views.boardHome),
    path('boardWrite', views.boardWrite),
    path('boardInsert', views.boardInsert),
    path('boardList', views.boardList),
    path('boardDetail', views.boardDetail),
    path('boardUpdate', views.boardUpdate),
    path('boardUpdateGo', views.boardUpdateGo),
    path('boardDelete', views.boardDelete),
    path('boardChart', views.boardChart),  # 기간별
    path('jjim', views.jjim),

    path('commentWrite', views.commentWrite),
    path('commDetail', views.commDetail),
    path('commUpdate', views.commUpdate),
    path('commDelete', views.commDelete),
    path('sessionEnd', views.sessionEnd),

    path('insertJim', views.insertJim),
    path('deleteJim', views.deleteJim),
    path('countAllJim', views.countAllJim),
    path('countJim', views.countJim),

]