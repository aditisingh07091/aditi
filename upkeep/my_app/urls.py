from django.urls import path,include
from my_app.views import UserPasswordResetView, SendPasswordResetEmailView, UserRegistrationView, UserLoginView, UserProfileView
urlpatterns = [
    path('register', UserRegistrationView.as_view(), name='register'),
    path('login', UserLoginView.as_view(), name='login'),
    path('profile', UserProfileView.as_view(), name='profile'),
    path('SendResetPasswordEmail', SendPasswordResetEmailView.as_view(), name='SendResetPasswordEmail'),
    path('resetPassword/<uid>/<token>', UserPasswordResetView.as_view(), name = 'reset-password')
]
