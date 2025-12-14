import logging
import json
from django.utils.deprecation import MiddlewareMixin

logger = logging.getLogger('app_logger')


class ActivityLoggingMiddleware(MiddlewareMixin):
    """
    Middleware to log all user activities and API requests
    """
    
    def process_request(self, request):
        """Log incoming requests"""
        # Skip logging for static files and admin media
        if request.path.startswith('/static/') or request.path.startswith('/media/'):
            return None
        
        # Get user information
        user = request.user if request.user.is_authenticated else 'Anonymous'
        ip_address = self.get_client_ip(request)
        
        # Store in request for later use
        request.log_data = {
            'user': str(user),
            'ip': ip_address,
        }
        
        return None
    
    def process_response(self, request, response):
        """Log completed requests with response status"""
        # Skip logging for static files and admin media
        if request.path.startswith('/static/') or request.path.startswith('/media/'):
            return response
        
        # Get log data from request
        log_data = getattr(request, 'log_data', {})
        user = log_data.get('user', 'Unknown')
        ip = log_data.get('ip', 'Unknown')
        
        # Determine action type
        action = self.get_action_description(request)
        
        # Log the request
        if response.status_code >= 400:
            logger.error(
                f"{action} | Status: {response.status_code} | Path: {request.path}",
                extra={'user': user, 'ip': ip}
            )
        else:
            logger.info(
                f"{action} | Status: {response.status_code} | Path: {request.path}",
                extra={'user': user, 'ip': ip}
            )
        
        return response
    
    def get_client_ip(self, request):
        """Get the client's IP address"""
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR', 'Unknown')
        return ip
    
    def get_action_description(self, request):
        """Generate human-readable action description"""
        method = request.method
        path = request.path
        
        # Parse common API patterns
        if '/api/login/' in path:
            return 'User Login Attempt'
        elif '/api/logout/' in path:
            return 'User Logout'
        elif '/api/employees/' in path:
            if method == 'GET':
                return 'View Employees'
            elif method == 'POST':
                return 'Create Employee'
            elif method == 'PUT' or method == 'PATCH':
                return 'Update Employee'
            elif method == 'DELETE':
                return 'Delete Employee'
        elif '/api/users/' in path:
            if method == 'GET':
                return 'View Users'
            elif method == 'POST':
                return 'Create User'
            elif method == 'PUT' or method == 'PATCH':
                return 'Update User'
            elif method == 'DELETE':
                return 'Delete User'
        elif '/api/branches/' in path:
            if method == 'GET':
                return 'View Branches'
            elif method == 'POST':
                return 'Create Branch'
            elif method == 'PUT' or method == 'PATCH':
                return 'Update Branch'
            elif method == 'DELETE':
                return 'Delete Branch'
        elif '/api/departments/' in path:
            if method == 'GET':
                return 'View Departments'
            elif method == 'POST':
                return 'Create Department'
            elif method == 'PUT' or method == 'PATCH':
                return 'Update Department'
            elif method == 'DELETE':
                return 'Delete Department'
        elif '/api/positions/' in path:
            if method == 'GET':
                return 'View Positions'
            elif method == 'POST':
                return 'Create Position'
            elif method == 'PUT' or method == 'PATCH':
                return 'Update Position'
            elif method == 'DELETE':
                return 'Delete Position'
        elif '/api/groups/' in path:
            if method == 'GET':
                return 'View Groups'
            elif method == 'POST':
                return 'Create Group'
            elif method == 'PUT' or method == 'PATCH':
                return 'Update Group'
            elif method == 'DELETE':
                return 'Delete Group'
        elif '/admin/' in path:
            return f'Admin Panel Access ({method})'
        else:
            return f'{method} Request'
