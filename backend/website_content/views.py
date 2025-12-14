from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import HeroSection, Service, AboutSection, AboutFeature, ContactInfo, SiteSettings
from .serializers import (
    HeroSectionSerializer, ServiceSerializer, AboutSectionSerializer,
    AboutFeatureSerializer, ContactInfoSerializer, SiteSettingsSerializer
)
from .models import Holiday
from .serializers import HolidaySerializer

class HeroSectionViewSet(viewsets.ModelViewSet):
    queryset = HeroSection.objects.all()
    serializer_class = HeroSectionSerializer
    
    def get_permissions(self):
        if self.action in ['list', 'retrieve', 'get_active']:
            return []
        return [IsAuthenticated()]
    
    @action(detail=False, methods=['get'])
    def get_active(self, request):
        """Get the active hero section"""
        hero = HeroSection.objects.filter(is_active=True).first()
        if hero:
            serializer = self.get_serializer(hero)
            return Response(serializer.data)
        return Response({'error': 'No active hero section found'}, status=status.HTTP_404_NOT_FOUND)

class ServiceViewSet(viewsets.ModelViewSet):
    serializer_class = ServiceSerializer
    
    def get_queryset(self):
        # For authenticated users (admin), show all services
        # For public access, show only active services
        if self.request.user.is_authenticated:
            return Service.objects.all()
        return Service.objects.filter(is_active=True)
    
    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return []
        return [IsAuthenticated()]

class AboutSectionViewSet(viewsets.ModelViewSet):
    queryset = AboutSection.objects.all()
    serializer_class = AboutSectionSerializer
    
    def get_permissions(self):
        if self.action in ['list', 'retrieve', 'get_active']:
            return []
        return [IsAuthenticated()]
    
    @action(detail=False, methods=['get'])
    def get_active(self, request):
        """Get the active about section"""
        about = AboutSection.objects.filter(is_active=True).first()
        if about:
            serializer = self.get_serializer(about)
            return Response(serializer.data)
        return Response({'error': 'No active about section found'}, status=status.HTTP_404_NOT_FOUND)

class AboutFeatureViewSet(viewsets.ModelViewSet):
    queryset = AboutFeature.objects.all()
    serializer_class = AboutFeatureSerializer
    permission_classes = [IsAuthenticated]

class ContactInfoViewSet(viewsets.ModelViewSet):
    queryset = ContactInfo.objects.all()
    serializer_class = ContactInfoSerializer
    
    def get_permissions(self):
        if self.action in ['list', 'retrieve', 'get_active']:
            return []
        return [IsAuthenticated()]
    
    @action(detail=False, methods=['get'])
    def get_active(self, request):
        """Get the active contact info"""
        contact = ContactInfo.objects.filter(is_active=True).first()
        if contact:
            serializer = self.get_serializer(contact)
            return Response(serializer.data)
        return Response({'error': 'No active contact info found'}, status=status.HTTP_404_NOT_FOUND)

class SiteSettingsViewSet(viewsets.ModelViewSet):
    queryset = SiteSettings.objects.all()
    serializer_class = SiteSettingsSerializer
    
    def get_permissions(self):
        if self.action in ['list', 'retrieve', 'get_settings']:
            return []
        return [IsAuthenticated()]
    
    @action(detail=False, methods=['get'])
    def get_settings(self, request):
        """Get the first site settings"""
        settings = SiteSettings.objects.first()
        if settings:
            serializer = self.get_serializer(settings)
            return Response(serializer.data)
        return Response({'error': 'No site settings found'}, status=status.HTTP_404_NOT_FOUND)


class HolidayViewSet(viewsets.ModelViewSet):
    queryset = Holiday.objects.all()
    serializer_class = HolidaySerializer

    def get_permissions(self):
        # allow public read access, but restrict modifications to authenticated users
        if self.action in ['list', 'retrieve']:
            return []
        return [IsAuthenticated()]

    def perform_create(self, serializer):
        serializer.save()
