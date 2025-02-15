
from django.urls import path
from .views import *
from django.contrib.auth import views as auth_views
from .views import job_detail, register_user

urlpatterns = [

    path('register/', register_user, name='register'),
    path('login/', login_user, name='login'),
    path('logout/', logout_user, name='logout'),
    path('current-user/', get_current_user, name='current-user'),
    path('users/', user_list_create, name='user-list'),
    path('users/<int:pk>/', user_detail, name='user-detail'),
    path('artisan-profile/<int:pk>/', artisan_profile, name='artisan-profile'),

    path('jobs/<int:pk>/', job_detail, name='job-detail'),
    path('login/', auth_views.LoginView.as_view(template_name='users/login.html'), name='login'),
    path('register/', register_user, name='register'),
    path('jobs/', job_list_create, name='job-list'),
    path('jobs/<int:pk>/', job_detail, name='job-detail'),

    path('job-applications/', job_application_list_create, name='job-application-list'),

    path('transactions/', transaction_list_create, name='transaction-list'),
    path('reviews/', review_list_create, name='review-list'),
    path('notifications/', notification_list, name='notification-list'),
]