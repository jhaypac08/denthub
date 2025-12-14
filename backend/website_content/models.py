from django.db import models
from django.core.validators import MaxValueValidator

class HeroSection(models.Model):
    ICON_CHOICES = [
        ('fa-tooth', 'Tooth'),
        ('fa-teeth', 'Teeth'),
        ('fa-smile-beam', 'Smile Beam'),
        ('fa-user-md', 'Doctor'),
        ('fa-star', 'Star'),
        ('fa-heart', 'Heart'),
        ('fa-shield-alt', 'Shield'),
        ('fa-award', 'Award'),
        ('fa-magic', 'Magic'),
        ('fa-crown', 'Crown'),
    ]
    
    title = models.CharField(max_length=200, default="Welcome to DentHub Dental Clinic")
    subtitle = models.TextField(default="Your smile is our priority. Experience world-class dental care with cutting-edge technology and compassionate professionals.")
    primary_button_text = models.CharField(max_length=50, default="Book Appointment")
    primary_button_link = models.CharField(max_length=200, default="#contact")
    secondary_button_text = models.CharField(max_length=50, default="Our Services")
    secondary_button_link = models.CharField(max_length=200, default="#services")
    background_image = models.ImageField(upload_to='hero_images/', null=True, blank=True, help_text="Upload HD background image for this slide")
    icon = models.CharField(max_length=50, choices=ICON_CHOICES, default='fa-tooth', help_text="Icon to display when no background image is set")
    order = models.IntegerField(default=0, validators=[MaxValueValidator(4)], help_text="Display order in carousel (0-4, maximum 5 slides)")
    is_active = models.BooleanField(default=True)
    
    class Meta:
        verbose_name = "Hero Slide"
        verbose_name_plural = "Hero Slides"
        ordering = ['order']
    
    def __str__(self):
        return f"Slide {self.order}: {self.title[:50]}"
    
    def save(self, *args, **kwargs):
        # Ensure maximum of 5 slides (0-4)
        if self.order > 4:
            self.order = 4
        super().save(*args, **kwargs)

class Service(models.Model):
    ICON_CHOICES = [
        ('fa-teeth', 'Teeth'),
        ('fa-smile-beam', 'Smile Beam'),
        ('fa-tooth', 'Tooth'),
        ('fa-user-md', 'Doctor'),
        ('fa-crown', 'Crown'),
        ('fa-child', 'Child'),
        ('fa-x-ray', 'X-Ray'),
        ('fa-syringe', 'Syringe'),
    ]
    
    title = models.CharField(max_length=100)
    description = models.TextField()
    icon = models.CharField(max_length=50, choices=ICON_CHOICES, default='fa-tooth')
    order = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        ordering = ['order', 'title']
    
    def __str__(self):
        return self.title

class AboutSection(models.Model):
    title = models.CharField(max_length=200, default="About DentHub")
    description = models.TextField(default="DentHub Dental Clinic has been serving the community with exceptional dental care for over a decade.")
    
    # Stats
    patients_count = models.CharField(max_length=20, default="10,000+")
    patients_label = models.CharField(max_length=50, default="Happy Patients")
    years_count = models.CharField(max_length=20, default="15+")
    years_label = models.CharField(max_length=50, default="Years Experience")
    dentists_count = models.CharField(max_length=20, default="25+")
    dentists_label = models.CharField(max_length=50, default="Expert Dentists")
    
    is_active = models.BooleanField(default=True)
    
    class Meta:
        verbose_name = "About Section"
        verbose_name_plural = "About Section"
    
    def __str__(self):
        return f"About Section - {self.title}"

class AboutFeature(models.Model):
    about_section = models.ForeignKey(AboutSection, on_delete=models.CASCADE, related_name='features')
    text = models.CharField(max_length=200)
    order = models.IntegerField(default=0)
    
    class Meta:
        ordering = ['order']
    
    def __str__(self):
        return self.text

class ContactInfo(models.Model):
    section_title = models.CharField(max_length=200, default="Contact Us")
    section_subtitle = models.TextField(default="Get in touch with us for appointments or inquiries")
    
    # Social Links
    facebook_url = models.URLField(blank=True, null=True)
    twitter_url = models.URLField(blank=True, null=True)
    instagram_url = models.URLField(blank=True, null=True)
    linkedin_url = models.URLField(blank=True, null=True)
    
    # Footer Text
    footer_text = models.TextField(default="© 2024 DentHub Dental Clinic. All rights reserved.")
    
    is_active = models.BooleanField(default=True)
    
    class Meta:
        verbose_name = "Contact Information"
        verbose_name_plural = "Contact Information"
    
    def __str__(self):
        return "Contact Information"

class SiteSettings(models.Model):
    site_name = models.CharField(max_length=100, default="DentHub")
    patient_portal_url = models.URLField(default="http://192.168.1.18:5173")
    primary_color = models.CharField(max_length=7, default="#00B2A9", help_text="Hex color code")
    secondary_color = models.CharField(max_length=7, default="#0097A7", help_text="Hex color code")
    carousel_interval = models.IntegerField(default=5000, help_text="Carousel auto-slide interval in milliseconds (e.g., 5000 = 5 seconds)")
    
    class Meta:
        verbose_name = "Site Settings"
        verbose_name_plural = "Site Settings"
    
    def __str__(self):
        return f"Site Settings - {self.site_name}"


class Holiday(models.Model):
    """Represents a holiday entry. Can be a recurring annual holiday (month/day)
    or a single specific date (specific_date)."""
    name = models.CharField(max_length=200)
    is_recurring = models.BooleanField(default=True, help_text="If true, use month/day as an annual recurrence")
    month = models.PositiveSmallIntegerField(null=True, blank=True, validators=[MaxValueValidator(12)])
    day = models.PositiveSmallIntegerField(null=True, blank=True, validators=[MaxValueValidator(31)])
    specific_date = models.DateField(null=True, blank=True, help_text="Optional specific date for one-off holidays")
    notes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    HOLIDAY_TYPE_CHOICES = [
        ('regular', 'Regular Holiday'),
        ('special_non_working', 'Special (Non-Working)'),
        ('special_working', 'Special (Working)')
    ]
    holiday_type = models.CharField(max_length=32, choices=HOLIDAY_TYPE_CHOICES, default='regular', help_text='Type of holiday')
    pay_multiplier = models.DecimalField(max_digits=4, decimal_places=2, default=1.00, help_text='Multiplier applied when employees work on this holiday (e.g., 1.30 for 30% additional, 2.00 for double pay)')

    class Meta:
        ordering = ['is_recurring', 'month', 'day', 'specific_date', 'name']

    def __str__(self):
        if self.is_recurring and self.month and self.day:
            return f"{self.name} ({self.month:02d}-{self.day:02d})"
        if self.specific_date:
            return f"{self.name} ({self.specific_date})"
        return self.name
