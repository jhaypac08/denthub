<template>
  <div class="content-header">
    <div class="container-fluid">
      <div class="row mb-2">
        <div class="col-sm-6">
          <h1 class="m-0">Items Management</h1>
        </div>
        <div class="col-sm-6">
          <button class="btn btn-info float-right ml-2" @click="refreshTable" title="Refresh">
            <i class="fas fa-sync-alt"></i>
          </button>
          <button class="btn btn-primary float-right" @click="openAddModal">
            <i class="fas fa-plus"></i> Add Item
          </button>
        </div>
      </div>
    </div>
  </div>

  <section class="content">
    <div class="container-fluid">
      <div class="card">
        <div class="card-header">
          <h3 class="card-title">Item List</h3>
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
                <th>Item Code</th>
                <th>Name</th>
                <th>Category</th>
                <th>Unit</th>
                <th>Current Stock</th>
                <th>Reorder Level</th>
                <th>Unit Price</th>
                <th>Actions</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="item in filteredItems" :key="item.id" @click="viewItem(item)" style="cursor: pointer;">
                <td class="align-middle">{{ item.item_code }}</td>
                <td class="align-middle">{{ item.name }}</td>
                <td class="align-middle">{{ item.category_name || 'N/A' }}</td>
                <td class="align-middle">{{ item.unit }}</td>
                <td class="align-middle">
                  <span 
                    :class="{'badge badge-warning': item.is_low_stock, 'badge badge-success': !item.is_low_stock}"
                  >
                    {{ item.current_stock }}
                  </span>
                </td>
                <td class="align-middle">{{ item.reorder_level }}</td>
                <td class="align-middle">₱{{ parseFloat(item.unit_price).toFixed(2) }}</td>
                <td class="align-middle" @click.stop>
                  <button class="btn btn-sm btn-info" @click="openEditModal(item)">
                    <i class="fas fa-edit"></i>
                  </button>
                  <button class="btn btn-sm btn-danger ml-1" @click="deleteItem(item.id)">
                    <i class="fas fa-trash"></i>
                  </button>
                </td>
              </tr>
              <tr v-if="filteredItems.length === 0">
                <td colspan="8" class="text-center">No items found</td>
              </tr>
            </tbody>
          </table>
        </div>
        <div class="card-footer clearfix">
          <TablePagination
            :current-page="currentPage"
            :per-page="perPage"
            :total="totalItems"
            @page-change="handlePageChange"
          />
        </div>
      </div>
    </div>
  </section>

  <!-- Add/Edit Modal -->
  <div class="modal fade" id="itemModal" tabindex="-1">
    <div class="modal-dialog modal-lg">
      <div class="modal-content">
        <div class="modal-header">
          <h4 class="modal-title">{{ isEditMode ? 'Edit' : 'Add' }} Item</h4>
          <button type="button" class="close" @click="closeModal">
            <span>&times;</span>
          </button>
        </div>
        <form @submit.prevent="saveItem">
          <div class="modal-body">
            <div class="row">
              <div class="col-md-6">
                <div class="form-group">
                  <label>Item Code <span class="text-danger">*</span></label>
                  <input 
                    type="text" 
                    v-model="formData.item_code" 
                    class="form-control" 
                    required
                    maxlength="50"
                  >
                </div>
              </div>
              <div class="col-md-6">
                <div class="form-group">
                  <label>Name <span class="text-danger">*</span></label>
                  <input 
                    type="text" 
                    v-model="formData.name" 
                    class="form-control" 
                    required
                    maxlength="200"
                  >
                </div>
              </div>
            </div>

            <div class="row">
              <div class="col-md-6">
                <div class="form-group">
                  <label>Category <span class="text-danger">*</span></label>
                  <select 
                    v-model="formData.category" 
                    class="form-control" 
                    required
                  >
                    <option value="">Select Category</option>
                    <option v-for="cat in categories" :key="cat.id" :value="cat.id">
                      {{ cat.name }}
                    </option>
                  </select>
                </div>
              </div>
              <div class="col-md-6">
                <div class="form-group">
                  <label>Unit <span class="text-danger">*</span></label>
                  <select 
                    v-model="formData.unit" 
                    class="form-control" 
                    required
                  >
                    <option value="pcs">Pieces</option>
                    <option value="box">Box</option>
                    <option value="pack">Pack</option>
                    <option value="bottle">Bottle</option>
                    <option value="set">Set</option>
                    <option value="kit">Kit</option>
                  </select>
                </div>
              </div>
            </div>

            <div class="row">
              <div class="col-md-6">
                <div class="form-group">
                  <label>Reorder Level <span class="text-danger">*</span></label>
                  <input 
                    type="number" 
                    v-model.number="formData.reorder_level" 
                    class="form-control" 
                    required
                    min="0"
                  >
                </div>
              </div>
              <div class="col-md-6">
                <div class="form-group">
                  <label>Unit Price <span class="text-danger">*</span></label>
                  <input 
                    type="number" 
                    v-model.number="formData.unit_price" 
                    class="form-control" 
                    required
                    min="0"
                    step="0.01"
                  >
                </div>
              </div>
            </div>

            <div class="form-group">
              <label>Supplier</label>
              <input 
                type="text" 
                v-model="formData.supplier" 
                class="form-control" 
                maxlength="200"
              >
            </div>

            <div class="form-group">
              <label>Description</label>
              <textarea 
                v-model="formData.description" 
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

  <!-- View Modal -->
  <div class="modal fade" id="viewModal" tabindex="-1">
    <div class="modal-dialog modal-lg">
      <div class="modal-content">
        <div class="modal-header bg-info">
          <h4 class="modal-title">Item Details</h4>
          <button type="button" class="close" @click="closeViewModal" style="color: white;">
            <span>&times;</span>
          </button>
        </div>
        <div class="modal-body">
          <div class="row">
            <div class="col-md-6">
              <p><strong>Item Code:</strong> {{ viewData.item_code }}</p>
            </div>
            <div class="col-md-6">
              <p><strong>Name:</strong> {{ viewData.name }}</p>
            </div>
          </div>
          <div class="row">
            <div class="col-md-6">
              <p><strong>Category:</strong> {{ viewData.category_name || 'N/A' }}</p>
            </div>
            <div class="col-md-6">
              <p><strong>Unit:</strong> {{ viewData.unit }}</p>
            </div>
          </div>
          <div class="row">
            <div class="col-md-6">
              <p><strong>Current Stock:</strong> 
                <span :class="{'badge badge-warning': viewData.is_low_stock, 'badge badge-success': !viewData.is_low_stock}">
                  {{ viewData.current_stock }}
                </span>
              </p>
            </div>
            <div class="col-md-6">
              <p><strong>Reorder Level:</strong> {{ viewData.reorder_level }}</p>
            </div>
          </div>
          <div class="row">
            <div class="col-md-6">
              <p><strong>Unit Price:</strong> ₱{{ viewData.unit_price ? parseFloat(viewData.unit_price).toFixed(2) : '0.00' }}</p>
            </div>
            <div class="col-md-6">
              <p><strong>Supplier:</strong> {{ viewData.supplier || 'N/A' }}</p>
            </div>
          </div>
          <div class="row">
            <div class="col-md-12">
              <p><strong>Description:</strong> {{ viewData.description || 'N/A' }}</p>
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

const items = ref([])
const categories = ref([])
const searchQuery = ref('')
const isEditMode = ref(false)
const currentPage = ref(1)
const perPage = ref(10)
const viewData = ref({})

const formData = ref({
  item_code: '',
  name: '',
  category: '',
  unit: 'pcs',
  reorder_level: 0,
  unit_price: 0,
  supplier: '',
  description: ''
})

const allFilteredItems = computed(() => {
  if (!searchQuery.value) return items.value
  
  const query = searchQuery.value.toLowerCase()
  return items.value.filter(item => 
    item.item_code.toLowerCase().includes(query) ||
    item.name.toLowerCase().includes(query) ||
    (item.category_name && item.category_name.toLowerCase().includes(query)) ||
    (item.supplier && item.supplier.toLowerCase().includes(query))
  )
})

const totalItems = computed(() => allFilteredItems.value.length)

const filteredItems = computed(() => {
  const start = (currentPage.value - 1) * perPage.value
  const end = start + perPage.value
  return allFilteredItems.value.slice(start, end)
})

const handlePageChange = (page) => {
  currentPage.value = page
}

watch(searchQuery, () => {
  currentPage.value = 1
})

const fetchItems = async () => {
  try {
    const response = await api.get('/items/')
    items.value = response.data
  } catch (error) {
    console.error('Error fetching items:', error)
    Swal.fire({
      icon: 'error',
      title: 'Error',
      text: 'Failed to fetch items'
    })
  }
}

const fetchCategories = async () => {
  try {
    const response = await api.get('/categories/')
    categories.value = response.data.filter(cat => cat.is_active)
  } catch (error) {
    console.error('Error fetching categories:', error)
  }
}

const refreshTable = async () => {
  const button = event.target.closest('button')
  const icon = button.querySelector('i')
  icon.classList.add('fa-spin')
  
  await fetchItems()
  
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

const openEditModal = (item) => {
  isEditMode.value = true
  formData.value = { ...item }
  showModal()
}

const saveItem = async () => {
  try {
    if (isEditMode.value) {
      await api.put(`/items/${formData.value.id}/`, formData.value)
      Swal.fire({
        icon: 'success',
        title: 'Success!',
        text: 'Item updated successfully',
        timer: 1500,
        showConfirmButton: false
      })
    } else {
      await api.post('/items/', formData.value)
      Swal.fire({
        icon: 'success',
        title: 'Success!',
        text: 'Item created successfully',
        timer: 1500,
        showConfirmButton: false
      })
    }
    
    await fetchItems()
    closeModal()
  } catch (error) {
    console.error('Error saving item:', error)
    Swal.fire({
      icon: 'error',
      title: 'Error',
      text: error.response?.data?.message || 'Failed to save item'
    })
  }
}

const deleteItem = async (id) => {
  const result = await Swal.fire({
    title: 'Are you sure?',
    text: "You won't be able to revert this!",
    icon: 'warning',
    showCancelButton: true,
    confirmButtonColor: '#d33',
    cancelButtonColor: '#3085d6',
    confirmButtonText: 'Yes, delete it!'
  })
  
  if (result.isConfirmed) {
    try {
      await api.delete(`/items/${id}/`)
      Swal.fire('Deleted!', 'Item has been deleted.', 'success')
      await fetchItems()
    } catch (error) {
      console.error('Error deleting item:', error)
      Swal.fire({
        icon: 'error',
        title: 'Error',
        text: 'Failed to delete item'
      })
    }
  }
}

const resetForm = () => {
  formData.value = {
    item_code: '',
    name: '',
    category: '',
    unit: 'pcs',
    reorder_level: 0,
    unit_price: 0,
    supplier: '',
    description: ''
  }
}

const showModal = () => {
  const modal = document.getElementById('itemModal')
  modal.classList.add('show')
  modal.style.display = 'block'
  document.body.classList.add('modal-open')
  
  const backdrop = document.createElement('div')
  backdrop.className = 'modal-backdrop fade show'
  backdrop.id = 'modal-backdrop'
  document.body.appendChild(backdrop)
}

const closeModal = () => {
  const modal = document.getElementById('itemModal')
  modal.classList.remove('show')
  modal.style.display = 'none'
  document.body.classList.remove('modal-open')
  
  const backdrop = document.getElementById('modal-backdrop')
  if (backdrop) {
    backdrop.remove()
  }
  
  resetForm()
}

const viewItem = (item) => {
  viewData.value = { ...item }
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
  fetchItems()
  fetchCategories()
})
</script>
