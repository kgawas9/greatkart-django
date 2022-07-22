from django.urls import path
from . import views


urlpatterns = [
    path('register/', views.register_user, name='register-user'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),

    path('dashboard/', views.dashboard, name='user-dashboard'),
    path('', views.dashboard, name='user-dashboard'),

    path('forgot-password/', views.forgot_password, name='forgot-password'),

    path('activate/<uidb64>/<token>', views.activate, name='activate'),

    path('reset_password_validate/<uidb64>/<token>', views.reset_password_validate, name='reset_password_validate'),
    path('reset_password/', views.resetPassword, name='reset_password'),
]
