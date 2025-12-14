# 🎯 Quick Reference Guide

Push-Location 'C:\xampp\htdocs\Denthub\backend'; python manage.py migrate --noinput; python manage.py runserver 0.0.0.0:8000; Pop-Location

Push-Location 'C:\xampp\htdocs\Denthub\frontend'; npm run dev -- --host 0.0.0.0; Pop-Location

Push-Location 'C:\xampp\htdocs\Denthub\public-website'; python -m http.server 8080 --bind 0.0.0.0; Pop-Location



## 🚀 Starting the Application

### Method 1: Manual Start
```powershell
# Terminal 1 - Backend
cd c:\xampp\htdocs\Denthub\backend
python manage.py runserver

# Terminal 2 - Frontend  
cd c:\xampp\htdocs\Denthub\frontend
npm run dev
```

### Method 2: Using Scripts
```powershell
# Start backend
.\start-backend.ps1

# Start frontend (in new terminal)
.\start-frontend.ps1
```

## 🔗 Access URLs

| Service | URL | Credentials |
|---------|-----|-------------|
| **Frontend App** | http://localhost:3000 | admin / admin123 |
| **Backend API** | http://127.0.0.1:8000/api/ | - |
| **Django Admin** | http://127.0.0.1:8000/admin/ | admin / admin123 |

## 📋 Common Tasks

### Adding a New Employee
1. Login to http://localhost:3000
2. Click **"Employees"** in sidebar
3. Click **"+ Add Employee"** button
4. Fill in all fields:
   - Employee ID (e.g., EMP001)
   - Personal info
   - Contact details
   - Job information
   - Salary
5. Click **"Save"**

### Editing an Employee
1. Go to Employees page
2. Find the employee in the table
3. Click the **blue edit icon** (pencil)
4. Update the fields
5. Click **"Save"**

### Deleting an Employee
1. Go to Employees page
2. Find the employee
3. Click the **red delete icon** (trash)
4. Confirm deletion

### Searching for Employees
1. Go to Employees page
2. Type in the search box (top right)
3. Search by:
   - Employee ID
   - Name
   - Email
   - Position
   - Department

## 🗂️ API Usage Examples

### Login (POST)
```bash
POST http://127.0.0.1:8000/api/login/
Content-Type: application/json

{
  "username": "admin",
  "password": "admin123"
}
```

### Get All Employees (GET)
```bash
GET http://127.0.0.1:8000/api/employees/
Authorization: Session (Cookie)
```

### Create Employee (POST)
```bash
POST http://127.0.0.1:8000/api/employees/
Content-Type: application/json

{
  "employee_id": "EMP001",
  "first_name": "John",
  "last_name": "Doe",
  "email": "john.doe@example.com",
  "phone": "1234567890",
  "date_of_birth": "1990-01-15",
  "gender": "M",
  "address": "123 Main St",
  "position": "Software Engineer",
  "department": "IT",
  "hire_date": "2024-01-01",
  "salary": "75000.00",
  "status": "active"
}
```

### Update Employee (PUT)
```bash
PUT http://127.0.0.1:8000/api/employees/1/
Content-Type: application/json

{
  "employee_id": "EMP001",
  "first_name": "John",
  "last_name": "Doe",
  "salary": "80000.00",
  ...
}
```

### Delete Employee (DELETE)
```bash
DELETE http://127.0.0.1:8000/api/employees/1/
```

## 🔧 Configuration Files

### Backend Settings
**File**: `backend/denthub_project/settings.py`
```python
# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'denthub_db',
        'USER': 'root',
        'PASSWORD': '',
        'HOST': '127.0.0.1',
        'PORT': '3306',
    }
}

# Custom User Model
AUTH_USER_MODEL = 'employees.User'
```

### Frontend API Config
**File**: `frontend/src/services/api.js`
```javascript
const api = axios.create({
  baseURL: 'http://127.0.0.1:8000/api',
  withCredentials: true,
})
```

## 📊 Database Schema

### denthub_user Table
```sql
id (PK)
username (unique)
email (unique)
password (hashed)
first_name
last_name
phone
is_staff
is_superuser
is_active
date_joined
last_login
```

### denthub_emp Table
```sql
id (PK)
employee_id (unique)
first_name
last_name
email (unique)
phone
date_of_birth
gender
address
position
department
hire_date
salary
status
created_at
updated_at
```

## 🎨 UI Components

### Login Page
- Username field
- Password field
- Submit button
- Error message display

### Dashboard
- Statistics cards (4 boxes)
- Total employees
- Active employees
- Inactive employees
- Department count

### Employees Page
- Search bar
- Add Employee button
- Employee table
- Edit/Delete actions
- Modal form

## 🔐 Security Checklist

- ✅ Passwords are hashed
- ✅ CSRF tokens on all forms
- ✅ Session-based authentication
- ✅ Login required for API
- ✅ CORS properly configured
- ✅ SQL injection prevention (ORM)
- ✅ XSS protection

## 🐛 Troubleshooting Quick Fixes

### "Cannot connect to database"
```powershell
# Start XAMPP MySQL
# Check if database exists
cd c:\xampp
.\mysql\bin\mysql.exe -u root -e "SHOW DATABASES;"
```

### "Port already in use"
```powershell
# Backend (8000)
netstat -ano | findstr :8000

# Frontend (3000)
netstat -ano | findstr :3000
```

### "Login not working"
```powershell
# Reset superuser
cd c:\xampp\htdocs\Denthub\backend
python create_superuser.py
```

### "Frontend not loading"
```powershell
# Reinstall dependencies
cd c:\xampp\htdocs\Denthub\frontend
Remove-Item -Recurse -Force node_modules
npm install
```

## 📝 Sample Data

### Sample Employee Entry
```json
{
  "employee_id": "EMP001",
  "first_name": "Jane",
  "last_name": "Smith",
  "email": "jane.smith@denthub.com",
  "phone": "+1-555-0123",
  "date_of_birth": "1988-05-20",
  "gender": "F",
  "address": "456 Oak Avenue, Suite 12, New York, NY 10001",
  "position": "Senior Dentist",
  "department": "Clinical",
  "hire_date": "2020-03-15",
  "salary": "95000.00",
  "status": "active"
}
```

## 🎯 Tips & Best Practices

1. **Always start XAMPP MySQL first** before running backend
2. **Use unique Employee IDs** to avoid conflicts
3. **Validate email formats** before submission
4. **Keep salaries as decimal** with 2 places (e.g., 50000.00)
5. **Use proper date formats** (YYYY-MM-DD)
6. **Search is case-insensitive** for better UX
7. **Logout before closing** for security

## 🔄 Update Workflow

1. Make changes to code
2. Save files (auto-reload enabled)
3. Refresh browser
4. Test functionality
5. Check console for errors

## 📞 Command Cheat Sheet

```powershell
# Django Commands
python manage.py runserver          # Start server
python manage.py makemigrations     # Create migrations
python manage.py migrate            # Apply migrations
python manage.py createsuperuser    # Create admin user
python manage.py shell              # Django shell

# NPM Commands
npm install                         # Install dependencies
npm run dev                         # Start dev server
npm run build                       # Build for production
npm run preview                     # Preview production build

# Database
.\mysql\bin\mysql.exe -u root       # MySQL CLI
SHOW DATABASES;                     # List databases
USE denthub_db;                     # Select database
SHOW TABLES;                        # List tables
DESC denthub_emp;                   # Show table structure
```

---

**Need Help?** Check the full README.md or SETUP_COMPLETE.md files!

🎉 **Happy Employee Managing!**
