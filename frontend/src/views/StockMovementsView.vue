<template>
  <div class="content-header">
    <div class="container-fluid">
      <div class="row mb-2">
        <div class="col-sm-6">
          <h1 class="m-0">Stock Movements</h1>
        </div>
        <div class="col-sm-6">
          <button class="btn btn-info float-right ml-2" @click="refreshTable" title="Refresh">
            <i class="fas fa-sync-alt"></i>
          </button>
          <button class="btn btn-primary float-right" @click="openAddModal">
            <i class="fas fa-plus"></i> Add Stock Movement
          </button>
        </div>
      </div>
    </div>
  </div>

  <section class="content">
    <div class="container-fluid">
      <div class="card">
        <div class="card-header">
          <h3 class="card-title">Stock Movement History</h3>
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
                <th>Date</th>
                <th>Item Code</th>
                <th>Item Name</th>
                <th>Type</th>
                <th>Quantity</th>
                <th>Reference #</th>
                <th>User</th>
                <th>Actions</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="movement in filteredMovements" :key="movement.id" @click="viewMovement(movement)" style="cursor: pointer;">
                <td class="align-middle">{{ formatDate(movement.created_at) }}</td>
                <td class="align-middle">{{ movement.item_code || 'N/A' }}</td>
                <td class="align-middle">{{ movement.item_name || 'N/A' }}</td>
                <td class="align-middle">
                  <span 
                    :class="{
                      'badge badge-success': movement.movement_type === 'in',
                      'badge badge-danger': movement.movement_type === 'out',
                      'badge badge-warning': movement.movement_type === 'adjustment'
                    }"
                  >
                    {{ movement.movement_type.toUpperCase() }}
                  </span>
                </td>
                <td class="align-middle">{{ movement.quantity }}</td>
                <td class="align-middle">{{ movement.reference_number || 'N/A' }}</td>
                <td class="align-middle">{{ movement.user_username || 'System' }}</td>
                <td class="align-middle" @click.stop>
                  <button class="btn btn-sm btn-info" @click="viewMovement(movement)">
                    <i class="fas fa-eye"></i>
                  </button>
                  <button class="btn btn-sm btn-danger ml-1" @click="deleteMovement(movement.id)">
                    <i class="fas fa-trash"></i>
                  </button>
                </td>
              </tr>
              <tr v-if="filteredMovements.length === 0">
                <td colspan="8" class="text-center">No stock movements found</td>
              </tr>
            </tbody>
          </table>
        </div>
        <div class="card-footer clearfix">
          <TablePagination
            :current-page="currentPage"
            :per-page="perPage"
            :total="totalMovements"
            @page-change="handlePageChange"
          />
        </div>
      </div>
    </div>
  </section>

  <!-- Add Movement Modal -->
  <div class="modal fade" id="movementModal" tabindex="-1">
    <div class="modal-dialog modal-lg">
      <div class="modal-content">
        <div class="modal-header">
          <h4 class="modal-title">Add Stock Movement</h4>
          <button type="button" class="close" @click="closeModal">
            <span>&times;</span>
          </button>
        </div>
        <form @submit.prevent="saveMovement">
          <div class="modal-body">
            <div class="row">
              <div class="col-md-6">
                <div class="form-group">
                  <label>Item <span class="text-danger">*</span></label>
                  <select 
                    v-model="formData.item" 
                    class="form-control" 
                    required
                  >
                    <option value="">Select Item</option>
                    <option v-for="item in items" :key="item.id" :value="item.id">
                      {{ item.item_code }} - {{ item.name }}
                    </option>
                  </select>
                </div>
              </div>
              <div class="col-md-6">
                <div class="form-group">
                  <label>Movement Type <span class="text-danger">*</span></label>
                  <select 
                    v-model="formData.movement_type" 
                    class="form-control" 
                    required
                  >
                    <option value="in">Stock In</option>
                    <option value="out">Stock Out</option>
                    <option value="adjustment">Adjustment</option>
                  </select>
                </div>
              </div>
            </div>

            <div class="row">
              <div class="col-md-6">
                <div class="form-group">
                  <label>Quantity <span class="text-danger">*</span></label>
                  <input 
                    type="number" 
                    v-model.number="formData.quantity" 
                    class="form-control" 
                    required
                    min="1"
                  >
                </div>
              </div>
              <div class="col-md-6">
                <div class="form-group">
                  <label>Reference Number</label>
                  <input 
                    type="text" 
                    v-model="formData.reference_number" 
                    class="form-control" 
                    maxlength="100"
                  >
                </div>
              </div>
            </div>

            <div class="form-group">
              <label>Notes</label>
              <textarea 
                v-model="formData.notes" 
                class="form-control" 
                rows="3"
              ></textarea>
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

  <!-- View Movement Modal -->
  <div class="modal fade" id="viewModal" tabindex="-1">
    <div class="modal-dialog">
      <div class="modal-content">
        <div class="modal-header">
          <h4 class="modal-title">Stock Movement Details</h4>
          <button type="button" class="close" @click="closeViewModal">
            <span>&times;</span>
          </button>
        </div>
        <div class="modal-body">
          <table class="table table-bordered">
            <tbody>
              <tr>
                <th width="40%">Date</th>
                <td>{{ formatDate(viewData.created_at) }}</td>
              </tr>
              <tr>
                <th>Item Code</th>
                <td>{{ viewData.item_code }}</td>
              </tr>
              <tr>
                <th>Item Name</th>
                <td>{{ viewData.item_name }}</td>
              </tr>
              <tr>
                <th>Movement Type</th>
                <td>
                  <span 
                    :class="{
                      'badge badge-success': viewData.movement_type === 'in',
                      'badge badge-danger': viewData.movement_type === 'out',
                      'badge badge-warning': viewData.movement_type === 'adjustment'
                    }"
                  >
                    {{ viewData.movement_type ? viewData.movement_type.toUpperCase() : '' }}
                  </span>
                </td>
              </tr>
              <tr>
                <th>Quantity</th>
                <td>{{ viewData.quantity }}</td>
              </tr>
              <tr>
                <th>Reference Number</th>
                <td>{{ viewData.reference_number || 'N/A' }}</td>
              </tr>
              <tr>
                <th>User</th>
                <td>{{ viewData.user_username || 'System' }}</td>
              </tr>
              <tr>
                <th>Notes</th>
                <td>{{ viewData.notes || 'N/A' }}</td>
              </tr>
            </tbody>
          </table>
        </div>
        <div class="modal-footer">
          <button type="button" class="btn btn-default" @click="closeViewModal">Close</button>
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

const movements = ref([])
const items = ref([])
const searchQuery = ref('')
const currentPage = ref(1)
const perPage = ref(10)

const formData = ref({
  item: '',
  movement_type: 'in',
  quantity: 1,
  reference_number: '',
  notes: ''
})

const viewData = ref({})

const allFilteredMovements = computed(() => {
  if (!searchQuery.value) return movements.value
  
  const query = searchQuery.value.toLowerCase()
  return movements.value.filter(movement => 
    (movement.item_code && movement.item_code.toLowerCase().includes(query)) ||
    (movement.item_name && movement.item_name.toLowerCase().includes(query)) ||
    (movement.reference_number && movement.reference_number.toLowerCase().includes(query)) ||
    movement.movement_type.toLowerCase().includes(query)
  )
})

const totalMovements = computed(() => allFilteredMovements.value.length)

const filteredMovements = computed(() => {
  const start = (currentPage.value - 1) * perPage.value
  const end = start + perPage.value
  return allFilteredMovements.value.slice(start, end)
})

const handlePageChange = (page) => {
  currentPage.value = page
}

watch(searchQuery, () => {
  currentPage.value = 1
})

const formatDate = (dateString) => {
  if (!dateString) return 'N/A'
  const date = new Date(dateString)
  return date.toLocaleString('en-US', { 
    year: 'numeric', 
    month: 'short', 
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  })
}

const fetchMovements = async () => {
  try {
    const response = await api.get('/stock-movements/')
    movements.value = response.data
  } catch (error) {
    console.error('Error fetching movements:', error)
    Swal.fire({
      icon: 'error',
      title: 'Error',
      text: 'Failed to fetch stock movements'
    })
  }
}

const fetchItems = async () => {
  try {
    const response = await api.get('/items/')
    items.value = response.data
  } catch (error) {
    console.error('Error fetching items:', error)
  }
}

const refreshTable = async () => {
  const button = event.target.closest('button')
  const icon = button.querySelector('i')
  icon.classList.add('fa-spin')
  
  await fetchMovements()
  
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
  resetForm()
  showModal()
}

const viewMovement = (movement) => {
  viewData.value = { ...movement }
  showViewModal()
}

const saveMovement = async () => {
  try {
    await api.post('/stock-movements/', formData.value)
    Swal.fire({
      icon: 'success',
      title: 'Success!',
      text: 'Stock movement created successfully',
      timer: 1500,
      showConfirmButton: false
    })
    
    await fetchMovements()
    closeModal()
  } catch (error) {
    console.error('Error saving movement:', error)
    Swal.fire({
      icon: 'error',
      title: 'Error',
      text: error.response?.data?.message || 'Failed to save stock movement'
    })
  }
}

const deleteMovement = async (id) => {
  const result = await Swal.fire({
    title: 'Are you sure?',
    text: "Deleting this will not reverse the stock change!",
    icon: 'warning',
    showCancelButton: true,
    confirmButtonColor: '#d33',
    cancelButtonColor: '#3085d6',
    confirmButtonText: 'Yes, delete it!'
  })
  
  if (result.isConfirmed) {
    try {
      await api.delete(`/stock-movements/${id}/`)
      Swal.fire('Deleted!', 'Stock movement has been deleted.', 'success')
      await fetchMovements()
    } catch (error) {
      console.error('Error deleting movement:', error)
      Swal.fire({
        icon: 'error',
        title: 'Error',
        text: 'Failed to delete stock movement'
      })
    }
  }
}

const resetForm = () => {
  formData.value = {
    item: '',
    movement_type: 'in',
    quantity: 1,
    reference_number: '',
    notes: ''
  }
}

const showModal = () => {
  const modal = document.getElementById('movementModal')
  modal.classList.add('show')
  modal.style.display = 'block'
  document.body.classList.add('modal-open')
  
  const backdrop = document.createElement('div')
  backdrop.className = 'modal-backdrop fade show'
  backdrop.id = 'modal-backdrop'
  document.body.appendChild(backdrop)
}

const closeModal = () => {
  const modal = document.getElementById('movementModal')
  modal.classList.remove('show')
  modal.style.display = 'none'
  document.body.classList.remove('modal-open')
  
  const backdrop = document.getElementById('modal-backdrop')
  if (backdrop) {
    backdrop.remove()
  }
  
  resetForm()
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
  fetchMovements()
  fetchItems()
})
</script>
