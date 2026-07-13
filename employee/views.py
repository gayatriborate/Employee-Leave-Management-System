from django.shortcuts import render, redirect
from .forms import EmployeeForm, LeaveForm
from .models import Employee, Leave
from django.db.models import Q
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import EmployeeSerializer
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404

@login_required
def home(request):

    if request.user.is_superuser:
        return render(request, "hr_home.html")

    return render(request, "employee_home.html")


def add_employee(request):
    if request.method == "POST":
        form = EmployeeForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('employee_list')
    else:
        form = EmployeeForm()

    return render(request, 'employee_add.html', {'form': form})



def edit_employee(request, id):
    employee = Employee.objects.get(id=id)

    if request.method == "POST":
        form = EmployeeForm(request.POST, instance=employee)
        if form.is_valid():
            form.save()
            return redirect('employee_list')
    else:
        form = EmployeeForm(instance=employee)

    return render(request, 'employee_edit.html', {'form': form})

def delete_employee(request, id):
    employee = Employee.objects.get(id=id)
    employee.delete()
    return redirect('employee_list')


@login_required
def apply_leave(request):

    if request.method == "POST":

        form = LeaveForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect('leave_list')

    else:
        form = LeaveForm()

    return render(request, 'leave_apply.html', {'form': form})

@login_required
def leave_list(request):

    if request.user.is_superuser:

        status = request.GET.get('status')
        leave_type = request.GET.get('leave_type')

        leaves = Leave.objects.all()

        if status:
            leaves = leaves.filter(status=status)

        if leave_type:
            leaves = leaves.filter(leave_type=leave_type)

    else:

        employee = Employee.objects.get(email=request.user.email)
        leaves = Leave.objects.filter(employee=employee)

    return render(request, 'leave_list.html', {
        'leaves': leaves
    })
    
def edit_leave(request, id):
    leave = Leave.objects.get(id=id)

    if request.method == "POST":
        form = LeaveForm(request.POST, instance=leave)

        if form.is_valid():
            form.save()
            return redirect('leave_list')

    else:
        form = LeaveForm(instance=leave)

    return render(request, 'leave_edit.html', {'form': form})

def delete_leave(request, id):
    leave = Leave.objects.get(id=id)
    leave.delete()
    return redirect('leave_list')



def dashboard(request):

    total_employee = Employee.objects.count()
    total_leave = Leave.objects.count()
    pending_leave = Leave.objects.filter(status='Pending').count()
    approved_leave = Leave.objects.filter(status='Approved').count()
    rejected_leave = Leave.objects.filter(status='Rejected').count()

    context = {
        'total_employee': total_employee,
        'total_leave': total_leave,
        'pending_leave': pending_leave,
        'approved_leave': approved_leave,
        'rejected_leave': rejected_leave,
    }

    return render(request, 'dashboard.html', context)

def employee_list(request):

    search = request.GET.get('search')

    if search:
        employees = Employee.objects.filter(
            Q(name__icontains=search) |
            Q(employee_id__icontains=search)
        )
    else:
        employees = Employee.objects.all()

    return render(request, 'employee_list.html', {
        'employees': employees
    })
    
    
    
@api_view(['GET'])
def employee_api(request):

    employees = Employee.objects.all()

    serializer = EmployeeSerializer(employees, many=True)

    return Response(serializer.data)


@api_view(['POST'])
def add_employee_api(request):

    serializer = EmployeeSerializer(data=request.data)

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)

    return Response(serializer.errors)


@api_view(['PUT'])
def update_employee_api(request, id):

    employee = Employee.objects.get(id=id)

    serializer = EmployeeSerializer(employee, data=request.data)

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)

    return Response(serializer.errors)


@api_view(['DELETE'])
def delete_employee_api(request, id):

    employee = Employee.objects.get(id=id)

    employee.delete()

    return Response({"message": "Employee Deleted Successfully"})


def login_view(request):

    if request.method == "POST":

        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(username=username, password=password)

        if user is not None:

            login(request, user)

            if user.is_superuser:
                return redirect("dashboard")
            else:
                return redirect("home")

        else:
            messages.error(request, "Invalid Username or Password")

    return render(request, "login.html")


def logout_view(request):
    logout(request)
    return redirect("login")