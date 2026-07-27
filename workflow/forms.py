from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Project , Stage , Task
import datetime
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
        fields = ["title" , "description" , "start_date" , "deadline"]
        widgets = {
            'start_date': forms.DateInput(
                attrs={
                    'type': 'date',
                    'min': datetime.date.today().isoformat(),  
                    'class': 'form-control'
                }
            ),
            'deadline': forms.DateInput(
                attrs={
                    'type': 'date',
                    'min': datetime.date.today().isoformat(),  
                    'class': 'form-control'
                }
            )
        }

    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get('start_date')
        deadline = cleaned_data.get('deadline')
        today = datetime.date.today()

        if start_date and start_date < today:
            self.add_error('start_date', "Start date cannot be in the past.")

        if start_date and deadline and deadline < start_date:
            self.add_error('deadline', "Deadline must be after or equal to start date.")

        return cleaned_data

class StageCreationForm(forms.ModelForm):
    class Meta:
        model = Stage
        fields = ["title"]

class TaskCreationForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ["title" , "priority" , "start_date" , "deadline"]
        widgets = {
            "priority": forms.Select(
                attrs={
                    "class": "task-select",
                }
            ),
            "start_date": forms.DateInput(
                attrs={
                    "type": "date",
                    "min": datetime.date.today().isoformat(),
                    "class": "form-control"
                }
            ),
            "deadline": forms.DateInput(
                attrs={
                    "type": "date",
                    "min": datetime.date.today().isoformat(),
                    "class": "form-control"
                }
            )
        }
