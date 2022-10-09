from django.urls import path

from ranking import views

urlpatterns = [
    path('rankingmain', views.rankingmain),
    path('rankingRecipe', views.rankingRecipe),
    path('rankingSearch', views.rankingSearch),
    path('rankingRecipeCate', views.rankingRecipeCate),
    path('rankingSearchRange', views.rankingSearchRange),
    path('cateHitRanking', views.cateHitRanking),
    path('sessionEnd', views.sessionEnd),
]
