from django import forms
from .models import Employee,Leave

class EmployeeForm(forms.ModelForm):

    class Meta:
        model = Employee
        fields = '__all__'
        
class LeaveForm(forms.ModelForm):

    class Meta:
        model = Leave
        fields = '__all__'