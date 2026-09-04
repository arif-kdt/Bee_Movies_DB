from django.urls import path
from . import views

app_name = 'user'

urlpatterns =[

    path('user_home', views.user_home, name = 'user_home'),

    path('user_movies_list', views.user_movies_list, name='user_movies_list'),

    path('movie/<int:id>/', views.user_movie_details, name='user_movie_details'),

    path('director/<int:id>/', views.user_director_details, name='user_director_details'),

]