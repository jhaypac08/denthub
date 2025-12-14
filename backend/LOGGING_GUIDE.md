# Application Logging System

## Overview
The DentHub application includes a comprehensive logging system that tracks all user activities, data changes, and system events.

## Log Location
- **Directory**: `backend/app_log/`
- **File Format**: `applog_YYYYMMDD.log`
- **Example**: `applog_20251206.log`

## Features

### 1. Automatic Request Logging
Every HTTP request is automatically logged with:
- User who made the request
- Client IP address
- Action performed
- HTTP status code
- Request path
- Timestamp

### 2. Model Change Tracking
All CRUD operations on models are logged with:
- **CREATE**: New record creation with key details
- **UPDATE**: Modified fields with old and new values
- **DELETE**: Deleted record information

Tracked models:
- Users
- Employees
- Branches
- Departments
- Positions
- Groups

### 3. Authentication Events
- Login attempts (successful and failed)
- Logout events
- Password changes
- Permission denied events

### 4. Log Rotation
- Logs rotate daily at midnight
- 30 days of log files are retained
- Old logs are automatically archived with date suffix

## Log Format

### Standard Format
```
[LEVEL] YYYY-MM-DD HH:MM:SS | User: username | IP: xxx.xxx.xxx.xxx | Action description | Details
```

### Example Entries
```
[INFO] 2025-12-06 09:15:23 | User: admin | IP: 127.0.0.1 | Login Successful | Details: IP: 127.0.0.1 | Status: SUCCESS
[INFO] 2025-12-06 09:16:45 | User: admin | IP: 127.0.0.1 | CREATE Employee | Details: Model: Employee | ID: 5 | Action: CREATE | Changes: {"employee_id": "20251206-0916", "name": "John Doe"} | Status: SUCCESS
[INFO] 2025-12-06 09:18:12 | User: admin | IP: 127.0.0.1 | UPDATE User | Details: Model: User | ID: 2 | Action: UPDATE | Changes: {"email": {"old": "old@example.com", "new": "new@example.com"}} | Status: SUCCESS
[INFO] 2025-12-06 09:20:33 | User: admin | IP: 127.0.0.1 | Logout | Details: IP: 127.0.0.1 | Status: SUCCESS
[ERROR] 2025-12-06 09:22:15 | User: testuser | IP: 127.0.0.1 | Login Failed | Details: IP: 127.0.0.1 | Reason: Invalid credentials | Status: FAILED
```

## Configuration

### Log Levels
- **INFO**: Normal operations (create, read, update, delete)
- **WARNING**: Unusual events (permission denied, validation errors)
- **ERROR**: Failed operations (login failures, errors)

### Settings (in `denthub_project/settings.py`)
```python
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '[{levelname}] {asctime} | User: {user} | IP: {ip} | {message}',
        },
    },
    'handlers': {
        'app_actions': {
            'level': 'INFO',
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'filename': LOG_FILE_PATH,
            'when': 'midnight',
            'interval': 1,
            'backupCount': 30,
        },
    },
}
```

## Using the Logging System

### Automatic Logging (via Middleware)
All API requests are automatically logged. No action required.

### Manual Logging (in views)

#### 1. Import logging utilities
```python
from .logging_utils import log_action, log_model_change, log_login, get_client_ip
```

#### 2. Log a custom action
```python
from .logging_utils import log_action, get_client_ip

def my_view(request):
    ip = get_client_ip(request)
    
    # Do something...
    
    log_action(
        request.user,
        'Custom Action Description',
        {'detail1': 'value1', 'detail2': 'value2'},
        ip,
        'SUCCESS'  # or 'FAILED', 'WARNING'
    )
```

#### 3. Log model changes
```python
from .logging_utils import log_model_change, get_client_ip

def update_employee(request, employee_id):
    ip = get_client_ip(request)
    employee = Employee.objects.get(id=employee_id)
    
    # Make changes...
    
    log_model_change(
        request.user,
        'UPDATE',
        'Employee',
        employee.id,
        {'field': {'old': 'old_value', 'new': 'new_value'}},
        ip
    )
```

## Utility Functions

### Available Functions in `logging_utils.py`

1. **log_action**(user, action, details, ip_address, status)
   - General purpose action logging

2. **log_model_change**(user, action_type, model_name, instance_id, changes, ip_address)
   - Log model CRUD operations

3. **log_login**(user, success, ip_address, reason)
   - Log login attempts

4. **log_logout**(user, ip_address)
   - Log logout events

5. **log_password_change**(user, success, ip_address)
   - Log password changes

6. **log_permission_denied**(user, action, resource, ip_address)
   - Log permission denied events

7. **get_client_ip**(request)
   - Extract client IP from request

8. **get_changed_fields**(old_instance, new_data)
   - Compare and get changed fields

## Viewing Logs

### Command Line
```bash
# View today's log
cat backend/app_log/applog_20251206.log

# Tail real-time logs
tail -f backend/app_log/applog_20251206.log

# Search for specific user
grep "User: admin" backend/app_log/applog_20251206.log

# Search for failed actions
grep "FAILED" backend/app_log/applog_20251206.log

# Search for specific action
grep "Login" backend/app_log/applog_20251206.log
```

### PowerShell (Windows)
```powershell
# View today's log
Get-Content backend\app_log\applog_20251206.log

# Tail real-time logs
Get-Content backend\app_log\applog_20251206.log -Wait

# Search for specific user
Select-String "User: admin" backend\app_log\applog_20251206.log

# Search for failed actions
Select-String "FAILED" backend\app_log\applog_20251206.log
```

## Security Considerations

1. **Password Protection**: Password fields are never logged in plain text (shown as ***)
2. **IP Tracking**: All actions include the client IP address
3. **User Attribution**: Every action is associated with a user
4. **Tamper Evident**: Log entries include timestamps and are append-only

## Maintenance

### Log Cleanup
Old logs are automatically cleaned up after 30 days. To adjust:

```python
# In settings.py
LOGGING = {
    'handlers': {
        'app_actions': {
            'backupCount': 60,  # Keep 60 days instead of 30
        },
    },
}
```

### Manual Cleanup
```bash
# Delete logs older than 30 days
find backend/app_log -name "applog_*.log*" -mtime +30 -delete
```

## Troubleshooting

### Logs not being created
1. Check directory permissions: `backend/app_log/` must be writable
2. Verify middleware is enabled in `settings.py`
3. Check Django logging configuration

### Missing log entries
1. Verify middleware is in `MIDDLEWARE` list
2. Check log level is set to `INFO` or lower
3. Ensure logging utilities are imported in views

## Best Practices

1. **Always log sensitive operations** (user creation, deletion, permission changes)
2. **Include relevant context** in log details
3. **Use appropriate log levels** (INFO for normal, ERROR for failures)
4. **Monitor logs regularly** for suspicious activity
5. **Backup logs** for compliance and audit purposes
