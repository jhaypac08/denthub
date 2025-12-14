<template>
  <div class="content-header">
    <div class="container-fluid">
      <div class="row mb-2">
        <div class="col-sm-6">
          <h1 class="m-0">Branch Management</h1>
        </div>
        <div class="col-sm-6">
          <button class="btn btn-info float-right ml-2" @click="refreshTable" title="Refresh">
            <i class="fas fa-sync-alt"></i>
          </button>
          <button class="btn btn-primary float-right" @click="openAddModal">
            <i class="fas fa-plus"></i> Add Branch
          </button>
        </div>
      </div>
    </div>
  </div>

  <section class="content">
    <div class="container-fluid">
      <div class="card">
        <div class="card-header">
          <h3 class="card-title">Branch List</h3>
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
                <th>Phone</th>
                <th>Manager</th>
                <th>Status</th>
                <th>Actions</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="branch in filteredBranches" :key="branch.id" @click="viewBranch(branch)" style="cursor: pointer;">
                <td class="align-middle">{{ branch.code }}</td>
                <td class="align-middle">{{ branch.name }}</td>
                <td class="align-middle">{{ branch.phone }}</td>
                <td class="align-middle">{{ branch.manager || 'N/A' }}</td>
                <td class="align-middle">
                  <span :class="['badge', branch.is_active ? 'badge-success' : 'badge-secondary']">
                    {{ branch.is_active ? 'Active' : 'Inactive' }}
                  </span>
                </td>
                <td class="align-middle" @click.stop>
                  <button class="btn btn-sm btn-info" @click="openEditModal(branch)">
                    <i class="fas fa-edit"></i>
                  </button>
                  <button class="btn btn-sm btn-danger ml-1" @click="deleteBranch(branch.id)">
                    <i class="fas fa-trash"></i>
                  </button>
                </td>
              </tr>
              <tr v-if="filteredBranches.length === 0">
                <td colspan="6" class="text-center">No branches found</td>
              </tr>
            </tbody>
          </table>
        </div>
        <div class="card-footer clearfix">
          <TablePagination
            :current-page="currentPage"
            :per-page="perPage"
            :total="totalBranches"
            @page-change="handlePageChange"
          />
        </div>
      </div>
    </div>
  </section>

  <!-- Add/Edit Modal -->
  <div class="modal fade" id="branchModal" tabindex="-1">
    <div class="modal-dialog modal-lg">
      <div class="modal-content">
        <div class="modal-header">
          <h4 class="modal-title">{{ isEditMode ? 'Edit' : 'Add' }} Branch</h4>
          <button type="button" class="close" @click="closeModal">
            <span>&times;</span>
          </button>
        </div>
        <form @submit.prevent="saveBranch">
          <div class="modal-body">
            <div class="row">
              <div class="col-md-6">
                <div class="form-group">
                  <label>Branch Code</label>
                  <input type="text" v-model="formData.code" class="form-control" required>
                </div>
              </div>
              <div class="col-md-6">
                <div class="form-group">
                  <label>Branch Name</label>
                  <input type="text" v-model="formData.name" class="form-control" required>
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
                  <label>Phone</label>
                  <input type="text" v-model="formData.phone" class="form-control" required>
                </div>
              </div>
              <div class="col-md-6">
                <div class="form-group">
                  <label>Email</label>
                  <input type="email" v-model="formData.email" class="form-control" required>
                </div>
              </div>
            </div>

            <div class="form-group">
              <label>Branch Manager</label>
              <input type="text" v-model="formData.manager" class="form-control">
            </div>

            <div class="form-group">
              <div class="custom-control custom-switch">
                <input type="checkbox" class="custom-control-input" id="isActive" v-model="formData.is_active">
                <label class="custom-control-label" for="isActive">Active</label>
              </div>
            </div>

            <!-- Operating Hours Section -->
            <h6 class="text-muted mt-3">Operating Hours</h6>
            <div class="table-responsive">
              <table class="table table-bordered table-sm">
                <thead>
                  <tr>
                    <th width="20%">Day</th>
                    <th width="25%">Opening Time</th>
                    <th width="25%">Closing Time</th>
                    <th width="15%">Closed</th>
                    <th width="15%">Action</th>
                  </tr>
                </thead>
                <tbody>
                  <tr v-for="day in days" :key="day">
                    <td class="align-middle"><strong>{{ capitalizeDay(day) }}</strong></td>
                    <td>
                      <input 
                        type="time" 
                        v-model="formData[`${day}_open`]" 
                        class="form-control form-control-sm"
                        :disabled="formData[`${day}_closed`]"
                      >
                    </td>
                    <td>
                      <input 
                        type="time" 
                        v-model="formData[`${day}_close`]" 
                        class="form-control form-control-sm"
                        :disabled="formData[`${day}_closed`]"
                      >
                    </td>
                    <td class="text-center align-middle">
                      <div class="custom-control custom-checkbox">
                        <input 
                          type="checkbox" 
                          :id="`${day}_closed`" 
                          v-model="formData[`${day}_closed`]"
                          class="custom-control-input"
                        >
                        <label :for="`${day}_closed`" class="custom-control-label"></label>
                      </div>
                    </td>
                    <td class="text-center align-middle">
                      <button 
                        type="button" 
                        class="btn btn-xs btn-info" 
                        @click="copyToAll(day)"
                        title="Copy to all days"
                      >
                        <i class="fas fa-copy"></i>
                      </button>
                    </td>
                  </tr>
                </tbody>
              </table>
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
    <div class="modal-dialog modal-lg">
      <div class="modal-content">
        <div class="modal-header bg-info">
          <h4 class="modal-title">Branch Details</h4>
          <button type="button" class="close" @click="closeViewModal" style="color: white;">
            <span>&times;</span>
          </button>
        </div>
        <div class="modal-body">
          <div class="row">
            <div class="col-md-6">
              <p><strong>Branch Code:</strong> {{ viewData.code }}</p>
            </div>
            <div class="col-md-6">
              <p><strong>Branch Name:</strong> {{ viewData.name }}</p>
            </div>
          </div>
          <div class="row">
            <div class="col-md-12">
              <p><strong>Address:</strong> {{ viewData.address }}</p>
            </div>
          </div>
          <div class="row">
            <div class="col-md-6">
              <p><strong>Phone:</strong> {{ viewData.phone }}</p>
            </div>
            <div class="col-md-6">
              <p><strong>Email:</strong> {{ viewData.email }}</p>
            </div>
          </div>
          <div class="row">
            <div class="col-md-6">
              <p><strong>Manager:</strong> {{ viewData.manager || 'N/A' }}</p>
            </div>
            <div class="col-md-6">
              <p><strong>Status:</strong> 
                <span :class="['badge', viewData.is_active ? 'badge-success' : 'badge-secondary']">
                  {{ viewData.is_active ? 'Active' : 'Inactive' }}
                </span>
              </p>
            </div>
          </div>
          <hr>
          <h6>Operating Hours</h6>
          <div v-if="groupedSchedule.length > 0">
            <div v-for="(schedule, index) in groupedSchedule" :key="index" class="mb-2">
              <p class="mb-1">
                <strong>{{ schedule.days }}:&nbsp;</strong> 
                <span v-if="!schedule.closed" class="text-primary">
                  {{ formatTime12Hour(schedule.open) }} - {{ formatTime12Hour(schedule.close) }}
                </span>
                <span v-else class="badge badge-secondary">Closed</span>
              </p>
            </div>
          </div>
          <div v-else>
            <p class="text-muted">No operating hours set</p>
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

const branches = ref([])
const searchQuery = ref('')
const isEditMode = ref(false)
const currentPage = ref(1)
const viewData = ref({})
const perPage = ref(10)

const days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']

const formData = ref({
  code: '',
  name: '',
  address: '',
  phone: '',
  email: '',
  manager: '',
  is_active: true,
  // Operating hours for each day
  monday_open: '',
  monday_close: '',
  monday_closed: false,
  tuesday_open: '',
  tuesday_close: '',
  tuesday_closed: false,
  wednesday_open: '',
  wednesday_close: '',
  wednesday_closed: false,
  thursday_open: '',
  thursday_close: '',
  thursday_closed: false,
  friday_open: '',
  friday_close: '',
  friday_closed: false,
  saturday_open: '',
  saturday_close: '',
  saturday_closed: false,
  sunday_open: '',
  sunday_close: '',
  sunday_closed: false
})

const allFilteredBranches = computed(() => {
  if (!searchQuery.value) return branches.value
  
  const query = searchQuery.value.toLowerCase()
  return branches.value.filter(branch => 
    branch.code.toLowerCase().includes(query) ||
    branch.name.toLowerCase().includes(query) ||
    (branch.manager && branch.manager.toLowerCase().includes(query))
  )
})

const totalBranches = computed(() => allFilteredBranches.value.length)

const filteredBranches = computed(() => {
  const start = (currentPage.value - 1) * perPage.value
  const end = start + perPage.value
  return allFilteredBranches.value.slice(start, end)
})

const handlePageChange = (page) => {
  currentPage.value = page
}

const groupedSchedule = computed(() => {
  if (!viewData.value || Object.keys(viewData.value).length === 0) return []
  
  // Create a map of schedules
  const scheduleMap = new Map()
  
  days.forEach((day) => {
    const open = viewData.value[`${day}_open`]
    const close = viewData.value[`${day}_close`]
    const closed = viewData.value[`${day}_closed`] || false
    
    const key = `${open}|${close}|${closed}`
    
    if (!scheduleMap.has(key)) {
      scheduleMap.set(key, {
        open: open || '',
        close: close || '',
        closed: closed,
        days: []
      })
    }
    
    scheduleMap.get(key).days.push(day)
  })
  
  // Convert map to array and format day ranges
  const scheduleGroups = Array.from(scheduleMap.values()).map(schedule => {
    const daysList = schedule.days
    const formattedDays = []
    let rangeStart = null
    
    for (let i = 0; i < daysList.length; i++) {
      const currentDayIndex = days.indexOf(daysList[i])
      const nextDayIndex = i < daysList.length - 1 ? days.indexOf(daysList[i + 1]) : -1
      
      if (rangeStart === null) {
        rangeStart = currentDayIndex
      }
      
      // Check if next day is consecutive
      if (nextDayIndex !== currentDayIndex + 1) {
        // End of range
        if (rangeStart === currentDayIndex) {
          // Single day
          formattedDays.push(capitalizeDay(days[currentDayIndex]))
        } else {
          // Range of days
          formattedDays.push(`${capitalizeDay(days[rangeStart])} - ${capitalizeDay(days[currentDayIndex])}`)
        }
        rangeStart = null
      }
    }
    
    return {
      days: formattedDays.join(', '),
      open: schedule.open,
      close: schedule.close,
      closed: schedule.closed
    }
  })
  
  return scheduleGroups
})

const formatTime12Hour = (time) => {
  if (!time) return 'N/A'
  
  const [hours, minutes] = time.split(':')
  let hour = parseInt(hours)
  const ampm = hour >= 12 ? 'PM' : 'AM'
  
  hour = hour % 12 || 12
  
  return `${hour}:${minutes} ${ampm}`
}

watch(searchQuery, () => {
  currentPage.value = 1
})

const fetchBranches = async () => {
  try {
    const response = await api.get('/branches/')
    branches.value = response.data
  } catch (error) {
    console.error('Error fetching branches:', error)
  }
}

const refreshTable = async () => {
  const button = event.target.closest('button')
  const icon = button.querySelector('i')
  icon.classList.add('fa-spin')
  
  await fetchBranches()
  
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

const openEditModal = (branch) => {
  isEditMode.value = true
  formData.value = { ...branch }
  showModal()
}

const saveBranch = async () => {
  try {
    if (isEditMode.value) {
      await api.put(`/branches/${formData.value.id}/`, formData.value)
    } else {
      await api.post('/branches/', formData.value)
    }
    await fetchBranches()
    closeModal()
  } catch (error) {
    console.error('Error saving branch:', error)
    alert('Error saving branch: ' + (error.response?.data?.detail || error.message))
  }
}

const deleteBranch = async (id) => {
  if (confirm('Are you sure you want to delete this branch?')) {
    try {
      await api.delete(`/branches/${id}/`)
      await fetchBranches()
    } catch (error) {
      console.error('Error deleting branch:', error)
      alert('Cannot delete this branch. It may be assigned to employees.')
    }
  }
}

const resetForm = () => {
  formData.value = {
    code: '',
    name: '',
    address: '',
    phone: '',
    email: '',
    manager: '',
    is_active: true,
    monday_open: '',
    monday_close: '',
    monday_closed: false,
    tuesday_open: '',
    tuesday_close: '',
    tuesday_closed: false,
    wednesday_open: '',
    wednesday_close: '',
    wednesday_closed: false,
    thursday_open: '',
    thursday_close: '',
    thursday_closed: false,
    friday_open: '',
    friday_close: '',
    friday_closed: false,
    saturday_open: '',
    saturday_close: '',
    saturday_closed: false,
    sunday_open: '',
    sunday_close: '',
    sunday_closed: false
  }
}

const capitalizeDay = (day) => {
  return day.charAt(0).toUpperCase() + day.slice(1)
}

const copyToAll = (sourceDay) => {
  const openTime = formData.value[`${sourceDay}_open`]
  const closeTime = formData.value[`${sourceDay}_close`]
  const isClosed = formData.value[`${sourceDay}_closed`]
  
  days.forEach(day => {
    formData.value[`${day}_open`] = openTime
    formData.value[`${day}_close`] = closeTime
    formData.value[`${day}_closed`] = isClosed
  })
  
  Swal.fire({
    toast: true,
    position: 'top-end',
    icon: 'success',
    title: `${capitalizeDay(sourceDay)} hours copied to all days`,
    showConfirmButton: false,
    timer: 2000
  })
}

const showModal = () => {
  const modal = document.getElementById('branchModal')
  modal.classList.add('show')
  modal.style.display = 'block'
  document.body.classList.add('modal-open')
  
  const backdrop = document.createElement('div')
  backdrop.className = 'modal-backdrop fade show'
  backdrop.id = 'modal-backdrop'
  document.body.appendChild(backdrop)
}

const closeModal = () => {
  const modal = document.getElementById('branchModal')
  modal.classList.remove('show')
  modal.style.display = 'none'
  document.body.classList.remove('modal-open')
  
  const backdrop = document.getElementById('modal-backdrop')
  if (backdrop) {
    backdrop.remove()
  }
  
  resetForm()
}

const viewBranch = (branch) => {
  viewData.value = { ...branch }
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
  fetchBranches()
})
</script>
