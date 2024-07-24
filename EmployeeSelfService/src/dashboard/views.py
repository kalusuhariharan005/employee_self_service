from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib import messages
from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.db.models import Q

from employee.forms import EmployeeCreateForm
from leave.models import Leave
from employee.models import Employee, Department, Religion, Nationality, Role
from leave.forms import LeaveCreationForm

# Helper function to handle employee form
def handle_employee_form(request, form, employee=None):
    if form.is_valid():
        instance = form.save(commit=False)
        if employee:
            instance.id = employee.id
        instance.user = User.objects.get(id=request.POST.get('user'))
        instance.title = request.POST.get('title')
        instance.image = request.FILES.get('image')
        instance.firstname = request.POST.get('firstname')
        instance.lastname = request.POST.get('lastname')
        instance.othername = request.POST.get('othername')
        instance.birthday = request.POST.get('birthday')
        instance.role = Role.objects.get(id=request.POST.get('role'))
        instance.startdate = request.POST.get('startdate')
        instance.employeetype = request.POST.get('employeetype')
        instance.employeeid = request.POST.get('employeeid')
        instance.dateissued = request.POST.get('dateissued')
        instance.save()
        return True, None
    return False, form.errors

# Dashboard view
def dashboard(request):
    if not request.user.is_authenticated:
        return redirect('accounts:login')

    dataset = {
        'employees': Employee.objects.all(),
        'leaves': Leave.objects.all_pending_leaves(),
        'staff_leaves': Leave.objects.filter(user=request.user),
        'title': 'summary'
    }
    return render(request, 'dashboard/dashboard_index.html', dataset)

# Employees list view with pagination
def dashboard_employees(request):
    if not (request.user.is_authenticated and request.user.is_superuser and request.user.is_staff):
        return redirect('/')

    departments = Department.objects.all()
    employees = Employee.objects.all()
    
    query = request.GET.get('search')
    if query:
        employees = employees.filter(
            Q(firstname__icontains=query) |
            Q(lastname__icontains=query)
        )

    paginator = Paginator(employees, 10)  # Show 10 employees per page
    page = request.GET.get('page')
    try:
        employees_paginated = paginator.get_page(page)
    except PageNotAnInteger:
        employees_paginated = paginator.page(1)
    except EmptyPage:
        employees_paginated = paginator.page(paginator.num_pages)

    blocked_employees = Employee.objects.all_blocked_employees()

    dataset = {
        'departments': departments,
        'employees': employees_paginated,
        'blocked_employees': blocked_employees,
        'title': 'Employees'
    }
    return render(request, 'dashboard/employee_app.html', dataset)

# Employee creation view
def dashboard_employees_create(request):
    if not (request.user.is_authenticated and request.user.is_superuser and request.user.is_staff):
        return redirect('/')

    if request.method == 'POST':
        form = EmployeeCreateForm(request.POST, request.FILES)
        success, errors = handle_employee_form(request, form)
        if success:
            messages.success(request, 'Employee created successfully.', extra_tags='alert alert-success alert-dismissible show')
            return redirect('dashboard:employees')
        else:
            messages.error(request, 'Error creating employee. Please check your inputs.', extra_tags='alert alert-warning alert-dismissible show')
            return redirect('dashboard:employeecreate')

    form = EmployeeCreateForm()
    dataset = {
        'form': form,
        'title': 'Register Employee'
    }
    return render(request, 'dashboard/employee_create.html', dataset)

# Employee edit view
def employee_edit_data(request, id):
    if not (request.user.is_authenticated and request.user.is_superuser and request.user.is_staff):
        return redirect('/')

    employee = get_object_or_404(Employee, id=id)
    if request.method == 'POST':
        form = EmployeeCreateForm(request.POST or None, request.FILES or None, instance=employee)
        success, errors = handle_employee_form(request, form, employee)
        if success:
            messages.success(request, 'Employee updated successfully.', extra_tags='alert alert-success alert-dismissible show')
            return redirect('dashboard:employees')
        else:
            messages.error(request, 'Error updating employee. Please check your inputs.', extra_tags='alert alert-warning alert-dismissible show')
            return HttpResponse("Form data not valid")

    form = EmployeeCreateForm(request.POST or None, request.FILES or None, instance=employee)
    dataset = {
        'form': form,
        'title': f'Edit - {employee.get_full_name()}' if callable(getattr(employee, 'get_full_name', None)) else 'Edit Employee'
    }
    return render(request, 'dashboard/employee_create.html', dataset)

# Employee info view
def dashboard_employee_info(request, id):
    if not request.user.is_authenticated:
        return redirect('/')

    employee = get_object_or_404(Employee, id=id)
    dataset = {
        'employee': employee,
        'title': f'Profile - {employee.get_full_name()}' if callable(getattr(employee, 'get_full_name', None)) else 'Employee Profile'
    }
    return render(request, 'dashboard/employee_detail.html', dataset)

# Leave creation view
def leave_creation(request):
    if not request.user.is_authenticated:
        return redirect('accounts:login')

    if request.method == 'POST':
        form = LeaveCreationForm(data=request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.user = request.user
            instance.save()
            messages.success(request, 'Leave request sent. Await admin response.', extra_tags='alert alert-success alert-dismissible show')
            return redirect('dashboard:createleave')

        messages.error(request, 'Failed to request leave. Please check entry dates.', extra_tags='alert alert-warning alert-dismissible show')
        return redirect('dashboard:createleave')

    form = LeaveCreationForm()
    dataset = {
        'form': form,
        'title': 'Apply for Leave'
    }
    return render(request, 'dashboard/create_leave.html', dataset)

# List of pending leaves
def leaves_list(request):
    if not (request.user.is_staff and request.user.is_superuser):
        return redirect('/')

    leaves = Leave.objects.all_pending_leaves()
    dataset = {
        'leave_list': leaves,
        'title': 'Leaves List - Pending'
    }
    return render(request, 'dashboard/leaves_recent.html', dataset)

# List of approved leaves
def leaves_approved_list(request):
    if not (request.user.is_superuser and request.user.is_staff):
        return redirect('/')

    leaves = Leave.objects.all_approved_leaves()
    dataset = {
        'leave_list': leaves,
        'title': 'Approved Leave List'
    }
    return render(request, 'dashboard/leaves_approved.html', dataset)

# View for leave details
def leaves_view(request, id):
    if not request.user.is_authenticated:
        return redirect('accounts:login')

    leave = get_object_or_404(Leave, id=id)
    employee = Employee.objects.filter(user=leave.user).first()

    if not employee:
        messages.error(request, 'Employee not found.', extra_tags='alert alert-warning alert-dismissible show')
        return redirect('dashboard:leaveslist')

    dataset = {
        'leave': leave,
        'employee': employee,
        'title': f'{leave.user.username} - {leave.status} Leave'
    }
    return render(request, 'dashboard/leave_detail_view.html', dataset)

# Approve leave
def approve_leave(request, id):
    if not (request.user.is_superuser and request.user.is_authenticated):
        return redirect('/')

    leave = get_object_or_404(Leave, id=id)
    employee = Employee.objects.filter(user=leave.user).first()

    if not employee:
        messages.error(request, 'Employee not found.', extra_tags='alert alert-warning alert-dismissible show')
        return redirect('dashboard:leaveslist')

    leave.approve_leave()  # Ensure this method updates the leave status properly

    # Ensure get_full_name is callable
    full_name = employee.get_full_name() if callable(getattr(employee, 'get_full_name', None)) else "Employee"

    messages.success(request, f'Leave successfully approved for {full_name}.', extra_tags='alert alert-success alert-dismissible show')
    return redirect('dashboard:userleaveview', id=id)

# Cancel leave
def cancel_leave(request, id):
    if not (request.user.is_superuser and request.user.is_authenticated):
        return redirect('/')

    leave = get_object_or_404(Leave, id=id)
    leave.cancel_leave()  # Ensure this method updates the leave status properly

    messages.success(request, 'Leave is canceled.', extra_tags='alert alert-success alert-dismissible show')
    return redirect('dashboard:canceleaveslist')

# Unapprove leave
def unapprove_leave(request, id):
    if not (request.user.is_authenticated and request.user.is_superuser):
        return redirect('/')

    leave = get_object_or_404(Leave, id=id)
    leave.unapprove_leave()  # Ensure this method updates the leave status properly

    return redirect('dashboard:leaveslist')

# List of canceled leaves
def cancel_leaves_list(request):
    if not (request.user.is_superuser and request.user.is_authenticated):
        return redirect('/')

    leaves = Leave.objects.all_cancel_leaves()
    dataset = {
        'leave_list_cancel': leaves,
        'title': 'Cancel Leave List'
    }
    return render(request, 'dashboard/leaves_cancel.html', dataset)

# Uncancel leave
def uncancel_leave(request, id):
    if not request.user.is_superuser:
        return redirect('/')

    leave = get_object_or_404(Leave, id=id)
    leave.status = 'pending'
    leave.is_approved = False
    leave.save()

    messages.success(request, 'Leave is uncanceled and now in the pending list.', extra_tags='alert alert-success alert-dismissible show')
    return redirect('dashboard:canceleaveslist')

# List of rejected leaves
def leave_rejected_list(request):
    leaves = Leave.objects.all_rejected_leaves()
    dataset = {
        'leave_list_rejected': leaves,
        'title': 'Rejected Leaves List'
    }
    return render(request, 'dashboard/rejected_leaves_list.html', dataset)

# Reject leave
def reject_leave(request, id):
    leave = get_object_or_404(Leave, id=id)
    leave.reject_leave()  # Ensure this method updates the leave status properly

    messages.success(request, 'Leave is rejected.', extra_tags='alert alert-success alert-dismissible show')
    return redirect('dashboard:leavesrejected')

# Unreject leave
def unreject_leave(request, id):
    leave = get_object_or_404(Leave, id=id)
    leave.status = 'pending'
    leave.is_approved = False
    leave.save()

    messages.success(request, 'Leave is now in the pending list.', extra_tags='alert alert-success alert-dismissible show')
    return redirect('dashboard:leavesrejected')

# View for current user's leave
def view_my_leave_table(request):
    if request.user.is_authenticated:
        user = request.user
        leaves = Leave.objects.filter(user=user)
        employee = Employee.objects.filter(user=user).first()

        if not employee:
            messages.error(request, 'Employee not found.', extra_tags='alert alert-warning alert-dismissible show')
            return redirect('accounts:login')

        dataset = {
            'leave_list': leaves,
            'employee': employee,
            'title': 'Leaves List'
        }
        return render(request, 'dashboard/staff_leaves_table.html', dataset)
    else:
        return redirect('accounts:login')

# Attendance section view
def attendance_section(request):
    return render(request, 'dashboard/attendance_section.html')
