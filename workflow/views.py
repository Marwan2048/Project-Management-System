from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import CreateView , ListView , DetailView , UpdateView , DeleteView , View
from .forms import RegisterForm , ProjectCreationForm , TaskCreationForm , StageCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Project , User_Role , Task , Role , Stage , Invitation
from django.contrib.auth.models import User
from django.db.models import Count , Q

class Register(CreateView):
    form_class = RegisterForm
    template_name = "register.html"
    success_url = reverse_lazy("login")

class ProjectListView(LoginRequiredMixin, ListView):
    model = Project
    template_name = "home.html"
    context_object_name = "projects"

    def get_queryset(self):
        return (
            Project.objects.filter(
                projects__user=self.request.user,
                state__in=["NO PROGRESS", "IN PROGRESS"]
            )
            .annotate(
                total_tasks=Count("stages__tasks", distinct=True),
                completed_tasks=Count(
                    "stages__tasks",
                    filter=Q(stages__tasks__completed=True),
                    distinct=True
                )
            )
        )
    
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

        for project in context["projects"]:
            if project.total_tasks > 0:
                project.progress = (project.completed_tasks / project.total_tasks) * 100
            else:
                project.progress = 0

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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['existing_stages'] = Stage.objects.filter(project = self.kwargs.get("pk"))
        return context

    def form_valid(self, form):
        new_stage = self.request.POST.get("new_stage_title")
        Stage.objects.create(title = new_stage , project = self.object)
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy("detail_project" , kwargs = {"pk": self.object.id})
    
class DeleteProjectView(LoginRequiredMixin , DeleteView):
    model = Project
    template_name = "delete_project_confirm.html"
    success_url = reverse_lazy("home")

class UpdateStageView(LoginRequiredMixin , UpdateView):
    model = Stage
    form_class = StageCreationForm
    template_name = "edit_stage.html"
    context_object_name = "stage"

    def get_success_url(self):
        return reverse_lazy("detail_project" , kwargs = {"pk": self.object.id})

class DeleteStageView(LoginRequiredMixin , DeleteView):
    model = Stage
    template_name = "delete_stage_confirm.html"
    context_object_name = "stage"

    def get_success_url(self):
            print(self.kwargs)
            return reverse_lazy("detail_project" , kwargs = {"pk": self.object.project.id})

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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        user = self.request.GET.get("user")
        priority = self.request.GET.get("priority")
        completed = self.request.GET.get("completed")
        tasks = Task.objects.filter(stage__project=self.object)

        if user:
            tasks = tasks.filter(owner=user)

        if priority:
            tasks = tasks.filter(priority=priority)

        if completed:
            completed_value = completed.lower() == "true"
            tasks = tasks.filter(completed=completed_value)

        completed_tasks_count = Task.objects.filter(stage__project = self.object , completed = True).count()
        total_tasks_count = Task.objects.filter(stage__project = self.object ).count()
        progress = (completed_tasks_count / total_tasks_count) * 100 if total_tasks_count > 0 else 0

        context["tasks"] = tasks
        context["overall_progress"] = progress
        context["selected_user"] = user
        context["selected_priority"] = priority
        context["selected_completed"] = completed
        context["project_members"] = User.objects.filter(users__project=self.object).distinct()
        return context

class SendInvitationView(LoginRequiredMixin , View):
    template_name = "invite_member.html"

    def get(self, request, pk):
        project = get_object_or_404(Project, pk=pk)
        return render(
            request,
            self.template_name,
            {
                "project": project,
                "error_message": None,
                "success_message": None,
            },
        )

    def post(self, request, pk):
        project = get_object_or_404(Project, pk=pk)
        receiver_email = request.POST.get("user_email", "").strip()

        if not receiver_email:
            return render(
                request,
                self.template_name,
                {
                    "project": project,
                    "error_message": "Please enter an email.",
                    "success_message": None,
                },
            )

        receiver = User.objects.filter(email__iexact=receiver_email).first()

        if not receiver:
            return render(
                request,
                self.template_name,
                {
                    "project": project,
                    "error_message": "No user found with this email.",
                    "success_message": None,
                },
            )

        if receiver == request.user:
            return render(
                request,
                self.template_name,
                {
                    "project": project,
                    "error_message": "You cannot invite yourself.",
                    "success_message": None,
                },
            )

        if User_Role.objects.filter(user=receiver, project=project).exists():
            return render(
                request,
                self.template_name,
                {
                    "project": project,
                    "error_message": "This user is already a member of this project.",
                    "success_message": None,
                },
            )

        invitation, created = Invitation.objects.get_or_create(
            project=project,
            sender=request.user,
            receiver=receiver,
            defaults={"state": "PENDING"},
        )

        if created:
            success_message = f"Invitation sent to {receiver.username}."
        else:
            success_message = f"Invitation already exists for {receiver.username}."

        return render(
            request,
            self.template_name,
            {
                "project": project,
                "error_message": None,
                "success_message": success_message,
            },
        )

class InvitationsListView(LoginRequiredMixin , ListView):
    model = Invitation
    context_object_name = "invitations"
    template_name = "invitations_list.html"

    def get_queryset(self):
        queryset = Invitation.objects.filter(state = "PENDING" , receiver = self.request.user)
        return queryset