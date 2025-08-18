from config.urls import path
from second import views

urlpatterns=[
    path('', views.main)
]