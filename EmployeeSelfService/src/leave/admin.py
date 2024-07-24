# leave/admin.py
from django.contrib import admin
from leave.models import Leave

class LeaveAdmin(admin.ModelAdmin):
    list_display = ('user', 'startdate', 'enddate', 'leavetype', 'status', 'created', 'updated')
    search_fields = ('user__username', 'leavetype', 'status')
    list_filter = ('leavetype', 'status')

admin.site.register(Leave, LeaveAdmin)
