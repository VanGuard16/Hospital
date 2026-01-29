from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Department, Doctor, Patient, Appointment
# Register your models here.

@admin.register(User)
class CustomUser(UserAdmin):
    model = User
    list_display = ('username', 'email', 'role', 'is_staff')
    list_filter = ('role', 'is_staff')
    fieldsets = UserAdmin.fieldsets + (
        ('Additional Info', {'fields': ('role', 'phone', 'address')}),
    )
admin.site.register(Department)
admin.site.register(Doctor)
admin.site.register(Patient)
admin.site.register(Appointment)