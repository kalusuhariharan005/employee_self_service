# leave/models.py
from django.db import models
from django.contrib.auth.models import User

class Leave(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    startdate = models.DateField(verbose_name='Start Date', help_text='Leave start date is on ..')
    enddate = models.DateField(verbose_name='End Date', help_text='Coming back on ..')
    
    LEAVE_TYPE_CHOICES = [
        ('sick', 'Sick Leave'),
        ('casual', 'Casual Leave'),
        ('emergency', 'Emergency Leave'),
        ('study', 'Study Leave'),
        ('maternity', 'Maternity Leave'),
        ('bereavement', 'Bereavement Leave'),
        ('quarantine', 'Self Quarantine'),
        ('compensatory', 'Compensatory Leave'),
        ('sabbatical', 'Sabbatical Leave')
    ]
    leavetype = models.CharField(max_length=20, choices=LEAVE_TYPE_CHOICES, default='sick')
    reason = models.TextField(verbose_name='Reason for Leave', max_length=255, blank=True, null=True)
    defaultdays = models.IntegerField(verbose_name='Leave days per year counter', default=30, blank=True, null=True)
    
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('cancelled', 'Cancelled')
    ]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    is_approved = models.BooleanField(default=False)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Leave'
        verbose_name_plural = 'Leaves'
        ordering = ['-created']

    def __str__(self):
        return f'{self.leavetype} - {self.user}'

    @property
    def pretty_leave(self):
        return f'{self.user} - {self.leavetype}'

    @property
    def leave_days(self):
        if self.startdate and self.enddate:
            if self.startdate > self.enddate:
                return 0
            return (self.enddate - self.startdate).days + 1
        return 0

    @property
    def is_rejected(self):
        return self.status == 'rejected'

    def approve_leave(self):
        if not self.is_approved:
            self.is_approved = True
            self.status = 'approved'
            self.save()

    def unapprove_leave(self):
        if self.is_approved:
            self.is_approved = False
            self.status = 'pending'
            self.save()

    def cancel_leave(self):
        self.is_approved = False
        self.status = 'cancelled'
        self.save()

    def reject_leave(self):
        self.is_approved = False
        self.status = 'rejected'
        self.save()
