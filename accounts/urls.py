from django.contrib.auth.views import LogoutView, PasswordResetView
from .views import  UserRegistration, Login_User, ProfileListView
from django.urls import path, include

urlpatterns = [
    #path('login/', CustomLoginView.as_view(), name='login'),
    path('login/', Login_User, name='login'),
    path('profile/', ProfileListView.as_view(), name='profile'),
    path('registration/', UserRegistration, name='user_registration'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
    #path('password_reset/', PasswordResetView.as_view(template_name="registration/password_reset_form.html"),name="password_reset"),
    path('password_reset/', PasswordResetView.as_view(template_name="registration/password_reset_form.html",),name="reset_password")

]
