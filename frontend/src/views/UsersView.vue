<template>
  <div class="content-header">
    <div class="container-fluid">
      <div class="row mb-2">
        <div class="col-sm-6">
          <h1 class="m-0">User Management</h1>
        </div>
        <div class="col-sm-6">
          <button class="btn btn-info float-right ml-2" @click="refreshTable" title="Refresh">
            <i class="fas fa-sync-alt"></i>
          </button>
          <button class="btn btn-primary float-right" @click="openAddModal">
            <i class="fas fa-plus"></i> Add User
          </button>
        </div>
      </div>
    </div>
  </div>

  <section class="content">
    <div class="container-fluid">
      <!-- Filter Tabs -->
      <ul class="nav nav-tabs mb-3">
        <li class="nav-item">
          <a 
            class="nav-link" 
            :class="{ active: activeTab === 'all' }"
            @click="activeTab = 'all'"
            href="#"
            @click.prevent
          >
            All Users <span class="badge badge-secondary ml-1">{{ allFilteredUsers.length }}</span>
          </a>
        </li>
        <li class="nav-item">
          <a 
            class="nav-link" 
            :class="{ active: activeTab === 'patient' }"
            @click="activeTab = 'patient'"
            href="#"
            @click.prevent
          >
            Patients <span class="badge badge-primary ml-1">{{ patientUsers.length }}</span>
          </a>
        </li>
        <li class="nav-item">
          <a 
            class="nav-link" 
            :class="{ active: activeTab === 'staff' }"
            @click="activeTab = 'staff'"
            href="#"
            @click.prevent
          >
            Staff <span class="badge badge-success ml-1">{{ staffUsers.length }}</span>
          </a>
        </li>
        <li class="nav-item">
          <a 
            class="nav-link" 
            :class="{ active: activeTab === 'no-group' }"
            @click="activeTab = 'no-group'"
            href="#"
            @click.prevent
          >
            No Group <span class="badge badge-warning ml-1">{{ noGroupUsers.length }}</span>
          </a>
        </li>
      </ul>

      <div class="card">
        <div class="card-header">
          <h3 class="card-title">
            {{ activeTab === 'all' ? 'All Users' : 
               activeTab === 'patient' ? 'Patient Users' : 
               activeTab === 'staff' ? 'Staff Users' : 
               'Users Without Groups' }}
          </h3>
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
                <th>ID</th>
                <th>Username</th>
                <th>Name</th>
                <th>Email</th>
                <th>Phone</th>
                <th>Groups</th>
                <th>Staff</th>
                <th>Active</th>
                <th>Actions</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="user in filteredUsers" :key="user.id" @click="viewUser(user)" style="cursor: pointer;">
                <td>{{ user.id }}</td>
                <td>{{ user.username }}</td>
                <td>{{ user.first_name }} {{ user.last_name }}</td>
                <td>{{ user.email }}</td>
                <td>{{ user.phone || 'N/A' }}</td>
                <td>
                  <span 
                    v-for="groupName in user.group_names" 
                    :key="groupName" 
                    class="badge badge-info mr-1"
                  >
                    {{ groupName }}
                  </span>
                  <span v-if="!user.group_names || user.group_names.length === 0" class="text-muted">
                    No groups
                  </span>
                </td>
                <td>
                  <span :class="['badge', user.is_staff ? 'badge-success' : 'badge-secondary']">
                    {{ user.is_staff ? 'Yes' : 'No' }}
                  </span>
                </td>
                <td @click.stop>
                  <div class="custom-control custom-switch">
                    <input 
                      type="checkbox" 
                      class="custom-control-input" 
                      :id="'active-' + user.id"
                      :checked="user.is_active"
                      @change="toggleActive(user)"
                    >
                    <label class="custom-control-label" :for="'active-' + user.id">
                      {{ user.is_active ? 'Active' : 'Inactive' }}
                    </label>
                  </div>
                </td>
                <td class="align-middle" @click.stop>
                  <button class="btn btn-sm btn-info" @click="openEditModal(user)">
                    <i class="fas fa-edit"></i>
                  </button>
                  <button 
                    class="btn btn-sm btn-warning ml-1" 
                    @click="resetPassword(user)"
                    title="Reset Password"
                  >
                    <i class="fas fa-key"></i>
                  </button>
                  <button 
                    class="btn btn-sm btn-danger ml-1" 
                    @click="deleteUser(user.id)"
                    :disabled="user.is_superuser"
                  >
                    <i class="fas fa-trash"></i>
                  </button>
                </td>
              </tr>
              <tr v-if="filteredUsers.length === 0">
                <td colspan="9" class="text-center">No users found</td>
              </tr>
            </tbody>
          </table>
        </div>
        <div class="card-footer clearfix">
          <TablePagination
            :current-page="currentPage"
            :per-page="perPage"
            :total="totalUsers"
            @page-change="handlePageChange"
          />
        </div>
      </div>
    </div>
  </section>

  <!-- Add/Edit Modal -->
  <div class="modal fade" id="userModal" tabindex="-1" ref="modalElement">
    <div class="modal-dialog">
      <div class="modal-content">
        <div class="modal-header">
          <h4 class="modal-title">{{ isEditMode ? 'Edit' : 'Add' }} User</h4>
          <button type="button" class="close" @click="closeModal">
            <span>&times;</span>
          </button>
        </div>
        <form @submit.prevent="saveUser">
          <div class="modal-body">
            <div class="form-group" v-if="!isEditMode">
              <label>Select Employee</label>
              <select 
                v-model="selectedEmployeeId" 
                class="form-control" 
                required
                @change="onEmployeeSelected"
              >
                <option value="">-- Select Employee --</option>
                <option v-for="emp in employeesWithoutUser" :key="emp.id" :value="emp.id">
                  {{ emp.employee_id }} - {{ emp.first_name }} {{ emp.middle_name ? emp.middle_name + ' ' : '' }}{{ emp.last_name }}
                </option>
              </select>
              <small class="form-text text-muted">Only employees without user accounts are shown</small>
            </div>

            <div class="form-group" v-if="isEditMode">
              <label>Username</label>
              <input 
                type="text" 
                v-model="formData.username" 
                class="form-control" 
                required
                readonly
              >
            </div>

            <div class="row">
              <div class="col-md-6">
                <div class="form-group">
                  <label>First Name</label>
                  <input 
                    type="text" 
                    v-model="formData.first_name" 
                    class="form-control" 
                    required
                    :readonly="!isEditMode"
                  >
                </div>
              </div>
              <div class="col-md-6">
                <div class="form-group">
                  <label>Last Name</label>
                  <input 
                    type="text" 
                    v-model="formData.last_name" 
                    class="form-control" 
                    required
                    :readonly="!isEditMode"
                  >
                </div>
              </div>
            </div>

            <div class="form-group">
              <label>Email</label>
              <input 
                type="email" 
                v-model="formData.email" 
                class="form-control" 
                required
                :readonly="!isEditMode"
              >
            </div>

            <div class="form-group">
              <label>Phone <small class="text-muted">(Optional)</small></label>
              <input 
                type="text" 
                v-model="formData.phone" 
                class="form-control"
                :readonly="!isEditMode"
              >
            </div>

            <div class="form-group">
              <label>Groups <small class="text-muted">(Optional)</small></label>
              <select 
                v-model="formData.groups" 
                class="form-control" 
                multiple 
                size="4"
                style="height: auto;"
              >
                <option v-for="group in availableGroups" :key="group.id" :value="group.id">
                  {{ group.name }}
                </option>
              </select>
              <small class="form-text text-muted">Hold Ctrl/Cmd to select multiple groups</small>
            </div>

            <div class="form-group" v-if="!isEditMode">
              <label>Password</label>
              <input type="password" v-model="formData.password" class="form-control" required>
              <small class="form-text text-muted">Minimum 8 characters</small>
            </div>

            <div class="form-check">
              <input 
                type="checkbox" 
                class="form-check-input" 
                id="is_staff"
                v-model="formData.is_staff"
              >
              <label class="form-check-label" for="is_staff">
                Staff Status (Can access admin panel)
              </label>
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
    <div class="modal-dialog">
      <div class="modal-content">
        <div class="modal-header bg-info">
          <h4 class="modal-title">User Details</h4>
          <button type="button" class="close" @click="closeViewModal" style="color: white;">
            <span>&times;</span>
          </button>
        </div>
        <div class="modal-body">
          <div class="row">
            <div class="col-md-6">
              <p><strong>User ID:</strong> {{ viewData.id }}</p>
            </div>
            <div class="col-md-6">
              <p><strong>Username:</strong> {{ viewData.username }}</p>
            </div>
          </div>
          <div class="row">
            <div class="col-md-6">
              <p><strong>First Name:</strong> {{ viewData.first_name }}</p>
            </div>
            <div class="col-md-6">
              <p><strong>Last Name:</strong> {{ viewData.last_name }}</p>
            </div>
          </div>
          <div class="row">
            <div class="col-md-6">
              <p><strong>Email:</strong> {{ viewData.email }}</p>
            </div>
            <div class="col-md-6">
              <p><strong>Phone:</strong> {{ viewData.phone || 'N/A' }}</p>
            </div>
          </div>
          <div class="row">
            <div class="col-md-12">
              <p><strong>Groups:</strong>
                <span v-if="viewData.group_names && viewData.group_names.length > 0">
                  <span v-for="groupName in viewData.group_names" :key="groupName" class="badge badge-info mr-1">
                    {{ groupName }}
                  </span>
                </span>
                <span v-else class="text-muted">No groups assigned</span>
              </p>
            </div>
          </div>
          <div class="row">
            <div class="col-md-6">
              <p><strong>Staff Status:</strong> 
                <span :class="['badge', viewData.is_staff ? 'badge-success' : 'badge-secondary']">
                  {{ viewData.is_staff ? 'Yes' : 'No' }}
                </span>
              </p>
            </div>
            <div class="col-md-6">
              <p><strong>Active Status:</strong> 
                <span :class="['badge', viewData.is_active ? 'badge-success' : 'badge-secondary']">
                  {{ viewData.is_active ? 'Active' : 'Inactive' }}
                </span>
              </p>
            </div>
          </div>
          <div class="row" v-if="viewData.is_superuser">
            <div class="col-md-12">
              <p><strong>Superuser:</strong> 
                <span class="badge badge-danger">Yes</span>
              </p>
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

const users = ref([])
const employees = ref([])
const availableGroups = ref([])
const searchQuery = ref('')
const isEditMode = ref(false)
const modalElement = ref(null)
const selectedEmployeeId = ref('')
const currentPage = ref(1)
const perPage = ref(10)
const viewData = ref({})
const activeTab = ref('all')

const formData = ref({
  username: '',
  first_name: '',
  last_name: '',
  email: '',
  phone: '',
  password: '',
  is_staff: false,
  groups: []
})

const employeesWithoutUser = computed(() => {
  return employees.value.filter(emp => !emp.has_user)
})

// Separate users by groups
const patientUsers = computed(() => {
  return users.value.filter(user => 
    user.id !== 1 && user.group_names && user.group_names.includes('patient')
  )
})

const staffUsers = computed(() => {
  return users.value.filter(user => 
    user.id !== 1 && 
    user.group_names && 
    user.group_names.length > 0 && 
    !user.group_names.includes('patient')
  )
})

const noGroupUsers = computed(() => {
  return users.value.filter(user => 
    user.id !== 1 && (!user.group_names || user.group_names.length === 0)
  )
})

const allFilteredUsers = computed(() => {
  // Filter out user with ID 1 (superuser/admin)
  let userList = users.value.filter(user => user.id !== 1)
  
  // Filter by active tab
  if (activeTab.value === 'patient') {
    userList = patientUsers.value
  } else if (activeTab.value === 'staff') {
    userList = staffUsers.value
  } else if (activeTab.value === 'no-group') {
    userList = noGroupUsers.value
  }
  
  if (!searchQuery.value) return userList
  
  const query = searchQuery.value.toLowerCase()
  return userList.filter(user => 
    user.username.toLowerCase().includes(query) ||
    user.email.toLowerCase().includes(query) ||
    user.first_name.toLowerCase().includes(query) ||
    user.last_name.toLowerCase().includes(query)
  )
})

const totalUsers = computed(() => allFilteredUsers.value.length)

const filteredUsers = computed(() => {
  const start = (currentPage.value - 1) * perPage.value
  const end = start + perPage.value
  return allFilteredUsers.value.slice(start, end)
})

const handlePageChange = (page) => {
  currentPage.value = page
}

watch(searchQuery, () => {
  currentPage.value = 1
})

watch(activeTab, () => {
  currentPage.value = 1
})

const fetchUsers = async () => {
  try {
    const response = await api.get('/users/')
    users.value = response.data
  } catch (error) {
    console.error('Error fetching users:', error)
    await Swal.fire({
      title: 'Error!',
      text: 'Failed to fetch users',
      icon: 'error'
    })
  }
}

const refreshTable = async () => {
  const button = event.target.closest('button')
  const icon = button.querySelector('i')
  icon.classList.add('fa-spin')
  
  await fetchUsers()
  
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

const fetchGroups = async () => {
  try {
    const response = await api.get('/groups/')
    availableGroups.value = response.data
  } catch (error) {
    console.error('Error fetching groups:', error)
  }
}

const fetchEmployees = async () => {
  try {
    const response = await api.get('/employees/')
    employees.value = response.data
  } catch (error) {
    console.error('Error fetching employees:', error)
  }
}

const onEmployeeSelected = () => {
  if (!selectedEmployeeId.value) {
    resetForm()
    return
  }
  
  const employee = employees.value.find(emp => emp.id === parseInt(selectedEmployeeId.value))
  if (employee) {
    formData.value = {
      username: employee.employee_id,
      first_name: employee.first_name,
      last_name: employee.last_name,
      email: employee.email || '',
      phone: employee.phone || '',
      password: employee.employee_id, // Default password to employee_id
      is_staff: false,
      groups: []
    }
  }
}

const openAddModal = () => {
  isEditMode.value = false
  selectedEmployeeId.value = ''
  resetForm()
  showModal()
}

const openEditModal = (user) => {
  isEditMode.value = true
  formData.value = { 
    ...user,
    password: '', // Don't populate password
    groups: user.groups || [] // Populate groups
  }
  showModal()
}

const saveUser = async () => {
  try {
    if (isEditMode.value) {
      // Remove password field if empty during edit
      const updateData = { ...formData.value }
      if (!updateData.password) {
        delete updateData.password
      }
      await api.put(`/users/${formData.value.id}/`, updateData)
    } else {
      await api.post('/users/', formData.value)
    }
    await fetchUsers()
    await fetchEmployees() // Refresh employees to update has_user status
    closeModal()
    await Swal.fire({
      title: 'Success!',
      text: `User ${isEditMode.value ? 'updated' : 'created'} successfully`,
      icon: 'success',
      timer: 2000
    })
  } catch (error) {
    console.error('Error saving user:', error)
    await Swal.fire({
      title: 'Error!',
      text: error.response?.data?.detail || error.response?.data?.username?.[0] || 'Failed to save user',
      icon: 'error'
    })
  }
}

const deleteUser = async (id) => {
  const result = await Swal.fire({
    title: 'Are you sure?',
    text: 'You will not be able to recover this user!',
    icon: 'warning',
    showCancelButton: true,
    confirmButtonColor: '#d33',
    cancelButtonColor: '#3085d6',
    confirmButtonText: 'Yes, delete it!',
    cancelButtonText: 'Cancel'
  })

  if (result.isConfirmed) {
    try {
      await api.delete(`/users/${id}/`)
      await fetchUsers()
      await Swal.fire({
        title: 'Deleted!',
        text: 'User has been deleted',
        icon: 'success',
        timer: 2000
      })
    } catch (error) {
      console.error('Error deleting user:', error)
      await Swal.fire({
        title: 'Error!',
        text: 'Failed to delete user',
        icon: 'error'
      })
    }
  }
}

const toggleActive = async (user) => {
  try {
    const newStatus = !user.is_active
    await api.patch(`/users/${user.id}/`, { is_active: newStatus })
    await fetchUsers()
  } catch (error) {
    console.error('Error toggling active status:', error)
    await Swal.fire({
      title: 'Error!',
      text: 'Failed to update user status',
      icon: 'error'
    })
  }
}

const resetPassword = async (user) => {
  const result = await Swal.fire({
    title: 'Reset Password',
    html: `
      <p>Reset password for user: <strong>${user.username}</strong></p>
      <input type="password" id="new-password" class="swal2-input" placeholder="New Password" minlength="8">
      <input type="password" id="confirm-password" class="swal2-input" placeholder="Confirm Password">
    `,
    icon: 'question',
    showCancelButton: true,
    confirmButtonColor: '#3085d6',
    cancelButtonColor: '#6c757d',
    confirmButtonText: 'Reset Password',
    cancelButtonText: 'Cancel',
    preConfirm: () => {
      const password = document.getElementById('new-password').value
      const confirm = document.getElementById('confirm-password').value
      
      if (!password || password.length < 8) {
        Swal.showValidationMessage('Password must be at least 8 characters')
        return false
      }
      
      if (password !== confirm) {
        Swal.showValidationMessage('Passwords do not match')
        return false
      }
      
      return password
    }
  })

  if (result.isConfirmed) {
    try {
      await api.patch(`/users/${user.id}/`, { password: result.value })
      await Swal.fire({
        title: 'Success!',
        text: 'Password has been reset',
        icon: 'success',
        timer: 2000
      })
    } catch (error) {
      console.error('Error resetting password:', error)
      await Swal.fire({
        title: 'Error!',
        text: 'Failed to reset password',
        icon: 'error'
      })
    }
  }
}

const resetForm = () => {
  formData.value = {
    username: '',
    first_name: '',
    last_name: '',
    email: '',
    phone: '',
    password: '',
    is_staff: false,
    groups: []
  }
}

const showModal = () => {
  const modal = document.getElementById('userModal')
  modal.classList.add('show')
  modal.style.display = 'block'
  document.body.classList.add('modal-open')
  
  const backdrop = document.createElement('div')
  backdrop.className = 'modal-backdrop fade show'
  backdrop.id = 'modal-backdrop'
  document.body.appendChild(backdrop)
}

const closeModal = () => {
  const modal = document.getElementById('userModal')
  modal.classList.remove('show')
  modal.style.display = 'none'
  document.body.classList.remove('modal-open')
  
  const backdrop = document.getElementById('modal-backdrop')
  if (backdrop) {
    backdrop.remove()
  }
  
  resetForm()
}

const viewUser = (user) => {
  viewData.value = { ...user }
  showViewModal()
}

const editFromView = () => {
  closeViewModal()
  formData.value = { 
    ...viewData.value,
    password: '',
    groups: viewData.value.groups || []
  }
  isEditMode.value = true
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
  fetchUsers()
  fetchGroups()
  fetchEmployees()
})
</script>
