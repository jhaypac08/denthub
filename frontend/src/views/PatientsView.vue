<template>
  <div class="content-header">
    <div class="container-fluid">
      <div class="row mb-2">
        <div class="col-sm-6">
          <h1 class="m-0">Patients</h1>
        </div>
        <div class="col-sm-6">
          <button class="btn btn-secondary float-right ml-2" @click="fetchPatients" title="Refresh">
            <i class="fas fa-sync-alt"></i>
          </button>
          <button class="btn btn-primary float-right" @click="openAddModal">
            <i class="fas fa-plus"></i> Add New Patient
          </button>
        </div>
      </div>
    </div>
  </div>

  <section class="content">
    <div class="container-fluid">
      <div class="card">
        <div class="card-header">
          <div class="row">
            <div class="col-md-6">
              <input
                type="text"
                v-model="searchQuery"
                class="form-control"
                placeholder="Search by name, ID, or phone..."
              />
            </div>
            <div class="col-md-3">
              <select v-model="statusFilter" class="form-control">
                <option value="">All Status</option>
                <option value="active">Active</option>
                <option value="inactive">Inactive</option>
                <option value="archived">Archived</option>
              </select>
            </div>
          </div>
        </div>
        <div class="card-body">
          <div class="table-responsive">
            <table class="table table-bordered table-striped">
              <thead>
                <tr>
                  <th>Patient ID</th>
                  <th>Name</th>
                <th>Gender</th>
                <th>Age</th>
                <th>Phone</th>
                <th>Email</th>
                <th>Status</th>
                <th>Actions</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="patient in filteredPatients" :key="patient.id" @click="viewPatient(patient)" style="cursor: pointer;">
                <td>{{ patient.patient_id }}</td>
                <td>{{ patient.full_name }}</td>
                <td>{{ patient.gender }}</td>
                <td>{{ patient.age }}</td>
                <td>{{ patient.phone || 'N/A' }}</td>
                <td>{{ patient.email || 'N/A' }}</td>
                <td>
                  <span :class="getStatusClass(patient.status)">
                    {{ patient.status }}
                  </span>
                </td>
                <td @click.stop>
                  <button class="btn btn-sm btn-info" @click="viewPatient(patient)" title="View">
                    <i class="fas fa-eye"></i>
                  </button>
                  <button class="btn btn-sm btn-primary" @click="viewHistory(patient)" title="History">
                    <i class="fas fa-history"></i>
                  </button>
                  <button class="btn btn-sm btn-warning" @click="editPatient(patient)" title="Edit">
                    <i class="fas fa-edit"></i>
                  </button>
                  <button class="btn btn-sm btn-danger" @click="deletePatient(patient.id)" title="Delete">
                    <i class="fas fa-trash"></i>
                  </button>
                </td>
              </tr>
              <tr v-if="filteredPatients.length === 0">
                <td colspan="8" class="text-center">No patients found</td>
              </tr>
            </tbody>
          </table>
          </div>
        </div>
        <div class="card-footer clearfix">
          <TablePagination
            :current-page="currentPage"
            :per-page="perPage"
            :total="totalPatients"
            @page-change="handlePageChange"
          />
        </div>
      </div>
    </div>
  </section>

  <!-- Add/Edit Modal -->
  <div class="modal fade" id="patientModal" tabindex="-1">
    <div class="modal-dialog modal-lg">
      <div class="modal-content">
        <div class="modal-header" style="background-color: #00B2A9; color: white;">
          <h5 class="modal-title">{{ isEditing ? 'Edit Patient' : 'Add New Patient' }}</h5>
          <button type="button" class="close" @click="closeModal" style="color: white;">
            <span>&times;</span>
          </button>
        </div>
        <div class="modal-body">
          <form @submit.prevent="savePatient">
            <!-- Basic Information -->
            <h6 class="text-muted">Basic Information</h6>
            <div class="row">
              <div class="col-md-4">
                <div class="form-group">
                  <label>First Name *</label>
                  <input type="text" v-model="form.first_name" class="form-control" required />
                </div>
              </div>
              <div class="col-md-4">
                <div class="form-group">
                  <label>Middle Name</label>
                  <input type="text" v-model="form.middle_name" class="form-control" />
                </div>
              </div>
              <div class="col-md-4">
                <div class="form-group">
                  <label>Last Name *</label>
                  <input type="text" v-model="form.last_name" class="form-control" required />
                </div>
              </div>
            </div>
            <div class="row">
              <div v-if="isEditing" class="col-md-3">
                <div class="form-group">
                  <label>Patient ID</label>
                  <input type="text" v-model="form.patient_id" class="form-control" readonly />
                </div>
              </div>
              <div :class="isEditing ? 'col-md-3' : 'col-md-4'">
                <div class="form-group">
                  <label>Date of Birth *</label>
                  <input type="date" v-model="form.date_of_birth" class="form-control" required />
                  <small class="text-muted" v-if="form.date_of_birth">
                    Age: {{ calculateAge(form.date_of_birth) }} years {{ isMinor ? '(Minor)' : '(Adult)' }}
                  </small>
                </div>
              </div>
              <div :class="isEditing ? 'col-md-3' : 'col-md-4'">
                <div class="form-group">
                  <label>Gender *</label>
                  <select v-model="form.gender" class="form-control" required>
                    <option value="">Select Gender</option>
                    <option value="male">Male</option>
                    <option value="female">Female</option>
                    <option value="other">Other</option>
                  </select>
                </div>
              </div>
              <div :class="isEditing ? 'col-md-3' : 'col-md-4'">
                <div class="form-group">
                  <label>Blood Type</label>
                  <select v-model="form.blood_type" class="form-control">
                    <option value="">Select Blood Type</option>
                    <option value="A+">A+</option>
                    <option value="A-">A-</option>
                    <option value="B+">B+</option>
                    <option value="B-">B-</option>
                    <option value="AB+">AB+</option>
                    <option value="AB-">AB-</option>
                    <option value="O+">O+</option>
                    <option value="O-">O-</option>
                  </select>
                </div>
              </div>
            </div>

            <!-- Contact Information -->
            <h6 class="text-muted mt-3">Contact Information</h6>
            <div class="row">
              <div class="col-md-6">
                <div class="form-group">
                  <label>Phone {{ !isMinor ? '*' : '' }}</label>
                  <input type="tel" v-model="form.phone" class="form-control" :required="!isMinor" />
                </div>
              </div>
              <div class="col-md-6">
                <div class="form-group">
                  <label>Email</label>
                  <input type="email" v-model="form.email" class="form-control" />
                </div>
              </div>
            </div>
            <div class="form-group">
              <label>Address *</label>
              <textarea v-model="form.address" class="form-control" rows="2" required></textarea>
            </div>
            <div class="form-group">
              <label>City *</label>
              <input 
                type="text" 
                v-model="form.city" 
                class="form-control" 
                list="cityList" 
                placeholder="Type or select city"
                required 
              />
              <datalist id="cityList">
                <option v-for="city in philippineCities" :key="city" :value="city"></option>
              </datalist>
            </div>

            <!-- Parent/Guardian Information (For Minors Only) -->
            <div v-if="isMinor">
              <h6 class="text-muted mt-3">Parent/Guardian Information *</h6>
              <div class="row">
                <div class="col-md-3">
                  <div class="form-group">
                    <label>Parent/Guardian Name *</label>
                    <input type="text" v-model="form.emergency_contact_name" class="form-control" required />
                  </div>
                </div>
                <div class="col-md-3">
                  <div class="form-group">
                    <label>Date of Birth *</label>
                    <input type="date" v-model="form.guardian_date_of_birth" class="form-control" required />
                  </div>
                </div>
                <div class="col-md-3">
                  <div class="form-group">
                    <label>Contact Number *</label>
                    <input type="tel" v-model="form.emergency_contact_phone" class="form-control" required />
                  </div>
                </div>
                <div class="col-md-3">
                  <div class="form-group">
                    <label>Occupation *</label>
                    <input type="text" v-model="form.guardian_occupation" class="form-control" required placeholder="Occupation" />
                  </div>
                </div>
              </div>
              <div class="row">
                <div class="col-md-12">
                  <div class="form-group">
                    <label>Relationship to Patient *</label>
                    <select v-model="form.emergency_contact_relation" class="form-control" required>
                      <option value="">Select Relationship</option>
                      <option value="Mother">Mother</option>
                      <option value="Father">Father</option>
                      <option value="Legal Guardian">Legal Guardian</option>
                      <option value="Grandmother">Grandmother</option>
                      <option value="Grandfather">Grandfather</option>
                      <option value="Aunt">Aunt</option>
                      <option value="Uncle">Uncle</option>
                      <option value="Other">Other</option>
                    </select>
                  </div>
                </div>
              </div>
              <div v-if="form.emergency_contact_relation === 'Other'" class="row">
                <div class="col-md-12">
                  <div class="form-group">
                    <label>Specify Relationship *</label>
                    <input type="text" v-model="form.other_relation" class="form-control" required placeholder="Please specify the relationship" />
                  </div>
                </div>
              </div>
            </div>

            <!-- Emergency Contact Information (For Adults Only) -->
            <div v-if="!isMinor">
              <h6 class="text-muted mt-3">Emergency Contact (Optional)</h6>
              <div class="row">
                <div class="col-md-4">
                  <div class="form-group">
                    <label>Contact Name</label>
                    <input type="text" v-model="form.emergency_contact_name" class="form-control" />
                  </div>
                </div>
                <div class="col-md-4">
                  <div class="form-group">
                    <label>Contact Phone</label>
                    <input type="tel" v-model="form.emergency_contact_phone" class="form-control" />
                  </div>
                </div>
                <div class="col-md-4">
                  <div class="form-group">
                    <label>Relation</label>
                    <input type="text" v-model="form.emergency_contact_relation" class="form-control" placeholder="e.g., Spouse, Sibling, Friend" />
                  </div>
                </div>
              </div>
            </div>

            <!-- Medical & Dental Information -->
            <h6 class="text-muted mt-3">Medical & Dental Information</h6>
            <div class="form-group">
              <label>Allergies</label>
              <textarea v-model="form.allergies" class="form-control" rows="2" placeholder="List any allergies"></textarea>
            </div>
            <div class="form-group">
              <label>Medical Conditions</label>
              <textarea v-model="form.medical_conditions" class="form-control" rows="2" placeholder="Existing medical conditions"></textarea>
            </div>
            <div class="form-group">
              <label>Current Medications</label>
              <textarea v-model="form.current_medications" class="form-control" rows="2" placeholder="Current medications"></textarea>
            </div>
            <div class="row">
              <div class="col-md-6">
                <div class="form-group">
                  <label>Dental Insurance</label>
                  <input type="text" v-model="form.dental_insurance" class="form-control" />
                </div>
              </div>
              <div class="col-md-6">
                <div class="form-group">
                  <label>Insurance Policy Number</label>
                  <input type="text" v-model="form.insurance_policy_number" class="form-control" />
                </div>
              </div>
            </div>

            <!-- Status & Notes -->
            <h6 class="text-muted mt-3">Status & Notes</h6>
            <div class="row">
              <div class="col-md-12">
                <div class="form-group">
                  <label>Status *</label>
                  <select v-model="form.status" class="form-control" required>
                    <option value="active">Active</option>
                    <option value="inactive">Inactive</option>
                    <option value="archived">Archived</option>
                  </select>
                </div>
              </div>
            </div>
            <div class="form-group">
              <label>Notes</label>
              <textarea v-model="form.notes" class="form-control" rows="3"></textarea>
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
          <h5 class="modal-title">Patient Details</h5>
          <button type="button" class="close" @click="closeViewModal" style="color: white;">
            <span>&times;</span>
          </button>
        </div>
        <div class="modal-body">
          <div class="row">
            <div class="col-md-6">
              <p><strong>Patient ID:</strong> {{ viewData.patient_id }}</p>
              <p><strong>Full Name:</strong> {{ viewData.full_name }}</p>
              <p><strong>Gender:</strong> {{ viewData.gender }}</p>
              <p><strong>Age:</strong> {{ viewData.age }} years {{ viewData.age < 18 ? '(Minor)' : '(Adult)' }}</p>
              <p><strong>Date of Birth:</strong> {{ viewData.date_of_birth }}</p>
              <p><strong>Blood Type:</strong> {{ viewData.blood_type || 'N/A' }}</p>
            </div>
            <div class="col-md-6">
              <p><strong>Phone:</strong> {{ viewData.phone || 'N/A' }}</p>
              <p><strong>Email:</strong> {{ viewData.email || 'N/A' }}</p>
              <p><strong>Address:</strong> {{ viewData.address }}</p>
              <p><strong>City:</strong> {{ viewData.city }}</p>
              <p><strong>Status:</strong> <span :class="getStatusClass(viewData.status)">{{ viewData.status }}</span></p>
            </div>
          </div>
          <hr>
          <h6>{{ viewData.age < 18 ? 'Parent/Guardian Information' : 'Emergency Contact' }}</h6>
          <div v-if="viewData.age < 18">
            <p><strong>Parent/Guardian Name:</strong> {{ viewData.emergency_contact_name || 'N/A' }}</p>
            <p><strong>Date of Birth:</strong> {{ viewData.guardian_date_of_birth || 'N/A' }}</p>
            <p><strong>Contact Number:</strong> {{ viewData.emergency_contact_phone || 'N/A' }}</p>
            <p><strong>Occupation:</strong> {{ viewData.guardian_occupation || 'N/A' }}</p>
            <p><strong>Relationship:</strong> {{ viewData.emergency_contact_relation || 'N/A' }}
              <span v-if="viewData.emergency_contact_relation === 'Other' && viewData.other_relation"> - {{ viewData.other_relation }}</span>
            </p>
          </div>
          <div v-else>
            <p><strong>Contact Name:</strong> {{ viewData.emergency_contact_name || 'N/A' }}</p>
            <p><strong>Contact Phone:</strong> {{ viewData.emergency_contact_phone || 'N/A' }}</p>
            <p><strong>Relation:</strong> {{ viewData.emergency_contact_relation || 'N/A' }}</p>
          </div>
          <hr>
          <h6>Medical Information</h6>
          <p><strong>Allergies:</strong> {{ viewData.allergies || 'None' }}</p>
          <p><strong>Medical Conditions:</strong> {{ viewData.medical_conditions || 'None' }}</p>
          <p><strong>Current Medications:</strong> {{ viewData.current_medications || 'None' }}</p>
          <hr>
          <h6>Dental Insurance</h6>
          <p><strong>Insurance:</strong> {{ viewData.dental_insurance || 'N/A' }}</p>
          <p><strong>Policy Number:</strong> {{ viewData.insurance_policy_number || 'N/A' }}</p>
          <hr>
          <p><strong>Registration Date:</strong> {{ viewData.registration_date }}</p>
          <p><strong>Last Visit:</strong> {{ viewData.last_visit || 'Never' }}</p>
          <p><strong>Notes:</strong> {{ viewData.notes || 'No notes' }}</p>
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

  <!-- Patient History Modal -->
  <div class="modal fade" id="historyModal" tabindex="-1">
    <div class="modal-dialog modal-xl">
      <div class="modal-content">
        <div class="modal-header" style="background-color: #00B2A9; color: white;">
          <h5 class="modal-title">Patient History - {{ historyData.patient_name }}</h5>
          <button type="button" class="close" @click="closeHistoryModal" style="color: white;">
            <span>&times;</span>
          </button>
        </div>
        <div class="modal-body">
          <!-- Appointments Tab -->
          <h6>Appointments</h6>
          <table class="table table-sm table-bordered">
            <thead>
              <tr>
                <th>Date</th>
                <th>Time</th>
                <th>Type</th>
                <th>Dentist</th>
                <th>Status</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="appt in historyData.appointments" :key="appt.id">
                <td>{{ formatDate(appt.appointment_date) }}</td>
                <td>{{ appt.appointment_time }}</td>
                <td>{{ appt.appointment_type }}</td>
                <td>{{ appt.dentist_name || 'N/A' }}</td>
                <td><span class="badge badge-info">{{ appt.status }}</span></td>
              </tr>
              <tr v-if="!historyData.appointments || historyData.appointments.length === 0">
                <td colspan="5" class="text-center">No appointments found</td>
              </tr>
            </tbody>
          </table>

          <hr>

          <!-- Treatment Records Tab -->
          <h6>Treatment Records</h6>
          <table class="table table-sm table-bordered">
            <thead>
              <tr>
                <th>Date</th>
                <th>Diagnosis</th>
                <th>Treatment</th>
                <th>Dentist</th>
                <th>Cost</th>
                <th>Balance</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="treatment in historyData.treatments" :key="treatment.id">
                <td>{{ formatDate(treatment.treatment_date) }}</td>
                <td>{{ treatment.diagnosis }}</td>
                <td>{{ treatment.treatment_performed }}</td>
                <td>{{ treatment.dentist_name || 'N/A' }}</td>
                <td>₱{{ parseFloat(treatment.cost).toLocaleString() }}</td>
                <td>
                  <span :class="treatment.balance > 0 ? 'badge badge-danger' : 'badge badge-success'">
                    ₱{{ parseFloat(treatment.balance).toLocaleString() }}
                  </span>
                </td>
              </tr>
              <tr v-if="!historyData.treatments || historyData.treatments.length === 0">
                <td colspan="6" class="text-center">No treatment records found</td>
              </tr>
            </tbody>
          </table>
        </div>
        <div class="modal-footer">
          <button type="button" class="btn btn-secondary" @click="closeHistoryModal">Close</button>
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

const patients = ref([])
const searchQuery = ref('')
const statusFilter = ref('')
const isEditing = ref(false)
const currentPage = ref(1)
const perPage = ref(10)
const totalPatients = computed(() => filteredPatients.value.length)

const philippineCities = [
  'Alaminos', 'Angeles', 'Antipolo', 'Bacolod', 'Bacoor', 'Bago', 'Baguio', 'Bais', 'Balanga', 'Batac',
  'Batangas City', 'Bayawan', 'Baybay', 'Bayugan', 'Biñan', 'Bislig', 'Bogo', 'Borongan', 'Butuan', 'Cabadbaran',
  'Cabanatuan', 'Cabuyao', 'Cadiz', 'Cagayan de Oro', 'Calamba', 'Calapan', 'Calbayog', 'Caloocan', 'Candon', 'Canlaon',
  'Carcar', 'Catbalogan', 'Cauayan', 'Cavite City', 'Cebu City', 'Cotabato City', 'Dagupan', 'Danao', 'Dapitan', 'Dasmariñas',
  'Davao City', 'Digos', 'Dipolog', 'Dumaguete', 'El Salvador', 'Escalante', 'Gapan', 'General Santos', 'General Trias', 'Gingoog',
  'Guihulngan', 'Himamaylan', 'Ilagan', 'Iligan', 'Iloilo City', 'Imus', 'Iriga', 'Isabela', 'Kabankalan', 'Kidapawan',
  'Koronadal', 'La Carlota', 'Lamitan', 'Laoag', 'Lapu-Lapu', 'Las Piñas', 'Legazpi', 'Ligao', 'Lipa', 'Lucena',
  'Maasin', 'Mabalacat', 'Makati', 'Malabon', 'Malaybalay', 'Malolos', 'Mandaluyong', 'Mandaue', 'Manila', 'Marawi',
  'Marikina', 'Masbate City', 'Mati', 'Meycauayan', 'Muñoz', 'Muntinlupa', 'Naga (Camarines Sur)', 'Naga (Cebu)', 'Navotas', 'Olongapo',
  'Ormoc', 'Oroquieta', 'Ozamiz', 'Pagadian', 'Palayan', 'Panabo', 'Parañaque', 'Pasay', 'Pasig', 'Passi',
  'Puerto Princesa', 'Quezon City', 'Roxas', 'Sagay', 'Samal', 'San Carlos (Negros Occidental)', 'San Carlos (Pangasinan)', 'San Fernando (La Union)', 'San Fernando (Pampanga)', 'San Jose',
  'San Jose del Monte', 'San Juan', 'San Pablo', 'San Pedro', 'Santa Rosa', 'Santiago', 'Silay', 'Sipalay', 'Sorsogon City', 'Surigao City',
  'Tabaco', 'Tabuk', 'Tacloban', 'Tacurong', 'Tagaytay', 'Tagbilaran', 'Taguig', 'Tagum', 'Talisay (Cebu)', 'Talisay (Negros Occidental)',
  'Tandag', 'Tangub', 'Tanjay', 'Tarlac City', 'Tayabas', 'Toledo', 'Trece Martires', 'Tuguegarao', 'Urdaneta', 'Valencia',
  'Valenzuela', 'Victorias', 'Vigan', 'Zamboanga City'
]

const form = ref({
  patient_id: '',
  first_name: '',
  middle_name: '',
  last_name: '',
  gender: '',
  date_of_birth: '',
  blood_type: '',
  phone: '',
  email: '',
  address: '',
  city: '',
  state: '',
  postal_code: '',
  emergency_contact_name: '',
  emergency_contact_phone: '',
  emergency_contact_relation: '',
  other_relation: '',
  guardian_date_of_birth: '',
  guardian_occupation: '',
  allergies: '',
  medical_conditions: '',
  current_medications: '',
  dental_insurance: '',
  insurance_policy_number: '',
  status: 'active',
  notes: ''
})

// Computed property to check if patient is a minor (under 18)
const isMinor = computed(() => {
  if (!form.value.date_of_birth) return false
  
  const today = new Date()
  const birthDate = new Date(form.value.date_of_birth)
  let age = today.getFullYear() - birthDate.getFullYear()
  const monthDiff = today.getMonth() - birthDate.getMonth()
  
  if (monthDiff < 0 || (monthDiff === 0 && today.getDate() < birthDate.getDate())) {
    age--
  }
  
  return age < 18
})

const viewData = ref({})
const historyData = ref({
  patient_name: '',
  appointments: [],
  treatments: []
})

const allFilteredPatients = computed(() => {
  let filtered = patients.value

  if (searchQuery.value) {
    const query = searchQuery.value.toLowerCase()
    filtered = filtered.filter(p =>
      p.full_name.toLowerCase().includes(query) ||
      p.patient_id.toLowerCase().includes(query) ||
      p.phone.includes(query)
    )
  }

  if (statusFilter.value) {
    filtered = filtered.filter(p => p.status === statusFilter.value)
  }

  return filtered
})

const filteredPatients = computed(() => {
  const start = (currentPage.value - 1) * perPage.value
  const end = start + perPage.value
  return allFilteredPatients.value.slice(start, end)
})

const handlePageChange = (page) => {
  currentPage.value = page
}

// Reset to page 1 when filters change
watch([searchQuery, statusFilter], () => {
  currentPage.value = 1
})

const fetchPatients = async () => {
  try {
    const response = await api.get('/patient/patients/')
    patients.value = response.data
  } catch (error) {
    console.error('Error fetching patients:', error)
    Swal.fire('Error', 'Failed to fetch patients', 'error')
  }
}

const openAddModal = () => {
  isEditing.value = false
  resetForm()
  showModal()
}

const editPatient = (patient) => {
  isEditing.value = true
  form.value = { ...patient }
  showModal()
}

const editFromView = () => {
  closeViewModal()
  isEditing.value = true
  form.value = { ...viewData.value }
  showModal()
}

const viewPatient = (patient) => {
  viewData.value = { ...patient }
  showViewModal()
}

const viewHistory = async (patient) => {
  try {
    historyData.value.patient_name = patient.full_name
    
    // Fetch appointments
    const appointmentsResponse = await api.get(`/patient/patients/${patient.id}/appointments/`)
    historyData.value.appointments = appointmentsResponse.data
    
    // Fetch treatments
    const treatmentsResponse = await api.get(`/patient/patients/${patient.id}/treatments/`)
    historyData.value.treatments = treatmentsResponse.data
    
    showHistoryModal()
  } catch (error) {
    console.error('Error fetching patient history:', error)
    Swal.fire('Error', 'Failed to fetch patient history', 'error')
  }
}

const formatDate = (date) => {
  if (!date) return ''
  return new Date(date).toLocaleDateString('en-US', { 
    year: 'numeric', 
    month: 'short', 
    day: 'numeric' 
  })
}

const calculateAge = (dateOfBirth) => {
  if (!dateOfBirth) return 0
  const today = new Date()
  const birthDate = new Date(dateOfBirth)
  let age = today.getFullYear() - birthDate.getFullYear()
  const monthDiff = today.getMonth() - birthDate.getMonth()
  
  if (monthDiff < 0 || (monthDiff === 0 && today.getDate() < birthDate.getDate())) {
    age--
  }
  
  return age
}

const savePatient = async () => {
  try {
    if (isEditing.value) {
      await api.put(`/patient/patients/${form.value.id}/`, form.value)
      Swal.fire({
        toast: true,
        position: 'top-end',
        icon: 'success',
        title: 'Patient updated successfully',
        showConfirmButton: false,
        timer: 2000
      })
    } else {
      await api.post('/patient/patients/', form.value)
      Swal.fire({
        toast: true,
        position: 'top-end',
        icon: 'success',
        title: 'Patient added successfully',
        showConfirmButton: false,
        timer: 2000
      })
    }

    await fetchPatients()
    closeModal()
  } catch (error) {
    console.error('Error saving patient:', error)
    Swal.fire('Error', 'Failed to save patient', 'error')
  }
}

const deletePatient = async (id) => {
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
      await api.delete(`/patient/patients/${id}/`)
      await fetchPatients()
      Swal.fire('Deleted!', 'Patient has been deleted.', 'success')
    } catch (error) {
      console.error('Error deleting patient:', error)
      Swal.fire('Error', 'Failed to delete patient', 'error')
    }
  }
}

const resetForm = () => {
  form.value = {
    patient_id: '',
    first_name: '',
    middle_name: '',
    last_name: '',
    gender: '',
    date_of_birth: '',
    blood_type: '',
    phone: '',
    email: '',
    address: '',
    city: '',
    state: '',
    postal_code: '',
    emergency_contact_name: '',
    emergency_contact_phone: '',
    emergency_contact_relation: '',
    other_relation: '',
    guardian_date_of_birth: '',
    guardian_occupation: '',
    allergies: '',
    medical_conditions: '',
    current_medications: '',
    dental_insurance: '',
    insurance_policy_number: '',
    status: 'active',
    notes: ''
  }
}

const showModal = () => {
  const modal = document.getElementById('patientModal')
  modal.classList.add('show')
  modal.style.display = 'block'
  document.body.classList.add('modal-open')
  
  const backdrop = document.createElement('div')
  backdrop.className = 'modal-backdrop fade show'
  backdrop.id = 'patientModalBackdrop'
  document.body.appendChild(backdrop)
}

const closeModal = () => {
  const modal = document.getElementById('patientModal')
  modal.classList.remove('show')
  modal.style.display = 'none'
  document.body.classList.remove('modal-open')
  
  const backdrop = document.getElementById('patientModalBackdrop')
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

const showHistoryModal = () => {
  const modal = document.getElementById('historyModal')
  modal.classList.add('show')
  modal.style.display = 'block'
  document.body.classList.add('modal-open')
  
  const backdrop = document.createElement('div')
  backdrop.className = 'modal-backdrop fade show'
  backdrop.id = 'historyModalBackdrop'
  document.body.appendChild(backdrop)
}

const closeHistoryModal = () => {
  const modal = document.getElementById('historyModal')
  modal.classList.remove('show')
  modal.style.display = 'none'
  document.body.classList.remove('modal-open')
  
  const backdrop = document.getElementById('historyModalBackdrop')
  if (backdrop) {
    backdrop.remove()
  }
  
  historyData.value = {
    patient_name: '',
    appointments: [],
    treatments: []
  }
}

const getStatusClass = (status) => {
  const classes = {
    active: 'badge badge-success',
    inactive: 'badge badge-warning',
    archived: 'badge badge-secondary'
  }
  return classes[status] || 'badge badge-secondary'
}

onMounted(() => {
  fetchPatients()
})
</script>

<style scoped>
.modal {
  overflow-y: auto;
}
</style>
