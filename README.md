<<<<<<< HEAD
# denthub
Personal project
=======
# DentHub Employee Management System

A full-stack employee management web application built with Vue.js and Django.

## Features

- **User Authentication**: Secure login system with session management
- **Employee Management**: Full CRUD operations for employee records
- **Dashboard**: Overview with statistics and insights
- **AdminLTE Interface**: Professional and responsive admin panel
- **RESTful API**: Django REST Framework backend

## Tech Stack

### Frontend
- Vue.js 3
- Vue Router
- Pinia (State Management)
- AdminLTE 3
- Axios
- Vite

### Backend
- Python Django
- Django REST Framework
- MariaDB Database
- Django CORS Headers

## Prerequisites

- Python 3.8+
- Node.js 20+
- XAMPP (MariaDB)
- Virtual Environment (venv)

## Installation

### 1. Database Setup

Make sure XAMPP MySQL/MariaDB is running, then create the database:

```bash
cd c:\xampp
.\mysql\bin\mysql.exe -u root -e "CREATE DATABASE IF NOT EXISTS denthub_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;"
```

### 2. Backend Setup

```bash
cd backend

# Activate virtual environment (if not already activated)
.\venv\Scripts\Activate.ps1

# Install dependencies (already installed)
pip install django djangorestframework django-cors-headers pymysql python-decouple

# Run migrations
python manage.py migrate

# Create superuser (already created)
# Username: admin
# Password: admin123

# Start Django server
python manage.py runserver
```

The backend API will be available at: `http://127.0.0.1:8000`
Admin panel: `http://127.0.0.1:8000/admin`

### 3. Frontend Setup

```bash
cd frontend

# Install dependencies (already installed)
npm install

# Start development server
npm run dev
```

The frontend will be available at: `http://localhost:3000`

## Default Credentials

- **Username**: admin
- **Password**: admin123

## Database Schema

### denthub_user Table
Custom user model with authentication fields:
- username
- email
- password
- phone
- first_name, last_name
- is_staff, is_superuser, is_active

### denthub_emp Table
Employee records:
- employee_id (unique)
- first_name, last_name
- email, phone
- date_of_birth
- gender
- address
- position, department
- hire_date
- salary
- status (active/inactive)
- created_at, updated_at

## API Endpoints

### Authentication
- `POST /api/login/` - User login
- `POST /api/logout/` - User logout
- `GET /api/current-user/` - Get current user

### Employees
- `GET /api/employees/` - List all employees
- `POST /api/employees/` - Create new employee
- `GET /api/employees/{id}/` - Get employee details
- `PUT /api/employees/{id}/` - Update employee
- `DELETE /api/employees/{id}/` - Delete employee

## Project Structure

```
Denthub/
├── backend/
│   ├── denthub_project/      # Django project settings
│   ├── employees/             # Main app
│   │   ├── models.py         # User and Employee models
│   │   ├── serializers.py    # DRF serializers
│   │   ├── views.py          # API views
│   │   ├── admin.py          # Admin configuration
│   │   └── urls.py           # App URL routes
│   ├── manage.py
│   └── venv/                 # Virtual environment
│
└── frontend/
    ├── src/
    │   ├── components/       # Vue components
    │   │   └── DashboardLayout.vue
    │   ├── views/            # Page views
    │   │   ├── LoginView.vue
    │   │   ├── DashboardView.vue
    │   │   └── EmployeesView.vue
    │   ├── stores/           # Pinia stores
    │   │   └── auth.js
    │   ├── services/         # API services
    │   │   └── api.js
    │   ├── router/           # Vue Router
    │   │   └── index.js
    │   ├── App.vue
    │   └── main.js
    ├── package.json
    └── vite.config.js
```

## Usage

1. Start the Django backend server (port 8000)
2. Start the Vue.js frontend server (port 3000)
3. Navigate to `http://localhost:3000`
4. Login with admin/admin123
5. Manage employees through the dashboard

## Development Notes

- CORS is enabled for frontend-backend communication
- Session-based authentication is used
- CSRF tokens are automatically handled
- All API requests require authentication except login

## Future Enhancements

- File upload for employee photos
- Advanced reporting and analytics
- Role-based access control
- Email notifications
- Export to PDF/Excel
- Employee performance tracking

## License

This project is for educational/demonstration purposes.
>>>>>>> 3529527 (Initial commit for Render deployment)
