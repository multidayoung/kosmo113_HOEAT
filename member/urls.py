from django.urls import path
from member import views

urlpatterns = [
    path('join', views.memberJoin),
    path('memberInsert', views.memberInsert),
    path('memberIdchk', views.memberIdchk),
    path('memberEmailchk', views.memberEmailchk),
    path('joinChart', views.joinChart),
    path('sessionEnd', views.sessionEnd),
]