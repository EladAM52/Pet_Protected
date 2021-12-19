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


