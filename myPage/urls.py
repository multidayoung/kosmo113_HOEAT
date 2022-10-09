from django.urls import path

from myPage import views

urlpatterns = [
    path('', views.recipeList),
    path('detail', views.detail),
    path('jjimList', views.jjimList),
    path('reviewList', views.reviewList),
    path('recipeList', views.recipeList),
    path('msgCheck', views.msgCheck),
    path('msgTest', views.msgTest),
    path('sessionStart', views.sessionStart),
    path('sessionEnd', views.sessionEnd),
    path('chart', views.chart),
    path('dropMember', views.dropMember),
    path('emailCheck', views.emailCheck),
    path('confirm', views.confirm),
    path('pwdCheck', views.pwdCheck),
    path('memberUpdate', views.memberUpdate),

]
