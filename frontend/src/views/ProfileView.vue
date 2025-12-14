<template>
  <div class="content-header">
    <div class="container-fluid">
      <div class="row mb-2">
        <div class="col-sm-6">
          <h1 class="m-0">My Profile</h1>
        </div>
      </div>
    </div>
  </div>

  <section class="content">
    <div class="container-fluid">
      <div class="row">
        <!-- Profile Information -->
        <div class="col-md-6">
          <div class="card">
            <div class="card-header">
              <h3 class="card-title">Profile Information</h3>
            </div>
            <div class="card-body">
              <form @submit.prevent="updateProfile">
                <!-- Photo Section -->
                <div class="form-group text-center">
                  <div class="mb-3">
                    <img 
                      v-if="photoPreview || profileData.employee_photo" 
                      :src="photoPreview || profileData.employee_photo" 
                      alt="Profile Photo" 
                      style="width: 150px; height: 150px; object-fit: cover; border-radius: 50%;"
                      class="img-thumbnail"
                    >
                    <i v-else class="fas fa-user-circle fa-8x text-muted"></i>
                  </div>
                  
                  <div class="custom-file" style="max-width: 300px; margin: 0 auto;">
                    <input 
                      type="file" 
                      class="custom-file-input" 
                      id="profilePhotoInput"
                      @change="handlePhotoChange"
                      accept="image/*"
                    >
                    <label class="custom-file-label" for="profilePhotoInput">
                      {{ photoFileName || 'Change Photo...' }}
                    </label>
                  </div>
                  <small class="form-text text-muted">Accepted formats: JPG, PNG, GIF (Max 5MB)</small>
                  
                  <button 
                    v-if="photoPreview || profileData.employee_photo"
                    type="button" 
                    class="btn btn-sm btn-danger mt-2"
                    @click="removePhoto"
                  >
                    <i class="fas fa-trash"></i> Remove Photo
                  </button>
                </div>

                <hr>

                <div class="form-group">
                  <label>Username</label>
                  <input 
                    type="text" 
                    v-model="profileData.username" 
                    class="form-control" 
                    readonly
                  >
                  <small class="text-muted">Username cannot be changed</small>
                </div>

                <div class="row">
                  <div class="col-md-6">
                    <div class="form-group">
                      <label>First Name</label>
                      <input 
                        type="text" 
                        v-model="profileData.first_name" 
                        class="form-control" 
                        required
                      >
                    </div>
                  </div>
                  <div class="col-md-6">
                    <div class="form-group">
                      <label>Last Name</label>
                      <input 
                        type="text" 
                        v-model="profileData.last_name" 
                        class="form-control" 
                        required
                      >
                    </div>
                  </div>
                </div>

                <div class="form-group">
                  <label>Email</label>
                  <input 
                    type="email" 
                    v-model="profileData.email" 
                    class="form-control" 
                    required
                  >
                </div>

                <div class="form-group">
                  <label>Phone <small class="text-muted">(Optional)</small></label>
                  <input 
                    type="text" 
                    v-model="profileData.phone" 
                    class="form-control"
                  >
                </div>

                <button type="submit" class="btn btn-primary">
                  <i class="fas fa-save"></i> Update Profile
                </button>
              </form>
            </div>
          </div>
        </div>

        <!-- Change Password -->
        <div class="col-md-6">
          <!-- Employee Information (if linked) -->
          <div class="card" v-if="employeeData">
            <div class="card-header">
              <h3 class="card-title">Employee Information</h3>
            </div>
            <div class="card-body">
              <table class="table table-sm">
                <tbody>
                  <tr>
                    <th width="40%">Employee ID:</th>
                    <td>{{ employeeData.employee_id }}</td>
                  </tr>
                  <tr>
                    <th>Department:</th>
                    <td>{{ employeeData.department_name || 'N/A' }}</td>
                  </tr>
                  <tr>
                    <th>Position:</th>
                    <td>{{ employeeData.position_name || 'N/A' }}</td>
                  </tr>
                  <tr>
                    <th>Branch:</th>
                    <td>{{ employeeData.branch_name || 'N/A' }}</td>
                  </tr>
                  <tr>
                    <th>Hire Date:</th>
                    <td>{{ formatDate(employeeData.hire_date) }}</td>
                  </tr>
                  <tr>
                    <th>Status:</th>
                    <td>
                      <span :class="['badge', employeeData.status === 'active' ? 'badge-success' : 'badge-secondary']">
                        {{ employeeData.status }}
                      </span>
                    </td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>

          <div class="card">
            <div class="card-header">
              <h3 class="card-title">Change Password</h3>
            </div>
            <div class="card-body">
              <form @submit.prevent="changePassword">
                <div class="form-group">
                  <label>Current Password</label>
                  <input 
                    type="password" 
                    v-model="passwordData.current_password" 
                    class="form-control" 
                    required
                  >
                </div>

                <div class="form-group">
                  <label>New Password</label>
                  <input 
                    type="password" 
                    v-model="passwordData.new_password" 
                    class="form-control" 
                    required
                    minlength="8"
                  >
                  <small class="text-muted">Minimum 8 characters</small>
                </div>

                <div class="form-group">
                  <label>Confirm New Password</label>
                  <input 
                    type="password" 
                    v-model="passwordData.confirm_password" 
                    class="form-control" 
                    required
                  >
                </div>

                <button type="submit" class="btn btn-warning">
                  <i class="fas fa-key"></i> Change Password
                </button>
              </form>
            </div>
          </div>
        </div>
      </div>
    </div>
  </section>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useAuthStore } from '../stores/auth'
import api from '../services/api'
import Swal from 'sweetalert2'

const authStore = useAuthStore()

const profileData = ref({
  username: '',
  first_name: '',
  last_name: '',
  email: '',
  phone: '',
  employee_photo: null
})

const passwordData = ref({
  current_password: '',
  new_password: '',
  confirm_password: ''
})

const employeeData = ref(null)
const photoFile = ref(null)
const photoPreview = ref(null)
const photoFileName = ref('')

const fetchProfile = async () => {
  try {
    const response = await api.get('/current-user/')
    profileData.value = {
      id: response.data.id,
      username: response.data.username,
      first_name: response.data.first_name,
      last_name: response.data.last_name,
      email: response.data.email,
      phone: response.data.phone || '',
      employee_photo: null
    }

    // Fetch employee data if user is linked to an employee
    await fetchEmployeeData()
  } catch (error) {
    console.error('Error fetching profile:', error)
    await Swal.fire({
      title: 'Error!',
      text: 'Failed to load profile',
      icon: 'error'
    })
  }
}

const fetchEmployeeData = async () => {
  try {
    const response = await api.get('/employees/')
    // Find employee linked to current user
    const employee = response.data.find(emp => emp.user === profileData.value.id)
    if (employee) {
      employeeData.value = employee
      profileData.value.employee_photo = employee.photo
    }
  } catch (error) {
    console.error('Error fetching employee data:', error)
  }
}

const handlePhotoChange = (event) => {
  const file = event.target.files[0]
  if (file) {
    // Validate file size (25MB max)
    if (file.size > 25 * 1024 * 1024) {
      Swal.fire({
        icon: 'error',
        title: 'File Too Large',
        text: 'Photo must be less than 25MB'
      })
      event.target.value = ''
      return
    }
    
    // Validate file type
    if (!file.type.startsWith('image/')) {
      Swal.fire({
        icon: 'error',
        title: 'Invalid File Type',
        text: 'Please select an image file'
      })
      event.target.value = ''
      return
    }
    
    photoFile.value = file
    photoFileName.value = file.name
    
    // Create preview
    const reader = new FileReader()
    reader.onload = (e) => {
      photoPreview.value = e.target.result
    }
    reader.readAsDataURL(file)
  }
}

const removePhoto = () => {
  photoFile.value = null
  photoPreview.value = null
  photoFileName.value = ''
  
  // Reset file input
  const fileInput = document.getElementById('profilePhotoInput')
  if (fileInput) {
    fileInput.value = ''
  }
}

const updateProfile = async () => {
  try {
    // Update user data
    const updateData = {
      first_name: profileData.value.first_name,
      last_name: profileData.value.last_name,
      email: profileData.value.email,
      phone: profileData.value.phone
    }

    await api.patch(`/users/${profileData.value.id}/`, updateData)
    
    // Update auth store
    authStore.user.first_name = profileData.value.first_name
    authStore.user.last_name = profileData.value.last_name
    authStore.user.email = profileData.value.email
    authStore.user.phone = profileData.value.phone

    // Update employee photo if changed and user has employee record
    if (photoFile.value && employeeData.value) {
      const formData = new FormData()
      formData.append('photo', photoFile.value)
      
      await api.patch(`/employees/${employeeData.value.id}/`, formData, {
        headers: {
          'Content-Type': 'multipart/form-data'
        }
      })
      
      // Refresh employee data to get new photo URL
      await fetchEmployeeData()
      photoFile.value = null
      photoPreview.value = null
      photoFileName.value = ''
    }

    await Swal.fire({
      title: 'Success!',
      text: 'Profile updated successfully',
      icon: 'success',
      timer: 2000
    })
  } catch (error) {
    console.error('Error updating profile:', error)
    await Swal.fire({
      title: 'Error!',
      text: error.response?.data?.detail || 'Failed to update profile',
      icon: 'error'
    })
  }
}

const changePassword = async () => {
  // Validate passwords match
  if (passwordData.value.new_password !== passwordData.value.confirm_password) {
    await Swal.fire({
      title: 'Error!',
      text: 'New passwords do not match',
      icon: 'error'
    })
    return
  }

  // Validate password length
  if (passwordData.value.new_password.length < 8) {
    await Swal.fire({
      title: 'Error!',
      text: 'Password must be at least 8 characters',
      icon: 'error'
    })
    return
  }

  try {
    await api.post('/change-password/', {
      current_password: passwordData.value.current_password,
      new_password: passwordData.value.new_password
    })

    // Reset form
    passwordData.value = {
      current_password: '',
      new_password: '',
      confirm_password: ''
    }

    await Swal.fire({
      title: 'Success!',
      text: 'Password changed successfully',
      icon: 'success',
      timer: 2000
    })
  } catch (error) {
    console.error('Error changing password:', error)
    await Swal.fire({
      title: 'Error!',
      text: error.response?.data?.error || 'Failed to change password',
      icon: 'error'
    })
  }
}

const formatDate = (dateString) => {
  if (!dateString) return 'N/A'
  const date = new Date(dateString)
  return date.toLocaleDateString('en-US', { year: 'numeric', month: 'long', day: 'numeric' })
}

onMounted(() => {
  fetchProfile()
})
</script>

<style scoped>
.card {
  box-shadow: 0 0 1px rgba(0,0,0,.125), 0 1px 3px rgba(0,0,0,.2);
}

.card-header {
  background-color: #f4f6f9;
  border-bottom: 1px solid #dee2e6;
}

.table th {
  font-weight: 600;
}
</style>
