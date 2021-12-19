from django.shortcuts import render, redirect
from django.http import JsonResponse
from .models import Category, Post, Review, Favorite
from django.contrib.auth.models import User
import json
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.views.decorators.http import require_POST, require_http_methods


def home_page(request):
    return render(request, 'home.html')


def login_page(request):
    if request.user.is_authenticated:
        return redirect('home_page')

    return render(request, 'login.html')


def register_page(request):
    if request.user.is_authenticated:
        return redirect('home_page')

    return render(request, 'register.html')


def profile_page(request):
    if request.user.is_authenticated:
        return render(request, 'profile_page.html')

    return redirect('home_page')


@login_required(login_url='/login')
def management_page(request):
    if request.user.is_superuser:
        return render(request, 'management.html')
    else:
        return redirect('home_page')


@login_required(login_url='/login')
def get_stats(request):
    return JsonResponse(
        data={
            "amount_users": User.objects.all().count(),
            "amount_posts": Post.objects.all().count(),
            "amount_reviews": Review.objects.all().count()
        }
    )
def get_categories(request):
    return JsonResponse(data={
        "categories": list(Category.objects.values_list('title', flat=True))
    })


def get_posts(request):
    category = request.GET.get('category')
    author_id = request.GET.get('author__id')
    is_favorite = request.GET.get('is_favorite')
    queryset = Post.objects.all()

    if category:
        queryset = queryset.filter(category__title=category)

    if author_id:
        queryset = queryset.filter(author__id=author_id)

    post_list = []

    queryset_list = list(queryset.values(
        'id', 'title', 'description', 'category', 'category__title', 'created_at', 'image',
        'author_id', 'author__username', 'author__first_name', 'author__last_name', 'author__profile__phone_number'
    ))

    for post in queryset_list:
        post['is_favorite'] = Favorite.objects.filter(user=request.user, post_id=post['id']).exists()  # true or false
        if is_favorite:  # user ask favorite
            # add to list if is favorite
            if post['is_favorite']:
                post_list.append(post)
        else:
            post_list.append(post)

    return JsonResponse(data={
        "posts": post_list
    })
def get_reviews(request):
    queryset = Review.objects.all()

    return JsonResponse(data={
        "reviews": list(
            queryset.values(
                'id', 'Fullname', 'title', 'description', 'email'
            )
        )
    })
