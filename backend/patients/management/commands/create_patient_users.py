from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group
from patients.models import Patient
from employees.models import User


class Command(BaseCommand):
    help = 'Create user accounts for existing patients who don\'t have one'

    def handle(self, *args, **kwargs):
        # Get or create patient group
        patient_group, created = Group.objects.get_or_create(name='patient')
        if created:
            self.stdout.write(self.style.SUCCESS('Created "patient" group'))
        
        # Get all patients
        patients = Patient.objects.all()
        total_patients = patients.count()
        created_users = 0
        skipped_users = 0
        
        self.stdout.write(f'\nProcessing {total_patients} patients...\n')
        
        for patient in patients:
            # Check if user already exists
            if User.objects.filter(username=patient.patient_id).exists():
                self.stdout.write(
                    self.style.WARNING(f'⊗ Skipped {patient.patient_id} - User already exists')
                )
                skipped_users += 1
                continue
            
            try:
                # Create user
                user = User.objects.create_user(
                    username=patient.patient_id,
                    password=patient.last_name,
                    first_name=patient.first_name,
                    last_name=patient.last_name,
                    email=patient.email or '',
                    phone=patient.phone or '',
                    is_staff=False,
                    is_active=True
                )
                
                # Add to patient group
                user.groups.add(patient_group)
                user.save()
                
                self.stdout.write(
                    self.style.SUCCESS(
                        f'✓ Created user for {patient.patient_id} ({patient.full_name}) | '
                        f'Password: {patient.last_name}'
                    )
                )
                created_users += 1
                
            except Exception as e:
                self.stdout.write(
                    self.style.ERROR(f'✗ Error creating user for {patient.patient_id}: {str(e)}')
                )
        
        # Summary
        self.stdout.write('\n' + '=' * 70)
        self.stdout.write(self.style.SUCCESS(f'\nSUMMARY:'))
        self.stdout.write(f'Total patients: {total_patients}')
        self.stdout.write(self.style.SUCCESS(f'Users created: {created_users}'))
        self.stdout.write(self.style.WARNING(f'Users skipped: {skipped_users}'))
        self.stdout.write('=' * 70 + '\n')
