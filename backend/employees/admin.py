from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import Employee, User, Branch, Department, Position


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ['username', 'email', 'first_name', 'last_name', 'is_staff']
    fieldsets = BaseUserAdmin.fieldsets + (
        ('Additional Info', {'fields': ('phone',)}),
    )


@admin.register(Branch)
class BranchAdmin(admin.ModelAdmin):
    list_display = ['code', 'name', 'phone', 'manager', 'is_active']
    list_filter = ['is_active']
    search_fields = ['code', 'name', 'manager']
    ordering = ['name']


@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ['code', 'name', 'is_active']
    list_filter = ['is_active']
    search_fields = ['code', 'name']
    ordering = ['name']


@admin.register(Position)
class PositionAdmin(admin.ModelAdmin):
    list_display = ['code', 'title', 'min_salary', 'max_salary', 'is_active']
    list_filter = ['is_active']
    search_fields = ['code', 'title']
    ordering = ['title']


@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ['employee_id', 'get_full_name', 'get_position', 'get_department', 'get_branch', 'status', 'hire_date']
    list_filter = ['status', 'department', 'position', 'branch', 'gender']
    search_fields = ['employee_id', 'first_name', 'middle_name', 'last_name', 'email']
    ordering = ['-created_at']
    
    def get_full_name(self, obj):
        middle = ''
        if obj.middle_name:
            m = str(obj.middle_name).strip()
            if len(m) > 0:
                middle = f" {m[0].upper()}."
        return f"{obj.first_name}{middle} {obj.last_name}".strip()
    get_full_name.short_description = 'Name'
    
    def get_position(self, obj):
        return obj.position.title if obj.position else 'N/A'
    get_position.short_description = 'Position'
    
    def get_department(self, obj):
        return obj.department.name if obj.department else 'N/A'
    get_department.short_description = 'Department'
    
    def get_branch(self, obj):
        return obj.branch.name if obj.branch else 'N/A'
    get_branch.short_description = 'Branch'
