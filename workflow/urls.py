from django.urls import path
from .views import Register, ProjectListView, CreateProject , ProjectDetailView , UpdateProjectView , DeleteProjectView
from django.contrib.auth.views import LoginView, LogoutView

urlpatterns = [
    path("register/", Register.as_view(), name="register"),
    path("login/", LoginView.as_view(template_name="login.html"), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("", ProjectListView.as_view() , name="home"),
    path("projects/new/", CreateProject.as_view(), name="create_project"),
    path("project/<int:pk>/", ProjectDetailView.as_view(), name="detail_project"),
    path("project/<int:pk>/edit" , UpdateProjectView.as_view() , name="update_project"),
    path("project/<int:pk>/delete" , DeleteProjectView.as_view(), name="delete_project"),
]