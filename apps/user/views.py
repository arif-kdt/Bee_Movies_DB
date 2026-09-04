from django.shortcuts import get_object_or_404, redirect, render
from apps.movies.models import *
from django.contrib.auth.decorators import login_required
from django.utils import timezone

current_year = timezone.now().year


def user_home(request):
    movie_dict = {
        'recent_movies' : Movie.objects.order_by('-pk')[:5],
        'latest_movies' : Movie.objects.filter(year__year=current_year).order_by('-year')[:5]
    }
    return render(request, 'user/user_home.html', movie_dict)


def user_movies_list(request):
    context = {
        'new_releases': Movie.objects.order_by('-id')[:10],
        'malayalam_movies': Movie.objects.filter(language='Malayalam'),
        'hindi_movies': Movie.objects.filter(language='Hindi'),
        'tamil_movies': Movie.objects.filter(language='Tamil'),
        'english_movies': Movie.objects.filter(language='English'),
    }
    return render(request, 'user/user_movies_list.html',context)


def user_movie_details(request, id):

    movie = get_object_or_404(Movie, id=id)
    
    return render(request, 'user/user_movie_details.html', {'movie': movie})


def user_director_details(request, id):

    director = get_object_or_404(Director, id=id)
    movies = Movie.objects.filter(director=director)

    return render(request, 'user/user_director_details.html', {'director': director, 'movies': movies})