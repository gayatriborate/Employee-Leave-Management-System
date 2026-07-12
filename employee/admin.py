from django.contrib import admin
from .models import Employee, Leave

admin.site.register(Employee)
admin.site.register(Leave)