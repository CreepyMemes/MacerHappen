from django.urls import path
from ..views import (
    get_current_user,
    register_participant,
    register_organizer,
    get_email_from_token,
    verify_user_email,
    login_user,
    logout_user,
    request_password_reset,
    confirm_password_reset,
    refresh_token
)

urlpatterns = [
    # User registration management
    path('register/participant/', register_participant, name='register_participant'),
    path('register/organizer/', register_organizer, name='register_organizer'),

    # Email verification management
    path('email/<uidb64>/<token>/', get_email_from_token, name='get_email_from_token'),
    path('verify/<uidb64>/<token>/', verify_user_email, name='verify_user_email'),
    
    # Operations for authenticated users
    path('me/', get_current_user, name='get_current_user'),
    path('login/', login_user, name='login_user'),
    path('logout/', logout_user, name='logout_user'),
    
    # Password recovery management
    path('reset-password/', request_password_reset, name='request_password_reset'),
    path('reset-password/<uidb64>/<token>/', confirm_password_reset, name='confirm_password_reset' ),
    
    # Session refresh management
    path('refresh-token/', refresh_token, name='refresh_token'),
]
