from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Attendance
from .forms import AttendanceForm
from django.contrib import messages

@login_required
def mark_attendance(request):
    if request.method == 'POST':
        form = AttendanceForm(request.POST)
        if form.is_valid():
            attendance = form.save(commit=False)
            attendance.user = request.user
            attendance.status = 'Present'
            attendance.save()
            messages.success(request, 'Attendance marked successfully.')
            return redirect('attendance:mark_attendance')
    else:
        form = AttendanceForm()
    return render(request, 'attendance/mark_attendance.html', {'form': form})

@login_required
def view_attendance(request):
    attendance_records = Attendance.objects.filter(user=request.user).order_by('-date')
    return render(request, 'attendance/view_attendance.html', {'attendance_records': attendance_records})
