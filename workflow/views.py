from django.shortcuts import render 
from django.urls import reverse_lazy
from django.views.generic import CreateView , ListView
from .forms import RegisterForm , ProjectCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Project , User_Role , Task

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
    
