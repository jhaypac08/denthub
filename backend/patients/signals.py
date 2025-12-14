from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import Group
from .models import Patient
from employees.models import User
from employees.logging_utils import log_model_change


@receiver(post_save, sender=Patient)
def create_user_for_patient(sender, instance, created, **kwargs):
    """
    Automatically create a user account when a new patient is created.
    Username: patient_id
    Password: last_name
    Group: patient
    """
    if created:  # Only run when a new patient is created
        try:
            # Check if user already exists
            if User.objects.filter(username=instance.patient_id).exists():
                print(f"User {instance.patient_id} already exists. Skipping user creation.")
                return
            
            # Get or create 'patient' group
            patient_group, group_created = Group.objects.get_or_create(name='patient')
            
            # Create user with patient_id as username and last_name as password
            user = User.objects.create_user(
                username=instance.patient_id,
                password=instance.last_name,
                first_name=instance.first_name,
                last_name=instance.last_name,
                email=instance.email or '',
                phone=instance.phone or '',
                is_staff=False,
                is_active=True,
                force_password_change=True  # Force password change on first login
            )
            
            # Add user to patient group
            user.groups.add(patient_group)
            user.save()
            
            print(f"✓ User created for patient {instance.patient_id}: username={user.username}, password={instance.last_name}")
            
            # Log user creation (with system user since this is automatic)
            try:
                system_user = User.objects.filter(is_superuser=True).first()
                if system_user:
                    log_model_change(
                        system_user,
                        'CREATE',
                        'User',
                        user.id,
                        {
                            'username': user.username,
                            'created_for_patient': instance.patient_id,
                            'automatic_creation': True
                        },
                        '127.0.0.1'  # System IP
                    )
            except Exception as log_error:
                print(f"Warning: Could not log user creation: {str(log_error)}")
            
        except Exception as e:
            # Log error but don't fail patient creation
            print(f"✗ Error creating user for patient {instance.patient_id}: {str(e)}")
