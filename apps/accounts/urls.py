from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('login_view', views.login_view, name='login_view'),
    path('register', views.register, name='register'),
    path('logout_view', views.logout_view, name='logout_view'),
    path('change-password/', views.change_password, name='change_password'),
]