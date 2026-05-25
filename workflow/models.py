from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Project(models.Model):
    states = [
        ("COMPLETED" , "Completed"),
        ("NO PROGRESS" , "No Progress"),
        ("IN PROGRESS" , "In Progress")
    ]
    
    title = models.CharField(max_length= 100)
    desription = models.TextField()
    start_date = models.DateField()
    deadline = models.DateField()
    state = models.CharField(max_length= 30 , choices =states) 

    def __str__(self):
        return self.title 

class Stage(models.Model):
    project = models.ForeignKey(Project , on_delete= models.CASCADE , related_name="stages", null=True)
    title = models.CharField(max_length=100)


    def __str__(self):
        return self.title

class Task(models.Model):
    priorites = [
        ("LOW" , "Low"),
        ("MEDIUM" , "Medium"),
        ("HIGH" , "High")
    ]
    
    owner = models.ForeignKey(User , on_delete= models.SET_NULL , null= True)
    stage = models.ForeignKey(Stage , on_delete=models.CASCADE , related_name= "tasks" , null=True)
    title = models.CharField(max_length = 100)
    completed = models.BooleanField(default= False , blank = True)
    priority = models.CharField(max_length= 20 , choices= priorites)
    start_time = models.DateField()
    deadline = models.DateField()
    last_update = models.DateField(auto_now= True , blank= True)
    

    def __str__(self):
        return f"{self.title} in {self.stage} with deadline until {self.deadline}"

class Role(models.Model):
    roles = [
        ("TEAM LEADER" , "Team Leader"),
        ("MEMBER" , "Member")
    ]

    role = models.CharField(max_length= 30 , choices = roles)

    def __str__(self):
        return self.role

class User_Role(models.Model):
    user = models.ForeignKey(User , on_delete= models.CASCADE , related_name= "users", null=True)
    role = models.ForeignKey(Role , on_delete= models.CASCADE , related_name="roles", null=True)
    project = models.ForeignKey(Project , on_delete= models.CASCADE , related_name="projects", null=True)

    def __str__(self):
        return f"{self.user} in {self.project} has {self.role} role"
