from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path("signup/", views.signup, name="signup"),
    path('login/', auth_views.LoginView.as_view(template_name='accounts/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page="/"), name='logout'),
    path("profile/", views.profile, name="profile"),
    path("profile/<int:user_id>/", views.profile_admin, name="profile_admin"),  # 특정 유저 프로필
    path("profile/update/", views.profile_update, name="update"),
    path("admin_page/", views.admin_page, name="admin_page"),
    path('suggestions/', views.suggestion_list, name='suggestion_list'),
    path('suggestions/create/', views.suggestion_create, name='suggestion_create'),
    path('suggestions/<int:pk>/', views.suggestion_detail, name='suggestion_detail'),
    path('suggestions/<int:pk>/reply/', views.suggestion_reply, name='suggestion_reply'),
    path("suggestion/reply/delete/<int:reply_id>/", views.suggestion_reply_delete, name="suggestion_reply_delete"),

]