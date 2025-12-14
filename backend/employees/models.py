from django.db import models
from django.contrib.auth.models import AbstractUser
import os

def employee_photo_path(instance, filename):
    """Generate file path for employee photo using employee_id"""
    # Get file extension
    ext = filename.split('.')[-1]
    # Use employee_id as filename
    filename = f"{instance.employee_id}.{ext}"
    return os.path.join('employee_photos', filename)

class User(AbstractUser):
    """Custom User model"""
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15, blank=True, null=True)
    force_password_change = models.BooleanField(default=False)
    
    class Meta:
        db_table = 'denthub_user'
    
    def __str__(self):
        return self.username


class Branch(models.Model):
    """Branch model"""
    name = models.CharField(max_length=100, unique=True)
    code = models.CharField(max_length=20, unique=True)
    address = models.TextField()
    phone = models.CharField(max_length=15)
    email = models.EmailField()
    manager = models.CharField(max_length=100, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    
    # Operating Hours - JSON field to store schedule for each day
    monday_open = models.TimeField(blank=True, null=True)
    monday_close = models.TimeField(blank=True, null=True)
    monday_closed = models.BooleanField(default=False)
    
    tuesday_open = models.TimeField(blank=True, null=True)
    tuesday_close = models.TimeField(blank=True, null=True)
    tuesday_closed = models.BooleanField(default=False)
    
    wednesday_open = models.TimeField(blank=True, null=True)
    wednesday_close = models.TimeField(blank=True, null=True)
    wednesday_closed = models.BooleanField(default=False)
    
    thursday_open = models.TimeField(blank=True, null=True)
    thursday_close = models.TimeField(blank=True, null=True)
    thursday_closed = models.BooleanField(default=False)
    
    friday_open = models.TimeField(blank=True, null=True)
    friday_close = models.TimeField(blank=True, null=True)
    friday_closed = models.BooleanField(default=False)
    
    saturday_open = models.TimeField(blank=True, null=True)
    saturday_close = models.TimeField(blank=True, null=True)
    saturday_closed = models.BooleanField(default=False)
    
    sunday_open = models.TimeField(blank=True, null=True)
    sunday_close = models.TimeField(blank=True, null=True)
    sunday_closed = models.BooleanField(default=False)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'denthub_branch'
        ordering = ['name']
        verbose_name_plural = 'Branches'
    
    def __str__(self):
        return f"{self.code} - {self.name}"


class Department(models.Model):
    """Department model"""
    name = models.CharField(max_length=100, unique=True)
    code = models.CharField(max_length=20, unique=True)
    description = models.TextField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'denthub_department'
        ordering = ['name']
    
    def __str__(self):
        return self.name


class Position(models.Model):
    """Position model"""
    title = models.CharField(max_length=100, unique=True)
    code = models.CharField(max_length=20, unique=True)
    description = models.TextField(blank=True, null=True)
    min_salary = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    max_salary = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'denthub_position'
        ordering = ['title']
    
    def __str__(self):
        return self.title


class Employee(models.Model):
    """Employee model"""
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    ]
    
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('inactive', 'Inactive'),
    ]
    
    employee_id = models.CharField(max_length=20, unique=True, blank=True)
    user = models.OneToOneField(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='employee')
    photo = models.ImageField(upload_to=employee_photo_path, null=True, blank=True)
    first_name = models.CharField(max_length=100)
    middle_name = models.CharField(max_length=100, blank=True, null=True)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15)
    date_of_birth = models.DateField()
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    address = models.TextField()
    position = models.ForeignKey(Position, on_delete=models.SET_NULL, null=True, blank=True, related_name='employees')
    department = models.ManyToManyField(Department, blank=True, related_name='employees')
    branch = models.ForeignKey(Branch, on_delete=models.SET_NULL, null=True, related_name='employees')
    hire_date = models.DateField()
    salary = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='active')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'denthub_emp'
        ordering = ['-created_at']
    
    def save(self, *args, **kwargs):
        # Generate employee_id if it doesn't exist
        if not self.employee_id:
            from django.utils import timezone
            now = timezone.now()
            self.employee_id = now.strftime('%Y%m%d-%H%M')
            
            # Ensure uniqueness by adding a counter if needed
            base_id = self.employee_id
            counter = 1
            while Employee.objects.filter(employee_id=self.employee_id).exists():
                self.employee_id = f"{base_id}-{counter}"
                counter += 1
        
        # Handle photo file replacement - delete old photo if it exists
        if self.pk:
            try:
                old_instance = Employee.objects.get(pk=self.pk)
                if old_instance.photo and old_instance.photo != self.photo:
                    # Delete old photo file if it exists and is different
                    if os.path.isfile(old_instance.photo.path):
                        os.remove(old_instance.photo.path)
            except Employee.DoesNotExist:
                pass
        
        super().save(*args, **kwargs)
    
    def delete(self, *args, **kwargs):
        # Delete photo file when employee is deleted
        if self.photo:
            if os.path.isfile(self.photo.path):
                os.remove(self.photo.path)
        super().delete(*args, **kwargs)
    
    def __str__(self):
        middle = ''
        if self.middle_name:
            m = str(self.middle_name).strip()
            if len(m) > 0:
                middle = f" {m[0].upper()}."
        return f"{self.employee_id} - {self.first_name}{middle} {self.last_name}".strip()


class Category(models.Model):
    """Inventory Category model"""
    name = models.CharField(max_length=100, unique=True)
    code = models.CharField(max_length=20, unique=True)
    description = models.TextField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'denthub_category'
        ordering = ['name']
        verbose_name_plural = 'Categories'
    
    def __str__(self):
        return self.name


class Item(models.Model):
    """Inventory Item model"""
    UNIT_CHOICES = [
        ('pcs', 'Pieces'),
        ('box', 'Box'),
        ('pack', 'Pack'),
        ('bottle', 'Bottle'),
        ('set', 'Set'),
        ('kit', 'Kit'),
    ]
    
    item_code = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=200)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name='items')
    description = models.TextField(blank=True, null=True)
    unit = models.CharField(max_length=20, choices=UNIT_CHOICES, default='pcs')
    reorder_level = models.IntegerField(default=10)
    current_stock = models.IntegerField(default=0)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    supplier = models.CharField(max_length=200, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'denthub_item'
        ordering = ['name']
    
    def __str__(self):
        return f"{self.item_code} - {self.name}"
    
    @property
    def is_low_stock(self):
        return self.current_stock <= self.reorder_level


class StockMovement(models.Model):
    """Stock Movement/Transaction model"""
    MOVEMENT_TYPES = [
        ('in', 'Stock In'),
        ('out', 'Stock Out'),
        ('adjustment', 'Adjustment'),
    ]
    
    item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name='movements')
    movement_type = models.CharField(max_length=20, choices=MOVEMENT_TYPES)
    quantity = models.IntegerField()
    reference_number = models.CharField(max_length=50, blank=True, null=True)
    remarks = models.TextField(blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='stock_movements')
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'denthub_stock_movement'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.movement_type} - {self.item.name} ({self.quantity})"
    
    def save(self, *args, **kwargs):
        # Update item stock based on movement type
        if self.movement_type == 'in':
            self.item.current_stock += self.quantity
        elif self.movement_type == 'out':
            self.item.current_stock -= self.quantity
        elif self.movement_type == 'adjustment':
            # For adjustment, quantity is the new stock level
            self.item.current_stock = self.quantity
        
        self.item.save()
        super().save(*args, **kwargs)


class Message(models.Model):
    """Message/Notification model for inbox system"""
    MESSAGE_TYPES = [
        ('message', 'Message'),
        ('notification', 'Notification'),
        ('system', 'System Alert'),
    ]
    
    PRIORITY_LEVELS = [
        ('low', 'Low'),
        ('normal', 'Normal'),
        ('high', 'High'),
        ('urgent', 'Urgent'),
    ]
    
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages', null=True, blank=True)
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_messages')
    message_type = models.CharField(max_length=20, choices=MESSAGE_TYPES, default='message')
    priority = models.CharField(max_length=20, choices=PRIORITY_LEVELS, default='normal')
    subject = models.CharField(max_length=200)
    body = models.TextField()
    is_read = models.BooleanField(default=False)
    read_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    # Soft delete fields
    deleted_by_sender = models.BooleanField(default=False)
    deleted_by_receiver = models.BooleanField(default=False)
    
    # For future live notification support
    is_pushed = models.BooleanField(default=False)  # Track if push notification was sent
    
    class Meta:
        db_table = 'denthub_message'
        ordering = ['-created_at']
    
    def __str__(self):
        sender_name = self.sender.username if self.sender else 'System'
        return f"{sender_name} → {self.receiver.username}: {self.subject}"
