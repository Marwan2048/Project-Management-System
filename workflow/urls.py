from django.urls import path
from .views import Register , ProjectListView
from django.contrib.auth.views import LoginView, LogoutView

urlpatterns = [
    path("register/", Register.as_view(), name="register"),
    path("login/", LoginView.as_view(template_name="login.html"), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("", ProjectListView.as_view() , name="home")
]