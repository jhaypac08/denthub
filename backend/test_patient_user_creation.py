import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'denthub_project.settings')
django.setup()

from patients.models import Patient
from employees.models import User
from django.contrib.auth.models import Group
from datetime import date

# Check existing patients and users
print("=== Before Test ===")
print(f"Total patients: {Patient.objects.count()}")
print(f"Total users: {User.objects.count()}")
print(f"Users in 'patient' group: {User.objects.filter(groups__name='patient').count()}")

# Create a test patient
print("\n=== Creating Test Patient ===")
test_patient = Patient.objects.create(
    patient_id='TEST001',
    first_name='John',
    middle_name='Michael',
    last_name='Doe',
    gender='male',
    date_of_birth=date(1990, 1, 15),
    phone='09123456789',
    email='john.doe@example.com',
    address='123 Test Street, Test City',
    blood_type='O+',
    emergency_contact_name='Jane Doe',
    emergency_contact_phone='09187654321',
    status='active'
)
print(f"Patient created: {test_patient.patient_id} - {test_patient.full_name}")

# Check if user was created
print("\n=== Checking User Creation ===")
try:
    user = User.objects.get(username=test_patient.patient_id)
    print(f"✓ User found: {user.username}")
    print(f"  - Name: {user.first_name} {user.last_name}")
    print(f"  - Email: {user.email}")
    print(f"  - Phone: {user.phone}")
    print(f"  - Is staff: {user.is_staff}")
    print(f"  - Groups: {', '.join([g.name for g in user.groups.all()])}")
    
    # Test login with last name as password
    from django.contrib.auth import authenticate
    auth_user = authenticate(username=test_patient.patient_id, password=test_patient.last_name)
    if auth_user:
        print(f"✓ Password authentication successful (password: {test_patient.last_name})")
    else:
        print(f"✗ Password authentication failed")
        
except User.DoesNotExist:
    print("✗ User NOT found - automatic creation failed!")

# Cleanup
print("\n=== Cleanup ===")
test_patient.delete()
try:
    user = User.objects.get(username='TEST001')
    user.delete()
    print("Test patient and user deleted")
except User.DoesNotExist:
    print("Test patient deleted (user was not created)")

print("\n=== After Test ===")
print(f"Total patients: {Patient.objects.count()}")
print(f"Total users: {User.objects.count()}")
