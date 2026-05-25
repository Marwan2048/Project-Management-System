from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Project , Stage , Task
class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ["username" , "email" , "password1" , "password2"]

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("This email is already registered.")
        return email

class ProjectCreationForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ["title" , "description" , "start_date" , "deadline" , "state"]

class StageCreationForm(forms.ModelForm):
    class Meta:
        model = Stage
        fields = ["title"]

class TaskCreationForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ["owner" , "stage" , "title" , "priority" , "start_date" , "deadline"]