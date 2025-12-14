from django.contrib import admin
from .models import HeroSection, Service, AboutSection, AboutFeature, ContactInfo, SiteSettings, Holiday

class HolidayAdmin(admin.ModelAdmin):
    list_display = ('name', 'holiday_type', 'is_recurring', 'month', 'day', 'specific_date', 'pay_multiplier')
    list_filter = ('holiday_type', 'is_recurring')
    search_fields = ('name',)
    readonly_fields = ('created_at',)


class AboutFeatureInline(admin.TabularInline):
    model = AboutFeature
    extra = 1

@admin.register(HeroSection)
class HeroSectionAdmin(admin.ModelAdmin):
    list_display = ['title', 'is_active']
    list_filter = ['is_active']

@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ['title', 'icon', 'order', 'is_active']
    list_filter = ['is_active']
    list_editable = ['order', 'is_active']

@admin.register(AboutSection)
class AboutSectionAdmin(admin.ModelAdmin):
    list_display = ['title', 'is_active']
    inlines = [AboutFeatureInline]

@admin.register(ContactInfo)
class ContactInfoAdmin(admin.ModelAdmin):
    list_display = ['section_title', 'is_active']

@admin.register(SiteSettings)
class SiteSettingsAdmin(admin.ModelAdmin):
    list_display = ['site_name', 'patient_portal_url']


# Register Holiday
admin.site.register(Holiday, HolidayAdmin)
