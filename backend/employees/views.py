from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import Group
from django.middleware.csrf import get_token
from django.views.decorators.csrf import ensure_csrf_cookie
from django.utils import timezone
from django.db import models
from rest_framework import viewsets, status
from rest_framework.decorators import api_view, permission_classes, action
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.contrib.auth.hashers import make_password
from .models import Employee, User, Branch, Department, Position, Category, Item, StockMovement, Message
from .serializers import (
    EmployeeSerializer, UserSerializer, BranchSerializer, 
    DepartmentSerializer, PositionSerializer, GroupSerializer,
    CategorySerializer, ItemSerializer, StockMovementSerializer, MessageSerializer
)
from .logging_utils import (
    log_action, log_model_change, log_login, log_logout, 
    log_password_change, get_client_ip, get_changed_fields
)


class UserViewSet(viewsets.ModelViewSet):
    """
    ViewSet for User CRUD operations with logging
    Password hashing is handled in UserSerializer
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
    
    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        if response.status_code == 201:
            ip = get_client_ip(request)
            log_model_change(
                request.user,
                'CREATE',
                'User',
                response.data.get('id'),
                {'username': response.data.get('username')},
                ip
            )
        return response
    
    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        old_data = UserSerializer(instance).data
        response = super().update(request, *args, **kwargs)
        
        if response.status_code == 200:
            ip = get_client_ip(request)
            changes = get_changed_fields(instance, request.data)
            log_model_change(
                request.user,
                'UPDATE',
                'User',
                instance.id,
                changes,
                ip
            )
        return response
    
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        user_id = instance.id
        username = instance.username
        response = super().destroy(request, *args, **kwargs)
        
        if response.status_code == 204:
            ip = get_client_ip(request)
            log_model_change(
                request.user,
                'DELETE',
                'User',
                user_id,
                {'username': username},
                ip
            )
        return response


class GroupViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Group CRUD operations
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [IsAuthenticated]


@api_view(['GET'])
@permission_classes([AllowAny])
@ensure_csrf_cookie
def get_csrf_token(request):
    """Get CSRF token"""
    return Response({'detail': 'CSRF cookie set'})


@api_view(['POST'])
@permission_classes([AllowAny])
@ensure_csrf_cookie
def login_view(request):
    """Login endpoint with logging"""
    username = request.data.get('username')
    password = request.data.get('password')
    ip = get_client_ip(request)
    
    if not username or not password:
        log_login(username, False, ip, 'Missing credentials')
        return Response(
            {'error': 'Please provide both username and password'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    user = authenticate(request, username=username, password=password)
    
    if user is not None:
        login(request, user)
        log_login(user, True, ip)
        return Response({
            'message': 'Login successful',
            'user': UserSerializer(user).data
        })
    else:
        log_login(username, False, ip, 'Invalid credentials')
        return Response(
            {'error': 'Invalid credentials'},
            status=status.HTTP_401_UNAUTHORIZED
        )


@api_view(['POST'])
@permission_classes([AllowAny])
def logout_view(request):
    """Logout endpoint with logging"""
    user = request.user if request.user.is_authenticated else None
    ip = get_client_ip(request)
    
    if user:
        log_logout(user, ip)
    
    logout(request)
    return Response({'message': 'Logout successful'})


@api_view(['GET'])
@permission_classes([AllowAny])  # Temporarily change to AllowAny for debugging
def current_user(request):
    """Get current logged in user"""
    print(f"Session Key: {request.session.session_key}")
    print(f"User: {request.user}")
    print(f"Is Authenticated: {request.user.is_authenticated}")
    print(f"Cookies: {request.COOKIES}")
    
    if request.user.is_authenticated:
        return Response(UserSerializer(request.user).data)
    else:
        return Response(
            {'detail': 'Authentication credentials were not provided.'},
            status=status.HTTP_401_UNAUTHORIZED
        )


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def change_password(request):
    """Change user password"""
    current_password = request.data.get('current_password')
    new_password = request.data.get('new_password')
    ip = get_client_ip(request)
    
    if not current_password or not new_password:
        return Response(
            {'error': 'Both current and new password are required'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    # Verify current password
    if not request.user.check_password(current_password):
        log_password_change(request.user, False, ip)
        return Response(
            {'error': 'Current password is incorrect'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    # Set new password
    request.user.set_password(new_password)
    request.user.force_password_change = False  # Clear force password change flag
    request.user.save()
    
    log_password_change(request.user, True, ip)
    
    return Response({
        'message': 'Password changed successfully'
    })


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_user_account(request):
    """Create user account for employee with logging"""
    employee_id = request.data.get('employee_id')
    ip = get_client_ip(request)
    
    if not employee_id:
        return Response(
            {'error': 'Employee ID is required'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    try:
        employee = Employee.objects.get(employee_id=employee_id)
        
        # Check if employee already has a user account
        if employee.user:
            return Response(
                {'error': 'Employee already has a user account'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Create user with employee_id as username
        # Default password is employee_id (should be changed on first login)
        user = User.objects.create_user(
            username=employee.employee_id,
            email=employee.email,
            password=employee.employee_id,  # Default password
            first_name=employee.first_name,
            last_name=employee.last_name,
            phone=employee.phone
        )
        
        # Link user to employee
        employee.user = user
        employee.save()
        
        # Log the action
        log_action(
            request.user,
            'Created User Account from Employee',
            {
                'employee_id': employee.employee_id,
                'username': user.username,
                'employee_name': f"{employee.first_name} {employee.last_name}"
            },
            ip,
            'SUCCESS'
        )
        
        return Response({
            'message': 'User account created successfully',
            'username': user.username,
            'default_password': employee.employee_id,
            'user': UserSerializer(user).data
        })
        
    except Employee.DoesNotExist:
        log_action(
            request.user,
            'Create User Account Failed',
            {'employee_id': employee_id, 'reason': 'Employee not found'},
            ip,
            'FAILED'
        )
        return Response(
            {'error': 'Employee not found'},
            status=status.HTTP_404_NOT_FOUND
        )
    except Exception as e:
        log_action(
            request.user,
            'Create User Account Failed',
            {'employee_id': employee_id, 'error': str(e)},
            ip,
            'FAILED'
        )
        return Response(
            {'error': str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


class BranchViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Branch CRUD operations
    """
    queryset = Branch.objects.all()
    serializer_class = BranchSerializer
    
    def get_permissions(self):
        """
        Allow public read access (GET), require authentication for other operations
        """
        if self.action in ['list', 'retrieve']:
            return []  # Public access for viewing branches
        return [IsAuthenticated()]  # Require authentication for create, update, delete
    
    def get_queryset(self):
        queryset = Branch.objects.all()
        is_active = self.request.query_params.get('is_active', None)
        
        if is_active is not None:
            queryset = queryset.filter(is_active=is_active.lower() == 'true')
            
        return queryset


class DepartmentViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Department CRUD operations
    """
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        queryset = Department.objects.all()
        is_active = self.request.query_params.get('is_active', None)
        
        if is_active is not None:
            queryset = queryset.filter(is_active=is_active.lower() == 'true')
            
        return queryset


class PositionViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Position CRUD operations
    """
    queryset = Position.objects.all()
    serializer_class = PositionSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        queryset = Position.objects.all()
        is_active = self.request.query_params.get('is_active', None)
        
        if is_active is not None:
            queryset = queryset.filter(is_active=is_active.lower() == 'true')
            
        return queryset


class EmployeeViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Employee CRUD operations with logging
    """
    queryset = Employee.objects.select_related('position', 'branch').prefetch_related('department').all()
    serializer_class = EmployeeSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        queryset = Employee.objects.select_related('position', 'branch').prefetch_related('department').all()
        status_filter = self.request.query_params.get('status', None)
        department = self.request.query_params.get('department', None)
        
        if status_filter:
            queryset = queryset.filter(status=status_filter)
        if department:
            queryset = queryset.filter(department__id=department)
            
        return queryset
    
    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        if response.status_code == 201:
            ip = get_client_ip(request)
            log_model_change(
                request.user,
                'CREATE',
                'Employee',
                response.data.get('id'),
                {
                    'employee_id': response.data.get('employee_id'),
                    'name': f"{response.data.get('first_name')} {response.data.get('last_name')}"
                },
                ip
            )
        return response
    
    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        old_data = EmployeeSerializer(instance).data
        response = super().update(request, *args, **kwargs)
        
        if response.status_code == 200:
            ip = get_client_ip(request)
            changes = get_changed_fields(instance, request.data)
            log_model_change(
                request.user,
                'UPDATE',
                'Employee',
                instance.id,
                changes,
                ip
            )
        return response
    
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        employee_id = instance.id
        employee_name = f"{instance.first_name} {instance.last_name}"
        response = super().destroy(request, *args, **kwargs)
        
        if response.status_code == 204:
            ip = get_client_ip(request)
            log_model_change(
                request.user,
                'DELETE',
                'Employee',
                employee_id,
                {'name': employee_name},
                ip
            )
        return response


class CategoryViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Category CRUD operations with logging
    """
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated]
    
    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        if response.status_code == 201:
            ip = get_client_ip(request)
            log_model_change(
                request.user,
                'CREATE',
                'Category',
                response.data.get('id'),
                {'name': response.data.get('name')},
                ip
            )
        return response
    
    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        response = super().update(request, *args, **kwargs)
        
        if response.status_code == 200:
            ip = get_client_ip(request)
            changes = get_changed_fields(instance, request.data)
            log_model_change(
                request.user,
                'UPDATE',
                'Category',
                instance.id,
                changes,
                ip
            )
        return response
    
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        category_id = instance.id
        category_name = instance.name
        response = super().destroy(request, *args, **kwargs)
        
        if response.status_code == 204:
            ip = get_client_ip(request)
            log_model_change(
                request.user,
                'DELETE',
                'Category',
                category_id,
                {'name': category_name},
                ip
            )
        return response


class ItemViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Item CRUD operations with logging
    """
    queryset = Item.objects.all()
    serializer_class = ItemSerializer
    permission_classes = [IsAuthenticated]
    
    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        if response.status_code == 201:
            ip = get_client_ip(request)
            log_model_change(
                request.user,
                'CREATE',
                'Item',
                response.data.get('id'),
                {
                    'item_code': response.data.get('item_code'),
                    'name': response.data.get('name')
                },
                ip
            )
        return response
    
    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        response = super().update(request, *args, **kwargs)
        
        if response.status_code == 200:
            ip = get_client_ip(request)
            changes = get_changed_fields(instance, request.data)
            log_model_change(
                request.user,
                'UPDATE',
                'Item',
                instance.id,
                changes,
                ip
            )
        return response
    
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        item_id = instance.id
        item_name = instance.name
        response = super().destroy(request, *args, **kwargs)
        
        if response.status_code == 204:
            ip = get_client_ip(request)
            log_model_change(
                request.user,
                'DELETE',
                'Item',
                item_id,
                {'name': item_name},
                ip
            )
        return response


class StockMovementViewSet(viewsets.ModelViewSet):
    """
    ViewSet for StockMovement CRUD operations with logging
    """
    queryset = StockMovement.objects.all()
    serializer_class = StockMovementSerializer
    permission_classes = [IsAuthenticated]
    
    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        if response.status_code == 201:
            ip = get_client_ip(request)
            log_model_change(
                request.user,
                'CREATE',
                'StockMovement',
                response.data.get('id'),
                {
                    'item': response.data.get('item_name'),
                    'movement_type': response.data.get('movement_type'),
                    'quantity': response.data.get('quantity')
                },
                ip
            )
        return response
    
    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        response = super().update(request, *args, **kwargs)
        
        if response.status_code == 200:
            ip = get_client_ip(request)
            changes = get_changed_fields(instance, request.data)
            log_model_change(
                request.user,
                'UPDATE',
                'StockMovement',
                instance.id,
                changes,
                ip
            )
        return response
    
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        movement_id = instance.id
        item_name = instance.item.name
        response = super().destroy(request, *args, **kwargs)
        
        if response.status_code == 204:
            ip = get_client_ip(request)
            log_model_change(
                request.user,
                'DELETE',
                'StockMovement',
                movement_id,
                {'item': item_name},
                ip
            )
        return response


class MessageViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Message operations with custom actions for inbox/sent/unread
    """
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        # Only return messages for the current user that aren't deleted
        user = self.request.user
        return Message.objects.filter(
            (models.Q(receiver=user) & models.Q(deleted_by_receiver=False)) |
            (models.Q(sender=user) & models.Q(deleted_by_sender=False))
        )
    
    @action(detail=False, methods=['get'])
    def inbox(self, request):
        """Get all received messages"""
        messages = Message.objects.filter(
            receiver=request.user,
            deleted_by_receiver=False
        ).order_by('-created_at')
        serializer = self.get_serializer(messages, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def sent(self, request):
        """Get all sent messages"""
        messages = Message.objects.filter(
            sender=request.user,
            deleted_by_sender=False
        ).order_by('-created_at')
        serializer = self.get_serializer(messages, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def unread_count(self, request):
        """Get count of unread messages"""
        count = Message.objects.filter(
            receiver=request.user,
            is_read=False,
            deleted_by_receiver=False
        ).count()
        return Response({'count': count})
    
    @action(detail=True, methods=['post'])
    def mark_as_read(self, request, pk=None):
        """Mark a message as read"""
        message = self.get_object()
        if message.receiver != request.user:
            return Response(
                {'error': 'You can only mark your own messages as read'}, 
                status=status.HTTP_403_FORBIDDEN
            )
        
        message.is_read = True
        message.read_at = timezone.now()
        message.save()
        
        ip = get_client_ip(request)
        log_action(request.user, 'READ_MESSAGE', {'message_id': message.id, 'subject': message.subject}, ip)
        
        return Response({'status': 'Message marked as read'})
    
    @action(detail=True, methods=['post'])
    def mark_as_unread(self, request, pk=None):
        """Mark a message as unread"""
        message = self.get_object()
        if message.receiver != request.user:
            return Response(
                {'error': 'You can only mark your own messages as unread'}, 
                status=status.HTTP_403_FORBIDDEN
            )
        
        message.is_read = False
        message.read_at = None
        message.save()
        
        return Response({'status': 'Message marked as unread'})
    
    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        if response.status_code == 201:
            ip = get_client_ip(request)
            log_model_change(
                request.user,
                'CREATE',
                'Message',
                response.data.get('id'),
                {
                    'receiver': response.data.get('receiver_username'),
                    'subject': response.data.get('subject')
                },
                ip
            )
        return response
    
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        message_id = instance.id
        subject = instance.subject
        
        # Only allow sender or receiver to delete
        if instance.sender != request.user and instance.receiver != request.user:
            return Response(
                {'error': 'You can only delete your own messages'}, 
                status=status.HTTP_403_FORBIDDEN
            )
        
        # Soft delete: mark as deleted by the current user
        if instance.sender == request.user:
            instance.deleted_by_sender = True
        if instance.receiver == request.user:
            instance.deleted_by_receiver = True
        
        # Only permanently delete if both users have deleted it
        if instance.deleted_by_sender and instance.deleted_by_receiver:
            response = super().destroy(request, *args, **kwargs)
        else:
            instance.save()
            response = Response(status=status.HTTP_204_NO_CONTENT)
        
        ip = get_client_ip(request)
        log_model_change(
            request.user,
            'DELETE',
            'Message',
            message_id,
            {'subject': subject},
            ip
        )
        return response

