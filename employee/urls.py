from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('add/', views.add_employee, name='add_employee'),
    path('list/', views.employee_list, name='employee_list'),
    path('edit/<int:id>/', views.edit_employee, name='edit_employee'),
    path('delete/<int:id>/', views.delete_employee, name='delete_employee'),
    
    path('leave/apply/', views.apply_leave, name='apply_leave'),
    path('leave/list/', views.leave_list, name='leave_list'),
    path('leave/edit/<int:id>/', views.edit_leave, name='edit_leave'),
    path('leave/delete/<int:id>/', views.delete_leave, name='delete_leave'),
    
    path('dashboard/', views.dashboard, name='dashboard'),
    
    path('api/employees/', views.employee_api, name='employee_api'),
    path('api/addemployee/', views.add_employee_api, name='add_employee_api'),
    path('api/updateemployee/<int:id>/', views.update_employee_api, name='update_employee_api'),
    path('api/deleteemployee/<int:id>/', views.delete_employee_api, name='delete_employee_api'),
]

