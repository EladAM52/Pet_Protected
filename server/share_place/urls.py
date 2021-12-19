from django.urls import path
from .views import home_page, login_page, register_page, get_categories, create_post, get_posts, management_page, \
    get_stats, edit_post,delete_post,create_review,get_reviews,profile_page, add_to_favorite

urlpatterns = [
    path('', home_page, name='home_page'),
    path('login', login_page, name='login_page'),
    path('register', register_page, name='register_page'),
    path('management', management_page, name='management_page'),

]
