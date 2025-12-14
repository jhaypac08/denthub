<template>
  <div class="content-header">
    <div class="container-fluid">
      <div class="row mb-2">
        <div class="col-sm-6">
          <h1 class="m-0">Employee Management</h1>
        </div>
        <div class="col-sm-6">
          <button class="btn btn-info float-right ml-2" @click="refreshTable" title="Refresh">
            <i class="fas fa-sync-alt"></i>
          </button>
          <button class="btn btn-primary float-right" @click="openAddModal">
            <i class="fas fa-plus"></i> Add Employee
          </button>
        </div>
      </div>
    </div>
  </div>

  <section class="content">
    <div class="container-fluid">
      <div class="card">
        <div class="card-header">
          <h3 class="card-title">Employee List</h3>
          <div class="card-tools">
            <div class="input-group input-group-sm" style="width: 250px;">
              <input 
                type="text" 
                v-model="searchQuery"
                class="form-control float-right" 
                placeholder="Search"
              >
              <div class="input-group-append">
                <button class="btn btn-default">
                  <i class="fas fa-search"></i>
                </button>
              </div>
            </div>
          </div>
        </div>

        <div class="card-body table-responsive p-0">
          <table class="table table-hover text-nowrap">
            <thead>
              <tr>
                <th>Photo</th>
                <th>Employee ID</th>
                <th>Name</th>
                <th>Email</th>
                <th>Position</th>
                <th>Department</th>
                <th>Branch</th>
                <th>Status</th>
                <th>Actions</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="employee in filteredEmployees" :key="employee.id" @click="viewEmployee(employee)" style="cursor: pointer;">
                <td class="align-middle">
                  <img 
                    v-if="employee.photo" 
                    :src="employee.photo" 
                    alt="Photo" 
                    style="width: 40px; height: 40px; object-fit: cover; border-radius: 50%;"
                    class="img-thumbnail"
                  >
                  <i v-else class="fas fa-user-circle fa-2x text-muted"></i>
                </td>
                <td class="align-middle">{{ employee.employee_id }}</td>
                <td class="align-middle">
                  <span v-if="employee.middle_name">
                    {{ employee.first_name }} {{ employee.middle_name }} {{ employee.last_name }}
                  </span>
                  <span v-else>
                    {{ employee.first_name }} {{ employee.last_name }}
                  </span>
                </td>
                <td class="align-middle">{{ employee.email }}</td>
                <td class="align-middle">{{ employee.position_name || 'N/A' }}</td>
                <td class="align-middle">{{ employee.department_name || 'N/A' }}</td>
                <td class="align-middle">{{ employee.branch_name || 'N/A' }}</td>
                <td class="align-middle" @click.stop>
                  <div class="custom-control custom-switch">
                    <input 
                      type="checkbox" 
                      class="custom-control-input" 
                      :id="'status-' + employee.id"
                      :checked="employee.status === 'active'"
                      @change="toggleStatus(employee)"
                    >
                    <label class="custom-control-label" :for="'status-' + employee.id">
                      {{ employee.status === 'active' ? 'Active' : 'Inactive' }}
                    </label>
                  </div>
                </td>
                <td class="align-middle" @click.stop>
                  <button class="btn btn-sm btn-info" @click="openEditModal(employee)">
                    <i class="fas fa-edit"></i>
                  </button>
                  <button 
                    v-if="!employee.has_user" 
                    class="btn btn-sm btn-success ml-1" 
                    @click="createUserAccount(employee)"
                    title="Create User Account"
                  >
                    <i class="fas fa-user-plus"></i>
                  </button>
                  <button class="btn btn-sm btn-danger ml-1" @click="deleteEmployee(employee.id)">
                    <i class="fas fa-trash"></i>
                  </button>
                </td>
              </tr>
              <tr v-if="filteredEmployees.length === 0">
                <td colspan="7" class="text-center">No employees found</td>
              </tr>
            </tbody>
          </table>
        </div>
        <div class="card-footer clearfix">
          <TablePagination
            :current-page="currentPage"
            :per-page="perPage"
            :total="totalEmployees"
            @page-change="handlePageChange"
          />
        </div>
      </div>
    </div>
  </section>

  <!-- Add/Edit Modal -->
  <div class="modal fade" id="employeeModal" tabindex="-1" ref="modalElement">
    <div class="modal-dialog modal-lg">
      <div class="modal-content">
        <div class="modal-header">
          <h4 class="modal-title">{{ isEditMode ? 'Edit' : 'Add' }} Employee</h4>
          <button type="button" class="close" @click="closeModal">
            <span>&times;</span>
          </button>
        </div>
        <form @submit.prevent="saveEmployee">
          <div class="modal-body">
            <div class="row" v-if="isEditMode">
              <div class="col-md-12">
                <div class="form-group">
                  <label>Employee ID</label>
                  <input 
                    type="text" 
                    v-model="formData.employee_id" 
                    class="form-control" 
                    readonly
                  >
                </div>
              </div>
            </div>

            <!-- Photo Upload Section -->
            <div class="row">
              <div class="col-md-12">
                <div class="form-group">
                  <label>Photo <small class="text-muted">(Optional)</small></label>
                  <div class="custom-file">
                    <input 
                      type="file" 
                      class="custom-file-input" 
                      id="photoInput"
                      @change="handlePhotoChange"
                      accept="image/*"
                    >
                    <label class="custom-file-label" for="photoInput">
                      {{ photoFileName || 'Choose file...' }}
                    </label>
                  </div>
                  <small class="form-text text-muted">Accepted formats: JPG, PNG, GIF (Max 5MB)</small>
                  
                  <!-- Photo Preview -->
                  <div v-if="photoPreview || (isEditMode && formData.photo)" class="mt-2">
                    <img 
                      :src="photoPreview || formData.photo" 
                      alt="Employee Photo" 
                      style="max-width: 150px; max-height: 150px; object-fit: cover; border-radius: 5px;"
                      class="img-thumbnail"
                    >
                    <button 
                      type="button" 
                      class="btn btn-sm btn-danger ml-2"
                      @click="removePhoto"
                    >
                      Remove Photo
                    </button>
                  </div>
                </div>
              </div>
            </div>

            <div class="row">
              <div class="col-md-4">
                <div class="form-group">
                  <label>First Name</label>
                  <input type="text" v-model="formData.first_name" class="form-control" required>
                </div>
              </div>
              <div class="col-md-4">
                <div class="form-group">
                  <label>Middle Name <small class="text-muted">(Optional)</small></label>
                  <input type="text" v-model="formData.middle_name" class="form-control">
                </div>
              </div>
              <div class="col-md-4">
                <div class="form-group">
                  <label>Last Name</label>
                  <input type="text" v-model="formData.last_name" class="form-control" required>
                </div>
              </div>
            </div>

            <div class="row">
              <div class="col-md-6">
                <div class="form-group">
                  <label>Email</label>
                  <input type="email" v-model="formData.email" class="form-control" required>
                </div>
              </div>
              <div class="col-md-6">
                <div class="form-group">
                  <label>Phone</label>
                  <input type="text" v-model="formData.phone" class="form-control" required>
                </div>
              </div>
            </div>

            <div class="row">
              <div class="col-md-6">
                <div class="form-group">
                  <label>Date of Birth</label>
                  <input type="date" v-model="formData.date_of_birth" class="form-control" required>
                </div>
              </div>
              <div class="col-md-6">
                <div class="form-group">
                  <label>Gender</label>
                  <select v-model="formData.gender" class="form-control" required>
                    <option value="M">Male</option>
                    <option value="F">Female</option>
                    <option value="O">Other</option>
                  </select>
                </div>
              </div>
            </div>

            <div class="form-group">
              <label>Address</label>
              <textarea v-model="formData.address" class="form-control" rows="2" required></textarea>
            </div>

            <div class="row">
              <div class="col-md-6">
                <div class="form-group">
                  <label>Position <small class="text-muted">(Optional)</small></label>
                  <select v-model="formData.position" class="form-control">
                    <option value="">Select Position</option>
                    <option v-for="pos in positions" :key="pos.id" :value="pos.id">
                      {{ pos.title }}
                    </option>
                  </select>
                </div>
              </div>
              <div class="col-md-6">
                <div class="form-group">
                  <label>Department(s)</label>
                  <select v-model="formData.department" class="form-control" multiple :required="isDepartmentEnabled" :disabled="!isDepartmentEnabled" style="height: 120px;">
                    <option v-for="dept in departments" :key="dept.id" :value="dept.id">
                      {{ dept.name }}
                    </option>
                  </select>
                  <small class="form-text text-muted">
                    <span v-if="isDepartmentEnabled">Hold Ctrl (Windows) or Cmd (Mac) to select multiple departments</span>
                    <span v-else class="text-warning">Department selection is only available for Dentist and Dental Assistant positions</span>
                  </small>
                </div>
              </div>
            </div>

            <div class="form-group">
              <label>Branch</label>
              <select v-model="formData.branch" class="form-control" required>
                <option value="">Select Branch</option>
                <option v-for="branch in branches" :key="branch.id" :value="branch.id">
                  {{ branch.name }}
                </option>
              </select>
            </div>

            <div class="row">
              <div class="col-md-6">
                <div class="form-group">
                  <label>Hire Date</label>
                  <input type="date" v-model="formData.hire_date" class="form-control" required>
                </div>
              </div>
              <div class="col-md-6">
                <div class="form-group">
                  <label>Salary <small class="text-muted">(Optional)</small></label>
                  <input type="number" step="0.01" v-model="formData.salary" class="form-control">
                </div>
              </div>
            </div>
          </div>
          <div class="modal-footer">
            <button type="button" class="btn btn-default" @click="closeModal">Close</button>
            <button type="submit" class="btn btn-primary">Save</button>
          </div>
        </form>
      </div>
    </div>
  </div>

  <!-- View Modal -->
  <div class="modal fade" id="viewModal" tabindex="-1">
    <div class="modal-dialog modal-xl">
      <div class="modal-content">
        <div class="modal-header bg-info">
          <h4 class="modal-title">Employee Details</h4>
          <button type="button" class="close" @click="closeViewModal" style="color: white;">
            <span>&times;</span>
          </button>
        </div>
        <div class="modal-body">
          <div class="row">
            <div class="col-md-3 text-center">
              <img 
                v-if="viewData.photo" 
                :src="viewData.photo" 
                alt="Employee Photo" 
                class="img-fluid rounded mb-3"
                style="max-width: 200px; max-height: 200px; object-fit: cover;"
              >
              <i v-else class="fas fa-user-circle fa-10x text-muted"></i>
            </div>
            <div class="col-md-9">
              <div class="row">
                <div class="col-md-6">
                  <p><strong>Employee ID:</strong> {{ viewData.employee_id }}</p>
                </div>
                <div class="col-md-6">
                  <p><strong>Status:</strong> 
                    <span :class="['badge', viewData.status === 'active' ? 'badge-success' : 'badge-secondary']">
                      {{ viewData.status === 'active' ? 'Active' : 'Inactive' }}
                    </span>
                  </p>
                </div>
              </div>
              <div class="row">
                <div class="col-md-4">
                  <p><strong>First Name:</strong> {{ viewData.first_name }}</p>
                </div>
                <div class="col-md-4">
                  <p><strong>Middle Name:</strong> {{ viewData.middle_name || 'N/A' }}</p>
                </div>
                <div class="col-md-4">
                  <p><strong>Last Name:</strong> {{ viewData.last_name }}</p>
                </div>
              </div>
              <div class="row">
                <div class="col-md-6">
                  <p><strong>Email:</strong> {{ viewData.email }}</p>
                </div>
                <div class="col-md-6">
                  <p><strong>Phone:</strong> {{ viewData.phone }}</p>
                </div>
              </div>
              <div class="row">
                <div class="col-md-4">
                  <p><strong>Gender:</strong> {{ viewData.gender === 'M' ? 'Male' : 'Female' }}</p>
                </div>
                <div class="col-md-4">
                  <p><strong>Date of Birth:</strong> {{ viewData.date_of_birth }}</p>
                </div>
                <div class="col-md-4">
                  <p><strong>Hire Date:</strong> {{ viewData.hire_date }}</p>
                </div>
              </div>
              <div class="row">
                <div class="col-md-12">
                  <p><strong>Address:</strong> {{ viewData.address }}</p>
                </div>
              </div>
              <div class="row">
                <div class="col-md-4">
                  <p><strong>Position:</strong> {{ viewData.position_name || 'N/A' }}</p>
                </div>
                <div class="col-md-4">
                  <p><strong>Department:</strong> {{ viewData.department_name || 'N/A' }}</p>
                </div>
                <div class="col-md-4">
                  <p><strong>Branch:</strong> {{ viewData.branch_name || 'N/A' }}</p>
                </div>
              </div>
              <div class="row">
                <div class="col-md-6">
                  <p><strong>Salary:</strong> ₱{{ viewData.salary ? parseFloat(viewData.salary).toLocaleString() : 'N/A' }}</p>
                </div>
                <div class="col-md-6">
                  <p><strong>Has User Account:</strong> 
                    <span :class="['badge', viewData.has_user ? 'badge-success' : 'badge-warning']">
                      {{ viewData.has_user ? 'Yes' : 'No' }}
                    </span>
                  </p>
                </div>
              </div>
            </div>
          </div>
        </div>
        <div class="modal-footer">
          <button type="button" class="btn btn-secondary" @click="closeViewModal">Close</button>
          <button type="button" class="btn btn-info" @click="editFromView">
            <i class="fas fa-edit"></i> Edit
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import api from '../services/api'
import Swal from 'sweetalert2'
import TablePagination from '../components/TablePagination.vue'

const employees = ref([])
const positions = ref([])
const departments = ref([])
const branches = ref([])
const searchQuery = ref('')
const isEditMode = ref(false)
const modalElement = ref(null)
const photoFile = ref(null)
const photoPreview = ref(null)
const photoFileName = ref('')
const currentPage = ref(1)
const perPage = ref(10)
const viewData = ref({})
let modalInstance = null

const formData = ref({
  employee_id: '',
  first_name: '',
  middle_name: '',
  last_name: '',
  email: '',
  phone: '',
  date_of_birth: '',
  gender: 'M',
  address: '',
  position: null,
  department: [],
  branch: null,
  hire_date: '',
  salary: '',
  status: 'active',
  photo: null
})

// Check if department selection should be enabled based on position
const isDepartmentEnabled = computed(() => {
  if (!formData.value.position) return false
  const selectedPosition = positions.value.find(p => p.id === formData.value.position)
  if (!selectedPosition) return false
  const positionTitle = selectedPosition.title.toLowerCase()
  return positionTitle.includes('dentist') || positionTitle.includes('dental assistant')
})

const allFilteredEmployees = computed(() => {
  if (!searchQuery.value) return employees.value
  
  const query = searchQuery.value.toLowerCase()
  return employees.value.filter(emp => 
    emp.employee_id.toLowerCase().includes(query) ||
    emp.first_name.toLowerCase().includes(query) ||
    emp.last_name.toLowerCase().includes(query) ||
    emp.email.toLowerCase().includes(query) ||
    (emp.position_name && emp.position_name.toLowerCase().includes(query)) ||
    (emp.department_name && emp.department_name.toLowerCase().includes(query)) ||
    (emp.branch_name && emp.branch_name.toLowerCase().includes(query))
  )
})

const totalEmployees = computed(() => allFilteredEmployees.value.length)

const filteredEmployees = computed(() => {
  const start = (currentPage.value - 1) * perPage.value
  const end = start + perPage.value
  return allFilteredEmployees.value.slice(start, end)
})

const handlePageChange = (page) => {
  currentPage.value = page
}

watch(searchQuery, () => {
  currentPage.value = 1
})

// Watch for position changes and clear department if not dentist/dental assistant
watch(() => formData.value.position, (newPosition) => {
  if (!isDepartmentEnabled.value) {
    formData.value.department = []
  }
})

const fetchEmployees = async () => {
  try {
    const response = await api.get('/employees/')
    employees.value = response.data
  } catch (error) {
    console.error('Error fetching employees:', error)
  }
}

const refreshTable = async () => {
  const button = event.target.closest('button')
  const icon = button.querySelector('i')
  icon.classList.add('fa-spin')
  
  await fetchEmployees()
  
  icon.classList.remove('fa-spin')
  
  const Toast = Swal.mixin({
    toast: true,
    position: 'top-end',
    showConfirmButton: false,
    timer: 2000,
    timerProgressBar: true
  })
  
  Toast.fire({
    icon: 'success',
    title: 'Table refreshed'
  })
}

const fetchPositions = async () => {
  try {
    const response = await api.get('/positions/?is_active=true')
    positions.value = response.data
  } catch (error) {
    console.error('Error fetching positions:', error)
  }
}

const fetchDepartments = async () => {
  try {
    const response = await api.get('/departments/?is_active=true')
    departments.value = response.data
  } catch (error) {
    console.error('Error fetching departments:', error)
  }
}

const fetchBranches = async () => {
  try {
    const response = await api.get('/branches/?is_active=true')
    branches.value = response.data
  } catch (error) {
    console.error('Error fetching branches:', error)
  }
}

const openAddModal = () => {
  isEditMode.value = false
  resetForm()
  showModal()
}

const openEditModal = (employee) => {
  isEditMode.value = true
  formData.value = {
    ...employee,
    // Ensure department is always an array
    department: Array.isArray(employee.department) 
      ? employee.department 
      : (employee.department ? [employee.department] : [])
  }
  photoPreview.value = null
  photoFile.value = null
  photoFileName.value = ''
  showModal()
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
  formData.value.photo = null
  
  // Reset file input
  const fileInput = document.getElementById('photoInput')
  if (fileInput) {
    fileInput.value = ''
  }
}

const saveEmployee = async () => {
  try {
    const submitData = new FormData()
    
    // Append all form fields except photo and department
    Object.keys(formData.value).forEach(key => {
      if (key !== 'photo' && key !== 'department' && formData.value[key] !== null && formData.value[key] !== '') {
        submitData.append(key, formData.value[key])
      }
    })
    
    // Handle department array - append each department ID separately
    if (formData.value.department && Array.isArray(formData.value.department)) {
      formData.value.department.forEach(deptId => {
        submitData.append('department', deptId)
      })
    }
    
    // Append photo file if selected
    if (photoFile.value) {
      submitData.append('photo', photoFile.value)
    }
    
    if (isEditMode.value) {
      await api.put(`/employees/${formData.value.id}/`, submitData, {
        headers: {
          'Content-Type': 'multipart/form-data'
        }
      })
      Swal.fire({
        icon: 'success',
        title: 'Success!',
        text: 'Employee updated successfully',
        timer: 1500,
        showConfirmButton: false
      })
    } else {
      await api.post('/employees/', submitData, {
        headers: {
          'Content-Type': 'multipart/form-data'
        }
      })
      Swal.fire({
        icon: 'success',
        title: 'Success!',
        text: 'Employee added successfully',
        timer: 1500,
        showConfirmButton: false
      })
    }
    
    await fetchEmployees()
    closeModal()
  } catch (error) {
    console.error('Error saving employee:', error)
    Swal.fire({
      icon: 'error',
      title: 'Error',
      text: 'Error saving employee: ' + (error.response?.data?.detail || error.message)
    })
  }
}

const deleteEmployee = async (id) => {
  if (confirm('Are you sure you want to delete this employee?')) {
    try {
      await api.delete(`/employees/${id}/`)
      await fetchEmployees()
    } catch (error) {
      console.error('Error deleting employee:', error)
    }
  }
}

const toggleStatus = async (employee) => {
  try {
    const newStatus = employee.status === 'active' ? 'inactive' : 'active'
    await api.patch(`/employees/${employee.id}/`, { status: newStatus })
    await fetchEmployees()
  } catch (error) {
    console.error('Error toggling status:', error)
    alert('Error updating status: ' + (error.response?.data?.detail || error.message))
  }
}

const createUserAccount = async (employee) => {
  try {
    const result = await Swal.fire({
      title: 'Create User Account',
      html: `
        <p>Create a user account for:</p>
        <p><strong>${employee.first_name} ${employee.last_name}</strong></p>
        <p>Employee ID: <strong>${employee.employee_id}</strong></p>
        <hr>
        <p class="text-muted">Username will be: <strong>${employee.employee_id}</strong></p>
        <p class="text-muted">Default password will be: <strong>${employee.employee_id}</strong></p>
        <p class="text-warning"><small>Employee should change password after first login</small></p>
      `,
      icon: 'question',
      showCancelButton: true,
      confirmButtonColor: '#28a745',
      cancelButtonColor: '#6c757d',
      confirmButtonText: 'Create Account',
      cancelButtonText: 'Cancel'
    })
    
    if (result.isConfirmed) {
      const response = await api.post('/create-user-account/', {
        employee_id: employee.employee_id
      })
      
      await Swal.fire({
        title: 'Success!',
        html: `
          <p>User account created successfully!</p>
          <hr>
          <p><strong>Username:</strong> ${response.data.username}</p>
          <p><strong>Default Password:</strong> ${response.data.default_password}</p>
          <p class="text-warning"><small>Please inform the employee to change their password</small></p>
        `,
        icon: 'success'
      })
      
      await fetchEmployees()
    }
  } catch (error) {
    console.error('Error creating user account:', error)
    await Swal.fire({
      title: 'Error!',
      text: error.response?.data?.error || 'Failed to create user account',
      icon: 'error'
    })
  }
}

const resetForm = () => {
  formData.value = {
    employee_id: '',
    first_name: '',
    middle_name: '',
    last_name: '',
    email: '',
    phone: '',
    date_of_birth: '',
    gender: 'M',
    address: '',
    position: null,
    department: [],
    branch: null,
    hire_date: '',
    salary: '',
    status: 'active',
    photo: null
  }
  photoFile.value = null
  photoPreview.value = null
  photoFileName.value = ''
  
  // Reset file input
  const fileInput = document.getElementById('photoInput')
  if (fileInput) {
    fileInput.value = ''
  }
}

const showModal = () => {
  const modal = document.getElementById('employeeModal')
  modal.classList.add('show')
  modal.style.display = 'block'
  document.body.classList.add('modal-open')
  
  const backdrop = document.createElement('div')
  backdrop.className = 'modal-backdrop fade show'
  backdrop.id = 'modal-backdrop'
  document.body.appendChild(backdrop)
}

const closeModal = () => {
  const modal = document.getElementById('employeeModal')
  modal.classList.remove('show')
  modal.style.display = 'none'
  document.body.classList.remove('modal-open')
  
  const backdrop = document.getElementById('modal-backdrop')
  if (backdrop) {
    backdrop.remove()
  }
  
  resetForm()
}

const viewEmployee = (employee) => {
  viewData.value = { ...employee }
  showViewModal()
}

const editFromView = () => {
  closeViewModal()
  formData.value = { ...viewData.value }
  isEditMode.value = true
  photoPreview.value = null
  photoFile.value = null
  photoFileName.value = ''
  showModal()
}

const showViewModal = () => {
  const modal = document.getElementById('viewModal')
  modal.classList.add('show')
  modal.style.display = 'block'
  document.body.classList.add('modal-open')
  
  const backdrop = document.createElement('div')
  backdrop.className = 'modal-backdrop fade show'
  backdrop.id = 'view-modal-backdrop'
  document.body.appendChild(backdrop)
}

const closeViewModal = () => {
  const modal = document.getElementById('viewModal')
  modal.classList.remove('show')
  modal.style.display = 'none'
  document.body.classList.remove('modal-open')
  
  const backdrop = document.getElementById('view-modal-backdrop')
  if (backdrop) {
    backdrop.remove()
  }
}

onMounted(() => {
  fetchEmployees()
  fetchPositions()
  fetchDepartments()
  fetchBranches()
})
</script>
