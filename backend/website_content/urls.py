from django.urls import path
from rest_framework.routers import SimpleRouter
from .views import (
    HeroSectionViewSet, ServiceViewSet, AboutSectionViewSet,
    AboutFeatureViewSet, ContactInfoViewSet, SiteSettingsViewSet
    , HolidayViewSet
)

router = SimpleRouter()
router.register(r'hero', HeroSectionViewSet, basename='hero')
router.register(r'services', ServiceViewSet, basename='services')
router.register(r'about', AboutSectionViewSet, basename='about')
router.register(r'about-features', AboutFeatureViewSet, basename='about-features')
router.register(r'contact', ContactInfoViewSet, basename='contact')
router.register(r'settings', SiteSettingsViewSet, basename='settings')
router.register(r'holidays', HolidayViewSet, basename='holidays')

urlpatterns = router.urls
