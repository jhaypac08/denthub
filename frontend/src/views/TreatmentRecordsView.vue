<template>
  <div class="content-header">
    <div class="container-fluid">
      <div class="row mb-2">
        <div class="col-sm-6">
          <h1 class="m-0">Treatment Records</h1>
        </div>
        <div class="col-sm-6">
          <button class="btn btn-secondary float-right ml-2" @click="fetchRecords" title="Refresh">
            <i class="fas fa-sync-alt"></i>
          </button>
          <button class="btn btn-primary float-right" @click="openAddModal">
            <i class="fas fa-plus"></i> Add Treatment Record
          </button>
        </div>
      </div>
    </div>
  </div>

  <section class="content">
    <div class="container-fluid">
      <!-- Summary Cards -->
      <div class="row mb-3">
        <div v-if="authStore.isAdmin" class="col-lg-3 col-6">
          <div class="small-box bg-info">
            <div class="inner">
              <h3>{{ stats.total }}</h3>
              <p>Total Records</p>
            </div>
            <div class="icon">
              <i class="fas fa-file-medical"></i>
            </div>
          </div>
        </div>
        <div v-if="authStore.isAdmin" class="col-lg-3 col-6">
          <div class="small-box bg-success">
            <div class="inner">
              <h3>₱{{ stats.totalRevenue.toLocaleString() }}</h3>
              <p>Total Revenue</p>
            </div>
            <div class="icon">
              <i class="fas fa-dollar-sign"></i>
            </div>
          </div>
        </div>
        <div v-if="authStore.isAdmin" class="col-lg-3 col-6">
          <div class="small-box bg-warning">
            <div class="inner">
              <h3>₱{{ stats.pendingPayments.toLocaleString() }}</h3>
              <p>Pending Payments</p>
            </div>
            <div class="icon">
              <i class="fas fa-exclamation-triangle"></i>
            </div>
          </div>
        </div>
        <div v-if="authStore.isAdmin" class="col-lg-3 col-6">
          <div class="small-box bg-danger">
            <div class="inner">
              <h3>{{ stats.unpaidCount }}</h3>
              <p>Unpaid Records</p>
            </div>
            <div class="icon">
              <i class="fas fa-receipt"></i>
            </div>
          </div>
        </div>
      </div>

      <div class="card">
        <div class="card-header">
          <div class="row">
            <div class="col-md-6">
              <input
                type="text"
                v-model="searchQuery"
                class="form-control"
                placeholder="Search by patient name or diagnosis..."
              />
            </div>
            <div class="col-md-3">
              <select v-model="patientFilter" class="form-control">
                <option value="">All Patients</option>
                <option v-for="patient in patients" :key="patient.id" :value="patient.id">
                  {{ patient.patient_id }} - {{ patient.full_name }}
                </option>
              </select>
            </div>
            <div class="col-md-3">
              <button class="btn btn-warning btn-block" @click="showPendingPayments">
                <i class="fas fa-exclamation-circle"></i> Pending Payments
              </button>
            </div>
          </div>
        </div>
        <div class="card-body">
          <div v-if="isLoading" class="text-center py-5">
            <i class="fas fa-spinner fa-spin fa-3x text-primary"></i>
            <p class="mt-3">Loading treatment records...</p>
          </div>
          <div v-else class="table-responsive">
            <table class="table table-bordered table-striped">
              <thead>
                <tr>
                  <th>Date</th>
                  <th>Patient</th>
                <th>Diagnosis</th>
                <th>Treatment</th>
                <th>Dentist</th>
                <th>Cost</th>
                <th>Paid</th>
                <th>Balance</th>
                <th>Actions</th>
              </tr>
            </thead>
            <tbody>
              <tr v-if="filteredRecords.length === 0">
                <td colspan="9" class="text-center">No treatment records found</td>
              </tr>
              <tr v-for="record in filteredRecords" :key="record.id" @click="viewRecord(record)" style="cursor: pointer;">
                <td>{{ formatDate(record.treatment_date) }}</td>
                <td>{{ record.patient_name }}</td>
                <td>{{ truncate(record.diagnosis, 30) }}</td>
                <td>{{ truncate(record.treatment_performed, 30) }}</td>
                <td>{{ record.dentist_name || 'N/A' }}</td>
                <td>₱{{ parseFloat(record.cost).toLocaleString() }}</td>
                <td>₱{{ parseFloat(record.paid_amount).toLocaleString() }}</td>
                <td>
                  <span :class="getBalanceClass(record.balance)">
                    ₱{{ parseFloat(record.balance).toLocaleString() }}
                  </span>
                </td>
                <td @click.stop>
                  <button class="btn btn-sm btn-info" @click="viewRecord(record)" title="View">
                    <i class="fas fa-eye"></i>
                  </button>
                  <button class="btn btn-sm btn-warning" @click="editRecord(record)" title="Edit">
                    <i class="fas fa-edit"></i>
                  </button>
                  <button class="btn btn-sm btn-success" @click="recordPayment(record)" title="Record Payment" v-if="record.balance > 0">
                    <i class="fas fa-money-bill"></i>
                  </button>
                  <button class="btn btn-sm btn-danger" @click="deleteRecord(record.id)" title="Delete">
                    <i class="fas fa-trash"></i>
                  </button>
                </td>
              </tr>
            </tbody>
          </table>
          </div>
        </div>
        <div class="card-footer clearfix">
          <TablePagination
            :current-page="currentPage"
            :per-page="perPage"
            :total="totalRecords"
            @page-change="handlePageChange"
          />
        </div>
      </div>
    </div>
  </section>

  <!-- Add/Edit Modal -->
  <div class="modal fade" id="treatmentModal" tabindex="-1">
    <div class="modal-dialog modal-lg">
      <div class="modal-content">
        <div class="modal-header" style="background-color: #00B2A9; color: white;">
          <h5 class="modal-title">{{ isEditing ? 'Edit Treatment Record' : 'Add Treatment Record' }}</h5>
          <button type="button" class="close" @click="closeModal" style="color: white;">
            <span>&times;</span>
          </button>
        </div>
        <div class="modal-body">
          <form @submit.prevent="saveRecord">
            <div class="row">
              <div class="col-md-6">
                <div class="form-group">
                  <label>Patient *</label>
                  <select v-model="form.patient" class="form-control" required :disabled="isEditing">
                    <option value="">Select Patient</option>
                    <option v-for="patient in patients" :key="patient.id" :value="patient.id">
                      {{ patient.patient_id }} - {{ patient.full_name }}
                    </option>
                  </select>
                </div>
              </div>
              <div class="col-md-6">
                <div class="form-group">
                  <label>Dentist</label>
                  <select v-model="form.dentist" class="form-control">
                    <option value="">Select Dentist</option>
                    <option v-for="user in users" :key="user.id" :value="user.id">
                      {{ user.first_name }} {{ user.last_name }}
                    </option>
                  </select>
                </div>
              </div>
            </div>
            <div class="row">
              <div class="col-md-6">
                <div class="form-group">
                  <label>Treatment Date *</label>
                  <input type="date" v-model="form.treatment_date" class="form-control" required />
                </div>
              </div>
              <div class="col-md-6">
                <div class="form-group">
                  <label>Tooth Number(s)</label>
                  <input type="text" v-model="form.tooth_number" class="form-control" placeholder="e.g., 14, 15" />
                </div>
              </div>
            </div>
            <div class="form-group">
              <label>Diagnosis *</label>
              <textarea v-model="form.diagnosis" class="form-control" rows="2" required></textarea>
            </div>
            <div class="form-group">
              <label>Treatment Performed *</label>
              <textarea v-model="form.treatment_performed" class="form-control" rows="2" required></textarea>
            </div>
            <div class="form-group">
              <label>Prescription</label>
              <textarea v-model="form.prescription" class="form-control" rows="2"></textarea>
            </div>
            <div class="row">
              <div class="col-md-6">
                <div class="form-group">
                  <label>Cost *</label>
                  <input type="number" v-model="form.cost" class="form-control" required step="0.01" min="0" />
                </div>
              </div>
              <div class="col-md-6">
                <div class="form-group">
                  <label>Paid Amount *</label>
                  <input type="number" v-model="form.paid_amount" class="form-control" required step="0.01" min="0" />
                </div>
              </div>
            </div>
            <div class="form-group">
              <label>Notes</label>
              <textarea v-model="form.notes" class="form-control" rows="2"></textarea>
            </div>

            <div class="modal-footer">
              <button type="button" class="btn btn-secondary" @click="closeModal">Cancel</button>
              <button type="submit" class="btn btn-primary" style="background-color: #00B2A9; border-color: #00B2A9;">
                {{ isEditing ? 'Update' : 'Save' }}
              </button>
            </div>
          </form>
        </div>
      </div>
    </div>
  </div>

  <!-- View Modal -->
  <div class="modal fade" id="viewModal" tabindex="-1">
    <div class="modal-dialog modal-lg">
      <div class="modal-content">
        <div class="modal-header" style="background-color: #00B2A9; color: white;">
          <h5 class="modal-title">Treatment Record Details</h5>
          <button type="button" class="close" @click="closeViewModal" style="color: white;">
            <span>&times;</span>
          </button>
        </div>
        <div class="modal-body">
          <div class="row">
            <div class="col-md-6">
              <p><strong>Patient:</strong> {{ viewData.patient_name }}</p>
              <p><strong>Patient ID:</strong> {{ viewData.patient_id_display }}</p>
              <p><strong>Treatment Date:</strong> {{ formatDate(viewData.treatment_date) }}</p>
              <p><strong>Tooth Number:</strong> {{ viewData.tooth_number || 'N/A' }}</p>
            </div>
            <div class="col-md-6">
              <p><strong>Dentist:</strong> {{ viewData.dentist_name || 'Not Assigned' }}</p>
              <p><strong>Cost:</strong> ₱{{ parseFloat(viewData.cost || 0).toLocaleString() }}</p>
              <p><strong>Paid:</strong> ₱{{ parseFloat(viewData.paid_amount || 0).toLocaleString() }}</p>
              <p><strong>Balance:</strong> <span :class="getBalanceClass(viewData.balance)">₱{{ parseFloat(viewData.balance || 0).toLocaleString() }}</span></p>
            </div>
          </div>
          <hr>
          <h6>Diagnosis</h6>
          <p>{{ viewData.diagnosis }}</p>
          <hr>
          <h6>Treatment Performed</h6>
          <p>{{ viewData.treatment_performed }}</p>
          <hr>
          <h6>Prescription</h6>
          <p>{{ viewData.prescription || 'No prescription' }}</p>
          <hr>
          <h6>Notes</h6>
          <p>{{ viewData.notes || 'No notes' }}</p>
        </div>
        <div class="modal-footer">
          <button type="button" class="btn btn-secondary" @click="closeViewModal">Close</button>
          <button type="button" class="btn btn-warning" @click="editFromView">
            <i class="fas fa-edit"></i> Edit
          </button>
        </div>
      </div>
    </div>
  </div>

  <!-- Payment Modal -->
  <div class="modal fade" id="paymentModal" tabindex="-1">
    <div class="modal-dialog">
      <div class="modal-content">
        <div class="modal-header" style="background-color: #00B2A9; color: white;">
          <h5 class="modal-title">Record Payment</h5>
          <button type="button" class="close" @click="closePaymentModal" style="color: white;">
            <span>&times;</span>
          </button>
        </div>
        <div class="modal-body">
          <p><strong>Patient:</strong> {{ paymentData.patient_name }}</p>
          <p><strong>Total Cost:</strong> ₱{{ parseFloat(paymentData.cost || 0).toLocaleString() }}</p>
          <p><strong>Already Paid:</strong> ₱{{ parseFloat(paymentData.paid_amount || 0).toLocaleString() }}</p>
          <p><strong>Balance:</strong> ₱{{ parseFloat(paymentData.balance || 0).toLocaleString() }}</p>
          <hr>
          <div class="form-group">
            <label>Payment Amount *</label>
            <input type="number" v-model="paymentAmount" class="form-control" step="0.01" min="0" :max="paymentData.balance" required />
          </div>
        </div>
        <div class="modal-footer">
          <button type="button" class="btn btn-secondary" @click="closePaymentModal">Cancel</button>
          <button type="button" class="btn btn-success" @click="processPayment">
            <i class="fas fa-check"></i> Process Payment
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import { useAuthStore } from '../stores/auth'
import api from '../services/api'
import Swal from 'sweetalert2'
import TablePagination from '../components/TablePagination.vue'

const authStore = useAuthStore()
const records = ref([])
const patients = ref([])
const users = ref([])
const searchQuery = ref('')
const patientFilter = ref('')
const isEditing = ref(false)
const showPendingOnly = ref(false)
const isLoading = ref(true)
const currentPage = ref(1)
const perPage = ref(10)

const stats = ref({
  total: 0,
  totalRevenue: 0,
  pendingPayments: 0,
  unpaidCount: 0
})

const form = ref({
  patient: '',
  dentist: '',
  treatment_date: '',
  tooth_number: '',
  diagnosis: '',
  treatment_performed: '',
  prescription: '',
  cost: 0,
  paid_amount: 0,
  notes: ''
})

const viewData = ref({})
const paymentData = ref({})
const paymentAmount = ref(0)

const allFilteredRecords = computed(() => {
  let filtered = records.value

  if (searchQuery.value) {
    const query = searchQuery.value.toLowerCase()
    filtered = filtered.filter(r =>
      r.patient_name.toLowerCase().includes(query) ||
      r.diagnosis.toLowerCase().includes(query) ||
      r.treatment_performed.toLowerCase().includes(query)
    )
  }

  if (patientFilter.value) {
    filtered = filtered.filter(r => r.patient === parseInt(patientFilter.value))
  }

  if (showPendingOnly.value) {
    filtered = filtered.filter(r => parseFloat(r.balance) > 0)
  }

  return filtered
})

const totalRecords = computed(() => allFilteredRecords.value.length)

const filteredRecords = computed(() => {
  const start = (currentPage.value - 1) * perPage.value
  const end = start + perPage.value
  return allFilteredRecords.value.slice(start, end)
})

const handlePageChange = (page) => {
  currentPage.value = page
}

// Reset to page 1 when filters change
watch([searchQuery, patientFilter, showPendingOnly], () => {
  currentPage.value = 1
})

const fetchRecords = async () => {
  try {
    isLoading.value = true
    const response = await api.get('/patient/treatments/')
    records.value = response.data
    calculateStats()
  } catch (error) {
    console.error('Error fetching records:', error)
    Swal.fire('Error', 'Failed to fetch treatment records', 'error')
  } finally {
    isLoading.value = false
  }
}

const fetchPatients = async () => {
  try {
    const response = await api.get('/patient/patients/')
    patients.value = response.data.filter(p => p.status === 'active')
  } catch (error) {
    console.error('Error fetching patients:', error)
  }
}

const fetchUsers = async () => {
  try {
    const response = await api.get('/users/')
    users.value = response.data
  } catch (error) {
    console.error('Error fetching users:', error)
  }
}

const calculateStats = () => {
  stats.value.total = records.value.length
  stats.value.totalRevenue = records.value.reduce((sum, r) => sum + parseFloat(r.cost), 0)
  stats.value.pendingPayments = records.value.reduce((sum, r) => sum + parseFloat(r.balance), 0)
  stats.value.unpaidCount = records.value.filter(r => parseFloat(r.balance) > 0).length
}

const showPendingPayments = async () => {
  showPendingOnly.value = !showPendingOnly.value
}

const openAddModal = () => {
  isEditing.value = false
  resetForm()
  showModal()
}

const editRecord = (record) => {
  isEditing.value = true
  form.value = { ...record }
  showModal()
}

const editFromView = () => {
  closeViewModal()
  isEditing.value = true
  form.value = { ...viewData.value }
  showModal()
}

const viewRecord = (record) => {
  viewData.value = { ...record }
  showViewModal()
}

const recordPayment = (record) => {
  paymentData.value = { ...record }
  paymentAmount.value = parseFloat(record.balance)
  showPaymentModal()
}

const processPayment = async () => {
  try {
    const newPaidAmount = parseFloat(paymentData.value.paid_amount) + parseFloat(paymentAmount.value)
    
    await api.put(`/patient/treatments/${paymentData.value.id}/`, {
      ...paymentData.value,
      paid_amount: newPaidAmount
    })

    Swal.fire({
      toast: true,
      position: 'top-end',
      icon: 'success',
      title: 'Payment recorded successfully',
      showConfirmButton: false,
      timer: 2000
    })

    await fetchRecords()
    closePaymentModal()
  } catch (error) {
    console.error('Error recording payment:', error)
    Swal.fire('Error', 'Failed to record payment', 'error')
  }
}

const saveRecord = async () => {
  try {
    if (isEditing.value) {
      await api.put(`/patient/treatments/${form.value.id}/`, form.value)
      Swal.fire({
        toast: true,
        position: 'top-end',
        icon: 'success',
        title: 'Treatment record updated successfully',
        showConfirmButton: false,
        timer: 2000
      })
    } else {
      await api.post('/patient/treatments/', form.value)
      Swal.fire({
        toast: true,
        position: 'top-end',
        icon: 'success',
        title: 'Treatment record added successfully',
        showConfirmButton: false,
        timer: 2000
      })
    }

    await fetchRecords()
    closeModal()
  } catch (error) {
    console.error('Error saving record:', error)
    Swal.fire('Error', 'Failed to save treatment record', 'error')
  }
}

const deleteRecord = async (id) => {
  const result = await Swal.fire({
    title: 'Are you sure?',
    text: 'You won\'t be able to revert this!',
    icon: 'warning',
    showCancelButton: true,
    confirmButtonColor: '#d33',
    cancelButtonColor: '#3085d6',
    confirmButtonText: 'Yes, delete it!'
  })

  if (result.isConfirmed) {
    try {
      await api.delete(`/patient/treatments/${id}/`)
      await fetchRecords()
      Swal.fire('Deleted!', 'Treatment record has been deleted.', 'success')
    } catch (error) {
      console.error('Error deleting record:', error)
      Swal.fire('Error', 'Failed to delete treatment record', 'error')
    }
  }
}

const resetForm = () => {
  const today = new Date().toISOString().split('T')[0]
  form.value = {
    patient: '',
    dentist: '',
    treatment_date: today,
    tooth_number: '',
    diagnosis: '',
    treatment_performed: '',
    prescription: '',
    cost: 0,
    paid_amount: 0,
    notes: ''
  }
}

const formatDate = (date) => {
  if (!date) return ''
  return new Date(date).toLocaleDateString('en-US', { 
    year: 'numeric', 
    month: 'long', 
    day: 'numeric' 
  })
}

const truncate = (text, length) => {
  if (!text) return ''
  return text.length > length ? text.substring(0, length) + '...' : text
}

const getBalanceClass = (balance) => {
  const bal = parseFloat(balance)
  if (bal === 0) return 'badge badge-success'
  return 'badge badge-danger'
}

const showModal = () => {
  const modal = document.getElementById('treatmentModal')
  modal.classList.add('show')
  modal.style.display = 'block'
  document.body.classList.add('modal-open')
  
  const backdrop = document.createElement('div')
  backdrop.className = 'modal-backdrop fade show'
  backdrop.id = 'treatmentModalBackdrop'
  document.body.appendChild(backdrop)
}

const closeModal = () => {
  const modal = document.getElementById('treatmentModal')
  modal.classList.remove('show')
  modal.style.display = 'none'
  document.body.classList.remove('modal-open')
  
  const backdrop = document.getElementById('treatmentModalBackdrop')
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
  backdrop.id = 'viewModalBackdrop'
  document.body.appendChild(backdrop)
}

const closeViewModal = () => {
  const modal = document.getElementById('viewModal')
  modal.classList.remove('show')
  modal.style.display = 'none'
  document.body.classList.remove('modal-open')
  
  const backdrop = document.getElementById('viewModalBackdrop')
  if (backdrop) {
    backdrop.remove()
  }
}

const showPaymentModal = () => {
  const modal = document.getElementById('paymentModal')
  modal.classList.add('show')
  modal.style.display = 'block'
  document.body.classList.add('modal-open')
  
  const backdrop = document.createElement('div')
  backdrop.className = 'modal-backdrop fade show'
  backdrop.id = 'paymentModalBackdrop'
  document.body.appendChild(backdrop)
}

const closePaymentModal = () => {
  const modal = document.getElementById('paymentModal')
  modal.classList.remove('show')
  modal.style.display = 'none'
  document.body.classList.remove('modal-open')
  
  const backdrop = document.getElementById('paymentModalBackdrop')
  if (backdrop) {
    backdrop.remove()
  }
  
  paymentAmount.value = 0
  paymentData.value = {}
}

onMounted(() => {
  fetchRecords()
  fetchPatients()
  fetchUsers()
})
</script>

<style scoped>
.modal {
  overflow-y: auto;
}
</style>
