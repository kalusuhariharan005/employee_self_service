from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Attendance(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField(default=timezone.now)
    check_in = models.TimeField(null=True, blank=True)
    check_out = models.TimeField(null=True, blank=True)
    status = models.CharField(max_length=10, default='Absent')

    def __str__(self):
        return f"{self.user.username} - {self.date}"

    @property
    def worked_hours(self):
        if self.check_in and self.check_out:
            return (self.check_out - self.check_in).seconds // 3600
        return 0
