from django.shortcuts import render, redirect
from django.http import JsonResponse
from .models import Category, Post, Review, Favorite
from django.contrib.auth.models import User
import json
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.views.decorators.http import require_POST, require_http_methods
from django.contrib.auth import login


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


@require_POST
def create_post(request):
    if not request.user.is_authenticated:
        return JsonResponse(data={'message': "Unauthorized"}, status=401)

    request_body = json.loads(request.POST['data'])
    image = None

    if len(request.FILES) > 0:
        image = request.FILES['file']

    title = request_body.get('title')
    description = request_body.get('description')
    category = request_body.get('category')

    try:
        Post.objects.create(
            author=request.user,
            title=title,
            description=description,
            category=Category.objects.get(title=category),
            image=image
        )
        return JsonResponse(data={'success': True}, status=201)
    except Exception as e:
        print(e)
        return JsonResponse(data={'message': "Failed to create post"}, status=500)


@require_POST
def create_review(request):
    request_body = json.loads(request.body)

    Fullname = request_body.get('Fullname')
    title = request_body.get('title')
    description = request_body.get('description')
    email = request_body.get('email')

    try:
        Review.objects.create(
            Fullname=Fullname,
            title=title,
            description=description,
            email=email

        )
        return JsonResponse(data={'success': True}, status=201)
    except Exception as e:
        print(e)
        return JsonResponse(data={'message': "Failed to create Review"}, status=500)


@require_POST
def edit_post(request, pk):
    if not request.user.is_authenticated:
        return JsonResponse(data={'message': "Unauthorized"}, status=401)

    try:
        post = Post.objects.get(id=pk)
        if post.author != request.user:
            return JsonResponse(
                data={"message": "Not permitted"},
                status=401
            )

        request_body = json.loads(request.POST['data'])
        image = None

        if len(request.FILES) > 0:
            image = request.FILES['file']

        title = request_body.get('title')
        description = request_body.get('description')
        category = request_body.get('category')

        post.title = title
        post.description = description
        post.category = Category.objects.get(title=category)

        if image:
            post.image = image

        post.save()

        return JsonResponse(data={'success': True}, status=201)
    except ObjectDoesNotExist:
        return JsonResponse(
            data={"message": "Post not found"},
            status=404
        )

@login_required
@require_POST
def edit_profile(request):
    if not request.user.is_authenticated:
        return JsonResponse(data={'message': "Unauthorized"}, status=401)

    try:
        user = request.user

        request_body = json.loads(request.POST['data'])

        first_name = request_body.get('first_name')
        last_name = request_body.get('last_name')
        phone_number = request_body.get('phone_number')
        email = request_body.get('email')
        password = request_body.get('password')

        if first_name:
            user.first_name = first_name

        if last_name:
            user.last_name = last_name
        if phone_number:
            user.profile.phone_number = phone_number

        if email:
            user.email = email

        if password:
            user.set_password(password)
            login(request, user=request.user)
        user.save()

        return JsonResponse(data={'success': True}, status=201)
    except ObjectDoesNotExist:
        return JsonResponse(
            data={"message": "Post not found"},
            status=404
        )


@require_http_methods(['DELETE'])
@login_required
def delete_post(request, pk):
    try:
        post = Post.objects.get(id=pk)
        if post.author != request.user and not request.user.is_superuser:
            return JsonResponse(
                data={"message": "Not permitted"},
                status=401
            )
        post.delete()
        return JsonResponse(
            data={
                "success": True
            }
        )
    except ObjectDoesNotExist:
        return JsonResponse(
            data={
                "message": "Post not found"
            },
            status=404
        )


@login_required
@require_POST
