from django.shortcuts import render 
from django.urls import reverse_lazy
from django.views.generic import CreateView , ListView , DetailView
from .forms import RegisterForm , ProjectCreationForm , StageCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Project , User_Role , Task , Role , Stage
from django.contrib.auth.models import User

class Register(CreateView):
    form_class = RegisterForm
    template_name = "register.html"
    success_url = reverse_lazy("login")

class ProjectListView(LoginRequiredMixin, ListView):
    model = Project
    template_name = "home.html"
    context_object_name = "projects"

    def get_queryset(self):
        return Project.objects.filter(
            projects__user = self.request.user,
            state__in = ["NO PROGRESS" , "IN PROGRESS"])
    
    def get_context_data(self, **kwargs):
        context =  super().get_context_data(**kwargs)

        context["num_of_tasks"] = Task.objects.filter(
            completed = False ,
            owner = self.request.user).count()
        
        context["num_of_active_projects"] = Project.objects.filter(
            state__in = ["NO PROGRESS" , "IN PROGRESS"],
            projects__user = self.request.user).count()
        
        context["completed_projects"] = Project.objects.filter(
            projects__user = self.request.user,
            state = "COMPLETED").count()

        return context
    
class CreateProject(LoginRequiredMixin ,  CreateView):
    model = Project
    form_class = ProjectCreationForm
    template_name = "create_project.html"
    success_url = reverse_lazy("home")

    def form_valid(self, form):
        self.object = form.save()
        self.object.state = "NO PROGRESS"
        self.object.save()

        stage_title = self.request.POST.get("stage_title", "").strip()
        if stage_title:
            Stage.objects.create(project=self.object, title=stage_title)

        role = Role.objects.get(role = "TEAM LEADER")
        User_Role.objects.create(user = self.request.user , role = role , project = self.object)
        return super().form_valid(form)
