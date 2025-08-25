from django.urls import path
from second import views

urlpatterns = [
    path('', views.map_view, name='map_view'),
    path('favorites/', views.favorite_list, name='favorite_list'),  # ★ 즐겨찾기 페이지
    path('favorites/<str:pkplcId>/toggle/', views.toggle_favorite, name='toggle_favorite'),# 즐겨찾기 토글
    path('favorites/ids/', views.favorite_ids, name='favorite_ids'),# 즐겨찾기 목록 (현재 로그인 사용자 기준)
]
