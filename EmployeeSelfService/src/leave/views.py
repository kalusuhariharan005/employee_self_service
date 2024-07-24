# leave/views.py
from django.shortcuts import render, redirect
from django import forms
from django.http import HttpResponse
import mongoengine as me
from .models import Leave

class LeaveForm(forms.Form):
    user = forms.CharField(max_length=255)
    startdate = forms.DateField()
    enddate = forms.DateField()
    leavetype = forms.ChoiceField(choices=[
        ('sick', 'Sick Leave'),
        ('casual', 'Casual Leave'),
        ('emergency', 'Emergency Leave'),
        ('study', 'Study Leave'),
        ('maternity', 'Maternity Leave'),
        ('bereavement', 'Bereavement Leave'),
        ('quarantine', 'Self Quarantine'),
        ('compensatory', 'Compensatory Leave'),
        ('sabbatical', 'Sabbatical Leave')
    ])
    reason = forms.CharField(max_length=255, required=False)
    status = forms.ChoiceField(choices=[
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('cancelled', 'Cancelled')
    ])

def leave_list(request):
    leaves = Leave.objects()
    return render(request, 'leave_list.html', {'leaves': leaves})

def leave_create(request):
    if request.method == 'POST':
        form = LeaveForm(request.POST)
        if form.is_valid():
            Leave(
                user=form.cleaned_data['user'],
                startdate=form.cleaned_data['startdate'],
                enddate=form.cleaned_data['enddate'],
                leavetype=form.cleaned_data['leavetype'],
                reason=form.cleaned_data['reason'],
                status=form.cleaned_data['status']
            ).save()
            return redirect('leave_list')
    else:
        form = LeaveForm()
    return render(request, 'leave_form.html', {'form': form})
