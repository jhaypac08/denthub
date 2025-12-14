<template>
  <div class="content-header">
    <div class="container-fluid">
      <div class="row mb-2">
        <div class="col-sm-6">
          <h1 class="m-0">Categories Management</h1>
        </div>
        <div class="col-sm-6">
          <button class="btn btn-info float-right ml-2" @click="refreshTable" title="Refresh">
            <i class="fas fa-sync-alt"></i>
          </button>
          <button class="btn btn-primary float-right" @click="openAddModal">
            <i class="fas fa-plus"></i> Add Category
          </button>
        </div>
      </div>
    </div>
  </div>

  <section class="content">
    <div class="container-fluid">
      <div class="card">
        <div class="card-header">
          <h3 class="card-title">Category List</h3>
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
              <tr v-for="category in filteredCategories" :key="category.id" @click="viewCategory(category)" style="cursor: pointer;">
                <td class="align-middle">{{ category.code }}</td>
                <td class="align-middle">{{ category.name }}</td>
                <td class="align-middle">{{ category.description || 'N/A' }}</td>
                <td class="align-middle" @click.stop>
                  <div class="custom-control custom-switch">
                    <input 
                      type="checkbox" 
                      class="custom-control-input" 
                      :id="'status-' + category.id"
                      :checked="category.is_active"
                      @change="toggleStatus(category)"
                    >
                    <label class="custom-control-label" :for="'status-' + category.id">
                      {{ category.is_active ? 'Active' : 'Inactive' }}
                    </label>
                  </div>
                </td>
                <td class="align-middle" @click.stop>
                  <button class="btn btn-sm btn-info" @click="openEditModal(category)">
                    <i class="fas fa-edit"></i>
                  </button>
                  <button class="btn btn-sm btn-danger ml-1" @click="deleteCategory(category.id)">
                    <i class="fas fa-trash"></i>
                  </button>
                </td>
              </tr>
              <tr v-if="filteredCategories.length === 0">
                <td colspan="5" class="text-center">No categories found</td>
              </tr>
            </tbody>
          </table>
        </div>
        <div class="card-footer clearfix">
          <TablePagination
            :current-page="currentPage"
            :per-page="perPage"
            :total="totalCategories"
            @page-change="handlePageChange"
          />
        </div>
      </div>
    </div>
  </section>

  <!-- Add/Edit Modal -->
  <div class="modal fade" id="categoryModal" tabindex="-1">
    <div class="modal-dialog">
      <div class="modal-content">
        <div class="modal-header">
          <h4 class="modal-title">{{ isEditMode ? 'Edit' : 'Add' }} Category</h4>
          <button type="button" class="close" @click="closeModal">
            <span>&times;</span>
          </button>
        </div>
        <form @submit.prevent="saveCategory">
          <div class="modal-body">
            <div class="form-group">
              <label>Code <span class="text-danger">*</span></label>
              <input 
                type="text" 
                v-model="formData.code" 
                class="form-control" 
                required
                maxlength="20"
              >
            </div>

            <div class="form-group">
              <label>Name <span class="text-danger">*</span></label>
              <input 
                type="text" 
                v-model="formData.name" 
                class="form-control" 
                required
                maxlength="100"
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

            <div class="form-group">
              <div class="custom-control custom-switch">
                <input 
                  type="checkbox" 
                  class="custom-control-input" 
                  id="is_active"
                  v-model="formData.is_active"
                >
                <label class="custom-control-label" for="is_active">Active</label>
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
          <h4 class="modal-title">Category Details</h4>
          <button type="button" class="close" @click="closeViewModal" style="color: white;">
            <span>&times;</span>
          </button>
        </div>
        <div class="modal-body">
          <div class="row">
            <div class="col-md-6">
              <p><strong>Category Code:</strong> {{ viewData.code }}</p>
            </div>
            <div class="col-md-6">
              <p><strong>Category Name:</strong> {{ viewData.name }}</p>
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

const categories = ref([])
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

const allFilteredCategories = computed(() => {
  if (!searchQuery.value) return categories.value
  
  const query = searchQuery.value.toLowerCase()
  return categories.value.filter(cat => 
    cat.code.toLowerCase().includes(query) ||
    cat.name.toLowerCase().includes(query) ||
    (cat.description && cat.description.toLowerCase().includes(query))
  )
})

const totalCategories = computed(() => allFilteredCategories.value.length)

const filteredCategories = computed(() => {
  const start = (currentPage.value - 1) * perPage.value
  const end = start + perPage.value
  return allFilteredCategories.value.slice(start, end)
})

const handlePageChange = (page) => {
  currentPage.value = page
}

watch(searchQuery, () => {
  currentPage.value = 1
})

const fetchCategories = async () => {
  try {
    const response = await api.get('/categories/')
    categories.value = response.data
  } catch (error) {
    console.error('Error fetching categories:', error)
    Swal.fire({
      icon: 'error',
      title: 'Error',
      text: 'Failed to fetch categories'
    })
  }
}

const refreshTable = async () => {
  const button = event.target.closest('button')
  const icon = button.querySelector('i')
  icon.classList.add('fa-spin')
  
  await fetchCategories()
  
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

const openEditModal = (category) => {
  isEditMode.value = true
  formData.value = { ...category }
  showModal()
}

const saveCategory = async () => {
  try {
    if (isEditMode.value) {
      await api.put(`/categories/${formData.value.id}/`, formData.value)
      Swal.fire({
        icon: 'success',
        title: 'Success!',
        text: 'Category updated successfully',
        timer: 1500,
        showConfirmButton: false
      })
    } else {
      await api.post('/categories/', formData.value)
      Swal.fire({
        icon: 'success',
        title: 'Success!',
        text: 'Category created successfully',
        timer: 1500,
        showConfirmButton: false
      })
    }
    
    await fetchCategories()
    closeModal()
  } catch (error) {
    console.error('Error saving category:', error)
    Swal.fire({
      icon: 'error',
      title: 'Error',
      text: error.response?.data?.message || 'Failed to save category'
    })
  }
}

const toggleStatus = async (category) => {
  try {
    await api.patch(`/categories/${category.id}/`, { is_active: !category.is_active })
    await fetchCategories()
    
    const Toast = Swal.mixin({
      toast: true,
      position: 'top-end',
      showConfirmButton: false,
      timer: 2000
    })
    
    Toast.fire({
      icon: 'success',
      title: 'Status updated'
    })
  } catch (error) {
    console.error('Error updating status:', error)
    Swal.fire({
      icon: 'error',
      title: 'Error',
      text: 'Failed to update status'
    })
  }
}

const deleteCategory = async (id) => {
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
      await api.delete(`/categories/${id}/`)
      Swal.fire('Deleted!', 'Category has been deleted.', 'success')
      await fetchCategories()
    } catch (error) {
      console.error('Error deleting category:', error)
      Swal.fire({
        icon: 'error',
        title: 'Error',
        text: 'Failed to delete category'
      })
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
  const modal = document.getElementById('categoryModal')
  modal.classList.add('show')
  modal.style.display = 'block'
  document.body.classList.add('modal-open')
  
  const backdrop = document.createElement('div')
  backdrop.className = 'modal-backdrop fade show'
  backdrop.id = 'modal-backdrop'
  document.body.appendChild(backdrop)
}

const closeModal = () => {
  const modal = document.getElementById('categoryModal')
  modal.classList.remove('show')
  modal.style.display = 'none'
  document.body.classList.remove('modal-open')
  
  const backdrop = document.getElementById('modal-backdrop')
  if (backdrop) {
    backdrop.remove()
  }
  
  resetForm()
}

const viewCategory = (category) => {
  viewData.value = { ...category }
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
  fetchCategories()
})
</script>
