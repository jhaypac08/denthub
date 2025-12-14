from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.utils import timezone
from django.db import models
from datetime import datetime, timedelta
from .models import Patient, Appointment, TreatmentRecord
from employees.models import Message
from .serializers import PatientSerializer, AppointmentSerializer, TreatmentRecordSerializer, MessageSerializer
from employees.logging_utils import log_model_change, get_client_ip


class PatientViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Patient CRUD operations
    """
    serializer_class = PatientSerializer
    permission_classes = [IsAuthenticated]
    queryset = Patient.objects.all()
    
    def get_queryset(self):
        queryset = super().get_queryset()
        
        # Filter by status
        status_filter = self.request.query_params.get('status', None)
        if status_filter:
            queryset = queryset.filter(status=status_filter)
        
        # Search by name or patient_id
        search = self.request.query_params.get('search', None)
        if search:
            queryset = queryset.filter(
                models.Q(patient_id__icontains=search) |
                models.Q(first_name__icontains=search) |
                models.Q(last_name__icontains=search) |
                models.Q(phone__icontains=search)
            )
        
        return queryset
    
    @action(detail=True, methods=['get'])
    def appointments(self, request, pk=None):
        """Get all appointments for a patient"""
        patient = self.get_object()
        appointments = patient.appointments.all()
        serializer = AppointmentSerializer(appointments, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def upload_photo(self, request, pk=None):
        """Upload profile photo for a patient"""
        patient = self.get_object()
        
        if 'photo' not in request.FILES:
            return Response(
                {'error': 'No photo file provided'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Delete old photo if exists
        if patient.photo:
            patient.photo.delete(save=False)
        
        patient.photo = request.FILES['photo']
        patient.save()
        
        serializer = self.get_serializer(patient)
        return Response(serializer.data)
    
    @action(detail=True, methods=['get'])
    def treatments(self, request, pk=None):
        """Get all treatment records for a patient"""
        patient = self.get_object()
        treatments = patient.treatment_records.all()
        serializer = TreatmentRecordSerializer(treatments, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def stats(self, request):
        """Get patient statistics"""
        total = Patient.objects.count()
        active = Patient.objects.filter(status='active').count()
        inactive = Patient.objects.filter(status='inactive').count()
        archived = Patient.objects.filter(status='archived').count()
        
        return Response({
            'total': total,
            'active': active,
            'inactive': inactive,
            'archived': archived
        })
    
    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        if response.status_code == 201:
            # Log patient creation (user creation is handled by signals)
            ip = get_client_ip(request)
            log_model_change(
                request.user,
                'CREATE',
                'Patient',
                response.data.get('id'),
                {
                    'patient_id': response.data.get('patient_id'),
                    'name': response.data.get('full_name')
                },
                ip
            )
        return response
    
    def update(self, request, *args, **kwargs):
        response = super().update(request, *args, **kwargs)
        if response.status_code == 200:
            ip = get_client_ip(request)
            log_model_change(
                request.user,
                'UPDATE',
                'Patient',
                response.data.get('id'),
                {
                    'patient_id': response.data.get('patient_id'),
                    'name': response.data.get('full_name')
                },
                ip
            )
        return response
    
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        patient_id = instance.patient_id
        name = instance.full_name
        
        response = super().destroy(request, *args, **kwargs)
        
        if response.status_code == 204:
            ip = get_client_ip(request)
            log_model_change(
                request.user,
                'DELETE',
                'Patient',
                instance.id,
                {'patient_id': patient_id, 'name': name},
                ip
            )
        return response


class AppointmentViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Appointment CRUD operations
    """
    serializer_class = AppointmentSerializer
    permission_classes = [IsAuthenticated]
    queryset = Appointment.objects.all()
    
    def get_queryset(self):
        queryset = super().get_queryset()
        
        # Filter by status
        status_filter = self.request.query_params.get('status', None)
        if status_filter:
            queryset = queryset.filter(status=status_filter)
        
        # Filter by date range
        date_from = self.request.query_params.get('date_from', None)
        date_to = self.request.query_params.get('date_to', None)
        
        if date_from:
            queryset = queryset.filter(appointment_date__gte=date_from)
        if date_to:
            queryset = queryset.filter(appointment_date__lte=date_to)
        
        # Filter by patient
        patient_id = self.request.query_params.get('patient', None)
        if patient_id:
            queryset = queryset.filter(patient_id=patient_id)
        
        # Filter by dentist
        dentist_id = self.request.query_params.get('dentist', None)
        if dentist_id:
            queryset = queryset.filter(dentist_id=dentist_id)
        
        return queryset
    
    @action(detail=False, methods=['get'])
    def today(self, request):
        """Get today's appointments"""
        today = timezone.now().date()
        # Only include appointments that are scheduled or confirmed for today
        appointments = Appointment.objects.filter(
            appointment_date=today,
            status__in=['scheduled', 'confirmed']
        ).order_by('appointment_time')
        serializer = self.get_serializer(appointments, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def upcoming(self, request):
        """Get upcoming appointments: from tomorrow through seven days ahead (inclusive)"""
        today = timezone.now().date()
        # start at tomorrow, end at 7 days from today (inclusive)
        start = today + timedelta(days=1)
        end = today + timedelta(days=7)
        appointments = Appointment.objects.filter(
            appointment_date__gte=start,
            appointment_date__lte=end,
            status__in=['scheduled', 'confirmed']
        ).order_by('appointment_date', 'appointment_time')
        serializer = self.get_serializer(appointments, many=True)
        return Response(serializer.data)
    
    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        if response.status_code == 201:
            ip = get_client_ip(request)
            log_model_change(
                request.user,
                'CREATE',
                'Appointment',
                response.data.get('id'),
                {
                    'patient': response.data.get('patient_name'),
                    'date': response.data.get('appointment_date')
                },
                ip
            )
        return response
    
    def update(self, request, *args, **kwargs):
        response = super().update(request, *args, **kwargs)
        if response.status_code == 200:
            ip = get_client_ip(request)
            log_model_change(
                request.user,
                'UPDATE',
                'Appointment',
                response.data.get('id'),
                {
                    'patient': response.data.get('patient_name'),
                    'date': response.data.get('appointment_date')
                },
                ip
            )
        return response
    
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        appointment_id = instance.id
        patient_name = instance.patient.full_name
        
        response = super().destroy(request, *args, **kwargs)
        
        if response.status_code == 204:
            ip = get_client_ip(request)
            log_model_change(
                request.user,
                'DELETE',
                'Appointment',
                appointment_id,
                {'patient': patient_name},
                ip
            )
        return response


class TreatmentRecordViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Treatment Record CRUD operations
    """
    serializer_class = TreatmentRecordSerializer
    permission_classes = [IsAuthenticated]
    queryset = TreatmentRecord.objects.all()
    
    def get_queryset(self):
        queryset = super().get_queryset()
        
        # Filter by patient
        patient_id = self.request.query_params.get('patient', None)
        if patient_id:
            queryset = queryset.filter(patient_id=patient_id)
        
        # Filter by dentist
        dentist_id = self.request.query_params.get('dentist', None)
        if dentist_id:
            queryset = queryset.filter(dentist_id=dentist_id)
        
        return queryset
    
    @action(detail=False, methods=['get'])
    def pending_payments(self, request):
        """Get treatment records with pending payments"""
        from django.db.models import F
        treatments = TreatmentRecord.objects.filter(
            paid_amount__lt=F('cost')
        ).order_by('-treatment_date')
        serializer = self.get_serializer(treatments, many=True)
        return Response(serializer.data)
    
    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        if response.status_code == 201:
            ip = get_client_ip(request)
            log_model_change(
                request.user,
                'CREATE',
                'TreatmentRecord',
                response.data.get('id'),
                {
                    'patient': response.data.get('patient_name'),
                    'date': response.data.get('treatment_date')
                },
                ip
            )
        return response
    
    def update(self, request, *args, **kwargs):
        response = super().update(request, *args, **kwargs)
        if response.status_code == 200:
            ip = get_client_ip(request)
            log_model_change(
                request.user,
                'UPDATE',
                'TreatmentRecord',
                response.data.get('id'),
                {
                    'patient': response.data.get('patient_name'),
                    'date': response.data.get('treatment_date')
                },
                ip
            )
        return response
    
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        treatment_id = instance.id
        patient_name = instance.patient.full_name
        
        response = super().destroy(request, *args, **kwargs)
        
        if response.status_code == 204:
            ip = get_client_ip(request)
            log_model_change(
                request.user,
                'DELETE',
                'TreatmentRecord',
                treatment_id,
                {'patient': patient_name},
                ip
            )
        return response


class MessageViewSet(viewsets.ModelViewSet):
    """
    ViewSet for patient messaging
    """
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        user = self.request.user
        # Return messages where user is either sender or receiver (and not deleted)
        return Message.objects.filter(
            (models.Q(sender=user) & models.Q(deleted_by_sender=False)) |
            (models.Q(receiver=user) & models.Q(deleted_by_receiver=False))
        )
    
    @action(detail=False, methods=['get'])
    def inbox(self, request):
        """Get messages received by current user"""
        messages = Message.objects.filter(
            receiver=request.user,
            deleted_by_receiver=False
        ).order_by('-created_at')
        serializer = self.get_serializer(messages, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def sent(self, request):
        """Get messages sent by current user"""
        messages = Message.objects.filter(
            sender=request.user,
            deleted_by_sender=False
        ).order_by('-created_at')
        serializer = self.get_serializer(messages, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def unread_count(self, request):
        """Get count of unread messages for current user"""
        count = Message.objects.filter(
            receiver=request.user,
            is_read=False,
            deleted_by_receiver=False
        ).count()
        return Response({'count': count})
    
    @action(detail=True, methods=['post'])
    def mark_read(self, request, pk=None):
        """Mark a message as read"""
        message = self.get_object()
        
        # Only receiver can mark as read
        if message.receiver != request.user:
            return Response(
                {'error': 'You can only mark your own messages as read'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        if not message.is_read:
            message.is_read = True
            message.read_at = timezone.now()
            message.save()
        
        serializer = self.get_serializer(message)
        return Response(serializer.data)
