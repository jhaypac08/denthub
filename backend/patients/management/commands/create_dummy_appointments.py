from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import datetime, timedelta
from patients.models import Patient, Appointment, TreatmentRecord
from employees.models import User
import random


class Command(BaseCommand):
    help = 'Create dummy appointments and treatment records for testing'

    def handle(self, *args, **kwargs):
        # Get all patients and dentists
        patients = list(Patient.objects.all())
        # Get users who have employee records (staff members)
        dentists = list(User.objects.filter(employee__isnull=False, is_active=True))
        
        if not dentists:
            # Fallback to all active users
            dentists = list(User.objects.filter(is_active=True))

        if not patients:
            self.stdout.write(self.style.ERROR('No patients found. Please run create_dummy_patients first.'))
            return

        if not dentists:
            self.stdout.write(self.style.ERROR('No dentists found. Please create users first.'))
            return

        # Clear existing dummy data
        Appointment.objects.all().delete()
        TreatmentRecord.objects.all().delete()

        appointment_types = ['checkup', 'cleaning', 'filling', 'extraction', 'root_canal', 'crown', 'orthodontics', 'cosmetic', 'emergency', 'consultation']
        statuses = ['scheduled', 'confirmed', 'completed', 'cancelled']

        # Create appointments (past, present, and future)
        appointments_created = 0
        for patient in patients:
            dentist = random.choice(dentists)
            
            # Create 2-3 past appointments
            for i in range(random.randint(2, 3)):
                days_ago = random.randint(30, 180)
                appointment_date = (timezone.now() - timedelta(days=days_ago)).date()
                appointment_time = datetime.strptime(f"{random.randint(9, 16)}:00", "%H:%M").time()
                
                appointment = Appointment.objects.create(
                    patient=patient,
                    dentist=dentist,
                    appointment_date=appointment_date,
                    appointment_time=appointment_time,
                    duration=random.choice([30, 60, 90]),
                    appointment_type=random.choice(appointment_types),
                    status='completed',
                    reason=f'Regular {random.choice(["checkup", "cleaning", "follow-up"])}',
                    notes='Appointment completed successfully.'
                )
                appointments_created += 1
                
                # Create treatment record for completed appointment
                TreatmentRecord.objects.create(
                    patient=patient,
                    appointment=appointment,
                    dentist=dentist,
                    treatment_date=appointment_date,
                    tooth_number=random.choice(['11', '12', '21', '22', '31', '32', '41', '42', 'multiple']) if random.random() > 0.3 else '',
                    diagnosis=random.choice([
                        'Dental caries',
                        'Gingivitis',
                        'Periodontitis',
                        'Tooth sensitivity',
                        'Dental plaque buildup',
                        'Tooth discoloration',
                        'Impacted wisdom tooth',
                        'Root canal infection'
                    ]),
                    treatment_performed=random.choice([
                        'Dental cleaning and polishing',
                        'Tooth filling (composite)',
                        'Root canal therapy',
                        'Tooth extraction',
                        'Dental crown placement',
                        'Fluoride treatment',
                        'Teeth whitening',
                        'Scaling and root planing'
                    ]),
                    prescription=random.choice([
                        'Amoxicillin 500mg - 3x daily for 7 days',
                        'Ibuprofen 400mg - as needed for pain',
                        'Chlorhexidine mouthwash - twice daily',
                        'No prescription required',
                        'Paracetamol 500mg - 3x daily for 3 days'
                    ]),
                    cost=random.choice([1500.00, 2500.00, 3500.00, 5000.00, 7500.00, 10000.00]),
                    paid_amount=random.choice([0.00, 1000.00, 1500.00, 2500.00]),  # Some unpaid balances
                    notes='Treatment completed as planned.'
                )
            
            # Create 1 today appointment
            if random.random() > 0.5:
                appointment_time = datetime.strptime(f"{random.randint(9, 16)}:00", "%H:%M").time()
                Appointment.objects.create(
                    patient=patient,
                    dentist=random.choice(dentists),
                    appointment_date=timezone.now().date(),
                    appointment_time=appointment_time,
                    duration=random.choice([30, 60]),
                    appointment_type=random.choice(appointment_types),
                    status=random.choice(['scheduled', 'confirmed', 'in_progress']),
                    reason=f'Today\'s {random.choice(["checkup", "consultation", "treatment"])}',
                    notes='Patient scheduled for today.'
                )
                appointments_created += 1
            
            # Create 2-3 future appointments
            for i in range(random.randint(2, 3)):
                days_ahead = random.randint(1, 60)
                appointment_date = (timezone.now() + timedelta(days=days_ahead)).date()
                appointment_time = datetime.strptime(f"{random.randint(9, 16)}:00", "%H:%M").time()
                
                Appointment.objects.create(
                    patient=patient,
                    dentist=random.choice(dentists),
                    appointment_date=appointment_date,
                    appointment_time=appointment_time,
                    duration=random.choice([30, 60, 90]),
                    appointment_type=random.choice(appointment_types),
                    status=random.choice(['scheduled', 'confirmed']),
                    reason=f'Scheduled {random.choice(["checkup", "cleaning", "follow-up", "treatment"])}',
                    notes='Patient confirmed appointment.'
                )
                appointments_created += 1

        treatments_created = TreatmentRecord.objects.count()

        self.stdout.write(self.style.SUCCESS(f'Successfully created {appointments_created} appointments'))
        self.stdout.write(self.style.SUCCESS(f'Successfully created {treatments_created} treatment records'))
