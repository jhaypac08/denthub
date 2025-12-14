from django.core.management.base import BaseCommand
from website_content.models import HeroSection

class Command(BaseCommand):
    help = 'Populate hero carousel slides with initial data'

    def handle(self, *args, **kwargs):
        # Clear existing slides
        HeroSection.objects.all().delete()
        
        # Create hero slides
        slides = [
            {
                'title': 'Welcome to DentHub Dental Clinic',
                'subtitle': 'Your smile is our priority. Experience world-class dental care with cutting-edge technology and compassionate professionals.',
                'primary_button_text': 'Book Appointment',
                'primary_button_link': '#contact',
                'secondary_button_text': 'Our Services',
                'secondary_button_link': '#services',
                'order': 0,
                'is_active': True
            },
            {
                'title': 'Advanced Dental Technology',
                'subtitle': 'State-of-the-art equipment and modern techniques for the best dental care experience.',
                'primary_button_text': 'Explore Services',
                'primary_button_link': '#services',
                'secondary_button_text': 'Learn More',
                'secondary_button_link': '#about',
                'order': 1,
                'is_active': True
            },
            {
                'title': 'Expert Dental Professionals',
                'subtitle': 'Our experienced team is dedicated to providing you with exceptional care and beautiful smiles.',
                'primary_button_text': 'Find a Location',
                'primary_button_link': '#branches',
                'secondary_button_text': 'Contact Us',
                'secondary_button_link': '#contact',
                'order': 2,
                'is_active': True
            }
        ]
        
        for slide_data in slides:
            HeroSection.objects.create(**slide_data)
            self.stdout.write(self.style.SUCCESS(f'Created slide: {slide_data["title"]}'))
        
        self.stdout.write(self.style.SUCCESS(f'Successfully created {len(slides)} hero slides'))
