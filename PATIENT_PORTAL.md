# Patient Portal - Separate Profile Page

## Overview
Patients have a completely separate interface from the main application. When a patient logs in, they are directed to their own profile page where they can view their information, appointments, and treatment history.

## Features

### Access Control
- **Patient users** (in 'patient' group) are automatically redirected to `/patient-profile`
- **Staff users** cannot access the patient portal
- **Patients cannot access** the main application dashboard or any admin features

### Patient Profile Page
Located at: `/patient-profile`

#### Components:
1. **Personal Information Tab**
   - Full name, gender, date of birth
   - Contact information (phone, email, address)
   - Blood type
   - Medical notes
   - Emergency contact details

2. **My Appointments Tab**
   - View all past and upcoming appointments
   - Appointment date, time, type
   - Status (scheduled, confirmed, completed, cancelled)
   - Appointment notes

3. **Treatment History Tab**
   - All treatment records
   - Treatment type and date
   - Tooth number
   - Cost
   - Payment status (paid, partial, unpaid)

4. **Change Password**
   - Secure password change functionality
   - Requires current password
   - Password validation

## Implementation Details

### Route Guards
File: `frontend/src/router/index.js`

```javascript
// Patients can only access /patient-profile
if (to.meta.requiresStaff) {
  const isPatient = authStore.user?.group_names?.includes('patient')
  if (isPatient) {
    next('/patient-profile')
    return
  }
}

// Staff cannot access patient profile
if (to.meta.requiresPatient) {
  const isPatient = authStore.user?.group_names?.includes('patient')
  if (!isPatient) {
    next('/')
    return
  }
}
```

### Login Redirect Logic
File: `frontend/src/views/LoginView.vue`

```javascript
// Redirect based on user role
const isPatient = authStore.user?.group_names?.includes('patient')
if (isPatient) {
  router.push('/patient-profile')
} else {
  router.push('/')
}
```

### Auth Store Getters
File: `frontend/src/stores/auth.js`

```javascript
getters: {
  isPatient: (state) => {
    return state.user?.group_names?.includes('patient') || false
  },
  isStaff: (state) => {
    return state.user?.is_staff || false
  }
}
```

## Routes Configuration

### Patient Route
```javascript
{
  path: '/patient-profile',
  name: 'patient-profile',
  component: PatientProfileView,
  meta: { 
    requiresAuth: true,
    requiresPatient: true 
  }
}
```

### Staff Routes
```javascript
{
  path: '/',
  component: DashboardLayout,
  meta: { 
    requiresAuth: true,
    requiresStaff: true 
  },
  children: [/* all staff routes */]
}
```

## Testing

### Test Patient Login
1. Use credentials created for patients:
   - **Username**: Patient ID (e.g., `P001`)
   - **Password**: Patient Last Name (e.g., `Garcia`)

2. Expected behavior:
   - Patient is logged in
   - Redirected to `/patient-profile`
   - Cannot access `/`, `/employees`, etc.
   - Trying to access staff routes redirects back to `/patient-profile`

### Test Staff Login
1. Use staff credentials
2. Expected behavior:
   - Staff is logged in
   - Redirected to `/` (dashboard)
   - Cannot access `/patient-profile`
   - Has full access to all admin features

## API Endpoints Used

### Get Patient Data
```
GET /api/patient/patients/?search={patient_id}
```
Returns patient by searching for their patient ID (username)

### Get Patient Appointments
```
GET /api/patient/patients/{id}/appointments/
```
Returns all appointments for the patient

### Get Patient Treatments
```
GET /api/patient/patients/{id}/treatments/
```
Returns all treatment records for the patient

### Change Password
```
POST /api/change-password/
Body: {
  current_password: "string",
  new_password: "string"
}
```

## Security Features

1. **Route-Level Protection**
   - Navigation guards prevent unauthorized access
   - Automatic redirection based on user role

2. **Data Isolation**
   - Patients can only view their own data
   - API queries filter by patient ID (username)

3. **Password Management**
   - Patients can change their password
   - Current password verification required
   - Password strength validation (minimum 6 characters)

## User Experience

### Patient Portal UI
- Clean, simple interface
- No sidebar navigation
- Top navbar with:
  - DentHub branding
  - Patient name display
  - Logout button
- Card-based layout
- Tabbed interface for different information types

### Color Coding
- **Status badges**:
  - Active: Green
  - Inactive: Yellow
  - Archived: Gray

- **Appointment status**:
  - Scheduled: Blue
  - Confirmed: Light Blue
  - Completed: Green
  - Cancelled: Red
  - No Show: Yellow

- **Payment status**:
  - Paid: Green
  - Partial: Yellow
  - Unpaid: Red

## Future Enhancements

- [ ] Book new appointments
- [ ] Cancel/reschedule appointments
- [ ] Upload documents (X-rays, insurance)
- [ ] Message dentist/staff
- [ ] View bills and make payments
- [ ] Download treatment receipts
- [ ] Set appointment reminders
- [ ] Update contact information
- [ ] View dental health tips

## Troubleshooting

### Patient Redirected to Main Dashboard
- Check if user is in 'patient' group
- Verify `group_names` array includes 'patient'
- Check browser console for errors

### Cannot Access Patient Profile
- Ensure patient group exists in database
- Verify user has correct group assignment
- Check route guard logic in router

### Data Not Loading
- Check API endpoint accessibility
- Verify patient ID matches username
- Check browser network tab for failed requests
- Ensure Django server is running

## Files Modified/Created

1. **Created**: `frontend/src/views/PatientProfileView.vue` - Main patient portal page
2. **Modified**: `frontend/src/router/index.js` - Added route guards and patient route
3. **Modified**: `frontend/src/stores/auth.js` - Added isPatient and isStaff getters
4. **Modified**: `frontend/src/views/LoginView.vue` - Role-based redirect after login

## Current Status
✅ Patient profile page created  
✅ Role-based access control implemented  
✅ Route guards configured  
✅ Login redirect logic updated  
✅ Password change functionality  
✅ View appointments and treatments  
✅ Responsive design  
✅ AdminLTE styling integrated  

Patients now have a completely separate, secure portal to view their dental health information!
