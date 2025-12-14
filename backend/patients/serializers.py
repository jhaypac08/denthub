from rest_framework import serializers
from .models import Patient, Appointment, TreatmentRecord
from employees.models import User, Message
from django.utils.timesince import timesince


class PatientSerializer(serializers.ModelSerializer):
    full_name = serializers.CharField(read_only=True)
    age = serializers.IntegerField(read_only=True)
    registered_by_name = serializers.SerializerMethodField()
    patient_id = serializers.CharField(read_only=True)  # Make patient_id read-only since it's auto-generated
    
    class Meta:
        model = Patient
        fields = '__all__'
        read_only_fields = ['id', 'patient_id', 'registration_date', 'created_at', 'updated_at']
    
    def get_registered_by_name(self, obj):
        if obj.registered_by:
            return f"{obj.registered_by.first_name} {obj.registered_by.last_name}" if obj.registered_by.first_name else obj.registered_by.username
        return None
    
    def create(self, validated_data):
        # Auto-assign registered_by from request user
        request = self.context.get('request')
        if request and hasattr(request, 'user'):
            validated_data['registered_by'] = request.user
        return super().create(validated_data)


class AppointmentSerializer(serializers.ModelSerializer):
    patient_name = serializers.CharField(source='patient.full_name', read_only=True)
    patient_id_display = serializers.CharField(source='patient.patient_id', read_only=True)
    dentist_name = serializers.SerializerMethodField()
    created_by_name = serializers.SerializerMethodField()
    
    class Meta:
        model = Appointment
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'updated_at']
    
    def get_dentist_name(self, obj):
        # Prefer the Employee record (denthub_emp) for dentist display when available
        dentist_user = obj.dentist
        if not dentist_user:
            return None

        # If a related Employee record exists, use its names (authoritative)
        try:
            emp = dentist_user.employee
        except Exception:
            emp = None

        if emp:
            # Build full name from employee fields, use middle initial only
            if emp.first_name or emp.last_name:
                middle = ''
                if getattr(emp, 'middle_name', None):
                    m = str(emp.middle_name).strip()
                    if len(m) > 0:
                        middle = f" {m[0].upper()}."
                first = emp.first_name or ''
                last = emp.last_name or ''
                # Use the user id saved on the appointment (dentist FK) as identifier
                identifier = getattr(dentist_user, 'id', None)
                base = f"{first}{middle} {last}".strip()
                return f"{base}{f' - {identifier}' if identifier else ''}".strip()

        # Fallback to the User fields (include user id)
        if dentist_user.first_name or dentist_user.last_name:
            name = f"{dentist_user.first_name} {dentist_user.last_name}".strip()
        else:
            name = dentist_user.username
        identifier = getattr(dentist_user, 'id', None)
        return f"{name}{f' - {identifier}' if identifier else ''}".strip()
    
    def get_created_by_name(self, obj):
        if obj.created_by:
            return f"{obj.created_by.first_name} {obj.created_by.last_name}" if obj.created_by.first_name else obj.created_by.username
        return None
    
    def create(self, validated_data):
        # Auto-assign created_by from request user
        request = self.context.get('request')
        if request and hasattr(request, 'user'):
            validated_data['created_by'] = request.user
        return super().create(validated_data)


class TreatmentRecordSerializer(serializers.ModelSerializer):
    patient_name = serializers.CharField(source='patient.full_name', read_only=True)
    patient_id_display = serializers.CharField(source='patient.patient_id', read_only=True)
    dentist_name = serializers.SerializerMethodField()
    balance = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)
    
    class Meta:
        model = TreatmentRecord
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'updated_at']
    
    def get_dentist_name(self, obj):
        if obj.dentist:
            # Include user id after name
            if obj.dentist.first_name or obj.dentist.last_name:
                name = f"{obj.dentist.first_name} {obj.dentist.last_name}".strip()
            else:
                name = obj.dentist.username
            identifier = getattr(obj.dentist, 'id', None)
            return f"{name}{f' - {identifier}' if identifier else ''}".strip()
        return None


class MessageSerializer(serializers.ModelSerializer):
    sender_name = serializers.SerializerMethodField()
    receiver_name = serializers.SerializerMethodField()
    time_since = serializers.SerializerMethodField()
    
    class Meta:
        model = Message
        fields = '__all__'
        read_only_fields = ['id', 'is_read', 'read_at', 'created_at', 'deleted_by_sender', 'deleted_by_receiver', 'is_pushed']
    
    def get_sender_name(self, obj):
        if obj.sender:
            if obj.sender.first_name and obj.sender.last_name:
                return f"{obj.sender.first_name} {obj.sender.last_name}"
            return obj.sender.username
        return "System"
    
    def get_receiver_name(self, obj):
        if obj.receiver.first_name and obj.receiver.last_name:
            return f"{obj.receiver.first_name} {obj.receiver.last_name}"
        return obj.receiver.username
    
    def get_time_since(self, obj):
        return timesince(obj.created_at)
    
    def create(self, validated_data):
        # Auto-assign sender from request user
        request = self.context.get('request')
        if request and hasattr(request, 'user'):
            validated_data['sender'] = request.user
        return super().create(validated_data)
