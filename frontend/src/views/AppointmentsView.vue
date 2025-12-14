<template>
  

  <div class="content-header">
    <div class="container-fluid">
      <div class="row mb-2">
        <div class="col-sm-6">
          <h1 class="m-0">Appointments</h1>
        </div>
        <div class="col-sm-6">
          <button class="btn btn-secondary float-right ml-2" @click="fetchAppointments" title="Refresh">
            <i class="fas fa-sync-alt"></i>
          </button>
          <button class="btn btn-primary float-right" @click="openAddModal">
            <i class="fas fa-plus"></i> Schedule Appointment
          </button>
        </div>
      </div>
    </div>
  </div>

  <section class="content">
    <div class="container-fluid">
      <!-- Three Panel Tabs -->
      <div class="row mb-3">
        <div class="col-12">
          <div class="appointment-tabs">
            <button 
              class="tab-btn" 
              :class="{ active: activePanel === 'requests' }"
              @click="activePanel = 'requests'"
            >
              Requests
            </button>
            <button 
              class="tab-btn" 
              :class="{ active: activePanel === 'calendar' }"
              @click="activePanel = 'calendar'"
            >
              Calendar
            </button>
            <button 
              class="tab-btn" 
              :class="{ active: activePanel === 'search' }"
              @click="activePanel = 'search'"
            >
              Search
            </button>
          </div>
        </div>
      </div>

      <!-- Requests Panel -->
      <div v-if="activePanel === 'requests'">
        <div class="card">
          <div class="card-header d-flex justify-content-between align-items-center">
            <h5 class="mb-0">Appointment Requests</h5>
            <small class="text-muted">{{ requestedAppointments.length }} pending</small>
          </div>
          <div class="card-body">
            <div v-if="requestedAppointments.length === 0" class="text-center py-5">
              <i class="fas fa-inbox fa-5x text-info mb-3"></i>
              <h4>No Requested Appointments</h4>
              <p class="text-muted">There are no appointment requests at this time.</p>
            </div>
            <div v-else>
              <div class="list-group">
                <div v-for="apt in requestedPageItems" :key="apt.id" class="list-group-item list-group-item-action d-flex justify-content-between align-items-start">
                  <div class="ms-2 me-auto">
                    <div class="fw-bold">{{ apt.patient_name }} — {{ formatAppointmentType(apt.appointment_type) }}</div>
                    <div class="text-muted small">
                      {{ formatDate(apt.appointment_date) }} • {{ formatTime(apt.appointment_time) }}
                      <span v-if="getBranchName(apt.branch)"> • {{ getBranchName(apt.branch) }}</span>
                      <span> • Dentist: {{ getDentistDisplayFromApt(apt) || 'Any' }}</span>
                    </div>
                  </div>
                  <div class="btn-group btn-group-sm">
                    <button class="btn btn-info" @click="viewAppointment(apt)" title="View"><i class="fas fa-eye"></i></button>
                    <button class="btn btn-success" @click="acceptAppointment(apt)" title="Accept / Assign"><i class="fas fa-user-check"></i></button>
                    <button class="btn btn-danger" @click="denyAppointment(apt.id)" title="Deny / Provide Reason"><i class="fas fa-ban"></i></button>
                  </div>
                </div>
              </div>
              <div class="card-footer clearfix mt-2">
                <TablePagination
                  :current-page="currentPage"
                  :per-page="perPage"
                  :total="totalRequested"
                  @page-change="handlePageChange"
                />
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Calendar Panel -->
      <div v-if="activePanel === 'calendar'">
        <div class="card">
          <div class="card-header">
            <div class="d-flex justify-content-between align-items-center">
              <button class="btn btn-sm btn-outline-secondary" @click="previousMonth">
                <i class="fas fa-chevron-left"></i>
              </button>
              <div class="calendar-selector">
                <div class="month-year-selector">
                  <select v-model="currentMonth" @change="changeMonth" class="form-control form-control-sm month-select">
                    <option v-for="(month, index) in monthNames" :key="index" :value="index">
                      {{ month }}
                    </option>
                  </select>
                  <select v-model="currentYear" @change="changeYear" class="form-control form-control-sm year-select">
                    <option v-for="year in yearRange" :key="year" :value="year">
                      {{ year }}
                    </option>
                  </select>
                </div>
              </div>
              <button class="btn btn-sm btn-outline-secondary" @click="nextMonth">
                <i class="fas fa-chevron-right"></i>
              </button>
            </div>
          </div>
          <div class="card-body">
            <div class="calendar-grid">
              <div class="calendar-header" v-for="day in ['SUN', 'MON', 'TUE', 'WED', 'THU', 'FRI', 'SAT']" :key="day">
                {{ day }}
              </div>
              <div 
                v-for="day in calendarDays" 
                :key="day.date" 
                class="calendar-day"
                :class="{ 
                  'other-month': !day.isCurrentMonth,
                  'today': day.isToday,
                  'has-appointments': day.appointmentCount > 0,
                  'holiday': day.isHoliday
                }"
                @click="selectDate(day)"
              >
                <div class="day-number">{{ day.day }}</div>
                <div v-if="day.appointmentCount > 0" class="appointment-badge">
                  {{ day.appointmentCount }}
                </div>
                <div v-if="getHolidaysForDate(day.date).length" class="holiday-label">
                  <div v-for="h in getHolidaysForDate(day.date)" :key="h.id" class="small">
                    <strong>{{ h.name }}</strong>
                    <span class="text-muted"> — {{ formatHolidayType(h.holiday_type) }}</span>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Search Panel -->
      <div v-if="activePanel === 'search'">
        <!-- Filter Tabs -->
        <div class="row mb-3">
          <div class="col-12">
            <ul class="nav nav-tabs">
              <li class="nav-item">
                <a class="nav-link" :class="{ active: filterTab === 'all' }" @click="filterTab = 'all'" href="javascript:void(0)">
                  All
                </a>
              </li>
              <li class="nav-item">
                <a class="nav-link" :class="{ active: filterTab === 'today' }" @click="filterTab = 'today'" href="javascript:void(0)">
                  Today
                </a>
              </li>
              <li class="nav-item">
                <a class="nav-link" :class="{ active: filterTab === 'upcoming' }" @click="filterTab = 'upcoming'" href="javascript:void(0)">
                  Upcoming (7 days)
                </a>
              </li>
            </ul>
          </div>
        </div>

        <div class="card">
          <div class="card-header">
            <div class="row">
              <div class="col-md-4">
                <input
                  type="text"
                  v-model="searchQuery"
                  class="form-control"
                  placeholder="Search by patient name..."
                />
              </div>
              <div class="col-md-3">
                <select v-model="statusFilter" class="form-control">
                  <option value="">All Status</option>
                  <option value="scheduled">Scheduled</option>
                  <option value="confirmed">Confirmed</option>
                  <option value="in_progress">In Progress</option>
                  <option value="completed">Completed</option>
                  <option value="requested">Requested</option>
                  <option value="cancelled">Cancel/Reject</option>
                  <option value="no_show">No Show</option>
                </select>
              </div>
              <div class="col-md-3">
                <input type="date" v-model="dateFilter" class="form-control" />
              </div>
              <div class="col-md-2">
                <button class="btn btn-secondary btn-block" @click="clearFilters">
                  <i class="fas fa-times"></i> Clear
                </button>
              </div>
            </div>
          </div>
          <div class="card-body">
            <div v-if="isLoading" class="text-center py-5">
              <i class="fas fa-spinner fa-spin fa-3x text-primary"></i>
              <p class="mt-3">Loading appointments...</p>
            </div>
            <div class="table-responsive appointments-table-wrapper" v-else>
              <table class="table table-bordered table-striped">
              <thead>
                <tr>
                  <th>Date</th>
                  <th>Time</th>
                  <th>Patient</th>
                  <th>Type</th>
                  <th>Dentist</th>
                  <th>Status</th>
                  <th>Actions</th>
                </tr>
              </thead>
              <tbody>
                <tr v-if="filteredAppointments.length === 0">
                  <td colspan="7" class="text-center">No appointments found</td>
                </tr>
                <tr v-for="appointment in filteredAppointments" :key="appointment.id" @click="viewAppointment(appointment)" style="cursor: pointer;">
                  <td>{{ formatDate(appointment.appointment_date) }}</td>
                  <td>{{ formatTime(appointment.appointment_time) }}</td>
                <td>{{ appointment.patient_name }}</td>
                <td>{{ formatAppointmentType(appointment.appointment_type) }}</td>
                <td>{{ cleanDentistName(appointment.dentist_name) || 'N/A' }}</td>
                <td>
                  <span :class="getStatusClass(appointment.status)">
                    {{ appointment.status === 'cancelled' ? 'Cancelled/Rejected' : formatStatus(appointment.status) }}
                  </span>
                </td>
                <td @click.stop>
                  <button class="btn btn-sm btn-info" @click="viewAppointment(appointment)" title="View">
                    <i class="fas fa-eye"></i>
                  </button>
                  <button class="btn btn-sm btn-warning" @click="editAppointment(appointment)" title="Edit">
                    <i class="fas fa-edit"></i>
                  </button>
                  <button class="btn btn-sm btn-danger" @click="deleteAppointment(appointment.id)" title="Delete">
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
            :total="totalAppointments"
            @page-change="handlePageChange"
          />
        </div>
      </div>
      </div>
    </div>
  </section>

  <!-- Add/Edit Modal -->
  <div class="modal fade" id="appointmentModal" tabindex="-1">
    <div class="modal-dialog modal-lg">
      <div class="modal-content">
          <div class="modal-header" style="background-color: #00B2A9; color: white;">
            <h5 class="modal-title">{{ acceptingRequest ? 'Request Validation' : (isEditing ? 'Edit Appointment' : 'Schedule Appointment') }}</h5>
          <button type="button" class="close" @click="closeModal" style="color: white;">
            <span>&times;</span>
          </button>
        </div>
        <div class="modal-body">
          <form @submit.prevent="saveAppointment">
            <div class="row">
              <div class="col-md-12">
                <!-- Schedule for selected date: placed above Date input -->
                <div v-if="form.appointment_date" class="alert alert-info mb-2" style="border: 1px solid #b6f0f7; background: #eaffff; padding: .5rem .75rem;">
                  <i class="fas fa-calendar-alt"></i>
                  <strong class="ml-2">Appointments on {{ formatDate(form.appointment_date) }}</strong>
                  <div v-if="appointments.filter(a => a.appointment_date === form.appointment_date).length === 0" class="mt-1 text-muted" style="font-size: .9rem;">
                    No appointments scheduled for this date.
                  </div>
                      <div v-else class="mt-1" style="font-size: .9rem;">
                    <ul class="list-unstyled mb-0">
                      <li v-for="appointment in appointmentsForFormDate" :key="appointment.id">
                        <span class="badge badge-info mr-2">{{ formatTime(appointment.appointment_time) }}</span>
                        <strong>{{ appointment.patient_name }}</strong> is assigned to <strong>{{ getDentistDisplayFromApt(appointment) }}</strong>&nbsp;
                        <span v-if="getBranchNameFromAppointment(appointment)" class="text-muted">({{ getBranchNameFromAppointment(appointment) }})</span>
                        - <span :class="getStatusClass(appointment.status)">{{ formatStatus(appointment.status) }}</span>
                      </li>
                    </ul>
                  </div>
                </div>
              </div>
            </div>
            <!-- Moved: timeWarning appears here, below the 'Appointments on' note -->
            <div v-if="timeWarning" class="alert alert-danger small mt-2">{{ timeWarning }}</div>
            <div class="row">
              <div class="col-md-6">
                <div class="form-group">
                  <label>Patient *</label>
                  <select v-model="form.patient" class="form-control" required>
                    <option value="" disabled>Select Patient</option>
                    <option v-for="patient in patients" :key="patient.id" :value="patient.id">
                      {{ patient.patient_id }} - {{ patient.full_name }}
                    </option>
                  </select>
                </div>
              </div>
              <div class="col-md-6">
                <div class="form-group">
                  <label>Assign Branch</label>
                  <select v-model="form.branch" class="form-control">
                    <option v-if="!acceptingRequest" value="">Any</option>
                    <option v-for="b in branches" :key="b.id" :value="b.id">{{ b.name || b.title || ('Branch ' + b.id) }}</option>
                  </select>
                </div>
              </div>
            </div>
            <div class="row">
              <div class="col-md-4">
                <div class="form-group">
                  <label>Assign Dentist</label>
                  <select v-model="form.dentist" class="form-control">
                    <option v-if="!acceptingRequest" value="">Any</option>
                    <option v-for="emp in dentists" :key="emp.id" :value="getEmployeeUserId(emp)">
                      {{ formatDentistDisplay(emp) }}
                    </option>
                  </select>
                </div>
              </div>
              <div class="col-md-3">
                <div class="form-group">
                  <label>Date *</label>
                    <input type="date" v-model="form.appointment_date" class="form-control" :min="minDate" required />
                </div>
              </div>
              <div class="col-md-3">
                <div class="form-group">
                  <label>Time *</label>
                  <input type="time" v-model="form.appointment_time" class="form-control" required :list="(form.branch && availableTimeSlots.length > 0) ? 'branchSlots' : null" />
                  <datalist v-if="form.branch && availableTimeSlots.length > 0" id="branchSlots">
                    <option v-for="t in availableTimeSlots" :key="t" :value="t">{{ t }}</option>
                  </datalist>
                </div>
              </div>
              <div class="col-md-2">
                <div class="form-group">
                  <label>Duration *</label>
                  <input type="number" v-model="form.duration" class="form-control" required min="15" step="15" style="min-width:5ch; max-width:6rem;" />
                  <small class="form-text text-muted"> &nbsp;&nbsp;&nbsp;In minutes.</small>
                </div>
              </div>
            </div>
            <div class="row">
              <div class="col-md-6">
                <div class="form-group">
                  <label>Appointment Type *</label>
                  <select v-model="form.appointment_type" class="form-control" required>
                    <option value="">Select Type</option>
                    <option value="checkup">Regular Checkup</option>
                    <option value="cleaning">Teeth Cleaning</option>
                    <option value="filling">Filling</option>
                    <option value="extraction">Tooth Extraction</option>
                    <option value="root_canal">Root Canal</option>
                    <option value="crown">Crown/Bridge</option>
                    <option value="orthodontics">Orthodontics</option>
                    <option value="cosmetic">Cosmetic Procedure</option>
                    <option value="emergency">Emergency</option>
                    <option value="consultation">Consultation</option>
                    <option value="other">Other</option>
                  </select>
                </div>
              </div>
              <div v-if="form.appointment_type === 'other'" class="col-md-6">
                <div class="form-group">
                  <label>Please Specify <span class="text-danger">*</span></label>
                  <input v-model="form.other_type" type="text" class="form-control" :required="form.appointment_type === 'other'" />
                </div>
              </div>
              <div class="col-md-6" v-if="!acceptingRequest">
                <div class="form-group">
                  <label>Status *</label>
                  <select v-model="form.status" class="form-control" required>
                    <option value="" disabled>Select status</option>
                    <option value="requested">Requested</option>
                    <option value="scheduled">Scheduled</option>
                    <option value="confirmed">Confirmed</option>
                    <option value="in_progress">In Progress</option>
                    <option value="completed">Completed</option>
                    <option value="cancelled">Cancel/Reject</option>
                    <option value="no_show">No Show</option>
                  </select>
                </div>
              </div>
              <div class="col-md-6" v-else>
                <div class="form-group">
                  <label>Status</label>
                  <div><span class="badge badge-info">Scheduled</span></div>
                </div>
              </div>
            </div>
            <div class="form-group">
              <label>Reason *</label>
              <textarea v-model="form.reason" class="form-control" rows="2" required></textarea>
            </div>
            <div class="form-group">
              <label>Notes</label>
              <textarea v-model="form.notes" class="form-control" rows="2"></textarea>
            </div>

            <div class="modal-footer">
              <button type="button" class="btn btn-secondary" @click="closeModal">Cancel</button>
              <button type="submit" class="btn btn-primary" :disabled="submitDisabled" style="background-color: #00B2A9; border-color: #00B2A9;">
                {{ acceptingRequest ? 'Accept Request' : (isEditing ? 'Update' : 'Schedule') }}
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
          <h5 class="modal-title">Appointment Details</h5>
          <button type="button" class="close" @click="closeViewModal" style="color: white;">
            <span>&times;</span>
          </button>
        </div>
        <div class="modal-body">
          <div class="row">
            <div class="col-md-6">
              <p><strong>Patient:</strong> {{ viewData.patient_name }}</p>
              <p><strong>Patient ID:</strong> {{ viewData.patient_id_display }}</p>
              <p><strong>Date:</strong> {{ formatDate(viewData.appointment_date) }}</p>
              <p><strong>Time:</strong> {{ formatTime(viewData.appointment_time) }}</p>
              <p><strong>Duration:</strong> {{ viewData.duration }} minutes</p>
            </div>
            <div class="col-md-6">
              <p><strong>Type:</strong> {{ formatAppointmentType(viewData.appointment_type) }}</p>
              <p><strong>Dentist:</strong> {{ cleanDentistName(viewData.dentist_name) || 'Not Assigned' }}</p>
              <p><strong>Status:</strong> <span :class="getStatusClass(viewData.status)">{{ formatStatus(viewData.status) }}</span></p>
              <p><strong>Created By:</strong> {{ viewData.created_by_name }}</p>
            </div>
          </div>
          <hr>
            <h6>Reason for Visit</h6>
            <p>{{ viewData.reason }}</p>
            <hr>
            <div v-if="viewData.reject_reason">
              <h6>Rejection Reason</h6>
              <div class="reject-reason-box">
                <pre class="mb-0">{{ viewData.reject_reason }}</pre>
              </div>
              <hr>
            </div>
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

  <!-- Date Appointments Modal -->
  <Transition name="modal-fade">
    <div v-if="showDateModal" class="modal fade show" id="dateAppointmentsModal" tabindex="-1" role="dialog" aria-labelledby="dateAppointmentsModalLabel" style="display: block;" @click.self="closeDateModal">
      <Transition name="modal-slide">
        <div class="modal-dialog modal-xl" role="document">
          <div class="modal-content">
            <div class="modal-header">
              <h5 class="modal-title" id="dateAppointmentsModalLabel">
                Appointments for {{ selectedDate ? formatDateShort(selectedDate) : '' }}
              </h5>
              <button type="button" class="close" @click="closeDateModal" aria-label="Close">
                <span aria-hidden="true">&times;</span>
              </button>
            </div>
            <div class="modal-body">
              <div v-if="selectedDateAppointments.length === 0" class="text-center py-5">
                <i class="fas fa-calendar-times fa-3x text-muted mb-3"></i>
                <p class="text-muted">No appointments scheduled for this date.</p>
              </div>
              <div v-else>
                <div class="list-group">
                  <div v-for="appointment in selectedDateAppointments" :key="appointment.id" class="list-group-item list-group-item-action d-flex justify-content-between align-items-start">
                    <div class="ms-2 me-auto">
                      <div class="fw-bold">
                        <span class="me-2">{{ formatTime(appointment.appointment_time) }}</span>
                        {{ appointment.patient_name }}
                      </div>
                      <div class="text-muted small">
                        {{ formatAppointmentType(appointment.appointment_type) }}
                        <span v-if="cleanDentistName(appointment.dentist_name)"> • {{ cleanDentistName(appointment.dentist_name) }}</span>
                        <span> • {{ appointment.duration }} min</span>
                        <span class="d-block mt-1">
                          <span :class="getStatusClass(appointment.status)">{{ formatStatus(appointment.status) }}</span>
                        </span>
                      </div>
                    </div>
                    <div class="btn-group btn-group-sm">
                      <button class="btn btn-info" @click="viewAppointment(appointment)" title="View"><i class="fas fa-eye"></i></button>
                      <button class="btn btn-warning" @click="editAppointment(appointment)" title="Edit"><i class="fas fa-edit"></i></button>
                      <button class="btn btn-danger" @click="deleteAppointment(appointment.id)" title="Delete"><i class="fas fa-trash"></i></button>
                    </div>
                  </div>
                </div>
              </div>
            </div>
            <div class="modal-footer">
              <button type="button" class="btn btn-secondary" @click="closeDateModal">Close</button>
            </div>
          </div>
        </div>
      </Transition>
    </div>
  </Transition>
  <Transition name="backdrop-fade">
    <div v-if="showDateModal" class="modal-backdrop"></div>
  </Transition>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import api from '../services/api'
import Swal from 'sweetalert2'
import TablePagination from '../components/TablePagination.vue'

const appointments = ref([])
const holidays = ref([])
const patients = ref([])
const users = ref([])
const employees = ref([])
const positions = ref([])
const branches = ref([])
const timeWarning = ref('')
const conflictWarning = ref('')
const conflictingAppointments = ref([])
const submitDisabled = ref(false)
const searchQuery = ref('')
const statusFilter = ref('')
const dateFilter = ref('')
const filterTab = ref('all')
const activePanel = ref('requests')
const isEditing = ref(false)
const isLoading = ref(true)
const acceptingRequest = ref(false)
const currentPage = ref(1)
const perPage = ref(10)
const showDateModal = ref(false)
const returnToDateModal = ref(false)
const returnToViewModal = ref(false)
const currentMonth = ref(new Date().getMonth())
const currentYear = ref(new Date().getFullYear())
const selectedDate = ref(null)
const monthNames = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
const yearRange = computed(() => {
  const currentYearVal = new Date().getFullYear()
  const years = []
  for (let i = currentYearVal - 5; i <= currentYearVal + 10; i++) {
    years.push(i)
  }
  return years
})

const form = ref({
  patient: '',
  dentist: '',
  branch: '',
  appointment_date: '',
  appointment_time: '',
  duration: 30,
  appointment_type: '',
  status: 'scheduled',
  reason: '',
  notes: ''
})

// Helper: resolve employee user id and formatting similar to patient view
const getEmployeeUserId = (emp) => {
  if (!emp) return null
  if (emp.user && typeof emp.user === 'object' && emp.user.id) return emp.user.id
  if (emp.user && (typeof emp.user === 'number' || typeof emp.user === 'string')) return emp.user
  if (emp.user_id) return emp.user_id
  return null
}

const formatDentistDisplay = (emp) => {
  if (!emp) return ''
  const title = emp.gender === 'F' ? 'Dra.' : 'Dr.'
  const first = emp.first_name || ''
  const last = emp.last_name || ''
  let middleInitial = ''
  if (emp.middle_name) {
    const m = emp.middle_name.toString().trim()
    if (m.length > 0) middleInitial = ` ${m.charAt(0).toUpperCase()}.`
  }
  const name = `${first}${middleInitial} ${last}`.replace(/\s+/g, ' ').trim()
  return `${title} ${name}`.trim()
}

// Clean raw dentist name strings coming from the API by removing any trailing " - <id>" or numeric suffixes
const cleanDentistName = (name) => {
  if (!name) return ''
  let s = String(name).trim()
  // remove common prefixes
  s = s.replace(/^\s*(Dr\.?|Dra\.?)/i, '').trim()
  // remove trailing ' - 123' or ' - abc' patterns
  s = s.replace(/\s*[-–—]\s*\w+\s*$/i, '').trim()
  // remove trailing parenthesized numbers e.g. 'Name (123)'
  s = s.replace(/\s*\(\s*\d+\s*\)\s*$/, '').trim()
  return s
}

const dentistPositionIds = computed(() => {
  return positions.value
    .filter(p => (p.title || p.name || (p.code || '')).toString().toLowerCase().includes('dentist'))
    .map(p => p.id)
})

const dentists = computed(() => {
  return employees.value.filter(emp => {
    if (!emp) return false

    // Determine position shape
    let isDentist = false
    const posCandidate = emp.position_id || (emp.position && emp.position.id) || emp.position || null
    if (posCandidate != null) {
      const asNumber = Number(posCandidate)
      if (!isNaN(asNumber)) {
        if (dentistPositionIds.value.includes(asNumber) || dentistPositionIds.value.includes(posCandidate)) {
          isDentist = true
        }
      }
    }
    if (!isDentist) {
      const titleText = (typeof posCandidate === 'string') ? posCandidate : (emp.position && (emp.position.title || emp.position.name)) || ''
      if (titleText && titleText.toString().toLowerCase().includes('dentist')) isDentist = true
    }
    if (!isDentist) return false

    // branch filter
    const preferredBranch = form.value.branch
    if (preferredBranch) {
      const empBranchRaw = emp.branch || (emp.branch_id || null)
      const empBranchId = empBranchRaw && typeof empBranchRaw === 'object' ? empBranchRaw.id : empBranchRaw
      if (!empBranchId) return false
      if (String(empBranchId) !== String(preferredBranch)) return false
    }

    return true
  })
})

const viewData = ref({})

const allFilteredAppointments = computed(() => {
  let filtered = appointments.value

  if (searchQuery.value) {
    const query = searchQuery.value.toLowerCase()
    filtered = filtered.filter(a =>
      a.patient_name.toLowerCase().includes(query)
    )
  }

  if (statusFilter.value) {
    filtered = filtered.filter(a => a.status === statusFilter.value)
  }

  if (dateFilter.value) {
    const desired = String(dateFilter.value)
    filtered = filtered.filter(a => {
      if (!a || !a.appointment_date) return false
      // normalize appointment_date to YYYY-MM-DD when possible
      try {
        const raw = String(a.appointment_date)
        const normalized = raw.split('T')[0]
        return normalized === desired
      } catch (e) {
        return String(a.appointment_date) === desired
      }
    })
  }

  return filtered
})

const totalAppointments = computed(() => allFilteredAppointments.value.length)

const filteredAppointments = computed(() => {
  const start = (currentPage.value - 1) * perPage.value
  const end = start + perPage.value
  return allFilteredAppointments.value.slice(start, end)
})

const handlePageChange = (page) => {
  currentPage.value = page
}

// Calendar computed properties
const currentMonthYear = computed(() => {
  const date = new Date(currentYear.value, currentMonth.value)
  return date.toLocaleDateString('en-US', { month: 'long', year: 'numeric' })
})

const calendarDays = computed(() => {
  const firstDay = new Date(currentYear.value, currentMonth.value, 1)
  const lastDay = new Date(currentYear.value, currentMonth.value + 1, 0)
  const prevLastDay = new Date(currentYear.value, currentMonth.value, 0)
  
  const firstDayOfWeek = firstDay.getDay()
  const lastDate = lastDay.getDate()
  const prevLastDate = prevLastDay.getDate()
  
  const days = []
  const today = new Date()
  today.setHours(0, 0, 0, 0)
  
  // Previous month days
  for (let i = firstDayOfWeek - 1; i >= 0; i--) {
    const day = prevLastDate - i
    const date = new Date(currentYear.value, currentMonth.value - 1, day)
    days.push({
      day,
      date: formatDateForCalendar(date),
      isCurrentMonth: false,
      isToday: false,
      appointmentCount: getAppointmentCountForDate(formatDateForCalendar(date))
    })
  }
  
  // Current month days
  for (let day = 1; day <= lastDate; day++) {
    const date = new Date(currentYear.value, currentMonth.value, day)
    const dateStr = formatDateForCalendar(date)
    const isToday = date.getTime() === today.getTime()
    
    days.push({
      day,
      date: dateStr,
      isCurrentMonth: true,
      isHoliday: isHolidayDate(dateStr),
      isToday,
      appointmentCount: getAppointmentCountForDate(dateStr)
    })
  }
  
  // Next month days to fill the grid
  const remainingDays = 42 - days.length
  for (let day = 1; day <= remainingDays; day++) {
    const date = new Date(currentYear.value, currentMonth.value + 1, day)
    days.push({
      day,
      date: formatDateForCalendar(date),
      isCurrentMonth: false,
      isToday: false,
      isHoliday: isHolidayDate(formatDateForCalendar(date)),
      appointmentCount: getAppointmentCountForDate(formatDateForCalendar(date))
    })
  }
  
  return days
})

// Holidays handling
const fetchHolidays = async () => {
  try {
    const resp = await api.get('/website/holidays/')
    holidays.value = resp.data || []
  } catch (err) {
    console.error('Failed to load holidays', err)
    holidays.value = []
  }
}

const isHolidayDate = (dateStr) => {
  if (!holidays.value || holidays.value.length === 0) return false
  // dateStr is YYYY-MM-DD
  const year = String(dateStr).slice(0,4)
  for (const h of holidays.value) {
    if (!h) continue
    if (h.specific_date && String(h.specific_date).startsWith(year)) {
      if (String(h.specific_date).split('T')[0] === dateStr) return true
    }
    if (h.computed_date && String(h.computed_date).startsWith(year)) {
      if (String(h.computed_date).split('T')[0] === dateStr) return true
    }
    if (h.is_recurring && h.month && h.day) {
      const m = String(h.month).padStart(2,'0')
      const d = String(h.day).padStart(2,'0')
      if (`${year}-${m}-${d}` === dateStr) return true
    }
  }
  return false
}

const getHolidaysForDate = (dateStr) => {
  if (!holidays.value || holidays.value.length === 0) return []
  const year = String(dateStr).slice(0,4)
  const out = []
  for (const h of holidays.value) {
    if (!h) continue
    if (h.specific_date && String(h.specific_date).split('T')[0] === dateStr) {
      out.push(h); continue
    }
    if (h.computed_date && String(h.computed_date).split('T')[0] === dateStr) {
      out.push(h); continue
    }
    if (h.is_recurring && h.month && h.day) {
      const m = String(h.month).padStart(2,'0')
      const d = String(h.day).padStart(2,'0')
      if (`${year}-${m}-${d}` === dateStr) out.push(h)
    }
  }
  return out
}

const formatHolidayType = (t) => {
  if (!t) return 'Unknown'
  if (t === 'regular') return 'Regular Holiday'
  if (t === 'special_non_working') return 'Special (Non-Working)'
  if (t === 'special_working') return 'Special (Working)'
  return t
}

const selectedDateAppointments = computed(() => {
  if (!selectedDate.value) return []
  return appointments.value.filter(a => a.appointment_date === selectedDate.value)
})

// Calendar methods
const formatDateForCalendar = (date) => {
  const year = date.getFullYear()
  const month = String(date.getMonth() + 1).padStart(2, '0')
  const day = String(date.getDate()).padStart(2, '0')
  return `${year}-${month}-${day}`
}

const getAppointmentCountForDate = (date) => {
  return appointments.value.filter(a => a.appointment_date === date).length
}

const previousMonth = () => {
  if (currentMonth.value === 0) {
    currentMonth.value = 11
    currentYear.value--
  } else {
    currentMonth.value--
  }
}

const nextMonth = () => {
  if (currentMonth.value === 11) {
    currentMonth.value = 0
    currentYear.value++
  } else {
    currentMonth.value++
  }
}

const selectDate = (day) => {
  if (day.appointmentCount > 0 || day.isCurrentMonth) {
    selectedDate.value = day.date
    openDateModal()
  }
}

const openDateModal = () => {
  // Close view modal if it's open
  const viewModal = document.getElementById('viewModal')
  if (viewModal && viewModal.classList.contains('show')) {
    closeViewModal()
  }
  
  showDateModal.value = true
  document.body.classList.add('modal-open')
}

const closeDateModal = () => {
  showDateModal.value = false
  document.body.classList.remove('modal-open')
}

const changeMonth = () => {
  selectedDate.value = null
}

const changeYear = () => {
  selectedDate.value = null
}

// Reset to page 1 when filters change
watch([searchQuery, statusFilter, dateFilter, filterTab], () => {
  currentPage.value = 1
})

const fetchAppointments = async () => {
  try {
    isLoading.value = true
    // Default: load all appointments
    let endpoint = '/patient/appointments/'
    let response = null

    if (filterTab.value === 'today') {
      // Use client local date to request appointments for "today" explicitly
      const d = new Date()
      const localDate = `${d.getFullYear()}-${String(d.getMonth() + 1).padStart(2, '0')}-${String(d.getDate()).padStart(2, '0')}`
      response = await api.get(endpoint + 'today/', { params: { date_from: localDate, date_to: localDate } })
    } else if (filterTab.value === 'upcoming') {
      // Use dedicated upcoming endpoint when requested
      const d = new Date()
      const localDate = `${d.getFullYear()}-${String(d.getMonth() + 1).padStart(2, '0')}-${String(d.getDate()).padStart(2, '0')}`
      response = await api.get(endpoint + 'upcoming/', { params: { date_from: localDate, date_to: localDate } })
      // response = await api.get('/patient/appointments/upcoming/')
    } else {
      response = await api.get(endpoint)
    }

    appointments.value = response.data
  } catch (error) {
    console.error('Error fetching appointments:', error)
    Swal.fire('Error', 'Failed to fetch appointments', 'error')
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

const fetchEmployees = async () => {
  try {
    const resp = await api.get('/employees/')
    employees.value = resp.data
  } catch (err) {
    console.error('Error fetching employees:', err)
    employees.value = []
  }
}

const loadPositions = async () => {
  try {
    const response = await api.get('/positions/')
    positions.value = response.data
  } catch (err) {
    console.error('Error loading positions:', err)
    positions.value = []
  }
}

const loadBranches = async () => {
  try {
    const resp = await api.get('/branches/')
    branches.value = resp.data
  } catch (err) {
    console.error('Error loading branches:', err)
    branches.value = []
  }
}

const parseTimeToMinutes = (t) => {
  if (!t) return null
  let s = String(t).trim()
  // remove AM/PM if present
  s = s.replace(/\s*(am|pm)\.?$/i, '')
  // if contains space-separated AM/PM like '9:00 am'
  s = s.replace(/\s+(am|pm)\.?$/i, '')
  const parts = s.split(':')
  if (parts.length < 2) return null
  const h = parseInt(parts[0].replace(/^0+/, '') || '0', 10)
  const m = parseInt(parts[1].replace(/[^0-9].*$/, ''), 10)
  if (isNaN(h) || isNaN(m)) return null
  return h * 60 + m
}

const minDate = computed(() => {
  const tomorrow = new Date()
  tomorrow.setDate(tomorrow.getDate() + 1)
  return tomorrow.toISOString().split('T')[0]
})

const intervalsOverlap = (startA, durA, startB, durB) => {
  const a0 = startA
  const a1 = startA + (durA || 0)
  const b0 = startB
  const b1 = startB + (durB || 0)
  return (a0 < b1) && (b0 < a1)
}

// Check if a given HH:MM time string fits within branch hours for selected branch/date
const isTimeWithinBranchHours = (timeStr) => {
  if (!timeStr) return false
  const branchId = form.value.branch
  const dateStr = form.value.appointment_date
  if (!branchId || !dateStr) return true // no branch/date selected => allow any
  const branch = branches.value.find(b => String(b.id) === String(branchId))
  if (!branch) return true
  const hours = getBranchHoursForDate(branch, dateStr)
  if (!hours || hours.closed) return false
  const startM = parseTimeToMinutes(timeStr.toString().slice(0,5))
  if (startM === null) return false
  const duration = Number(form.value.duration) || 30
  // start must be >= open and end <= close
  return (startM >= hours.openM) && ((startM + duration) <= hours.closeM)
}

// Compute available time slots within branch hours for selected date and duration
const availableTimeSlots = computed(() => {
  const branchId = form.value.branch
  const dateStr = form.value.appointment_date
  const duration = Number(form.value.duration) || 30
  const interval = 15 // slot step in minutes
  if (!branchId || !dateStr) return []
  const branch = branches.value.find(b => String(b.id) === String(branchId))
  if (!branch) return []
  const hours = getBranchHoursForDate(branch, dateStr)
  if (!hours || hours.closed) return []
  const slots = []
  const start = hours.openM
  const end = hours.closeM
  const lastStart = end - duration
  for (let t = start; t <= lastStart; t += interval) {
    const hh = Math.floor(t / 60).toString().padStart(2, '0')
    const mm = (t % 60).toString().padStart(2, '0')
    slots.push(`${hh}:${mm}`)
  }
  // ensure slots are sorted earliest -> latest (by minutes) and unique
  const unique = Array.from(new Set(slots))
  unique.sort((a, b) => {
    const ma = parseTimeToMinutes(a)
    const mb = parseTimeToMinutes(b)
    return (ma === null ? 0 : ma) - (mb === null ? 0 : mb)
  })
  return unique
})

const appointmentsForFormDate = computed(() => {
  const date = form.value.appointment_date
  if (!date) return []
  const list = (appointments.value || []).filter(a => a.appointment_date === date && a.status === 'scheduled')
  return list.slice().sort((a, b) => {
    const ta = parseTimeToMinutes(a.appointment_time) || 0
    const tb = parseTimeToMinutes(b.appointment_time) || 0
    return ta - tb
  })
})

const requestedAppointments = computed(() => {
  return (appointments.value || []).filter(a => a && String(a.status).toLowerCase() === 'requested')
})

const totalRequested = computed(() => requestedAppointments.value.length)

const requestedPageItems = computed(() => {
  const start = (currentPage.value - 1) * perPage.value
  const end = start + perPage.value
  return requestedAppointments.value.slice(start, end)
})

const getBranchHoursForDate = (branchObj, dateString) => {
  if (!branchObj || !dateString) return null
  const d = new Date(dateString + 'T00:00:00')
  if (isNaN(d)) return null
  const day = d.getDay()
  const map = ['sunday','monday','tuesday','wednesday','thursday','friday','saturday']
  const prefix = map[day]
  const closedFlag = branchObj[`${prefix}_closed`]
  if (closedFlag) return { closed: true }
  const openRaw = branchObj[`${prefix}_open`] || branchObj[`${prefix}_open_time`] || null
  const closeRaw = branchObj[`${prefix}_close`] || branchObj[`${prefix}_close_time`] || null
  // If branch has no explicit hours defined for this day, default to 09:00 - 19:00
  if (!openRaw || !closeRaw) {
    const defaultOpen = 9 * 60 // 09:00
    const defaultClose = 19 * 60 // 19:00 (7:00 PM)
    return { closed: false, openM: defaultOpen, closeM: defaultClose }
  }
  const openM = parseTimeToMinutes(openRaw.toString().slice(0,5))
  const closeM = parseTimeToMinutes(closeRaw.toString().slice(0,5))
  if (openM === null || closeM === null) {
    // fallback to defaults if parsing fails
    return { closed: false, openM: 9 * 60, closeM: 19 * 60 }
  }
  return { closed: false, openM, closeM }
}

const minutesToHHMM = (mins) => {
  if (typeof mins !== 'number') return ''
  const hh = Math.floor(mins / 60).toString().padStart(2, '0')
  const mm = (mins % 60).toString().padStart(2, '0')
  return `${hh}:${mm}`
}

// Centralized schedule validation used by multiple watchers
const validateSchedule = () => {
  timeWarning.value = ''
  conflictWarning.value = ''
  conflictingAppointments.value = []
  submitDisabled.value = false

  // If status is 'scheduled', an assigned dentist is required
  if (form.value.status === 'scheduled') {
    if (!form.value.dentist) {
      timeWarning.value = 'Scheduled appointments require an assigned dentist.'
      submitDisabled.value = true
      return
    }
  }

  // If branch/date/time are present, verify branch operating hours
  if (form.value.branch && form.value.appointment_date && form.value.appointment_time) {
    const branch = branches.value.find(b => String(b.id) === String(form.value.branch))
    const hours = branch ? getBranchHoursForDate(branch, form.value.appointment_date) : null
    if (!hours || hours.closed) {
      timeWarning.value = 'Selected branch is closed on the chosen date.'
      submitDisabled.value = true
      return
    }
    const startM = parseTimeToMinutes(form.value.appointment_time)
    const dur = Number(form.value.duration) || 30
    if (startM === null || startM < hours.openM || (startM + dur) > hours.closeM) {
      timeWarning.value = `Selected time is outside operating hours (${formatTime(minutesToHHMM(hours.openM))} - ${formatTime(minutesToHHMM(hours.closeM))}).`
      submitDisabled.value = true
      return
    }
  }

  // If dentist selected, check assignment and conflicts
  if (form.value.dentist && form.value.appointment_date && form.value.appointment_time) {
    // Ensure dentist assigned to branch if branch selected
    if (form.value.branch) {
      const emp = employees.value.find(e => {
        if (!e) return false
        const uid = (e.user && (e.user.id || e.user)) || e.user_id || null
        return uid && String(uid) === String(form.value.dentist)
      })
      if (emp) {
        const empBranchRaw = emp.branch || (emp.branch_id || null)
        const empBranchId = empBranchRaw && typeof empBranchRaw === 'object' ? empBranchRaw.id : empBranchRaw
        if (empBranchId && String(empBranchId) !== String(form.value.branch)) {
          timeWarning.value = 'Selected dentist is not assigned to the chosen branch.'
          submitDisabled.value = true
          return
        }
      }
    }

    // Conflict detection
    const start = parseTimeToMinutes(form.value.appointment_time)
    const dur = Number(form.value.duration) || 30
    const conflicts = appointments.value.filter(a => {
      if (!a) return false
      if (a.appointment_date !== form.value.appointment_date) return false
      if (a.status === 'cancelled' || a.status === 'no_show') return false
      if (form.value.branch && a.branch && String(a.branch) !== String(form.value.branch)) return false
      if (!a.dentist) return false
      if (String(a.dentist) !== String(form.value.dentist)) return false
      if (isEditing.value && String(a.id) === String(form.value.id)) return false
      const aStart = parseTimeToMinutes(a.appointment_time)
      const aDur = Number(a.duration) || 30
      if (aStart === null) return false
      return intervalsOverlap(start, dur, aStart, aDur)
    })
    if (conflicts.length > 0) {
      conflictingAppointments.value = conflicts
      const first = conflicts[0]
      const firstStart = parseTimeToMinutes(first.appointment_time)
      const firstDur = Number(first.duration) || 30
      const firstEndHHMM = minutesToHHMM(firstStart + firstDur)
      timeWarning.value = `Schedule conflict: Selected dentist has an appointment at ${formatTime(first.appointment_time)} - ${formatTime(firstEndHHMM)}.`
      submitDisabled.value = true
      return
    }
  }
}

const openAddModal = () => {
  isEditing.value = false
  acceptingRequest.value = false
  // Reset to tomorrow default like patient UI
  const tomorrow = new Date()
  tomorrow.setDate(tomorrow.getDate() + 1)
    form.value = {
    patient: '',
    dentist: '',
    branch: '',
    appointment_date: tomorrow.toISOString().split('T')[0],
    appointment_time: '09:00',
    duration: 30,
    appointment_type: '',
    status: '',
    reason: '',
    notes: ''
  }
  conflictWarning.value = ''
  conflictingAppointments.value = []
  // start with the Schedule button enabled by default (original behavior)
  submitDisabled.value = false
  showModal()
  // Run initial validation when the modal opens
  validateSchedule()
}

const editAppointment = (appointment) => {
  // Close date modal if it's open
  if (showDateModal.value) {
    closeDateModal()
    returnToDateModal.value = true
  }
  
  isEditing.value = true
  form.value = { ...appointment }
  // Ensure duration has a sensible default (30 minutes) when opening the edit modal
  try {
    form.value.duration = Number(form.value.duration) || 30
  } catch (e) {
    form.value.duration = 30
  }
  // If branch is not set, try to infer it from the assigned dentist's employee record
  try {
    const rawDentist = form.value.dentist || form.value.dentist_id || null
    const dentistId = (rawDentist && typeof rawDentist === 'object') ? (rawDentist.id || null) : rawDentist
    if (dentistId && (!form.value.branch || String(form.value.branch).trim() === '')) {
      // Prefer resolving via users -> employee relationship
      let emp = null
      const userMatch = Array.isArray(users.value) ? users.value.find(u => u && (String(u.id) === String(dentistId) || String(u.user_id || '') === String(dentistId))) : null
      if (userMatch) {
        const empRef = userMatch.employee || userMatch.employee_id || (userMatch.employee && (userMatch.employee.id || userMatch.employee_id)) || null
        const empId = (empRef && typeof empRef === 'object') ? (empRef.id || empRef.employee_id || null) : empRef
        if (empId) {
          emp = employees.value.find(e => e && (String(e.id) === String(empId) || String(e.employee_id || '') === String(empId)))
        }
        // fallback: find employee by linked user field
        if (!emp) {
          emp = employees.value.find(e => {
            if (!e) return false
            const eUser = (e.user && (e.user.id || e.user)) || e.user_id || null
            return eUser && String(eUser) === String(userMatch.id)
          })
        }
      }
      // fallback: find employee directly by matching dentistId to employee.user or employee.id
      if (!emp) {
        emp = employees.value.find(e => {
          if (!e) return false
          const eUser = (e.user && (e.user.id || e.user)) || e.user_id || null
          if (eUser && String(eUser) === String(dentistId)) return true
          if (e.id && String(e.id) === String(dentistId)) return true
          return false
        })
      }
      if (emp) {
        const empBranchRaw = emp.branch || emp.branch_id || null
        const empBranchId = empBranchRaw && typeof empBranchRaw === 'object' ? empBranchRaw.id : empBranchRaw
        if (empBranchId) form.value.branch = empBranchId
      }
    }
  } catch (err) {
    console.error('Error inferring branch from dentist for edit modal:', err)
  }
  showModal()
  // If this modal was opened from the Accept button, run validation immediately
  if (acceptingRequest.value) {
    // run validation to surface branch-hours/conflict warnings right away
    validateSchedule()
  }
}

const editFromView = () => {
  // Save the date modal return state before clearing
  const shouldReturnToDate = returnToDateModal.value
  returnToDateModal.value = false
  returnToViewModal.value = true
  closeViewModal()
  isEditing.value = true
  form.value = { ...viewData.value }
  // Restore the flag so view modal knows to return to date modal
  returnToDateModal.value = shouldReturnToDate
  showModal()
  // validate when opening the modal from view to surface issues immediately
  // validateSchedule()
}

const viewAppointment = (appointment) => {
  // Close date modal if it's open
  if (showDateModal.value) {
    closeDateModal()
    returnToDateModal.value = true
  }
  
  viewData.value = { ...appointment }
  showViewModal()
}

const saveAppointment = async () => {
  try {
    // Validate time against branch hours if branch selected
    timeWarning.value = ''
    if (form.value.branch && form.value.appointment_date && form.value.appointment_time) {
      const branch = branches.value.find(b => String(b.id) === String(form.value.branch))
      const hours = branch ? getBranchHoursForDate(branch, form.value.appointment_date) : null
      if (!hours || hours.closed) {
        timeWarning.value = 'Selected branch is closed on the chosen date.'
        Swal.fire({ icon: 'error', title: 'Invalid Time', text: timeWarning.value })
        return
      }
      const startM = parseTimeToMinutes(form.value.appointment_time)
      const dur = Number(form.value.duration) || 30
      if (startM === null || startM < hours.openM || (startM + dur) > hours.closeM) {
        timeWarning.value = `Selected time is outside operating hours (${formatTime(minutesToHHMM(hours.openM))} - ${formatTime(minutesToHHMM(hours.closeM))}).`
        Swal.fire({ icon: 'error', title: 'Invalid Time', text: timeWarning.value })
        return
      }
    }

    // Conflict check: same dentist, overlapping time on same date
    if (form.value.dentist) {
      // Ensure selected dentist works at the selected branch (if branch selected)
      if (form.value.branch) {
        const emp = employees.value.find(e => {
          if (!e) return false
          const uid = (e.user && (e.user.id || e.user)) || e.user_id || null
          return uid && String(uid) === String(form.value.dentist)
        })
        if (emp) {
          const empBranchRaw = emp.branch || (emp.branch_id || null)
          const empBranchId = empBranchRaw && typeof empBranchRaw === 'object' ? empBranchRaw.id : empBranchRaw
          if (empBranchId && String(empBranchId) !== String(form.value.branch)) {
            Swal.fire({ icon: 'error', title: 'Invalid Dentist', text: 'Selected dentist is not assigned to the chosen branch.' })
            return
          }
        }
      }
      const start = parseTimeToMinutes(form.value.appointment_time)
      const dur = Number(form.value.duration) || 30
      const conflicts = appointments.value.filter(a => {
        if (!a) return false
        if (a.appointment_date !== form.value.appointment_date) return false
        if (a.status === 'cancelled' || a.status === 'no_show') return false
        // If branch set, only consider same branch appointments (if appointment has branch)
        if (form.value.branch && a.branch && String(a.branch) !== String(form.value.branch)) return false
        if (!a.dentist) return false
        if (String(a.dentist) !== String(form.value.dentist)) return false
        // allow editing the same appointment
        if (isEditing.value && String(a.id) === String(form.value.id)) return false
        const aStart = parseTimeToMinutes(a.appointment_time)
        const aDur = Number(a.duration) || 30
        if (aStart === null) return false
        return intervalsOverlap(start, dur, aStart, aDur)
      })
      if (conflicts.length > 0) {
        const first = conflicts[0]
        Swal.fire({ icon: 'warning', title: 'Schedule Conflict', text: `Selected dentist has a conflicting appointment at ${formatTime(first.appointment_time)}.` })
        return
      }
    }

    // include branch in payload
    const payload = { ...form.value }
    if (!payload.branch) payload.branch = null

    // If appointment_type is 'other', include the specified type in notes similar to patient flow
    let appointmentNotes = payload.notes || ''
    if (payload.appointment_type === 'other' && payload.other_type) {
      appointmentNotes = `Appointment Type: ${payload.other_type}\n\n${appointmentNotes}`
      payload.notes = appointmentNotes
    }

    if (isEditing.value) {
      await api.put(`/patient/appointments/${form.value.id}/`, payload)
      Swal.fire({ toast: true, position: 'top-end', icon: 'success', title: 'Appointment updated successfully', showConfirmButton: false, timer: 2000 })
    } else {
      await api.post('/patient/appointments/', payload)
      Swal.fire({ toast: true, position: 'top-end', icon: 'success', title: 'Appointment scheduled successfully', showConfirmButton: false, timer: 2000 })
    }

    await fetchAppointments()
    closeModal()
  } catch (error) {
    console.error('Error saving appointment:', error)
    Swal.fire('Error', 'Failed to save appointment', 'error')
  }
}

const deleteAppointment = async (id) => {
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
      await api.delete(`/patient/appointments/${id}/`)
      await fetchAppointments()
      Swal.fire('Deleted!', 'Appointment has been deleted.', 'success')
    } catch (error) {
      console.error('Error deleting appointment:', error)
      Swal.fire('Error', 'Failed to delete appointment', 'error')
    }
  }
}

const acceptAppointment = async (apt) => {
  // Instead of auto-accepting, open the edit modal pre-filled so admin can
  // assign branch, dentist, adjust time and duration (default 30) before saving.
  if (!apt || !apt.id) return
  try {
    // Prepare appointment object for editing: ensure duration and status defaults
    const toEdit = { ...apt }
    toEdit.duration = Number(toEdit.duration) || 30
    // Pre-select scheduled status so admin knows they are accepting the request
    toEdit.status = 'scheduled'
    // mark that we're opening the modal to accept a request so UI labels update
    acceptingRequest.value = true
    editAppointment(toEdit)
  } catch (err) {
    console.error('Error opening edit modal for acceptance:', err)
    Swal.fire('Error', 'Failed to open appointment for editing', 'error')
  }
}

const denyAppointment = async (id) => {
  // Prompt admin to provide a reason for denial before cancelling
  const result = await Swal.fire({
    title: 'Deny request',
    input: 'textarea',
    inputLabel: 'Reason for denial',
    inputPlaceholder: 'Enter the reason for denying this request...',
    inputAttributes: {
      'aria-label': 'Reason for denial',
      maxlength: 1000
    },
    showCancelButton: true,
    confirmButtonText: 'Deny request',
    cancelButtonText: 'Cancel',
    preConfirm: (value) => {
      if (!value || !String(value).trim()) {
        Swal.showValidationMessage('Please provide a reason for denying the request')
      }
      return value
    }
  })

  if (!result || !result.isConfirmed) return
  const reason = result.value || ''

  try {
    // find appointment to preserve previous notes if present
    const apt = appointments.value.find(a => String(a.id) === String(id))
    let combinedNotes = `Denied: ${reason}`
    if (apt && apt.notes) {
      combinedNotes = `Denied: ${reason}\n\nPrevious notes:\n${apt.notes}`
    }

    // mark as cancelled and include the denial reason in notes and a dedicated field
    // Use PATCH (partial update) so the backend won't require all fields on update
    const payload = { status: 'cancelled', reject_reason: reason, notes: combinedNotes }
    try {
      await api.patch(`/patient/appointments/${id}/`, payload)
    } catch (patchErr) {
      // If server rejects unknown field (400), retry without reject_reason using PATCH
      if (patchErr.response && patchErr.response.status === 400) {
        const serverData = patchErr.response.data || {}
        console.warn('Server validation failed when sending reject_reason:', serverData)
        const fallback = { status: 'cancelled', notes: combinedNotes }
        try {
          await api.patch(`/patient/appointments/${id}/`, fallback)
        } catch (fallbackErr) {
          console.error('Fallback deny failed:', fallbackErr)
          const msg = (fallbackErr.response && fallbackErr.response.data) ? JSON.stringify(fallbackErr.response.data) : 'Failed to deny request'
          Swal.fire('Error', msg, 'error')
          return
        }
      } else {
        throw patchErr
      }
    }

    await fetchAppointments()
    Swal.fire({ toast: true, position: 'top-end', icon: 'success', title: 'Request denied', showConfirmButton: false, timer: 1500 })
  } catch (err) {
    console.error('Error denying appointment:', err)
    // If server returned validation details, show them
    if (err.response && err.response.data) {
      const detail = err.response.data.detail || err.response.data
      Swal.fire('Error', JSON.stringify(detail), 'error')
    } else {
      Swal.fire('Error', 'Failed to deny request', 'error')
    }
  }
}

// Load appointments for a specific date (used to show schedule in modal and check conflicts)
const dateAppointments = ref([])
const loadDateAppointments = async () => {
  if (!form.value.appointment_date) {
    dateAppointments.value = []
    return
  }
  try {
    const response = await api.get('/patient/appointments/', {
      params: { appointment_date: form.value.appointment_date }
    })
    dateAppointments.value = response.data.filter(apt => apt.appointment_date === form.value.appointment_date && apt.status === 'scheduled')
      .sort((a, b) => a.appointment_time.localeCompare(b.appointment_time))
  } catch (err) {
    console.error('Error loading date appointments:', err)
    dateAppointments.value = []
  }
}

// Allow clicking an appointment in date list to select its dentist
const selectDentistFromApt = (apt) => {
  if (!apt) return
  const raw = apt.dentist || apt.dentist_id || (apt.dentist && apt.dentist.id) || null
  const dentistUserId = (raw && typeof raw === 'object') ? raw.id : raw
  if (dentistUserId) {
    form.value.dentist = dentistUserId
    // run the validation watcher logic by touching the time
    // watchers will automatically validate
  }
}

// Watch date changes to reload appointments
watch(() => form.value.appointment_date, async () => {
  await loadDateAppointments()
  validateSchedule()
})

const clearFilters = () => {
  searchQuery.value = ''
  statusFilter.value = ''
  dateFilter.value = ''
}

const resetForm = () => {
  const today = new Date().toISOString().split('T')[0]
  form.value = {
    patient: '',
    dentist: '',
    branch: '',
    appointment_date: today,
    appointment_time: '09:00',
    duration: 30,
    appointment_type: '',
    status: 'scheduled',
    reason: '',
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

// Short month format for compact titles (e.g., "Dec. 13, 2025") — ensure a trailing period
const formatDateShort = (date) => {
  if (!date) return ''
  const d = new Date(date)
  const rawMonth = d.toLocaleDateString('en-US', { month: 'short' })
  const month = rawMonth.endsWith('.') ? rawMonth : `${rawMonth}.`
  const day = d.getDate()
  const year = d.getFullYear()
  return `${month} ${day}, ${year}`
}

const formatTime = (time) => {
  if (!time) return ''
  // Use 'numeric' for hour to avoid leading zero (e.g., '9:00 AM' instead of '09:00 AM')
  return new Date(`2000-01-01T${time}`).toLocaleTimeString('en-US', { 
    hour: 'numeric', 
    minute: '2-digit' 
  })
}

const formatAppointmentType = (type) => {
  if (!type) return 'N/A'
  const types = {
    checkup: 'Regular Checkup',
    cleaning: 'Teeth Cleaning',
    filling: 'Filling',
    extraction: 'Tooth Extraction',
    root_canal: 'Root Canal',
    crown: 'Crown/Bridge',
    orthodontics: 'Orthodontics',
    cosmetic: 'Cosmetic Procedure',
    emergency: 'Emergency',
    consultation: 'Consultation',
    other: 'Other'
  }
  return types[type] || type
}

const formatStatus = (status) => {
  if (!status) return 'N/A'
  return status.replace('_', ' ').replace(/\b\w/g, l => l.toUpperCase())
}

const getBranchName = (branchRef) => {
  if (!branchRef) return ''
  const id = (branchRef && typeof branchRef === 'object') ? branchRef.id : branchRef
  const b = branches.value.find(x => String(x.id) === String(id))
  if (b) return b.name || b.title || (`Branch ${b.id}`)
  return id ? (`Branch ${id}`) : ''
}

const getDentistDisplayFromApt = (apt) => {
  if (!apt) return 'Not Assigned'
  // Prefer explicit dentist id if present
  const rawId = apt.dentist || apt.dentist_id || (apt.dentist && apt.dentist.id) || null
  const id = (rawId && typeof rawId === 'object') ? rawId.id : rawId
  if (id) {
    // First, treat id as a User PK: find the user and get their linked employee id
    const userMatch = (Array.isArray(users.value) ? users.value.find(u => {
      if (!u) return false
      return String(u.id) === String(id) || String(u.user_id || '') === String(id)
    }) : null)
    if (userMatch) {
      // Try common shapes for employee reference on the user object
      const empRef = userMatch.employee || userMatch.employee_id || (userMatch.employee && (userMatch.employee.id || userMatch.employee_id)) || null
      const empId = (empRef && typeof empRef === 'object') ? (empRef.id || empRef.employee_id || null) : empRef
      if (empId) {
        const empByEmpId = employees.value.find(e => e && (String(e.id) === String(empId) || String(e.employee_id || '') === String(empId)))
        if (empByEmpId) return formatDentistDisplay(empByEmpId)
      }
      // If user has no explicit employee id, try matching employee by linked user field
      const empByUser = employees.value.find(e => {
        if (!e) return false
        const eUser = (e.user && (e.user.id || e.user)) || e.user_id || null
        return eUser && String(eUser) === String(userMatch.id)
      })
      if (empByUser) return formatDentistDisplay(empByUser)
    }

    // Fallback: previously some appointments used dentist id that directly referenced employee PKs
    const empById = employees.value.find(e => {
      if (!e) return false
      const uid = (e.user && (e.user.id || e.user)) || e.user_id || null
      if (uid && String(uid) === String(id)) return true
      if (e.id && String(e.id) === String(id)) return true
      return false
    })
    if (empById) return formatDentistDisplay(empById)
  }

  if (apt.dentist_name) {
    // Fallback: try to match by name but use stricter rules (last name + first initial)
    let name = String(apt.dentist_name)
    name = name.replace(/^\s*(Dr\.?|Dra\.?)\s+/i, '')
    name = name.replace(/\s*[-–—]\s*\d+$/, '').replace(/\s*\(\s*\d+\s*\)$/, '').trim()
    const parts = name.split(/\s+/).filter(Boolean)
    const first = parts[0] ? parts[0].toLowerCase() : ''
    const last = parts.length > 0 ? parts[parts.length - 1].toLowerCase() : ''
    const found = employees.value.find(e => {
      if (!e) return false
      const eFirst = (e.first_name || '').toString().trim().toLowerCase()
      const eLast = (e.last_name || '').toString().trim().toLowerCase()
      if (!eLast) return false
      // require last name match and first initial match (if first available)
      const firstInitialMatches = !first || (eFirst && eFirst.charAt(0) === first.charAt(0))
      return eLast === last && firstInitialMatches
    })
    if (found) return formatDentistDisplay(found)
    return name
  }
  return 'Not Assigned'
}

const getBranchNameFromAppointment = (apt) => {
  if (!apt) return ''
  // Try to find dentist id from various shapes
  const raw = apt.dentist || apt.dentist_id || (apt.dentist && apt.dentist.id) || null
  const dentistId = (raw && typeof raw === 'object') ? raw.id : raw
  if (!dentistId) return ''
  // find employee matching user id or id
  const emp = employees.value.find(e => {
    if (!e) return false
    const uid = (e.user && (e.user.id || e.user)) || e.user_id || null
    // also allow matching by employee primary id if dentistId equals employee.id
    if (uid && String(uid) === String(dentistId)) return true
    if (e.id && String(e.id) === String(dentistId)) return true
    return false
  })
  if (!emp) return ''
  const empBranchRaw = emp.branch || (emp.branch_id || null)
  const empBranchId = empBranchRaw && typeof empBranchRaw === 'object' ? empBranchRaw.id : empBranchRaw
  if (!empBranchId) return ''
  return getBranchName(empBranchId)
}

const getStatusClass = (status) => {
  const classes = {
    requested: 'badge badge-secondary',
    scheduled: 'badge badge-info',
    confirmed: 'badge badge-primary',
    in_progress: 'badge badge-warning',
    completed: 'badge badge-success',
    cancelled: 'badge badge-danger',
    failed: 'badge badge-danger',
    no_show: 'badge badge-secondary'
  }
  return classes[status] || 'badge badge-secondary'
}

const showModal = () => {
  const modal = document.getElementById('appointmentModal')
  modal.classList.add('show')
  modal.style.display = 'block'
  document.body.classList.add('modal-open')
  
  const backdrop = document.createElement('div')
  backdrop.className = 'modal-backdrop fade show'
  backdrop.id = 'appointmentModalBackdrop'
  document.body.appendChild(backdrop)
}

const closeModal = () => {
  const modal = document.getElementById('appointmentModal')
  modal.classList.remove('show')
  modal.style.display = 'none'
  document.body.classList.remove('modal-open')
  
  const backdrop = document.getElementById('appointmentModalBackdrop')
  if (backdrop) {
    backdrop.remove()
  }
  
  // clear accepting flag when closing modal
  acceptingRequest.value = false

  resetForm()
  
  // Reopen view modal if we came from it
  if (returnToViewModal.value) {
    returnToViewModal.value = false
    showViewModal()
  }
  // Reopen date modal if we came from it
  else if (returnToDateModal.value) {
    returnToDateModal.value = false
    openDateModal()
  }
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
  
  // Reopen date modal if we came from it
  if (returnToDateModal.value) {
    returnToDateModal.value = false
    openDateModal()
  }
}

onMounted(async () => {
  fetchAppointments()
  fetchPatients()
  fetchUsers()
  await fetchEmployees()
  await loadPositions()
  loadBranches()
  await fetchHolidays()
})

watch(filterTab, () => {
  // If the Search panel's inner filter is set to 'today', set the dateFilter
  // so the computed `allFilteredAppointments` shows today's items. Clear it
  // for other filter tabs.
  if (filterTab.value === 'today') {
    const today = new Date().toISOString().split('T')[0]
    dateFilter.value = today
  } else {
    dateFilter.value = ''
  }
  fetchAppointments()
})

// Re-check validations when relevant fields change
watch(() => form.value.appointment_time, () => {
  // Always run the full validation first
  validateSchedule()

  // Then enforce 09:00-19:00 when 'Any' branch is selected
  const branchVal = (form.value.branch === undefined || form.value.branch === null) ? '' : String(form.value.branch)
  const isAnyBranch = branchVal.trim() === '' || branchVal.trim().toLowerCase() === 'any'
  if (isAnyBranch) {
    const startM = parseTimeToMinutes(form.value.appointment_time)
    const dur = Number(form.value.duration) || 30
    const openM = 9 * 60
    const closeM = 19 * 60
    if (startM === null || startM < openM || (startM + dur) > closeM) {
      const openStr = formatTime(minutesToHHMM(openM))
      const closeStr = formatTime(minutesToHHMM(closeM))
      timeWarning.value = `Selected time is outside operating hours (${openStr} - ${closeStr}).`
      submitDisabled.value = true
      return
    }
    // within defaults, ensure any previous timeWarning is cleared (validateSchedule may have set other warnings)
    if (timeWarning.value && timeWarning.value.includes('outside operating hours')) {
      timeWarning.value = ''
    }
  }
})

watch(() => form.value.dentist, () => {
  // When dentist changes, re-run conflict checks
  validateSchedule()
})

// Run validation when duration changes
watch(() => form.value.duration, () => {
  validateSchedule()
})

// Run validation when patient selection changes
watch(() => form.value.patient, () => {
  validateSchedule()
})

// Re-run validation when status changes (e.g., Scheduled requires dentist)
watch(() => form.value.status, () => {
  validateSchedule()
})

// When branch changes, if currently selected dentist isn't in that branch, clear selection
watch(() => form.value.branch, (newBranch) => {
  if (!newBranch) return
  const selectedDentist = form.value.dentist
  if (!selectedDentist) return
  const found = employees.value.find(e => {
    const uid = (e.user && (e.user.id || e.user)) || e.user_id || null
    return uid && String(uid) === String(selectedDentist)
  })
  if (!found) return
  const empBranchRaw = found.branch || (found.branch_id || null)
  const empBranchId = empBranchRaw && typeof empBranchRaw === 'object' ? empBranchRaw.id : empBranchRaw
  if (empBranchId && String(empBranchId) !== String(newBranch)) {
    // clear dentist selection to avoid invalid assignment
    form.value.dentist = ''
    timeWarning.value = 'Selected dentist was cleared because they are not assigned to the chosen branch.'
  }
  // If branch has slots and no time chosen, auto-fill first available slot
  if (newBranch && form.value.appointment_date && !form.value.appointment_time) {
    const slots = availableTimeSlots.value
    if (slots && slots.length > 0) {
      form.value.appointment_time = slots[0]
    }
  }
  // Re-validate when branch changes
  validateSchedule()
})
</script>

<style scoped>
.modal {
  overflow-y: auto;
}
.nav-tabs .nav-link {
  cursor: pointer;
}

.appointment-tabs {
  display: flex;
  gap: 10px;
  margin-bottom: 20px;
}

.tab-btn {
  flex: 1;
  padding: 12px 24px;
  border: none;
  background-color: #e9ecef;
  color: #495057;
  font-size: 16px;
  font-weight: 500;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.3s ease;
}

.tab-btn:hover {
  background-color: #d1d5db;
  transform: translateY(-2px);
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.tab-btn.active {
  background-color: #17a2b8;
  color: white;
  box-shadow: 0 4px 6px rgba(23, 162, 184, 0.3);
}

.tab-btn.active:hover {
  background-color: #138496;
}

/* Calendar Styles */
.calendar-grid {
  display: grid;
  grid-template-columns: repeat(7, 1fr);
  gap: 1px;
  background-color: #dee2e6;
  border: 1px solid #dee2e6;
}

.calendar-header {
  background-color: #17a2b8;
  color: white;
  padding: 12px;
  text-align: center;
  font-weight: 600;
  font-size: 14px;
}

.calendar-day {
  background-color: white;
  min-height: 80px;
  padding: 8px;
  cursor: pointer;
  position: relative;
  transition: all 0.2s ease;
}

.calendar-day:hover {
  background-color: #f8f9fa;
  transform: scale(1.02);
}

.calendar-day.other-month {
  background-color: #f8f9fa;
  color: #adb5bd;
}

.calendar-day.today {
  background-color: #fff3cd;
  border: 2px solid #ffc107;
}

.calendar-day.has-appointments {
  background-color: #e7f5f7;
}

.calendar-day.has-appointments:hover {
  background-color: #d1eef2;
}

.day-number {
  font-size: 16px;
  font-weight: 600;
  color: #495057;
}

.appointment-badge {
  position: absolute;
  top: 5px;
  right: 5px;
  background-color: #17a2b8;
  color: white;
  border-radius: 50%;
  width: 24px;
  height: 24px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 12px;
  font-weight: bold;
}

.calendar-day.today .appointment-badge {
  background-color: #ffc107;
  color: #000;
}

.calendar-selector {
  flex: 1;
  display: flex;
  justify-content: center;
}

.month-year-selector {
  display: flex;
  gap: 10px;
  align-items: center;
}

.month-select {
  width: 140px;
  font-weight: bold;
  border: 1px solid #17a2b8;
  color: #17a2b8;
}

.year-select {
  width: 90px;
  font-weight: bold;
  border: 1px solid #17a2b8;
  color: #17a2b8;
}

.month-select:focus,
.year-select:focus {
  border-color: #17a2b8;
  box-shadow: 0 0 0 0.2rem rgba(23, 162, 184, 0.25);
}

/* Responsive Styles */
@media (max-width: 1200px) {
  .calendar-day {
    min-height: 70px;
    padding: 6px;
  }
  
  .day-number {
    font-size: 14px;
  }
  
  .appointment-badge {
    width: 20px;
    height: 20px;
    font-size: 10px;
  }
}

@media (max-width: 992px) {
  .calendar-day {
    min-height: 60px;
    padding: 5px;
  }
  
  .calendar-header {
    padding: 10px;
    font-size: 12px;
  }
  
  .day-number {
    font-size: 13px;
  }
  
  .appointment-badge {
    width: 18px;
    height: 18px;
    font-size: 9px;
    top: 3px;
    right: 3px;
  }
}

@media (max-width: 768px) {
  .calendar-day {
    min-height: 50px !important;
    padding: 4px;
  }

  .holiday-label {
    margin-top: 1px !important;
    max-height: 48px;
    font-size: 8px;
  }
  
  .calendar-header {
    padding: 8px;
    font-size: 11px;
  }
  
  .day-number {
    font-size: 12px;
  }
  
  .appointment-badge {
    width: 16px;
    height: 16px;
    font-size: 8px;
    top: 2px;
    right: 2px;
  }
  
  .month-select {
    width: 120px;
    font-size: 14px;
  }
  
  .year-select {
    width: 80px;
    font-size: 14px;
  }
  
  .month-year-selector {
    gap: 8px;
  }
}

@media (max-width: 576px) {
  .calendar-day {
    min-height: 45px;
    padding: 3px;
  }
  
  .calendar-header {
    padding: 6px 4px;
    font-size: 10px;
  }
  
  .day-number {
    font-size: 11px;
  }
  
  .appointment-badge {
    width: 14px;
    height: 14px;
    font-size: 7px;
    top: 2px;
    right: 2px;
  }
  
  .month-select {
    width: 100px;
    font-size: 13px;
  }
  
  .year-select {
    width: 70px;
    font-size: 13px;
  }
  
  .month-year-selector {
    gap: 5px;
  }
  
  .card-header .btn-sm {
    padding: 0.15rem 0.4rem;
    font-size: 12px;
  }
}

@media (max-width: 400px) {
  .calendar-day {
    min-height: 40px;
    padding: 2px;
  }
  
  .calendar-header {
    padding: 5px 2px;
    font-size: 9px;
  }
  
  .day-number {
    font-size: 10px;
  }
  
  .appointment-badge {
    width: 12px;
    height: 12px;
    font-size: 6px;
    top: 1px;
    right: 1px;
  }
  
  .month-select {
    width: 90px;
    font-size: 12px;
  }
  
  .year-select {
    width: 60px;
    font-size: 12px;
  }
}

/* Make appointments tables scroll on small screens instead of overflowing */
.appointments-table-wrapper {
  overflow-x: auto;
  -webkit-overflow-scrolling: touch;
}
.appointments-table-wrapper table {
  min-width: 0;
  width: 100%;
  table-layout: auto;
}
.appointments-table-wrapper th,
.appointments-table-wrapper td {
  white-space: normal; /* allow wrapping at natural break points */
  word-break: normal;
  overflow-wrap: normal;
  padding: 0.5rem;
}
.appointments-table-wrapper tbody tr td {
  height: auto; /* let rows expand based on content */
}

@media (max-width: 576px) {
  .appointments-table-wrapper table { min-width: 0; }
  .appointments-table-wrapper th,
  .appointments-table-wrapper td { padding: 0.35rem; font-size: 0.9rem; }
}

/* Modal Animations */
.modal-fade-enter-active,
.modal-fade-leave-active {
  transition: opacity 0.3s ease;
}

.modal-fade-enter-from,
.modal-fade-leave-to {
  opacity: 0;
}

.modal-slide-enter-active {
  transition: all 0.3s ease;
}

.modal-slide-leave-active {
  transition: all 0.3s ease;
}

.modal-slide-enter-from {
  transform: translateY(-50px);
  opacity: 0;
}

.modal-slide-leave-to {
  transform: translateY(-50px);
  opacity: 0;
}

.backdrop-fade-enter-active,
.backdrop-fade-leave-active {
  transition: opacity 0.3s ease;
}

.backdrop-fade-enter-from,
.backdrop-fade-leave-to {
  opacity: 0;
}

.modal-backdrop {
  background-color: rgba(0, 0, 0, 0.5);
}

#dateAppointmentsModal {
  z-index: 1070 !important;
}

#dateAppointmentsModal + .modal-backdrop {
  z-index: 1065 !important;
}

#viewModal {
  z-index: 1050;
}

#viewModalBackdrop {
  z-index: 1045;
}

.reject-reason-box {
  border: 1px solid #dc3545;
  background-color: #fff5f6;
  color: #6b0f12;
  padding: 0.75rem;
  border-radius: 6px;
  white-space: pre-wrap;
  word-break: normal;
}

.reject-reason-box pre {
  margin: 0;
  font-family: inherit;
  font-size: 0.95rem;
  color: inherit;
  background: transparent;
}

/* Holiday highlight */
.calendar-day.holiday {
  background-color: rgba(220,10,30,0.06);
  border: 1px solid rgba(220,10,30,0.12);
}
.calendar-day.holiday .day-number {
  color: #c12a2a;
  font-weight: 700;
}
.calendar-day.holiday .appointment-badge {
  background-color: rgba(193,42,42,0.12);
  color: #8b1f1f;
}

.holiday-label { margin-top: 8px; max-height: 54px; overflow: hidden; }
.holiday-label .small { display: block; line-height: 1.05; color: #8b1f1f; }
</style>

