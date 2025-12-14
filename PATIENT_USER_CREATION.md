# Automatic User Creation for Patients

## Overview
When a new patient is created in the Denthub system, a user account is automatically created for them. This allows patients to have login credentials for accessing patient portal features.

## Quick Summary
✓ **Automatic**: Users are created automatically when a patient is created  
✓ **Username**: Patient ID (e.g., `P001`)  
✓ **Password**: Patient's last name (e.g., `Garcia`)  
✓ **Group**: `patient` (limited permissions)  

## Implementation Details

### Automatic User Creation
- **Trigger**: Django signal (`post_save`) on Patient model
- **Location**: `backend/patients/signals.py`
- **When**: Automatically runs whenever a new patient is created (via API, admin panel, or direct database)
- **Registration**: `backend/patients/apps.py` - Signal is registered in the `ready()` method

### User Credentials
When a patient is created, the system automatically creates a user with:

| Field | Value | Example |
|-------|-------|---------|
| **Username** | Patient ID | `P001` |
| **Password** | Patient Last Name | `Garcia` |
| **First Name** | Patient First Name | `Maria` |
| **Last Name** | Patient Last Name | `Garcia` |
| **Email** | Patient Email | `maria.garcia@email.com` |
| **Phone** | Patient Phone | `09123456789` |
| **Group** | `patient` | patient |
| **Is Staff** | `False` | No admin access |
| **Is Active** | `True` | Can login |

### Example
If you create a patient:
- **Patient ID**: `P006`
- **Name**: `Maria Santos`
- **Email**: `maria.santos@email.com`

The system automatically creates:
- **Username**: `P006`
- **Password**: `Santos` (the last name)
- **Group**: `patient`

The patient can now login with:
- Username: `P006`
- Password: `Santos`

## Creating Users for Existing Patients

If you have existing patients without user accounts, run this management command:

```bash
cd backend
python manage.py create_patient_users
```

This will:
- Find all patients without user accounts
- Create users for them with the same credentials (Patient ID as username, Last Name as password)
- Add them to the 'patient' group
- Skip patients who already have users

Example output:
```
Processing 5 patients...

✓ Created user for P005 (Patricia Ramos Santos) | Password: Santos
✓ Created user for P004 (Carlos Dela Cruz) | Password: Cruz
⊗ Skipped P003 - User already exists

SUMMARY:
Total patients: 5
Users created: 2
Users skipped: 3
```

## Security Notes
1. **Default Password**: The last name is used as the default password. Patients should be advised to change their password after first login.
2. **Password Reset**: Patients can reset their password through the standard user password reset mechanism.
3. **Group Permissions**: Users in the 'patient' group have limited permissions - they cannot access the admin panel (`is_staff=False`).
4. **Unique Usernames**: Patient IDs must be unique, which ensures unique usernames.

## Testing

### Automated Test Script
A comprehensive test script is available at `backend/verify_patient_users.py`:

```bash
cd backend
python verify_patient_users.py
```

Expected output:
```
[TEST 1] Creating new patient P999...
✓ User auto-created: P999
✓ Authentication successful (password: TestLast)

[TEST 2] Checking existing patients...
✓ P005 (Patricia Ramos Santos)
  User exists: P005 | Groups: patient
✓ P004 (Carlos Dela Cruz)
  User exists: P004 | Groups: patient

[TEST 3] User Group Statistics
Total users in 'patient' group: 5
```

### Manual Test via Frontend
1. Login to the admin panel
2. Navigate to **Patient Management > Patients**
3. Click **Add Patient**
4. Fill in patient details:
   - Patient ID: `P999`
   - First Name: `Test`
   - Last Name: `User`
   - Other required fields
5. Save the patient
6. Navigate to **Settings > Users**
7. You should see a new user `P999` in the 'patient' group
8. Verify login credentials:
   - Username: `P999`
   - Password: `User`

## Troubleshooting

### User Not Created
If a user is not automatically created:
1. **Check if user already exists**: Run `python manage.py shell -c "from employees.models import User; print(User.objects.filter(username='P001').exists())"`
2. **Verify signals are loaded**: Check Django startup logs for signal import errors
3. **Check patient group exists**: Run `python manage.py shell -c "from django.contrib.auth.models import Group; print(Group.objects.filter(name='patient').exists())"`
4. **View Django logs**: Check the terminal where Django server is running for error messages

### Duplicate Username Error
If the patient_id matches an existing username, the signal will:
- Skip user creation
- Log a message: "User {patient_id} already exists. Skipping user creation."
- Patient creation will succeed, but no user will be created

### Signal Not Firing
Ensure signals are properly registered in `backend/patients/apps.py`:
```python
def ready(self):
    """Import signals when the app is ready"""
    import patients.signals
```

## Verification Queries

### Check if all patients have users
```python
python manage.py shell -c "
from patients.models import Patient
from employees.models import User
patients_without_users = []
for p in Patient.objects.all():
    if not User.objects.filter(username=p.patient_id).exists():
        patients_without_users.append(p.patient_id)
print(f'Patients without users: {patients_without_users}')
"
```

### List all patient users
```python
python manage.py shell -c "
from django.contrib.auth.models import Group
from employees.models import User
patient_group = Group.objects.get(name='patient')
users = User.objects.filter(groups=patient_group)
print(f'Total patient users: {users.count()}')
for u in users:
    print(f'  - {u.username} ({u.first_name} {u.last_name})')
"
```

## Technical Details

### Files Created/Modified
1. **`backend/patients/signals.py`** (NEW) - Signal handler for automatic user creation
2. **`backend/patients/apps.py`** (MODIFIED) - Signal registration in `ready()` method
3. **`backend/patients/views.py`** (MODIFIED) - Removed manual user creation from ViewSet
4. **`backend/patients/management/commands/create_patient_users.py`** (NEW) - Management command for batch user creation

### Signal Flow
```
Patient Created 
    ↓
post_save signal triggered
    ↓
create_user_for_patient() function
    ↓
Check if user exists (username = patient_id)
    ↓ (No)
Create User object
    ↓
Set password = patient.last_name
    ↓
Add to 'patient' group
    ↓
Log creation in audit trail
    ↓
✓ User ready for login
```

### Code Snippet (Signal Handler)
```python
@receiver(post_save, sender=Patient)
def create_user_for_patient(sender, instance, created, **kwargs):
    if created:  # Only for new patients
        if User.objects.filter(username=instance.patient_id).exists():
            return  # Skip if user exists
        
        patient_group, _ = Group.objects.get_or_create(name='patient')
        
        user = User.objects.create_user(
            username=instance.patient_id,
            password=instance.last_name,
            first_name=instance.first_name,
            last_name=instance.last_name,
            email=instance.email or '',
            phone=instance.phone or '',
            is_staff=False,
            is_active=True
        )
        
        user.groups.add(patient_group)
        user.save()
```

## Current Status
✅ Automatic user creation implemented via signals  
✅ All existing patients (P001-P005) have user accounts  
✅ 'patient' group configured with 5 users  
✅ Authentication verified working  
✅ Management command available for batch creation  
✅ Audit logging enabled for user creation  

## Future Enhancements
- [ ] Send welcome email with login credentials
- [ ] Force password change on first login
- [ ] Custom password generation option (stronger passwords)
- [ ] Patient portal for self-service features
- [ ] SMS notification with credentials
- [ ] Password complexity requirements
- [ ] Two-factor authentication for patient accounts
