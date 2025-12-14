import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'denthub_project.settings')
django.setup()

from patients.models import Patient
from employees.models import User
from django.contrib.auth.models import Group
from datetime import date

print("=" * 70)
print("PATIENT USER AUTO-CREATION VERIFICATION")
print("=" * 70)

# Test 1: Create a new patient and verify user creation
print("\n[TEST 1] Creating new patient P999...")
try:
    # Delete if exists
    Patient.objects.filter(patient_id='P999').delete()
    User.objects.filter(username='P999').delete()
    
    patient = Patient.objects.create(
        patient_id='P999',
        first_name='TestFirst',
        last_name='TestLast',
        gender='male',
        date_of_birth=date(1995, 5, 20),
        phone='09999999999',
        email='test@example.com',
        address='Test Address',
        emergency_contact_name='Emergency Contact',
        emergency_contact_phone='09888888888',
        status='active'
    )
    
    # Check if user was created
    user = User.objects.get(username='P999')
    
    print(f"✓ Patient created: {patient.patient_id}")
    print(f"✓ User auto-created: {user.username}")
    print(f"  - Name: {user.first_name} {user.last_name}")
    print(f"  - Email: {user.email}")
    print(f"  - Groups: {', '.join([g.name for g in user.groups.all()])}")
    
    # Test authentication
    from django.contrib.auth import authenticate
    auth_user = authenticate(username='P999', password='TestLast')
    if auth_user:
        print(f"✓ Authentication successful (password: TestLast)")
    else:
        print(f"✗ Authentication FAILED")
    
    # Cleanup
    patient.delete()
    user.delete()
    print("✓ Cleanup completed\n")
    
except Exception as e:
    print(f"✗ Test failed: {str(e)}\n")

# Test 2: Verify existing patients
print("[TEST 2] Checking existing patients...")
patients = Patient.objects.all()[:5]
print(f"Total patients in database: {Patient.objects.count()}")
print(f"\nChecking first 5 patients:")
print("-" * 70)

for patient in patients:
    try:
        user = User.objects.get(username=patient.patient_id)
        print(f"✓ {patient.patient_id} ({patient.full_name})")
        print(f"  User exists: {user.username} | Groups: {', '.join([g.name for g in user.groups.all()])}")
    except User.DoesNotExist:
        print(f"✗ {patient.patient_id} ({patient.full_name})")
        print(f"  User NOT FOUND - needs to be created manually or re-saved")

# Test 3: Group statistics
print("\n" + "=" * 70)
print("[TEST 3] User Group Statistics")
print("=" * 70)
patient_group = Group.objects.filter(name='patient').first()
if patient_group:
    patient_users = User.objects.filter(groups=patient_group)
    print(f"Total users in 'patient' group: {patient_users.count()}")
    if patient_users.exists():
        print("\nSample users in patient group:")
        for user in patient_users[:5]:
            print(f"  - {user.username} ({user.first_name} {user.last_name})")
else:
    print("'patient' group not found!")

print("\n" + "=" * 70)
print("VERIFICATION COMPLETE")
print("=" * 70)
