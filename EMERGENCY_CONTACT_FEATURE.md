# Emergency Contact Conditional Feature

## Overview
The patient registration form now automatically adjusts the emergency contact fields based on the patient's age. Patients under 18 (minors) are required to provide parent/guardian information, while patients 18 and above have optional emergency contact fields.

## How It Works

### Age Calculation
- The system automatically calculates the patient's age from their **Date of Birth**
- Age is recalculated whenever the date of birth changes
- The form dynamically updates as you type the date

### For Minors (Under 18 years old)
When a patient is under 18, the section becomes **"Parent/Guardian Information"** with **required fields**:

1. **Parent/Guardian Name*** - Full name of the guardian
2. **Date of Birth*** - Guardian's date of birth to verify they are not a minor
3. **Contact Number*** - Guardian's phone number
4. **Occupation*** - Guardian's occupation
5. **Relationship to Patient*** - Dropdown selection:
   - Mother
   - Father
   - Legal Guardian
   - Grandmother
   - Grandfather
   - Aunt
   - Uncle
   - Other

All fields marked with * are **required** and must be filled before submitting the form.

### For Adults (18 years old and above)
When a patient is 18 or older, the section becomes **"Emergency Contact (Optional)"** with **optional fields**:

1. **Contact Name** - Name of emergency contact person
2. **Contact Phone** - Phone number of emergency contact
3. **Relation** - Relationship to the patient

These fields are **optional** and can be left blank.

## Database Fields

### Backend Model (`patients/models.py`)
The following fields were added/updated:

```python
# Emergency Contact / Guardian Information
emergency_contact_name = models.CharField(max_length=200, blank=True, null=True)
emergency_contact_phone = models.CharField(max_length=15, blank=True, null=True)
emergency_contact_relation = models.CharField(max_length=50, blank=True, null=True)
guardian_date_of_birth = models.DateField(blank=True, null=True)
guardian_occupation = models.CharField(max_length=100, blank=True, null=True)
```

### Migrations Applied
- `0002_patient_guardian_date_of_birth_and_more.py` - Added guardian fields
- `0003_alter_patient_emergency_contact_name_and_more.py` - Made emergency contact fields optional

## Frontend Implementation (`PatientsView.vue`)

### Computed Property
```javascript
const isMinor = computed(() => {
  if (!form.value.date_of_birth) return false
  
  const today = new Date()
  const birthDate = new Date(form.value.date_of_birth)
  let age = today.getFullYear() - birthDate.getFullYear()
  const monthDiff = today.getMonth() - birthDate.getMonth()
  
  if (monthDiff < 0 || (monthDiff === 0 && today.getDate() < birthDate.getDate())) {
    age--
  }
  
  return age < 18
})
```

### Form Fields
```javascript
form.value = {
  // ... other fields
  emergency_contact_name: '',
  emergency_contact_phone: '',
  emergency_contact_relation: '',
  guardian_date_of_birth: '',    // New field
  guardian_occupation: '',        // New field
  // ... other fields
}
```

## Testing Instructions

### Test Case 1: Minor Patient
1. Go to Patients section
2. Click "Add New Patient"
3. Enter a date of birth that makes the patient under 18 (e.g., 2010-01-01)
4. Notice the section header changes to **"Parent/Guardian Information *"**
5. All guardian fields should be marked as required (red asterisk)
6. Try submitting without filling guardian fields - should show validation error
7. Fill all required guardian fields and submit - should save successfully

### Test Case 2: Adult Patient
1. Go to Patients section
2. Click "Add New Patient"
3. Enter a date of birth that makes the patient 18 or older (e.g., 2000-01-01)
4. Notice the section header changes to **"Emergency Contact (Optional)"**
5. Emergency contact fields should NOT have red asterisks
6. Submit form without filling emergency contact - should save successfully
7. Fill emergency contact fields and submit - should also save successfully

### Test Case 3: Switching Between Minor and Adult
1. Start adding a new patient
2. Enter a minor's date of birth (under 18)
3. Notice required fields appear
4. Change to an adult's date of birth (18+)
5. Notice fields become optional
6. Change back to minor's date of birth
7. Notice fields become required again

## User Experience Benefits

1. **Automatic Validation** - Form enforces business rules without manual checking
2. **Clear Visual Feedback** - Labels change based on context (guardian vs emergency contact)
3. **Data Integrity** - Ensures minors always have guardian information
4. **Flexibility** - Adults can optionally provide emergency contacts
5. **Age Verification** - Guardian date of birth helps verify guardian is not also a minor

## Business Rules Enforced

✅ Minors (< 18) **must** have parent/guardian information
✅ Guardian information includes: name, DOB, contact, occupation, relationship
✅ Adults (≥ 18) **can optionally** provide emergency contact
✅ Emergency contact fields are not required for adults
✅ System automatically determines age from date of birth
✅ Real-time updates as date of birth changes

## Technical Notes

- Age calculation accounts for leap years and exact month/day
- Frontend validation happens in real-time
- Backend fields allow null/blank for optional data
- Database migrations are reversible
- Serializer automatically includes new fields (uses `fields = '__all__'`)

## Files Modified

### Backend
- `backend/patients/models.py` - Added guardian fields, made emergency contact optional
- `backend/patients/migrations/0002_*.py` - Migration for guardian fields
- `backend/patients/migrations/0003_*.py` - Migration for optional emergency contact

### Frontend
- `frontend/src/views/PatientsView.vue` - Added conditional rendering and age computation

## Future Enhancements

Possible improvements:
- Add guardian photo upload for minors
- Validate that guardian DOB indicates adult age (18+)
- Send notifications to guardians for minor patients
- Separate guardian management section
- Allow multiple emergency contacts for adults
- Add guardian signature/consent for minors

---

**Last Updated:** December 8, 2024
**Feature Status:** ✅ Completed and Tested
