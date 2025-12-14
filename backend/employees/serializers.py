from rest_framework import serializers
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import Group
from django.utils import timezone
from .models import Employee, User, Branch, Department, Position, Category, Item, StockMovement, Message

class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ['id', 'name']

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=False)
    groups = serializers.PrimaryKeyRelatedField(
        many=True, 
        queryset=Group.objects.all(), 
        required=False
    )
    group_names = serializers.SerializerMethodField()
    
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'phone', 
                  'is_staff', 'is_active', 'is_superuser', 'date_joined', 'last_login', 
                  'password', 'groups', 'group_names', 'force_password_change']
        read_only_fields = ['id', 'date_joined', 'last_login', 'is_superuser', 'group_names']
        extra_kwargs = {
            'password': {'write_only': True}
        }
    
    def get_group_names(self, obj):
        return [group.name for group in obj.groups.all()]
    
    def create(self, validated_data):
        # Hash password before creating user
        password = validated_data.pop('password', None)
        groups = validated_data.pop('groups', [])
        
        user = User(**validated_data)
        if password:
            user.password = make_password(password)
        user.save()
        
        # Set groups after user is saved
        if groups:
            user.groups.set(groups)
        
        return user
    
    def update(self, instance, validated_data):
        # Hash password if provided during update
        password = validated_data.pop('password', None)
        groups = validated_data.pop('groups', None)
        
        if password:
            instance.password = make_password(password)
        
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        
        instance.save()
        
        # Update groups if provided
        if groups is not None:
            instance.groups.set(groups)
        
        return instance


class BranchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Branch
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'updated_at']


class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'updated_at']


class PositionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Position
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'updated_at']


class EmployeeSerializer(serializers.ModelSerializer):
    position_name = serializers.CharField(source='position.title', read_only=True)
    department_name = serializers.SerializerMethodField()
    branch_name = serializers.CharField(source='branch.name', read_only=True)
    has_user = serializers.SerializerMethodField()
    
    class Meta:
        model = Employee
        fields = '__all__'
        read_only_fields = ['id', 'employee_id', 'created_at', 'updated_at']
    
    def get_has_user(self, obj):
        return obj.user is not None
    
    def get_department_name(self, obj):
        """Return comma-separated list of department names"""
        return ', '.join([dept.name for dept in obj.department.all()])


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'updated_at']


class ItemSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category.name', read_only=True)
    is_low_stock = serializers.BooleanField(read_only=True)
    
    class Meta:
        model = Item
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'updated_at', 'current_stock']


class StockMovementSerializer(serializers.ModelSerializer):
    item_name = serializers.CharField(source='item.name', read_only=True)
    item_code = serializers.CharField(source='item.item_code', read_only=True)
    user_username = serializers.CharField(source='user.username', read_only=True)
    
    class Meta:
        model = StockMovement
        fields = '__all__'
        read_only_fields = ['id', 'date', 'user']
    
    def create(self, validated_data):
        # Set the user from the request context
        request = self.context.get('request')
        if request and hasattr(request, 'user'):
            validated_data['user'] = request.user
        return super().create(validated_data)


class MessageSerializer(serializers.ModelSerializer):
    sender_username = serializers.CharField(source='sender.username', read_only=True)
    sender_name = serializers.SerializerMethodField()
    receiver_username = serializers.CharField(source='receiver.username', read_only=True)
    receiver_name = serializers.SerializerMethodField()
    time_ago = serializers.SerializerMethodField()
    
    class Meta:
        model = Message
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'read_at', 'is_read', 'sender_username', 
                            'sender_name', 'receiver_username', 'receiver_name', 'time_ago']
    
    def get_sender_name(self, obj):
        if obj.sender:
            full_name = f"{obj.sender.first_name} {obj.sender.last_name}".strip()
            return full_name if full_name else obj.sender.username
        return 'System'
    
    def get_receiver_name(self, obj):
        full_name = f"{obj.receiver.first_name} {obj.receiver.last_name}".strip()
        return full_name if full_name else obj.receiver.username
    
    def get_time_ago(self, obj):
        from django.utils.timesince import timesince
        return timesince(obj.created_at) + ' ago'
    
    def create(self, validated_data):
        # Set sender from request if not provided
        request = self.context.get('request')
        if request and hasattr(request, 'user') and not validated_data.get('sender'):
            validated_data['sender'] = request.user
        return super().create(validated_data)

