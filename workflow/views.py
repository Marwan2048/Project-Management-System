from django.shortcuts import render 
from django.urls import reverse_lazy
from django.views.generic import CreateView , ListView , DetailView , UpdateView , DeleteView
from .forms import RegisterForm , ProjectCreationForm , TaskCreationForm
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

        stages = self.request.POST.getlist("stages")
        for stage in stages:
            Stage.objects.create(title = stage , project = self.object)
            # bulk_create() is more efficent

        role = Role.objects.get(role = "TEAM LEADER")
        User_Role.objects.create(user = self.request.user , role = role , project = self.object)
        return super().form_valid(form)

class UpdateProjectView(LoginRequiredMixin , UpdateView):
    model = Project
    form_class = ProjectCreationForm
    template_name = "edit_project.html"
    success_url = reverse_lazy("home")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['existing_stages'] = Stage.objects.filter(project = self.kwargs.get("pk"))
        return context

    def form_valid(self, form):
        self.object = form.save()
        new_stages = self.request.POST.getlist("stages")
        self.object.stages.all().delete()
        
        for stage in new_stages:
            Stage.objects.create(title=stage, project=self.object)     
        return super().form_valid(form)

class DeleteProjectView(LoginRequiredMixin , DeleteView):
    model = Project
    template_name = "delete_project_confirm.html"
    success_url = reverse_lazy("home")

class CreateTask(LoginRequiredMixin , CreateView):
    model = Task
    form_class = TaskCreationForm
    template_name = "create_task.html"

    def get_context_data(self, **kwargs):
        context =  super().get_context_data(**kwargs)
        context["stages"] = Stage.objects.filter(project = self.kwargs.get("pk"))
        return context

    def form_valid(self, form):
        self.object = form.save(commit=False)
        stage = self.request.POST.get("stage_choosen")
        self.object.stage = Stage.objects.get(pk=stage)
        self.object.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy("detail_project" , kwargs = self.kwargs) 
    
class ProjectDetailView(LoginRequiredMixin , DetailView):
    model = Project
    template_name = "project_detail.html"
    context_object_name = "project"