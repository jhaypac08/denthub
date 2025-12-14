from django.contrib import admin
from .models import Patient, Appointment, TreatmentRecord


@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    list_display = ['patient_id', 'full_name', 'phone', 'status', 'registration_date']
    list_filter = ['status', 'gender', 'registration_date']
    search_fields = ['patient_id', 'first_name', 'last_name', 'phone', 'email']
    ordering = ['-registration_date']


@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ['patient', 'appointment_date', 'appointment_time', 'appointment_type', 'status', 'dentist']
    list_filter = ['status', 'appointment_type', 'appointment_date']
    search_fields = ['patient__first_name', 'patient__last_name', 'patient__patient_id']
    ordering = ['-appointment_date', '-appointment_time']


@admin.register(TreatmentRecord)
class TreatmentRecordAdmin(admin.ModelAdmin):
    list_display = ['patient', 'treatment_date', 'dentist', 'cost', 'paid_amount', 'balance']
    list_filter = ['treatment_date']
    search_fields = ['patient__first_name', 'patient__last_name', 'patient__patient_id', 'diagnosis']
    ordering = ['-treatment_date']
    
    def balance(self, obj):
        return obj.balance
    balance.short_description = 'Balance'
