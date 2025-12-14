from django.db import models
from employees.models import User
import os
from datetime import datetime


def patient_photo_path(instance, filename):
    """Generate file path for patient photo using patient_id"""
    ext = filename.split('.')[-1]
    filename = f"{instance.patient_id}.{ext}"
    return os.path.join('patient_photos', filename)


def generate_patient_id():
    """Generate patient ID in format PYYMMddHHMMSS"""
    now = datetime.now()
    return f"P{now.strftime('%y%m%d%H%M%S')}"


class Patient(models.Model):
    """Patient model for dental clinic"""
    GENDER_CHOICES = [
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other'),
    ]
    
    BLOOD_TYPE_CHOICES = [
        ('A+', 'A+'),
        ('A-', 'A-'),
        ('B+', 'B+'),
        ('B-', 'B-'),
        ('AB+', 'AB+'),
        ('AB-', 'AB-'),
        ('O+', 'O+'),
        ('O-', 'O-'),
    ]
    
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('inactive', 'Inactive'),
        ('archived', 'Archived'),
    ]
    
    # Basic Information
    patient_id = models.CharField(max_length=20, unique=True, db_index=True)
    first_name = models.CharField(max_length=100)
    middle_name = models.CharField(max_length=100, blank=True, null=True)
    last_name = models.CharField(max_length=100)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    date_of_birth = models.DateField()
    blood_type = models.CharField(max_length=3, choices=BLOOD_TYPE_CHOICES, blank=True, null=True)
    
    # Contact Information
    phone = models.CharField(max_length=15, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    address = models.TextField()
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100, blank=True, null=True)
    postal_code = models.CharField(max_length=20, blank=True, null=True)
    
    # Emergency Contact / Guardian Information
    emergency_contact_name = models.CharField(max_length=200, blank=True, null=True)
    emergency_contact_phone = models.CharField(max_length=15, blank=True, null=True)
    emergency_contact_relation = models.CharField(max_length=50, blank=True, null=True)
    other_relation = models.CharField(max_length=100, blank=True, null=True, help_text="Specify relationship if 'Other' is selected")
    guardian_date_of_birth = models.DateField(blank=True, null=True, help_text="Guardian's date of birth (for minors)")
    guardian_occupation = models.CharField(max_length=100, blank=True, null=True, help_text="Guardian's occupation (for minors)")
    
    # Medical Information
    allergies = models.TextField(blank=True, null=True, help_text="List any allergies")
    medical_conditions = models.TextField(blank=True, null=True, help_text="Existing medical conditions")
    current_medications = models.TextField(blank=True, null=True, help_text="Current medications")
    
    # Dental Information
    dental_insurance = models.CharField(max_length=200, blank=True, null=True)
    insurance_policy_number = models.CharField(max_length=100, blank=True, null=True)
    
    # Photo
    photo = models.ImageField(upload_to=patient_photo_path, blank=True, null=True)
    
    # Status and Metadata
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    notes = models.TextField(blank=True, null=True)
    registered_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='registered_patients')
    registration_date = models.DateField(auto_now_add=True)
    last_visit = models.DateField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'denthub_patient'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['patient_id']),
            models.Index(fields=['last_name', 'first_name']),
            models.Index(fields=['phone']),
        ]
    
    def __str__(self):
        return f"{self.patient_id} - {self.first_name} {self.last_name}"
    
    @property
    def full_name(self):
        if self.middle_name:
            m = str(self.middle_name).strip()
            if len(m) > 0:
                middle = f" {m[0].upper()}."
            else:
                middle = ''
            return f"{self.first_name}{middle} {self.last_name}".strip()
        return f"{self.first_name} {self.last_name}"
    
    @property
    def age(self):
        from datetime import date
        today = date.today()
        age = today.year - self.date_of_birth.year
        if today.month < self.date_of_birth.month or (today.month == self.date_of_birth.month and today.day < self.date_of_birth.day):
            age -= 1
        return age
    
    def save(self, *args, **kwargs):
        """Override save to auto-generate patient_id if not provided"""
        if not self.patient_id:
            # Generate unique patient_id
            patient_id = generate_patient_id()
            # Ensure uniqueness by checking if it exists
            while Patient.objects.filter(patient_id=patient_id).exists():
                import time
                time.sleep(1)  # Wait 1 second to get a different timestamp
                patient_id = generate_patient_id()
            self.patient_id = patient_id
        super().save(*args, **kwargs)


class Appointment(models.Model):
    """Appointment model for patient scheduling"""
    STATUS_CHOICES = [
        ('requested', 'Requested'),
        ('scheduled', 'Scheduled'),
        ('confirmed', 'Confirmed'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
        ('no_show', 'No Show'),
    ]
    
    APPOINTMENT_TYPE_CHOICES = [
        ('checkup', 'Regular Checkup'),
        ('cleaning', 'Teeth Cleaning'),
        ('filling', 'Filling'),
        ('extraction', 'Tooth Extraction'),
        ('root_canal', 'Root Canal'),
        ('crown', 'Crown/Bridge'),
        ('orthodontics', 'Orthodontics'),
        ('cosmetic', 'Cosmetic Procedure'),
        ('emergency', 'Emergency'),
        ('consultation', 'Consultation'),
        ('other', 'Other'),
    ]
    
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='appointments')
    dentist = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='appointments')
    appointment_date = models.DateField()
    appointment_time = models.TimeField()
    duration = models.IntegerField(default=30, help_text="Duration in minutes")
    appointment_type = models.CharField(max_length=50, choices=APPOINTMENT_TYPE_CHOICES)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='requested')
    reason = models.TextField()
    notes = models.TextField(blank=True, null=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='created_appointments')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'denthub_appointment'
        ordering = ['-appointment_date', '-appointment_time']
        indexes = [
            models.Index(fields=['appointment_date', 'appointment_time']),
            models.Index(fields=['patient', 'appointment_date']),
            models.Index(fields=['dentist', 'appointment_date']),
        ]
    
    def __str__(self):
        return f"{self.patient.full_name} - {self.appointment_date} {self.appointment_time}"


class TreatmentRecord(models.Model):
    """Treatment records for patients"""
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='treatment_records')
    appointment = models.ForeignKey(Appointment, on_delete=models.SET_NULL, null=True, blank=True, related_name='treatments')
    dentist = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='treatments_performed')
    treatment_date = models.DateField()
    tooth_number = models.CharField(max_length=10, blank=True, null=True, help_text="Tooth number(s) treated")
    diagnosis = models.TextField()
    treatment_performed = models.TextField()
    prescription = models.TextField(blank=True, null=True)
    cost = models.DecimalField(max_digits=10, decimal_places=2)
    paid_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    notes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'denthub_treatment_record'
        ordering = ['-treatment_date']
    
    def __str__(self):
        return f"{self.patient.full_name} - {self.treatment_date}"
    
    @property
    def balance(self):
        return self.cost - self.paid_amount
