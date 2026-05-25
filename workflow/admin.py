from django.contrib import admin
from .models import Project , Stage , Task , Role , User_Role
# Register your models here.

admin.site.register(Project)
admin.site.register(Stage)
admin.site.register(Task)
admin.site.register(Role)
admin.site.register(User_Role)