from django.contrib import admin
from employee.models import Employee, Role, Department, Nationality

class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('firstname', 'lastname', 'get_full_name', 'department', 'role', 'employeeid')  # Adjust as needed
    list_filter = ('department', 'role', 'employeetype')  # Adjust as needed
    search_fields = ('firstname', 'lastname', 'employeeid')
    ordering = ('-created',)

class RoleAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'created', 'updated')
    search_fields = ('name',)
    ordering = ('name',)

class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'created', 'updated')
    search_fields = ('name',)
    ordering = ('name',)

class NationalityAdmin(admin.ModelAdmin):
    list_display = ('name', 'code')
    search_fields = ('name',)
    ordering = ('name',)

admin.site.register(Employee, EmployeeAdmin)
admin.site.register(Role, RoleAdmin)
admin.site.register(Department, DepartmentAdmin)
admin.site.register(Nationality, NationalityAdmin)
