from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.login_page, name="login_page"),
    path('logout/', views.logout_page, name="logout_page"),
    path('account-signup/', views.account_signup, name="account_signup"),
    path('account-login/', views.account_login, name="account_login"),
    path('signup/', views.SignupView.as_view(), name="signup"),
    path('login/', views.LoginView.as_view(), name="login"),
]
