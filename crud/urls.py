from django.urls import path
from .views import SignUpView, LoginView, WelcomeView, UpdateProfileView, LogoutView, DeleteView

urlpatterns = [
    path('',WelcomeView.as_view(), name = 'welcome'),
    path('signup', SignUpView.as_view(), name='signup'),
    path('login', LoginView.as_view(), name='login'),
    path('update', UpdateProfileView.as_view(), name='profile'),
    path('logout', LogoutView.as_view(), name='logout'),
    path('delete', DeleteView.as_view(), name='delete'),
]