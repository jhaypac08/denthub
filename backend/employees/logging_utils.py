import logging
import json
from datetime import datetime

logger = logging.getLogger('app_logger')


def log_action(user, action, details=None, ip_address='Unknown', status='SUCCESS'):
    """
    Log a specific user action with details
    
    Args:
        user: User object or username string
        action: Action description (e.g., "Created Employee", "Updated User")
        details: Dictionary with additional details
        ip_address: Client IP address
        status: Action status (SUCCESS, FAILED, WARNING)
    """
    username = str(user) if user else 'Anonymous'
    
    log_message = f"{action}"
    
    if details:
        # Format details as readable string
        details_str = ' | '.join([f"{k}: {v}" for k, v in details.items()])
        log_message += f" | Details: {details_str}"
    
    log_message += f" | Status: {status}"
    
    extra_data = {
        'user': username,
        'ip': ip_address,
    }
    
    if status == 'FAILED':
        logger.error(log_message, extra=extra_data)
    elif status == 'WARNING':
        logger.warning(log_message, extra=extra_data)
    else:
        logger.info(log_message, extra=extra_data)


def log_model_change(user, action_type, model_name, instance_id, changes=None, ip_address='Unknown'):
    """
    Log changes to model instances
    
    Args:
        user: User object or username
        action_type: CREATE, UPDATE, DELETE
        model_name: Name of the model (e.g., "Employee", "User")
        instance_id: ID of the instance
        changes: Dictionary of changed fields (for UPDATE)
        ip_address: Client IP address
    """
    details = {
        'Model': model_name,
        'ID': instance_id,
        'Action': action_type,
    }
    
    if changes:
        details['Changes'] = json.dumps(changes)
    
    action_desc = f"{action_type} {model_name}"
    log_action(user, action_desc, details, ip_address)


def log_login(user, success=True, ip_address='Unknown', reason=None):
    """Log user login attempts"""
    if success:
        log_action(user, 'Login Successful', {'IP': ip_address}, ip_address, 'SUCCESS')
    else:
        details = {'IP': ip_address}
        if reason:
            details['Reason'] = reason
        log_action(user or 'Unknown', 'Login Failed', details, ip_address, 'FAILED')


def log_logout(user, ip_address='Unknown'):
    """Log user logout"""
    log_action(user, 'Logout', {'IP': ip_address}, ip_address, 'SUCCESS')


def log_password_change(user, success=True, ip_address='Unknown'):
    """Log password change attempts"""
    if success:
        log_action(user, 'Password Changed', {'IP': ip_address}, ip_address, 'SUCCESS')
    else:
        log_action(user, 'Password Change Failed', {'IP': ip_address}, ip_address, 'FAILED')


def log_permission_denied(user, action, resource, ip_address='Unknown'):
    """Log permission denied events"""
    details = {
        'Action': action,
        'Resource': resource,
    }
    log_action(user, 'Permission Denied', details, ip_address, 'WARNING')


def get_client_ip(request):
    """Extract client IP from request"""
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR', 'Unknown')
    return ip


def get_changed_fields(old_instance, new_data):
    """
    Compare old instance with new data and return changed fields
    
    Args:
        old_instance: Model instance before changes
        new_data: Dictionary with new data
    
    Returns:
        Dictionary of changed fields with old and new values
    """
    changes = {}
    
    for field, new_value in new_data.items():
        if hasattr(old_instance, field):
            old_value = getattr(old_instance, field)
            
            # Skip password fields for security
            if 'password' in field.lower():
                if old_value != new_value:
                    changes[field] = {'old': '***', 'new': '***'}
            elif old_value != new_value:
                changes[field] = {
                    'old': str(old_value),
                    'new': str(new_value)
                }
    
    return changes
