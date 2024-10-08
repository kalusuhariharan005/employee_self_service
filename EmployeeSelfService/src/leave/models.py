from django.db import models
from django.utils.translation import gettext as _
from django.contrib.auth.models import User
from .manager import LeaveManager

SICK = 'sick'
CASUAL = 'casual'
EMERGENCY = 'emergency'
STUDY = 'study'
MATERNITY = 'maternity'
BEREAVEMENT = 'bereavement'
QUARANTINE = 'quarantine'
COMPENSATORY = 'compensatory'
SABBATICAL = 'sabbatical'

LEAVE_TYPE = (
    (SICK, 'Sick Leave'),
    (CASUAL, 'Casual Leave'),
    (EMERGENCY, 'Emergency Leave'),
    (STUDY, 'Study Leave'),
    (MATERNITY, 'Maternity Leave'),
    (BEREAVEMENT, 'Bereavement Leave'),
    (QUARANTINE, 'Self Quarantine'),
    (COMPENSATORY, 'Compensatory Leave'),
    (SABBATICAL, 'Sabbatical Leave')
)

DAYS = 30

class Leave(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    startdate = models.DateField(verbose_name=_('Start Date'), help_text='leave start date is on ..', null=True, blank=False)
    enddate = models.DateField(verbose_name=_('End Date'), help_text='coming back on ...', null=True, blank=False)
    leavetype = models.CharField(choices=LEAVE_TYPE, max_length=25, default=SICK, null=True, blank=False)
    reason = models.CharField(verbose_name=_('Reason for Leave'), max_length=255, help_text='add additional information for leave', null=True, blank=True)
    defaultdays = models.PositiveIntegerField(verbose_name=_('Leave days per year counter'), default=DAYS, null=True, blank=True)

    status = models.CharField(max_length=12, default='pending')  # pending, approved, rejected, cancelled
    is_approved = models.BooleanField(default=False)  # hide

    updated = models.DateTimeField(auto_now=True, auto_now_add=False)
    created = models.DateTimeField(auto_now=False, auto_now_add=True)

    objects = LeaveManager()

    class Meta:
        verbose_name = _('Leave')
        verbose_name_plural = _('Leaves')
        ordering = ['-created']  # recent objects

    def __str__(self):
        return f'{self.leavetype} - {self.user}'

    @property
    def pretty_leave(self):
        leave = self.leavetype
        user = self.user
        employee = user.employee_set.first().get_full_name
        return f'{employee} - {leave}'

    @property
    def leave_days(self):
        if self.startdate > self.enddate:
            return
        dates = (self.enddate - self.startdate)
        return dates.days

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
        if self.is_approved or not self.is_approved:
            self.is_approved = False
            self.status = 'cancelled'
            self.save()

    def reject_leave(self):
        if self.is_approved or not self.is_approved:
            self.is_approved = False
            self.status = 'rejected'
            self.save()

    @property
    def is_rejected(self):
        return self.status == 'rejected'
