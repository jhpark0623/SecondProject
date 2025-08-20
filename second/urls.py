from django.urls import path
from second import views

urlpatterns = [
    path('', views.map_view),  # <-- main 대신 map_view 사용
]
