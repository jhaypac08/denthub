from django.core.management.base import BaseCommand
from patients.models import Patient
from employees.models import User
from datetime import date


class Command(BaseCommand):
    help = 'Create 5 dummy patients for testing'

    def handle(self, *args, **kwargs):
        # Get first user as registered_by
        user = User.objects.first()
        if not user:
            self.stdout.write(self.style.ERROR('No users found. Please create a user first.'))
            return

        patients_data = [
            {
                'patient_id': 'P001',
                'first_name': 'Maria',
                'middle_name': 'Santos',
                'last_name': 'Garcia',
                'gender': 'female',
                'date_of_birth': date(1990, 5, 15),
                'blood_type': 'O+',
                'phone': '09171234567',
                'email': 'maria.garcia@email.com',
                'address': '123 Sampaguita Street, Barangay San Jose',
                'city': 'Manila',
                'state': 'Metro Manila',
                'postal_code': '1000',
                'emergency_contact_name': 'Juan Garcia',
                'emergency_contact_phone': '09187654321',
                'emergency_contact_relation': 'Husband',
                'allergies': 'Penicillin',
                'medical_conditions': 'Hypertension',
                'current_medications': 'Losartan 50mg once daily',
                'dental_insurance': 'PhilHealth',
                'insurance_policy_number': 'PH-123456789',
                'status': 'active',
                'notes': 'Regular checkup every 6 months',
                'registered_by': user
            },
            {
                'patient_id': 'P002',
                'first_name': 'Roberto',
                'middle_name': 'Cruz',
                'last_name': 'Reyes',
                'gender': 'male',
                'date_of_birth': date(1985, 8, 22),
                'blood_type': 'A+',
                'phone': '09181234567',
                'email': 'roberto.reyes@email.com',
                'address': '456 Makabayan Avenue, Barangay Central',
                'city': 'Quezon City',
                'state': 'Metro Manila',
                'postal_code': '1100',
                'emergency_contact_name': 'Ana Reyes',
                'emergency_contact_phone': '09197654321',
                'emergency_contact_relation': 'Wife',
                'allergies': 'None',
                'medical_conditions': 'Diabetes Type 2',
                'current_medications': 'Metformin 500mg twice daily',
                'dental_insurance': 'Maxicare',
                'insurance_policy_number': 'MC-987654321',
                'status': 'active',
                'notes': 'Needs special care due to diabetes',
                'registered_by': user
            },
            {
                'patient_id': 'P003',
                'first_name': 'Jennifer',
                'middle_name': 'Lim',
                'last_name': 'Tan',
                'gender': 'female',
                'date_of_birth': date(1995, 12, 10),
                'blood_type': 'B+',
                'phone': '09191234567',
                'email': 'jennifer.tan@email.com',
                'address': '789 Rizal Street, Barangay Poblacion',
                'city': 'Makati',
                'state': 'Metro Manila',
                'postal_code': '1200',
                'emergency_contact_name': 'Richard Tan',
                'emergency_contact_phone': '09207654321',
                'emergency_contact_relation': 'Father',
                'allergies': 'Latex',
                'medical_conditions': 'None',
                'current_medications': 'None',
                'dental_insurance': 'Medicard',
                'insurance_policy_number': 'MD-456789123',
                'status': 'active',
                'notes': 'Young professional, prefers evening appointments',
                'registered_by': user
            },
            {
                'patient_id': 'P004',
                'first_name': 'Carlos',
                'middle_name': 'Dela',
                'last_name': 'Cruz',
                'gender': 'male',
                'date_of_birth': date(1978, 3, 28),
                'blood_type': 'AB+',
                'phone': '09201234567',
                'email': 'carlos.delacruz@email.com',
                'address': '321 Bonifacio Drive, Barangay Veterans',
                'city': 'Pasig',
                'state': 'Metro Manila',
                'postal_code': '1600',
                'emergency_contact_name': 'Carmen Dela Cruz',
                'emergency_contact_phone': '09217654321',
                'emergency_contact_relation': 'Wife',
                'allergies': 'Aspirin',
                'medical_conditions': 'Asthma',
                'current_medications': 'Salbutamol inhaler as needed',
                'dental_insurance': 'Intellicare',
                'insurance_policy_number': 'IC-789123456',
                'status': 'active',
                'notes': 'Requires pre-medication before dental procedures',
                'registered_by': user
            },
            {
                'patient_id': 'P005',
                'first_name': 'Patricia',
                'middle_name': 'Ramos',
                'last_name': 'Santos',
                'gender': 'female',
                'date_of_birth': date(2000, 7, 5),
                'blood_type': 'O-',
                'phone': '09211234567',
                'email': 'patricia.santos@email.com',
                'address': '654 Luna Street, Barangay Santolan',
                'city': 'Pasig',
                'state': 'Metro Manila',
                'postal_code': '1610',
                'emergency_contact_name': 'Rosa Santos',
                'emergency_contact_phone': '09227654321',
                'emergency_contact_relation': 'Mother',
                'allergies': 'None',
                'medical_conditions': 'None',
                'current_medications': 'None',
                'dental_insurance': 'PhilHealth',
                'insurance_policy_number': 'PH-321654987',
                'status': 'active',
                'notes': 'Student, prefers weekend appointments',
                'registered_by': user
            }
        ]

        created_count = 0
        for patient_data in patients_data:
            # Check if patient already exists
            if not Patient.objects.filter(patient_id=patient_data['patient_id']).exists():
                Patient.objects.create(**patient_data)
                created_count += 1
                self.stdout.write(self.style.SUCCESS(f'Created patient: {patient_data["patient_id"]} - {patient_data["first_name"]} {patient_data["last_name"]}'))
            else:
                self.stdout.write(self.style.WARNING(f'Patient {patient_data["patient_id"]} already exists, skipping...'))

        self.stdout.write(self.style.SUCCESS(f'\nTotal patients created: {created_count}'))
