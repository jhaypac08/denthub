from django.core.management.base import BaseCommand
from website_content.models import HeroSection, Service, AboutSection, AboutFeature, ContactInfo, SiteSettings

class Command(BaseCommand):
    help = 'Populate initial website content'

    def handle(self, *args, **kwargs):
        # Create Hero Section
        hero, created = HeroSection.objects.get_or_create(
            defaults={
                'title': 'Welcome to DentHub Dental Clinic',
                'subtitle': 'Your smile is our priority. Experience world-class dental care with cutting-edge technology and compassionate professionals.',
                'primary_button_text': 'Book Appointment',
                'primary_button_link': '#contact',
                'secondary_button_text': 'Our Services',
                'secondary_button_link': '#services',
                'is_active': True
            }
        )
        if created:
            self.stdout.write(self.style.SUCCESS('Created Hero Section'))

        # Create Services
        services_data = [
            {
                'title': 'General Dentistry',
                'description': 'Regular checkups, cleanings, fillings, and preventive care to maintain your oral health.',
                'icon': 'fa-teeth',
                'order': 0
            },
            {
                'title': 'Cosmetic Dentistry',
                'description': 'Teeth whitening, veneers, and smile makeovers to enhance your appearance.',
                'icon': 'fa-smile-beam',
                'order': 1
            },
            {
                'title': 'Orthodontics',
                'description': 'Braces, aligners, and other treatments to straighten and align your teeth.',
                'icon': 'fa-tooth',
                'order': 2
            },
            {
                'title': 'Oral Surgery',
                'description': 'Tooth extractions, wisdom teeth removal, and other surgical procedures.',
                'icon': 'fa-user-md',
                'order': 3
            },
            {
                'title': 'Dental Implants',
                'description': 'Permanent tooth replacement solutions for missing teeth.',
                'icon': 'fa-crown',
                'order': 4
            },
            {
                'title': 'Pediatric Dentistry',
                'description': 'Specialized care for children\'s dental health and development.',
                'icon': 'fa-child',
                'order': 5
            }
        ]

        for service_data in services_data:
            service, created = Service.objects.get_or_create(
                title=service_data['title'],
                defaults={
                    'description': service_data['description'],
                    'icon': service_data['icon'],
                    'order': service_data['order'],
                    'is_active': True
                }
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f'Created Service: {service.title}'))

        # Create About Section
        about, created = AboutSection.objects.get_or_create(
            defaults={
                'title': 'About DentHub',
                'description': 'DentHub Dental Clinic has been serving the community with exceptional dental care for over a decade. Our team of experienced dentists and modern facilities ensure you receive the best treatment possible.',
                'patients_count': '10,000+',
                'patients_label': 'Happy Patients',
                'years_count': '15+',
                'years_label': 'Years Experience',
                'dentists_count': '25+',
                'dentists_label': 'Expert Dentists',
                'is_active': True
            }
        )
        if created:
            self.stdout.write(self.style.SUCCESS('Created About Section'))

            # Create About Features
            features_data = [
                'State-of-the-art Equipment',
                'Experienced Professionals',
                'Flexible Scheduling',
                'Affordable Pricing'
            ]

            for idx, feature_text in enumerate(features_data):
                AboutFeature.objects.create(
                    about_section=about,
                    text=feature_text,
                    order=idx
                )
            self.stdout.write(self.style.SUCCESS('Created About Features'))

        # Create Contact Info
        contact, created = ContactInfo.objects.get_or_create(
            defaults={
                'section_title': 'Contact Us',
                'section_subtitle': 'Get in touch with us for appointments or inquiries',
                'facebook_url': 'https://facebook.com/denthub',
                'twitter_url': 'https://twitter.com/denthub',
                'instagram_url': 'https://instagram.com/denthub',
                'linkedin_url': 'https://linkedin.com/company/denthub',
                'footer_text': '© 2024 DentHub Dental Clinic. All rights reserved.',
                'is_active': True
            }
        )
        if created:
            self.stdout.write(self.style.SUCCESS('Created Contact Info'))

        # Create Site Settings
        settings, created = SiteSettings.objects.get_or_create(
            defaults={
                'site_name': 'DentHub',
                'patient_portal_url': 'http://192.168.1.18:5174',
                'primary_color': '#00B2A9',
                'secondary_color': '#0097A7'
            }
        )
        if created:
            self.stdout.write(self.style.SUCCESS('Created Site Settings'))

        self.stdout.write(self.style.SUCCESS('Website content initialization complete!'))
