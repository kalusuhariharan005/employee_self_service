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

def dashboard(request):
    '''
    Summary of all apps - display here with charts etc.
    eg. LEAVE - PENDING|APPROVED|RECENT|REJECTED - TOTAL THIS MONTH or NEXT MONTH
    EMPLOYEE - TOTAL | GENDER 
    CHART - AVERAGE EMPLOYEE AGES
    '''
    if not request.user.is_authenticated:
        return redirect('accounts:login')

    dataset = dict()
    user = request.user

    employees = Employee.objects.all()
    leaves = Leave.objects.all_pending_leaves()
    staff_leaves = Leave.objects.filter(user=user)

    dataset['employees'] = employees
    dataset['leaves'] = leaves
    dataset['staff_leaves'] = staff_leaves
    dataset['title'] = 'summary'

    return render(request, 'dashboard/dashboard_index.html', dataset)

def dashboard_employees(request):
    if not (request.user.is_authenticated and request.user.is_superuser and request.user.is_staff):
        return redirect('/')

    dataset = dict()
    departments = Department.objects.all()
    employees = Employee.objects.all()

    # Pagination
    query = request.GET.get('search')
    if query:
        employees = employees.filter(
            Q(firstname__icontains=query) |
            Q(lastname__icontains=query)
        )

    paginator = Paginator(employees, 10)  # Show 10 employee lists per page
    page = request.GET.get('page')
    try:
        employees_paginated = paginator.get_page(page)
    except PageNotAnInteger:
        employees_paginated = paginator.page(1)
    except EmptyPage:
        employees_paginated = paginator.page(paginator.num_pages)

    blocked_employees = Employee.objects.all_blocked_employees()

    dataset['departments'] = departments
    dataset['employees'] = employees_paginated
    dataset['blocked_employees'] = blocked_employees
    dataset['title'] = 'Employees'

    return render(request, 'dashboard/employee_app.html', dataset)

def dashboard_employees_create(request):
    if not (request.user.is_authenticated and request.user.is_superuser and request.user.is_staff):
        return redirect('/')

    if request.method == 'POST':
        form = EmployeeCreateForm(request.POST, request.FILES)
        if form.is_valid():
            instance = form.save(commit=False)
            user = request.POST.get('user')
            assigned_user = User.objects.get(id=user)
            instance.user = assigned_user

            instance.title = request.POST.get('title')
            instance.image = request.FILES.get('image')
            instance.firstname = request.POST.get('firstname')
            instance.lastname = request.POST.get('lastname')
            instance.othername = request.POST.get('othername')
            instance.birthday = request.POST.get('birthday')

            role = request.POST.get('role')
            role_instance = Role.objects.get(id=role)
            instance.role = role_instance

            instance.startdate = request.POST.get('startdate')
            instance.employeetype = request.POST.get('employeetype')
            instance.employeeid = request.POST.get('employeeid')
            instance.dateissued = request.POST.get('dateissued')

            instance.save()

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

def employee_edit_data(request, id):
    if not (request.user.is_authenticated and request.user.is_superuser and request.user.is_staff):
        return redirect('/')

    employee = get_object_or_404(Employee, id=id)
    if request.method == 'POST':
        form = EmployeeCreateForm(request.POST or None, request.FILES or None, instance=employee)
        if form.is_valid():
            instance = form.save(commit=False)
            user = request.POST.get('user')
            assigned_user = User.objects.get(id=user)
            instance.user = assigned_user

            instance.image = request.FILES.get('image')
            instance.firstname = request.POST.get('firstname')
            instance.lastname = request.POST.get('lastname')
            instance.othername = request.POST.get('othername')
            instance.birthday = request.POST.get('birthday')

            religion_id = request.POST.get('religion')
            religion = Religion.objects.get(id=religion_id)
            instance.religion = religion

            nationality_id = request.POST.get('nationality')
            nationality = Nationality.objects.get(id=nationality_id)
            instance.nationality = nationality

            department_id = request.POST.get('department')
            department = Department.objects.get(id=department_id)
            instance.department = department

            instance.hometown = request.POST.get('hometown')
            instance.region = request.POST.get('region')
            instance.residence = request.POST.get('residence')
            instance.address = request.POST.get('address')
            instance.education = request.POST.get('education')
            instance.lastwork = request.POST.get('lastwork')
            instance.position = request.POST.get('position')
            instance.ssnitnumber = request.POST.get('ssnitnumber')
            instance.tinnumber = request.POST.get('tinnumber')

            role = request.POST.get('role')
            role_instance = Role.objects.get(id=role)
            instance.role = role_instance

            instance.startdate = request.POST.get('startdate')
            instance.employeetype = request.POST.get('employeetype')
            instance.employeeid = request.POST.get('employeeid')
            instance.dateissued = request.POST.get('dateissued')

            instance.save()
            messages.success(request, 'Employee updated successfully.', extra_tags='alert alert-success alert-dismissible show')
            return redirect('dashboard:employees')
        else:
            messages.error(request, 'Error updating employee. Please check your inputs.', extra_tags='alert alert-warning alert-dismissible show')
            return HttpResponse("Form data not valid")

    form = EmployeeCreateForm(request.POST or None, request.FILES or None, instance=employee)
    dataset = {
        'form': form,
        'title': f'Edit - {employee.get_full_name()}'
    }
    return render(request, 'dashboard/employee_create.html', dataset)

def dashboard_employee_info(request, id):
    if not request.user.is_authenticated:
        return redirect('/')

    employee = get_object_or_404(Employee, id=id)
    dataset = {
        'employee': employee,
        'title': f'Profile - {employee.get_full_name()}'
    }
    return render(request, 'dashboard/employee_detail.html', dataset)

# ---------------------LEAVE-------------------------------------------

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

def leaves_list(request):
    if not (request.user.is_staff and request.user.is_superuser):
        return redirect('/')

    leaves = Leave.objects.all_pending_leaves()
    dataset = {
        'leave_list': leaves,
        'title': 'Leaves List - Pending'
    }
    return render(request, 'dashboard/leaves_recent.html', dataset)

def leaves_approved_list(request):
    if not (request.user.is_superuser and request.user.is_staff):
        return redirect('/')

    leaves = Leave.objects.all_approved_leaves()
    dataset = {
        'leave_list': leaves,
        'title': 'Approved Leave List'
    }
    return render(request, 'dashboard/leaves_approved.html', dataset)

def leaves_view(request, id):
    if not request.user.is_authenticated:
        return redirect('accounts:login')

    leave = get_object_or_404(Leave, id=id)
    employee = Employee.objects.filter(user=leave.user).first()

    if not employee:
        messages.error(request, 'Employee not found.', extra_tags='alert alert-warning alert-dismissible show')
        return redirect('dashboard:leaveslist')  # Use 'leaveslist' here

    dataset = {
        'leave': leave,
        'employee': employee,
        'title': f'{leave.user.username} - {leave.status} Leave'
    }
    return render(request, 'dashboard/leave_detail_view.html', dataset)

def approve_leave(request, id):
    if not (request.user.is_superuser and request.user.is_authenticated):
        return redirect('/')

    leave = get_object_or_404(Leave, id=id)
    employee = Employee.objects.filter(user=leave.user).first()

    if not employee:
        messages.error(request, 'Employee not found.', extra_tags='alert alert-warning alert-dismissible show')
        return redirect('dashboard:leaveslist')  # Use 'leaveslist' here

    leave.approve_leave()  # Make sure this method updates the leave status properly

    messages.success(request, f'Leave successfully approved for {employee.get_full_name()}.', extra_tags='alert alert-success alert-dismissible show')
    return redirect('dashboard:userleaveview', id=id)

def cancel_leave(request, id):
    if not (request.user.is_superuser and request.user.is_authenticated):
        return redirect('/')

    leave = get_object_or_404(Leave, id=id)
    leave.cancel_leave()  # Make sure this method updates the leave status properly

    messages.success(request, 'Leave is canceled.', extra_tags='alert alert-success alert-dismissible show')
    return redirect('dashboard:canceleaveslist')

def unapprove_leave(request, id):
    if not (request.user.is_authenticated and request.user.is_superuser):
        return redirect('/')

    leave = get_object_or_404(Leave, id=id)
    leave.unapprove_leave()  # Make sure this method updates the leave status properly

    return redirect('dashboard:leaveslist')  # Use 'leaveslist' here

def cancel_leaves_list(request):
    if not (request.user.is_superuser and request.user.is_authenticated):
        return redirect('/')

    leaves = Leave.objects.all_cancel_leaves()
    dataset = {
        'leave_list_cancel': leaves,
        'title': 'Cancel Leave List'
    }
    return render(request, 'dashboard/leaves_cancel.html', dataset)

def uncancel_leave(request, id):
    if not (request.user.is_superuser and request.user.is_authenticated):
        return redirect('/')

    leave = get_object_or_404(Leave, id=id)
    leave.status = 'pending'
    leave.is_approved = False
    leave.save()

    messages.success(request, 'Leave is uncanceled and now in the pending list.', extra_tags='alert alert-success alert-dismissible show')
    return redirect('dashboard:canceleaveslist')

def leave_rejected_list(request):
    leaves = Leave.objects.all_rejected_leaves()
    dataset = {
        'leave_list_rejected': leaves,
        'title': 'Rejected Leaves List'
    }
    return render(request, 'dashboard/rejected_leaves_list.html', dataset)

def reject_leave(request, id):
    leave = get_object_or_404(Leave, id=id)
    leave.reject_leave()  # Make sure this method updates the leave status properly

    messages.success(request, 'Leave is rejected.', extra_tags='alert alert-success alert-dismissible show')
    return redirect('dashboard:leavesrejected')

def unreject_leave(request, id):
    leave = get_object_or_404(Leave, id=id)
    leave.status = 'pending'
    leave.is_approved = False
    leave.save()

    messages.success(request, 'Leave is now in the pending list.', extra_tags='alert alert-success alert-dismissible show')
    return redirect('dashboard:leavesrejected')

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
