<template>
  <div class="content-header">
    <div class="container-fluid">
      <div class="row mb-2">
        <div class="col-sm-6">
          <h1 class="m-0">Position Management</h1>
        </div>
        <div class="col-sm-6">
          <button class="btn btn-info float-right ml-2" @click="refreshTable" title="Refresh">
            <i class="fas fa-sync-alt"></i>
          </button>
          <button class="btn btn-primary float-right" @click="openAddModal">
            <i class="fas fa-plus"></i> Add Position
          </button>
        </div>
      </div>
    </div>
  </div>

  <section class="content">
    <div class="container-fluid">
      <div class="card">
        <div class="card-header">
          <h3 class="card-title">Position List</h3>
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
                <th>Title</th>
                <th>Min Salary</th>
                <th>Max Salary</th>
                <th>Status</th>
                <th>Actions</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="position in filteredPositions" :key="position.id" @click="viewPosition(position)" style="cursor: pointer;">
                <td>{{ position.code }}</td>
                <td>{{ position.title }}</td>
                <td>{{ position.min_salary ? `$${parseFloat(position.min_salary).toLocaleString()}` : 'N/A' }}</td>
                <td>{{ position.max_salary ? `$${parseFloat(position.max_salary).toLocaleString()}` : 'N/A' }}</td>
                <td>
                  <span :class="['badge', position.is_active ? 'badge-success' : 'badge-secondary']">
                    {{ position.is_active ? 'Active' : 'Inactive' }}
                  </span>
                </td>
                <td class="align-middle" @click.stop>
                  <button class="btn btn-sm btn-info" @click="openEditModal(position)">
                    <i class="fas fa-edit"></i>
                  </button>
                  <button class="btn btn-sm btn-danger ml-1" @click="deletePosition(position.id)">
                    <i class="fas fa-trash"></i>
                  </button>
                </td>
              </tr>
              <tr v-if="filteredPositions.length === 0">
                <td colspan="6" class="text-center">No positions found</td>
              </tr>
            </tbody>
          </table>
        </div>
        <div class="card-footer clearfix">
          <TablePagination
            :current-page="currentPage"
            :per-page="perPage"
            :total="totalPositions"
            @page-change="handlePageChange"
          />
        </div>
      </div>
    </div>
  </section>

  <!-- Add/Edit Modal -->
  <div class="modal fade" id="positionModal" tabindex="-1">
    <div class="modal-dialog">
      <div class="modal-content">
        <div class="modal-header">
          <h4 class="modal-title">{{ isEditMode ? 'Edit' : 'Add' }} Position</h4>
          <button type="button" class="close" @click="closeModal">
            <span>&times;</span>
          </button>
        </div>
        <form @submit.prevent="savePosition">
          <div class="modal-body">
            <div class="form-group">
              <label>Position Code</label>
              <input type="text" v-model="formData.code" class="form-control" required>
            </div>

            <div class="form-group">
              <label>Position Title</label>
              <input type="text" v-model="formData.title" class="form-control" required>
            </div>

            <div class="form-group">
              <label>Description</label>
              <textarea v-model="formData.description" class="form-control" rows="3"></textarea>
            </div>

            <div class="row">
              <div class="col-md-6">
                <div class="form-group">
                  <label>Minimum Salary</label>
                  <input type="number" step="0.01" v-model="formData.min_salary" class="form-control">
                </div>
              </div>
              <div class="col-md-6">
                <div class="form-group">
                  <label>Maximum Salary</label>
                  <input type="number" step="0.01" v-model="formData.max_salary" class="form-control">
                </div>
              </div>
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
          <h4 class="modal-title">Position Details</h4>
          <button type="button" class="close" @click="closeViewModal" style="color: white;">
            <span>&times;</span>
          </button>
        </div>
        <div class="modal-body">
          <div class="row">
            <div class="col-md-6">
              <p><strong>Position Code:</strong> {{ viewData.code }}</p>
            </div>
            <div class="col-md-6">
              <p><strong>Position Title:</strong> {{ viewData.title }}</p>
            </div>
          </div>
          <div class="row">
            <div class="col-md-12">
              <p><strong>Description:</strong> {{ viewData.description || 'N/A' }}</p>
            </div>
          </div>
          <div class="row">
            <div class="col-md-6">
              <p><strong>Minimum Salary:</strong> {{ viewData.min_salary ? `$${parseFloat(viewData.min_salary).toLocaleString()}` : 'N/A' }}</p>
            </div>
            <div class="col-md-6">
              <p><strong>Maximum Salary:</strong> {{ viewData.max_salary ? `$${parseFloat(viewData.max_salary).toLocaleString()}` : 'N/A' }}</p>
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

const positions = ref([])
const searchQuery = ref('')
const isEditMode = ref(false)
const currentPage = ref(1)
const perPage = ref(10)
const viewData = ref({})

const formData = ref({
  code: '',
  title: '',
  description: '',
  min_salary: null,
  max_salary: null,
  is_active: true
})

const allFilteredPositions = computed(() => {
  if (!searchQuery.value) return positions.value
  
  const query = searchQuery.value.toLowerCase()
  return positions.value.filter(pos => 
    pos.code.toLowerCase().includes(query) ||
    pos.title.toLowerCase().includes(query)
  )
})

const totalPositions = computed(() => allFilteredPositions.value.length)

const filteredPositions = computed(() => {
  const start = (currentPage.value - 1) * perPage.value
  const end = start + perPage.value
  return allFilteredPositions.value.slice(start, end)
})

const handlePageChange = (page) => {
  currentPage.value = page
}

watch(searchQuery, () => {
  currentPage.value = 1
})

const fetchPositions = async () => {
  try {
    const response = await api.get('/positions/')
    positions.value = response.data
  } catch (error) {
    console.error('Error fetching positions:', error)
  }
}

const refreshTable = async () => {
  const button = event.target.closest('button')
  const icon = button.querySelector('i')
  icon.classList.add('fa-spin')
  
  await fetchPositions()
  
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

const openEditModal = (position) => {
  isEditMode.value = true
  formData.value = { ...position }
  showModal()
}

const savePosition = async () => {
  try {
    if (isEditMode.value) {
      await api.put(`/positions/${formData.value.id}/`, formData.value)
    } else {
      await api.post('/positions/', formData.value)
    }
    await fetchPositions()
    closeModal()
  } catch (error) {
    console.error('Error saving position:', error)
    alert('Error saving position: ' + (error.response?.data?.detail || error.message))
  }
}

const deletePosition = async (id) => {
  if (confirm('Are you sure you want to delete this position?')) {
    try {
      await api.delete(`/positions/${id}/`)
      await fetchPositions()
    } catch (error) {
      console.error('Error deleting position:', error)
      alert('Cannot delete this position. It may be assigned to employees.')
    }
  }
}

const resetForm = () => {
  formData.value = {
    code: '',
    title: '',
    description: '',
    min_salary: null,
    max_salary: null,
    is_active: true
  }
}

const showModal = () => {
  const modal = document.getElementById('positionModal')
  modal.classList.add('show')
  modal.style.display = 'block'
  document.body.classList.add('modal-open')
  
  const backdrop = document.createElement('div')
  backdrop.className = 'modal-backdrop fade show'
  backdrop.id = 'modal-backdrop'
  document.body.appendChild(backdrop)
}

const closeModal = () => {
  const modal = document.getElementById('positionModal')
  modal.classList.remove('show')
  modal.style.display = 'none'
  document.body.classList.remove('modal-open')
  
  const backdrop = document.getElementById('modal-backdrop')
  if (backdrop) {
    backdrop.remove()
  }
  
  resetForm()
}

const viewPosition = (position) => {
  viewData.value = { ...position }
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
  fetchPositions()
})
</script>
