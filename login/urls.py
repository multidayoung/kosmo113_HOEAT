from django.urls import path

from login import views

urlpatterns = [
    path('loginform', views.loginform),
    path('logout', views.logout),
    path('forgotId', views.forgotId),
    path('msgCheck', views.msgCheck),
    path('forgotPwd', views.forgotPwd),
    path('changePwdForm', views.changePwdForm),
    path('changePwd', views.changePwd),
    path('genderChart', views.genderChart),
    path('loginCheck', views.loginCheck),
    path('sessionEnd', views.sessionEnd),
]
