from django.shortcuts import render, redirect
from .forms import EmployeeForm, LeaveForm
from .models import Employee, Leave
from django.db.models import Q
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import EmployeeSerializer

def home(request):
    return render(request, 'index.html')


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



def apply_leave(request):

    if request.method == "POST":
        form = LeaveForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect('leave_list')

    else:
        form = LeaveForm()

    return render(request, 'leave_apply.html', {'form': form})

def leave_list(request):

    status = request.GET.get('status')

    if status:
        leaves = Leave.objects.filter(status=status)
    else:
        leaves = Leave.objects.all()

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