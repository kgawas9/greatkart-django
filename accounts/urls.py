from django.urls import path
from . import views


urlpatterns = [
    path('register/', views.register_user, name='register-user'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),

    path('dashboard/', views.dashboard, name='user-dashboard'),
    path('', views.dashboard, name='user-dashboard'),

    path('activate/<uidb64>/<token>', views.activate, name='activate'),
]
