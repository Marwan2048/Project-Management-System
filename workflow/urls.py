from django.urls import path
from .views import (Register, ProjectListView, CreateProject , ProjectDetailView , UpdateProjectView , DeleteProjectView , CreateTask , 
                    UpdateStageView , DeleteStageView, SendInvitationView, InvitationsListView , InvitationDecisionView ,AssignTaskView , 
                    CompleteTaskView , ChangeTaskOwnerView , RemoveMemberView )

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
    path("stage/<int:pk>/edit/" , UpdateStageView.as_view(), name="update_stage"),
    path("stage/<int:pk>/delete/" , DeleteStageView.as_view(), name="delete_stage"),
    path("project/<int:pk>/create_task/" , CreateTask.as_view() , name="create_task"),
    path("project/<int:pk>/invite/" , SendInvitationView.as_view(), name="send_invitation"),
    path("invitations/" , InvitationsListView.as_view(), name="invitations_list"),
    path("invitation/<int:pk>/action/" , InvitationDecisionView.as_view(), name="invitation_action"),
    path("task/<int:pk>/assign/" , AssignTaskView.as_view(), name="assign_task"),
    path("task/<int:pk>/complete/",CompleteTaskView.as_view() , name="complete_task"),
    path("task/<int:pk>/change/" , ChangeTaskOwnerView.as_view() , name="change_task"),
    path("project/<int:project_id>/member/<int:pk>/" , RemoveMemberView.as_view() , name="remove_member"),

]