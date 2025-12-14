<template>
  <div class="content-header">
    <div class="container-fluid">
      <div class="row mb-2">
        <div class="col-sm-6">
          <h1 class="m-0">Department Management</h1>
        </div>
        <div class="col-sm-6">
          <button class="btn btn-info float-right ml-2" @click="refreshTable" title="Refresh">
            <i class="fas fa-sync-alt"></i>
          </button>
          <button class="btn btn-primary float-right" @click="openAddModal">
            <i class="fas fa-plus"></i> Add Department
          </button>
        </div>
      </div>
    </div>
  </div>

  <section class="content">
    <div class="container-fluid">
      <div class="card">
        <div class="card-header">
          <h3 class="card-title">Department List</h3>
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
                <th>Code</th>
                <th>Name</th>
                <th>Description</th>
                <th>Status</th>
                <th>Actions</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="department in filteredDepartments" :key="department.id" @click="viewDepartment(department)" style="cursor: pointer;">
                <td>{{ department.code }}</td>
                <td>{{ department.name }}</td>
                <td>{{ department.description || 'N/A' }}</td>
                <td>
                  <span :class="['badge', department.is_active ? 'badge-success' : 'badge-secondary']">
                    {{ department.is_active ? 'Active' : 'Inactive' }}
                  </span>
                </td>
                <td class="align-middle" @click.stop>
                  <button class="btn btn-sm btn-info" @click="openEditModal(department)">
                    <i class="fas fa-edit"></i>
                  </button>
                  <button class="btn btn-sm btn-danger ml-1" @click="deleteDepartment(department.id)">
                    <i class="fas fa-trash"></i>
                  </button>
                </td>
              </tr>
              <tr v-if="filteredDepartments.length === 0">
                <td colspan="5" class="text-center">No departments found</td>
              </tr>
            </tbody>
          </table>
        </div>
        <div class="card-footer clearfix">
          <TablePagination
            :current-page="currentPage"
            :per-page="perPage"
            :total="totalDepartments"
            @page-change="handlePageChange"
          />
        </div>
      </div>
    </div>
  </section>

  <!-- Add/Edit Modal -->
  <div class="modal fade" id="departmentModal" tabindex="-1">
    <div class="modal-dialog">
      <div class="modal-content">
        <div class="modal-header">
          <h4 class="modal-title">{{ isEditMode ? 'Edit' : 'Add' }} Department</h4>
          <button type="button" class="close" @click="closeModal">
            <span>&times;</span>
          </button>
        </div>
        <form @submit.prevent="saveDepartment">
          <div class="modal-body">
            <div class="form-group">
              <label>Department Code</label>
              <input type="text" v-model="formData.code" class="form-control" required>
            </div>

            <div class="form-group">
              <label>Department Name</label>
              <input type="text" v-model="formData.name" class="form-control" required>
            </div>

            <div class="form-group">
              <label>Description</label>
              <textarea v-model="formData.description" class="form-control" rows="3"></textarea>
            </div>

            <div class="form-group">
              <div class="custom-control custom-switch">
                <input type="checkbox" class="custom-control-input" id="isActive" v-model="formData.is_active">
                <label class="custom-control-label" for="isActive">Active</label>
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
    <div class="modal-dialog">
      <div class="modal-content">
        <div class="modal-header bg-info">
          <h4 class="modal-title">Department Details</h4>
          <button type="button" class="close" @click="closeViewModal" style="color: white;">
            <span>&times;</span>
          </button>
        </div>
        <div class="modal-body">
          <div class="row">
            <div class="col-md-6">
              <p><strong>Department Code:</strong> {{ viewData.code }}</p>
            </div>
            <div class="col-md-6">
              <p><strong>Department Name:</strong> {{ viewData.name }}</p>
            </div>
          </div>
          <div class="row">
            <div class="col-md-12">
              <p><strong>Description:</strong> {{ viewData.description || 'N/A' }}</p>
            </div>
          </div>
          <div class="row">
            <div class="col-md-6">
              <p><strong>Status:</strong> 
                <span :class="['badge', viewData.is_active ? 'badge-success' : 'badge-secondary']">
                  {{ viewData.is_active ? 'Active' : 'Inactive' }}
                </span>
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

const departments = ref([])
const searchQuery = ref('')
const isEditMode = ref(false)
const currentPage = ref(1)
const perPage = ref(10)
const viewData = ref({})

const formData = ref({
  code: '',
  name: '',
  description: '',
  is_active: true
})

const allFilteredDepartments = computed(() => {
  if (!searchQuery.value) return departments.value
  
  const query = searchQuery.value.toLowerCase()
  return departments.value.filter(dept => 
    dept.code.toLowerCase().includes(query) ||
    dept.name.toLowerCase().includes(query)
  )
})

const totalDepartments = computed(() => allFilteredDepartments.value.length)

const filteredDepartments = computed(() => {
  const start = (currentPage.value - 1) * perPage.value
  const end = start + perPage.value
  return allFilteredDepartments.value.slice(start, end)
})

const handlePageChange = (page) => {
  currentPage.value = page
}

watch(searchQuery, () => {
  currentPage.value = 1
})

const fetchDepartments = async () => {
  try {
    const response = await api.get('/departments/')
    departments.value = response.data
  } catch (error) {
    console.error('Error fetching departments:', error)
  }
}

const refreshTable = async () => {
  const button = event.target.closest('button')
  const icon = button.querySelector('i')
  icon.classList.add('fa-spin')
  
  await fetchDepartments()
  
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

const openAddModal = () => {
  isEditMode.value = false
  resetForm()
  showModal()
}

const openEditModal = (department) => {
  isEditMode.value = true
  formData.value = { ...department }
  showModal()
}

const saveDepartment = async () => {
  try {
    if (isEditMode.value) {
      await api.put(`/departments/${formData.value.id}/`, formData.value)
    } else {
      await api.post('/departments/', formData.value)
    }
    await fetchDepartments()
    closeModal()
  } catch (error) {
    console.error('Error saving department:', error)
    alert('Error saving department: ' + (error.response?.data?.detail || error.message))
  }
}

const deleteDepartment = async (id) => {
  if (confirm('Are you sure you want to delete this department?')) {
    try {
      await api.delete(`/departments/${id}/`)
      await fetchDepartments()
    } catch (error) {
      console.error('Error deleting department:', error)
      alert('Cannot delete this department. It may be assigned to employees.')
    }
  }
}

const resetForm = () => {
  formData.value = {
    code: '',
    name: '',
    description: '',
    is_active: true
  }
}

const showModal = () => {
  const modal = document.getElementById('departmentModal')
  modal.classList.add('show')
  modal.style.display = 'block'
  document.body.classList.add('modal-open')
  
  const backdrop = document.createElement('div')
  backdrop.className = 'modal-backdrop fade show'
  backdrop.id = 'modal-backdrop'
  document.body.appendChild(backdrop)
}

const closeModal = () => {
  const modal = document.getElementById('departmentModal')
  modal.classList.remove('show')
  modal.style.display = 'none'
  document.body.classList.remove('modal-open')
  
  const backdrop = document.getElementById('modal-backdrop')
  if (backdrop) {
    backdrop.remove()
  }
  
  resetForm()
}

const viewDepartment = (department) => {
  viewData.value = { ...department }
  showViewModal()
}

const editFromView = () => {
  closeViewModal()
  formData.value = { ...viewData.value }
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
  fetchDepartments()
})
</script>
