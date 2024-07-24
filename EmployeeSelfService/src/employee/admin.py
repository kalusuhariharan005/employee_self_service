# employee/admin.py
from django.contrib import admin
from employee.models import Role, Department, Employee, Nationality

class RoleAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'created', 'updated')
    search_fields = ('name',)

class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'created', 'updated')
    search_fields = ('name',)

class NationalityAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'created', 'updated')
    search_fields = ('name',)

class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('get_full_name', 'user', 'department', 'role', 'nationality', 'startdate', 'employeetype', 'employeeid', 'dateissued', 'is_blocked', 'is_deleted', 'created', 'updated')
    search_fields = ('firstname', 'lastname', 'employeeid')
    list_filter = ('department', 'role', 'nationality', 'employeetype', 'is_blocked', 'is_deleted')

admin.site.register(Role, RoleAdmin)
admin.site.register(Department, DepartmentAdmin)
admin.site.register(Nationality, NationalityAdmin)  # Added line
admin.site.register(Employee, EmployeeAdmin)
