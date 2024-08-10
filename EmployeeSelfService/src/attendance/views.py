from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from .models import Attendance
from .forms import AttendanceForm
from django.contrib import messages

@login_required
def mark_attendance(request):
    if request.method == 'POST':
        if 'check_in' in request.POST:
            attendance, created = Attendance.objects.get_or_create(user=request.user, date=timezone.now().date())
            if not created and attendance.check_in:
                messages.error(request, 'You have already checked in today.')
            else:
                attendance.check_in = timezone.now().time()
                attendance.status = 'Present'
                attendance.save()
                messages.success(request, 'Checked in successfully.')
        elif 'check_out' in request.POST:
            attendance = get_object_or_404(Attendance, user=request.user, date=timezone.now().date())
            if not attendance.check_in:
                messages.error(request, 'You must check in before checking out.')
            else:
                attendance.check_out = timezone.now().time()
                attendance.save()
                messages.success(request, 'Checked out successfully.')
        return redirect('attendance:mark_attendance')
    else:
        return render(request, 'attendance/mark_attendance.html')
