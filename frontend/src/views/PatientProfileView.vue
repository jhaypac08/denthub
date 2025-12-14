<template>
  <div class="wrapper">
    <!-- Navbar -->
    <nav class="main-header navbar navbar-expand navbar-white navbar-light" style="padding: 0; height: 57px;">
      <!-- Brand Section -->
      <div class="brand-section">
        <div class="brand-box">
          <img :src="logoSrc" alt="DentHub" class="brand-logo-top" />
          <strong>DentHub Patient Portal</strong>
        </div>
      </div>

      <!-- User Section -->
      <ul class="navbar-nav ml-auto">
        <li class="nav-item dropdown">
          <a class="nav-link dropdown-toggle" href="#" id="userDropdown" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false" @click.prevent="toggleDropdown">
            <img 
              v-if="patient?.photo" 
              :src="getPhotoUrl(patient.photo)" 
              class="user-avatar" 
              alt="Patient photo"
            >
            <i v-else class="fas fa-user-circle fa-lg"></i>
            <span class="ml-2">{{ patient?.full_name || 'Loading...' }}</span>
          </a>
          <div class="dropdown-menu dropdown-menu-right" :class="{ show: showUserDropdown }" aria-labelledby="userDropdown">
            <a class="dropdown-item" href="#" @click.prevent="showChangePasswordModal">
              <i class="fas fa-key mr-2"></i> Change Password
            </a>
            <div class="dropdown-divider"></div>
            <a class="dropdown-item text-danger" href="#" @click.prevent="handleLogout">
              <i class="fas fa-sign-out-alt mr-2"></i> Logout
            </a>
          </div>
        </li>
      </ul>
    </nav>

    <!-- Content Wrapper -->
    <div class="content-wrapper" style="margin-left: 0;">
      <!-- Header -->
      <div class="content-header">
        <div class="container-fluid">
          <div class="row mb-2">
            <div class="col-sm-12">
              <h1 class="m-0">My Profile</h1>
            </div>
          </div>
        </div>
      </div>

      <!-- Main content -->
      <div class="content">
        <div class="container-fluid">
          <div v-if="loading" class="text-center py-5">
            <i class="fas fa-spinner fa-spin fa-3x text-primary"></i>
            <p class="mt-3">Loading your profile...</p>
          </div>

          <div v-else-if="patient" class="row">
            <!-- Profile Card -->
            <div class="col-md-4">
              <div class="card card-primary card-outline">
                <div class="card-body box-profile">
                  <div class="text-center">
                    <div class="profile-photo-wrapper">
                      <img 
                        v-if="patient.photo" 
                        :src="getPhotoUrl(patient.photo)" 
                        class="profile-user-img img-fluid img-circle" 
                        alt="Patient photo"
                      >
                      <div v-else class="profile-user-img-placeholder">
                        <i class="fas fa-user-circle fa-5x text-secondary"></i>
                      </div>
                      <div class="photo-upload-overlay">
                        <label for="photoUpload" class="photo-upload-label">
                          <i class="fas fa-camera"></i>
                        </label>
                        <input 
                          id="photoUpload" 
                          type="file" 
                          accept="image/*" 
                          @change="handlePhotoUpload" 
                          style="display: none;"
                        >
                      </div>
                    </div>
                  </div>

                  <h3 class="profile-username text-center mt-3">{{ patient.full_name }}</h3>
                  <p class="text-muted text-center">Patient ID: {{ patient.patient_id }}</p>

                  <ul class="list-group list-group-unbordered mb-3">
                    <li class="list-group-item">
                      <b>Status</b>
                      <span class="float-right">
                        <span :class="getStatusBadgeClass(patient.status)">
                          {{ patient.status.toUpperCase() }}
                        </span>
                      </span>
                    </li>
                    <li class="list-group-item">
                      <b>Age</b>
                      <span class="float-right">{{ patient.age }} years</span>
                    </li>
                    <li class="list-group-item">
                      <b>Blood Type</b>
                      <span class="float-right">{{ patient.blood_type || 'N/A' }}</span>
                    </li>
                  </ul>

                  <button @click="showRequestAppointmentModal" class="btn btn-success btn-block mb-2">
                    <i class="fas fa-calendar-plus"></i> Request Appointment
                  </button>
                  <button @click="showChangePasswordModal" class="btn btn-primary btn-block">
                    <i class="fas fa-key"></i> Change Password
                  </button>
                </div>
              </div>
            </div>

            <!-- Information Tabs -->
            <div class="col-md-8">
              <div class="card">
                <div class="card-header p-2" style="background-color: transparent; border-bottom: none;">
                  <ul class="nav nav-tabs">
                    <li class="nav-item">
                      <a class="nav-link" :class="{ active: activeTab === 'info' }" @click="activeTab = 'info'" href="javascript:void(0)">
                        <i class="fas fa-info-circle"></i>
                        <span class="tab-text">Personal Information</span>
                      </a>
                    </li>
                    <li class="nav-item">
                      <a class="nav-link" :class="{ active: activeTab === 'appointments' }" @click="activeTab = 'appointments'" href="javascript:void(0)">
                        <i class="fas fa-calendar-check"></i>
                        <span class="tab-text">My Appointments</span>
                      </a>
                    </li>
                    <li class="nav-item">
                      <a class="nav-link" :class="{ active: activeTab === 'treatments' }" @click="activeTab = 'treatments'" href="javascript:void(0)">
                        <i class="fas fa-notes-medical"></i>
                        <span class="tab-text">Treatment History</span>
                      </a>
                    </li>
                    <li class="nav-item">
                      <a class="nav-link" :class="{ active: activeTab === 'messages' }" @click="handleMessagesTabClick" href="javascript:void(0)">
                        <i class="fas fa-envelope"></i>
                        <span class="tab-text">Messages</span>
                        <span v-if="unreadCount > 0" class="badge badge-danger ml-1">{{ unreadCount }}</span>
                      </a>
                    </li>
                  </ul>
                </div>
                <div class="card-body">
                  <!-- Personal Information Tab -->
                  <div v-show="activeTab === 'info'" class="tab-pane">
                    <div class="row">
                      <div class="col-md-6">
                        <strong><i class="fas fa-user mr-1"></i> Full Name</strong>
                        <p class="text-muted">{{ patient.full_name }}</p>
                        <hr>
                      </div>
                      <div class="col-md-6">
                        <strong><i class="fas fa-venus-mars mr-1"></i> Gender</strong>
                        <p class="text-muted">{{ capitalizeFirst(patient.gender) }}</p>
                        <hr>
                      </div>
                      <div class="col-md-6">
                        <strong><i class="fas fa-birthday-cake mr-1"></i> Date of Birth</strong>
                        <p class="text-muted">{{ formatDate(patient.date_of_birth) }}</p>
                        <hr>
                      </div>
                      <div class="col-md-6">
                        <strong><i class="fas fa-phone mr-1"></i> Phone</strong>
                        <p class="text-muted">{{ patient.phone }}</p>
                        <hr>
                      </div>
                      <div class="col-md-12">
                        <strong><i class="fas fa-envelope mr-1"></i> Email</strong>
                        <p class="text-muted">{{ patient.email || 'N/A' }}</p>
                        <hr>
                      </div>
                      <div class="col-md-12">
                        <strong><i class="fas fa-map-marker-alt mr-1"></i> Address</strong>
                        <p class="text-muted">{{ patient.address }}</p>
                        <hr>
                      </div>
                      <div class="col-md-12">
                        <strong><i class="fas fa-notes-medical mr-1"></i> Medical Notes</strong>
                        <p class="text-muted">{{ patient.medical_notes || 'No medical notes' }}</p>
                        <hr>
                      </div>
                      <div class="col-md-6">
                        <strong><i class="fas fa-user-shield mr-1"></i> Emergency Contact</strong>
                        <p class="text-muted">{{ patient.emergency_contact_name }}</p>
                        <hr>
                      </div>
                      <div class="col-md-6">
                        <strong><i class="fas fa-phone-alt mr-1"></i> Emergency Phone</strong>
                        <p class="text-muted">{{ patient.emergency_contact_phone }}</p>
                      </div>
                    </div>
                  </div>

                  <!-- Appointments Tab -->
                  <div v-show="activeTab === 'appointments'" class="tab-pane">
                    <div class="d-flex mb-2 align-items-center">
                      <div class="mr-2 date-filter-wrap">
                        <label for="appointmentDateFilterInput" class="date-filter-label d-none d-sm-inline">Date</label>
                        <label for="appointmentDateFilterInput" class="date-filter-label-mobile d-inline d-sm-none">Date</label>
                        <input id="appointmentDateFilterInput" type="date" v-model="appointmentDateFilter" class="form-control form-control-sm appointment-date-filter" />
                      </div>
                      <div>
                        <button class="btn btn-sm btn-secondary mr-2" @click.prevent="(appointmentDateFilter=''), refreshAppointments()">All</button>
                        <button class="btn btn-sm btn-primary" @click.prevent="refreshAppointments">Refresh</button>
                      </div>
                    </div>
                    <div v-if="loadingAppointments" class="text-center py-4">
                      <i class="fas fa-spinner fa-spin"></i> Loading appointments...
                    </div>
                    <div v-else-if="appointments.length === 0" class="text-center text-muted py-4">
                      <i class="fas fa-calendar-times fa-3x mb-3"></i>
                      <p>No appointments found</p>
                    </div>
                    <div v-else>
                      <div class="appointments-list list-group">
                        <div v-for="appointment in appointments" :key="appointment.id" class="list-group-item d-flex justify-content-between align-items-start">
                          <div class="appointment-main">
                            <div class="appointment-header font-weight-bold">
                              {{ formatDate(appointment.appointment_date) }} • {{ formatTime12(appointment.appointment_time) }}
                            </div>
                            <div class="appointment-meta text-muted small">
                              <span>{{ appointment.appointment_type || 'N/A' }}</span>
                              <span class="mx-2">•</span>
                              <span :class="getAppointmentStatusClass(appointment.status)">{{ formatStatus(appointment.status) }}</span>
                            </div>
                            <div class="appointment-dentist text-muted small mt-1">
                              <strong>Assigned Dentist:</strong>
                              <span class="ml-1">{{ getDentistDisplay(appointment) }}</span>
                            </div>
                            <div class="appointment-notes text-muted small mt-1">
                              <strong>Note:</strong>
                              <span class="ml-1">{{ appointment.notes || '-' }}</span>
                            </div>
                          </div>
                          <div class="appointment-actions d-flex flex-column ml-3">
                            <template v-if="['requested','cancelled'].includes(String(appointment.status).toLowerCase())">
                              <button class="btn btn-sm btn-outline-primary mb-1 w-100" @click.prevent="updateAppointment(appointment)">
                                <i class="fas fa-edit btn-icon"></i>
                                <span class="btn-text">Update</span>
                              </button>
                              <button class="btn btn-sm btn-outline-success w-100" @click.prevent="resubmitAppointment(appointment)">
                                <i class="fas fa-redo btn-icon"></i>
                                <span class="btn-text">Resubmit</span>
                              </button>
                            </template>
                          </div>
                        </div>
                      </div>
                    </div>
                  </div>

                  <!-- Treatments Tab -->
                  <div v-show="activeTab === 'treatments'" class="tab-pane">
                    <div v-if="loadingTreatments" class="text-center py-4">
                      <i class="fas fa-spinner fa-spin"></i> Loading treatments...
                    </div>
                    <div v-else-if="treatments.length === 0" class="text-center text-muted py-4">
                      <i class="fas fa-notes-medical fa-3x mb-3"></i>
                      <p>No treatment records found</p>
                    </div>
                    <div v-else class="table-responsive">
                      <table class="table table-sm table-hover">
                        <thead>
                          <tr>
                            <th>Date</th>
                            <th>Treatment</th>
                            <th>Tooth Number</th>
                            <th>Cost</th>
                            <th>Payment Status</th>
                          </tr>
                        </thead>
                        <tbody>
                          <tr v-for="treatment in treatments" :key="treatment.id">
                            <td>{{ formatDate(treatment.treatment_date) }}</td>
                            <td>{{ treatment.treatment_type }}</td>
                            <td>{{ treatment.tooth_number || 'N/A' }}</td>
                            <td>₱{{ parseFloat(treatment.cost).toLocaleString() }}</td>
                            <td>
                              <span :class="getPaymentStatusClass(treatment.payment_status)">
                                {{ formatStatus(treatment.payment_status) }}
                              </span>
                            </td>
                          </tr>
                        </tbody>
                      </table>
                    </div>
                  </div>

                  <!-- Messages Tab -->
                  <div v-show="activeTab === 'messages'" class="tab-pane">
                    <div v-if="loadingMessages" class="text-center py-4">
                      <i class="fas fa-spinner fa-spin"></i> Loading messages...
                    </div>
                    <div v-else-if="messages.length === 0" class="text-center text-muted py-4">
                      <i class="fas fa-envelope-open fa-3x mb-3"></i>
                      <p>No messages in your inbox</p>
                    </div>
                    <div v-else>
                      <div v-for="message in messages" :key="message.id" 
                           class="message-item" 
                           :class="{ 'unread': !message.is_read }"
                           @click="openMessage(message)">
                        <div class="message-header">
                          <div class="message-sender">
                            <i class="fas fa-user-circle mr-2"></i>
                            <strong>{{ message.sender_name }}</strong>
                            <span v-if="!message.is_read" class="badge badge-primary ml-2">New</span>
                          </div>
                          <div class="message-time text-muted">
                            <small>{{ message.time_since }} ago</small>
                          </div>
                        </div>
                        <div class="message-subject">{{ message.subject }}</div>
                        <div class="message-preview">{{ getMessagePreview(message.body) }}</div>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <div v-else class="alert alert-warning">
            <i class="fas fa-exclamation-triangle"></i>
            Unable to load patient profile. Please contact support.
          </div>
        </div>
      </div>
    </div>

    <!-- Message Detail Modal -->
    <div v-if="showMessageModal" class="modal fade show" style="display: block;" tabindex="-1">
      <div class="modal-dialog modal-lg">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">{{ selectedMessage?.subject }}</h5>
            <button type="button" class="close" @click="closeMessageModal">
              <span>&times;</span>
            </button>
          </div>
          <div class="modal-body">
            <div class="message-meta mb-3">
              <p class="mb-1">
                <strong>From:</strong> {{ selectedMessage?.sender_name }}
              </p>
              <p class="mb-1">
                <strong>Date:</strong> {{ formatDate(selectedMessage?.created_at) }}
              </p>
              <p v-if="selectedMessage?.message_type" class="mb-1">
                <strong>Type:</strong> 
                <span :class="getMessageTypeBadge(selectedMessage.message_type)">
                  {{ formatStatus(selectedMessage.message_type) }}
                </span>
              </p>
            </div>
            <div class="message-body">
              <p style="white-space: pre-wrap;">{{ selectedMessage?.body }}</p>
            </div>
          </div>
          <div class="modal-footer">
            <button type="button" class="btn btn-secondary" @click="closeMessageModal">Close</button>
          </div>
        </div>
      </div>
    </div>
    <div v-if="showMessageModal" class="modal-backdrop fade show"></div>

    <!-- Change Password Modal -->
    <div v-if="showPasswordModal" class="modal fade show" style="display: block;" tabindex="-1">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">
              {{ forcePasswordChange ? 'Password Change Required' : 'Change Password' }}
            </h5>
            <button v-if="!forcePasswordChange" type="button" class="close" @click="closeChangePasswordModal">
              <span>&times;</span>
            </button>
          </div>
          <form @submit.prevent="changePassword">
            <div class="modal-body">
              <div v-if="forcePasswordChange" class="alert alert-warning">
                <i class="fas fa-exclamation-triangle"></i>
                For security reasons, you must change your password before accessing your profile.
              </div>
              <div class="form-group">
                <label>Current Password</label>
                <input 
                  v-model="passwordForm.current" 
                  type="password" 
                  class="form-control" 
                  required
                >
              </div>
              <div class="form-group">
                <label>New Password</label>
                <input 
                  v-model="passwordForm.new" 
                  type="password" 
                  class="form-control" 
                  required
                  minlength="6"
                >
                <small class="form-text text-muted">Minimum 6 characters</small>
              </div>
              <div class="form-group">
                <label>Confirm New Password</label>
                <input 
                  v-model="passwordForm.confirm" 
                  type="password" 
                  class="form-control" 
                  required
                >
              </div>
            </div>
            <div class="modal-footer">
              <button v-if="!forcePasswordChange" type="button" class="btn btn-default" @click="closeChangePasswordModal">Cancel</button>
              <button type="submit" class="btn btn-primary">Change Password</button>
            </div>
          </form>
        </div>
      </div>
    </div>
    <div v-if="showPasswordModal" class="modal-backdrop fade show"></div>

    <!-- Request Appointment Modal -->
    <div v-if="showAppointmentModal" class="modal fade show" style="display: block;" tabindex="-1">
      <div class="modal-dialog modal-lg">
        <div class="modal-content">
          <div class="modal-header bg-success text-white">
            <h5 class="modal-title">
              <i class="fas fa-calendar-plus"></i> {{ editingId ? 'Update Appointment' : 'Request Appointment' }}
            </h5>
            <button type="button" class="close text-white" @click="closeAppointmentModal">
              <span>&times;</span>
            </button>
          </div>
          <form @submit.prevent="submitAppointmentRequest">
            <div class="modal-body">

              <!-- Schedule for Selected Date: moved above Preferred Date -->
              <div v-if="appointmentForm.appointment_date" class="alert alert-info mb-3">
                <h6 class="mb-2"><i class="fas fa-calendar-day"></i> Appointments on {{ formatDate(appointmentForm.appointment_date) }}</h6>
                <div v-if="loadingDateAppointments" class="text-center py-2">
                  <i class="fas fa-spinner fa-spin"></i> Loading schedules...
                </div>
                <div v-else-if="dateAppointments.length === 0" class="text-muted">
                  <small>No appointments scheduled for this date.</small>
                </div>
                <div v-else>
                  <div class="schedule-list">
                    <div v-for="apt in dateAppointments" :key="apt.id" class="schedule-item" @click="selectDentistFromApt(apt)" style="cursor: pointer;">
                      <i class="fas fa-clock text-primary"></i>
                      <strong>{{ apt.appointment_time }}</strong>
                      <span class="text-muted ml-2">- {{ getDentistDisplay(apt) }}</span>
                      <span :class="getAppointmentStatusClass(apt.status)" class="ml-2">
                        {{ formatStatus(apt.status) }}
                      </span>
                    </div>
                  </div>
                  <small class="text-muted">
                    <i class="fas fa-info-circle"></i> Please avoid selecting times that are already booked.
                  </small>
                  <div v-if="conflictWarning" class="alert alert-danger small mt-2" role="alert">
                    <i class="fas fa-exclamation-circle"></i>&nbsp;
                    <span v-html="conflictWarning"></span>
                  </div>
                </div>
              </div>

              <div class="row">
                <div class="col-md-12">
                  <div class="form-group">
                    <label>Preferred Branch</label>
                    <select v-model="appointmentForm.branch" class="form-control">
                      <option value="">Any</option>
                      <option v-for="b in branches" :key="b.id" :value="b.id">
                        {{ b.name || b.title || b.location || ('Branch ' + b.id) }}
                      </option>
                    </select>
                  </div>
                </div>
              </div>

              <div class="row">
                <div class="col-md-6">
                  <div class="form-group">
                    <label>Preferred Date <span class="text-danger">*</span></label>
                    <input 
                      v-model="appointmentForm.appointment_date" 
                      type="date" 
                      class="form-control" 
                      :min="minDate"
                      :max="maxPreferredDate"
                      required
                    >
                    <div v-if="dateHolidayWarning" class="alert alert-warning small mt-2" role="alert">
                      <i class="fas fa-exclamation-circle"></i>&nbsp;{{ dateHolidayWarning }}
                    </div>
                    <div v-if="requestLimitWarning" class="alert alert-warning small mt-2" role="alert">
                      <i class="fas fa-exclamation-circle"></i>&nbsp;<span v-html="requestLimitWarning"></span>
                    </div>
                    <div v-if="existingAppointmentWarning" class="alert alert-info small mt-2" role="alert">
                      <i class="fas fa-info-circle"></i>&nbsp;{{ existingAppointmentWarning }}
                    </div>
                    <div v-if="dateRangeWarning" class="alert alert-warning small mt-2" role="alert">
                      <i class="fas fa-exclamation-circle"></i>&nbsp;{{ dateRangeWarning }}
                    </div>
                  </div>
                </div>
                <div class="col-md-6">
                  <div class="form-group">
                    <label>Preferred Time <span class="text-danger">*</span></label>

                    <!-- Use editable time input; when branch slots exist provide a datalist for suggestions -->
                    <div>
                      <input
                        v-model="appointmentForm.appointment_time"
                        type="time"
                        class="form-control"
                        :list="(appointmentForm.branch && availableTimeSlots.length > 0) ? 'branchSlots' : null"
                        required
                      >

                      <datalist v-if="appointmentForm.branch && availableTimeSlots.length > 0" id="branchSlots">
                        <option v-for="t in availableTimeSlots" :key="t" :value="t">{{ formatTime12(t) }}</option>
                      </datalist>

                      <small v-if="appointmentForm.branch && availableTimeSlots.length > 0" class="text-muted">Suggestions show operating hours for the selected branch.</small>

                      <div v-if="timeWarning" class="alert alert-danger small mt-2" role="alert">
                        <i class="fas fa-exclamation-circle"></i>&nbsp;{{ timeWarning }}
                      </div>
                    </div>
                  </div>
                </div>
              </div>

              <div class="row">
                <div class="col-md-6">
                  <div class="form-group">
                    <label>Appointment Type <span class="text-danger">*</span></label>
                    <select v-model="appointmentForm.appointment_type" class="form-control" required>
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
                <div class="col-md-6">
                  <div class="form-group">
                    <label>Preferred Dentist</label>
                    <select v-model="appointmentForm.dentist" class="form-control" @change="onPreferredDentistChange">
                      <option value="">Any</option>
                      <option v-for="emp in dentists.filter(e => getEmployeeUserId(e))" :key="emp.id" :value="getEmployeeUserId(emp)">
                        {{ formatDentistDisplay(emp) }}
                      </option>
                    </select>
                    
                  </div>
                </div>
              </div>

              <div v-if="appointmentForm.appointment_type === 'other'" class="form-group">
                <label>Please Specify Appointment Type <span class="text-danger">*</span></label>
                <input 
                  v-model="appointmentForm.other_type" 
                  type="text" 
                  class="form-control" 
                  placeholder="Please specify the type of appointment..."
                  :required="appointmentForm.appointment_type === 'other'"
                >
              </div>

              <div class="form-group">
                <label>Reason for Visit <span class="text-danger">*</span></label>
                <textarea 
                  v-model="appointmentForm.reason" 
                  class="form-control" 
                  rows="3" 
                  placeholder="Please describe your symptoms or reason for appointment..."
                  required
                ></textarea>
              </div>

              <div class="form-group">
                <label>Additional Notes</label>
                <textarea 
                  v-model="appointmentForm.notes" 
                  class="form-control" 
                  rows="2" 
                  placeholder="Any additional information we should know..."
                ></textarea>
              </div>

              <div class="alert alert-info">
                <i class="fas fa-info-circle"></i>
                <strong>Note:</strong> This is an appointment request. Our staff will review and confirm your appointment shortly.
              </div>
            </div>
            <div class="modal-footer">
              <button type="button" class="btn btn-secondary" @click="closeAppointmentModal">Cancel</button>
              <button
                type="submit"
                class="btn btn-success"
                :disabled="submitDisabled"
                :title="dateHolidayWarning ? dateHolidayWarning : (submitDisabled ? 'Submission disabled' : '')"
                :aria-disabled="submitDisabled ? 'true' : 'false'"
              >
                <i class="fas fa-paper-plane"></i> Submit Request
              </button>
            </div>
          </form>
        </div>
      </div>
    </div>
    <div v-if="showAppointmentModal" class="modal-backdrop fade show"></div>
  </div>
</template>

<script setup>
import logoSrc from '../../frontend/src/assets/icon_nobg.png'
import { ref, onMounted, computed, watch } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth'
import api from '../services/api'
import Swal from 'sweetalert2'

const router = useRouter()
const authStore = useAuthStore()

const loading = ref(true)
const loadingAppointments = ref(false)
const loadingTreatments = ref(false)
const loadingMessages = ref(false)
const loadingDateAppointments = ref(false)
const patient = ref(null)
const appointments = ref([])
const treatments = ref([])
const messages = ref([])
const unreadCount = ref(0)
const dateAppointments = ref([])
const activeTab = ref('info')
const showPasswordModal = ref(false)
const forcePasswordChange = ref(false)
const showUserDropdown = ref(false)
const uploadingPhoto = ref(false)
const showMessageModal = ref(false)
const selectedMessage = ref(null)
const showAppointmentModal = ref(false)

// UI: optional filter for appointments list and editing state
const appointmentDateFilter = ref('')
const editingId = ref(null)
let appointmentFilterTimer = null

const passwordForm = ref({
  current: '',
  new: '',
  confirm: ''
})

const appointmentForm = ref({
  appointment_date: '',
  appointment_time: '09:00',
  appointment_type: '',
  other_type: '',
  dentist: '',
  duration: 30,
  branch: '',
  reason: '',
  notes: ''
})

const employees = ref([])

// removed diagnostic dentistNote (no UI debug text)
const conflictWarning = ref('')
const conflictingAppointments = ref([])
const submitDisabled = ref(false)
const timeWarning = ref('')
const requestLimitWarning = ref('')
const dateHolidayWarning = ref('')
const holidayMatches = ref([])
const dateRangeWarning = ref('')

const holidays = ref([])

const existingAppointmentWarning = ref('')

const fetchHolidays = async () => {
  try {
    const resp = await api.get('/website/holidays/')
    holidays.value = resp.data || []
  } catch (err) {
    console.error('Failed to load holidays', err)
    holidays.value = []
  }
}

const checkPreferredDateHoliday = async (dateStr) => {
  dateHolidayWarning.value = ''
  holidayMatches.value = []
  if (!dateStr) return
  if (!holidays.value || holidays.value.length === 0) {
    await fetchHolidays()
  }
  const year = String(dateStr).slice(0,4)
  for (const h of holidays.value) {
    if (!h) continue
    if (h.specific_date && String(h.specific_date).split('T')[0] === dateStr) {
      holidayMatches.value.push(h); continue
    }
    if (h.computed_date && String(h.computed_date).split('T')[0] === dateStr) {
      holidayMatches.value.push(h); continue
    }
    if (h.is_recurring && h.month && h.day) {
      const m = String(h.month).padStart(2,'0')
      const d = String(h.day).padStart(2,'0')
      if (`${year}-${m}-${d}` === dateStr) holidayMatches.value.push(h)
    }
  }

  if (holidayMatches.value.length > 0) {
    // Build readable message listing holidays and types
    const parts = holidayMatches.value.map(h => `${h.name} (${h.holiday_type || 'Unknown'})`)
    dateHolidayWarning.value = `Selected date is a holiday: ${parts.join('; ')}. Please choose another date or contact the clinic.`
    submitDisabled.value = true
  } else {
    dateHolidayWarning.value = ''
    // Only clear submitDisabled if no other reasons exist
    // re-evaluate conflict-related disabling
    checkConflicts()
  }
}

// Watch preferred date and validate against holidays
watch(() => appointmentForm.value.appointment_date, (val) => {
  checkPreferredDateHoliday(val)
  // Only enforce per-person request limits for new requests, not when editing an existing appointment
  if (!editingId.value) checkRequestLimits(val)
  // Check if this patient already has an appointment on the selected date
  checkExistingPatientAppointment(val)
  // Check date is within allowed two-week span
  checkPreferredDateRange(val)
})

const checkRequestLimits = async (dateStr) => {
  requestLimitWarning.value = ''
  if (!patient.value || !patient.value.id) return
  if (!dateStr) return
  try {
    const resp = await api.get(`/patient/patients/${patient.value.id}/appointments/`)
    const apptsRaw = resp.data || []
    // Dedupe by id in case the API returns duplicates and ensure the record belongs to this patient
    const seen = new Set()
    const appts = []
    const targetPatientId = String(patient.value.id)
    for (const a of apptsRaw) {
      const aid = a && (a.id || a.appointment_id || a.pk)
      if (aid && seen.has(String(aid))) continue
      if (aid) seen.add(String(aid))
      // ensure appointment belongs to this patient (handle nested shapes)
      let apPatient = null
      if (a && a.patient) {
        apPatient = (typeof a.patient === 'object') ? (a.patient.id || a.patient.patient_id || null) : a.patient
      }
      // If the API is already scoped to the patient, apPatient may be null; allow those records
      if (apPatient && String(apPatient) !== targetPatientId) continue
      appts.push(a)
    }

    // Count only appointments with explicit 'requested' status
    const normalizeStatus = s => (s || '').toString().toLowerCase()
    const openCount = appts.filter(a => normalizeStatus(a.status) === 'requested').length
    // Per-day limit counts both 'requested' and 'scheduled' statuses
    const perDayCount = appts.filter(a => a.appointment_date === dateStr && ['requested','scheduled','completed','confirmed','in progress','no show'].includes(normalizeStatus(a.status))).length

    // Debugging: log counts and a few appointment ids when counts seem off
    if (openCount > 3) {
      console.debug('checkRequestLimits: rawCount=', apptsRaw.length, 'uniqueCount=', appts.length, 'openCount=', openCount, 'sample=', appts.slice(0,6).map(x=>({id:x.id,status:x.status,appointment_date:x.appointment_date,patient:x.patient})))
    }

    if (openCount >= 3) {
      requestLimitWarning.value = `You already have ${openCount} open appointment requests. Maximum of 3 open requests allowed.`
      submitDisabled.value = true
      return
    }

    if (perDayCount >= 1) {
      requestLimitWarning.value = `You already made an appointment on <strong>${formatDate(dateStr)}</strong>. Only one appointment per day is allowed.`
      submitDisabled.value = true
      return
    }

    // clear and re-evaluate conflicts
    requestLimitWarning.value = ''
    checkConflicts()
  } catch (err) {
    console.error('Failed to check request limits', err)
  }
}

const checkExistingPatientAppointment = async (dateStr) => {
  existingAppointmentWarning.value = ''
  if (!patient.value || !patient.value.id) return
  if (!dateStr) return
  try {
    const resp = await api.get(`/patient/patients/${patient.value.id}/appointments/`)
    const appts = resp.data || []
    const matches = appts.filter(a => {
      if (!a) return false
      const d = String(a.appointment_date || '').split('T')[0]
      if (d !== String(dateStr)) return false
      const st = String((a.status || '')).toLowerCase()
      return st === 'requested' || st === 'scheduled'
    })
    // If editing, exclude the appointment being edited from the check
    const relevant = matches.filter(a => !(editingId.value && String(a.id) === String(editingId.value)))
    if (relevant.length > 0) {
      existingAppointmentWarning.value = `You already have an appointment on ${formatDate(dateStr)}.`
      // Block submission when an existing appointment exists for this patient on that date
      if (!editingId.value) {
        submitDisabled.value = true
      }
    } else {
      existingAppointmentWarning.value = ''
      // No existing appointment for this date — re-evaluate other disabling reasons
      checkConflicts()
    }
  } catch (err) {
    console.error('Error checking existing patient appointments:', err)
    existingAppointmentWarning.value = ''
  }
}

const checkPreferredDateRange = (dateStr) => {
  dateRangeWarning.value = ''
  if (!dateStr) return
  const min = minDate.value
  const max = maxPreferredDate.value
  if (min && max) {
    if (dateStr < min || dateStr > max) {
      dateRangeWarning.value = `Please select a date between ${formatDate(min)} and ${formatDate(max)}.`
      // disable submit if out of range (do not block if editing the same appointment)
      if (!editingId.value) submitDisabled.value = true
      return
    }
  }
  dateRangeWarning.value = ''
  // re-evaluate other disabling reasons
  checkConflicts()
}

const branches = ref([])

const loadBranches = async () => {
  try {
    const resp = await api.get('/branches/')
    branches.value = resp.data
  } catch (err) {
    console.error('Error loading branches:', err)
    branches.value = []
  }
}

// Helper: normalize dentist id from appointment object
const getAppointmentDentistUserId = (apt) => {
  if (!apt) return null
  const raw = apt.dentist || apt.dentist_id || (apt.dentist && apt.dentist.id) || null
  return (raw && typeof raw === 'object') ? raw.id : raw
}

const parseTimeToMinutes = (t) => {
  if (!t) return null
  // Accept HH:MM or HH:MM:SS
  const parts = t.split(':').map(p => parseInt(p, 10))
  if (parts.length < 2 || isNaN(parts[0]) || isNaN(parts[1])) return null
  return parts[0] * 60 + parts[1]
}

// Format minutes or HH:MM string to 12-hour display
const formatTime12 = (t) => {
  if (t == null) return ''
  let mins
  if (typeof t === 'string') {
    const p = t.split(':').map(x => parseInt(x, 10))
    if (p.length < 2 || isNaN(p[0]) || isNaN(p[1])) return t
    mins = p[0] * 60 + p[1]
  } else {
    mins = Number(t)
  }
  const h = Math.floor(mins / 60) % 24
  const m = mins % 60
  const period = h >= 12 ? 'PM' : 'AM'
  let hh = h % 12
  if (hh === 0) hh = 12
  const mm = m.toString().padStart(2, '0')
  return `${hh}:${mm} ${period}`
}

// Check if a given HH:MM time string fits within branch hours for selected branch/date
const isTimeWithinBranchHours = (timeStr) => {
  if (!timeStr) return false
  const branchId = appointmentForm.value.branch
  const dateStr = appointmentForm.value.appointment_date
  if (!branchId || !dateStr) return true // no branch/date selected => allow any
  const branch = branches.value.find(b => String(b.id) === String(branchId))
  if (!branch) return true
  const hours = getBranchHoursForDate(branch, dateStr)
  if (!hours || hours.closed) return false
  const startM = parseTimeToMinutes(timeStr.toString().slice(0,5))
  if (startM === null) return false
  const duration = Number(appointmentForm.value.duration) || 30
  // start must be >= open and end <= close
  return (startM >= hours.openM) && ((startM + duration) <= hours.closeM)
}

// Determine branch operating hours for a given date string (YYYY-MM-DD)
const getBranchHoursForDate = (branchObj, dateString) => {
  if (!branchObj || !dateString) return null
  const d = new Date(dateString + 'T00:00:00')
  if (isNaN(d)) return null
  const day = d.getDay() // 0 = Sunday, 1 = Monday, ...
  const map = ['sunday', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday']
  const prefix = map[day]
  const closedFlag = branchObj[`${prefix}_closed`]
  if (closedFlag) return { closed: true }
  const openRaw = branchObj[`${prefix}_open`] || branchObj[`${prefix}_open_time`] || null
  const closeRaw = branchObj[`${prefix}_close`] || branchObj[`${prefix}_close_time`] || null
  if (!openRaw || !closeRaw) return { closed: true }
  // openRaw may be "09:00:00" or "09:00"
  const openM = parseTimeToMinutes(openRaw.toString().slice(0,5))
  const closeM = parseTimeToMinutes(closeRaw.toString().slice(0,5))
  if (openM === null || closeM === null) return { closed: true }
  return { closed: false, openM, closeM }
}

// Compute available time slots within branch hours for selected date and duration
const availableTimeSlots = computed(() => {
  const branchId = appointmentForm.value.branch
  const dateStr = appointmentForm.value.appointment_date
  const duration = Number(appointmentForm.value.duration) || 30
  const interval = 15 // slot step in minutes
  if (!branchId || !dateStr) return []
  const branch = branches.value.find(b => String(b.id) === String(branchId))
  if (!branch) return []
  const hours = getBranchHoursForDate(branch, dateStr)
  if (!hours || hours.closed) return []
  const slots = []
  const start = hours.openM
  const end = hours.closeM
  // last possible start is end - duration
  const lastStart = end - duration
  for (let t = start; t <= lastStart; t += interval) {
    const hh = Math.floor(t / 60).toString().padStart(2, '0')
    const mm = (t % 60).toString().padStart(2, '0')
    slots.push(`${hh}:${mm}`)
  }
  return slots
})

const intervalsOverlap = (startA, durA, startB, durB) => {
  const a0 = startA
  const a1 = startA + (durA || 0)
  const b0 = startB
  const b1 = startB + (durB || 0)
  return (a0 < b1) && (b0 < a1)
}

const checkConflicts = () => {
  conflictWarning.value = ''
  conflictingAppointments.value = []
  // If a holiday or request-limit warning is active, keep submission disabled
  if (typeof dateHolidayWarning !== 'undefined' && dateHolidayWarning.value) {
    submitDisabled.value = true
    return
  }
  if (typeof requestLimitWarning !== 'undefined' && requestLimitWarning.value) {
    submitDisabled.value = true
    return
  }
  // If an existing-appointment warning is active, keep submission disabled
  if (typeof existingAppointmentWarning !== 'undefined' && existingAppointmentWarning.value) {
    submitDisabled.value = true
    return
  }
  submitDisabled.value = false

  const date = appointmentForm.value.appointment_date
  const time = appointmentForm.value.appointment_time
  const dentistSelected = appointmentForm.value.dentist // empty means Any
  const duration = Number(appointmentForm.value.duration) || 30

  if (!date || !time) return

  // If dentist is Any or not selected, don't block submission
  if (!dentistSelected) return

  const startM = parseTimeToMinutes(time)
  if (startM === null) return

  // Find scheduled appointments on this date for the same dentist
  const conflicts = dateAppointments.value.filter(apt => {
    if (!apt) return false
    if (apt.appointment_date !== date) return false
    // Only consider scheduled appointments
    if (apt.status !== 'scheduled') return false
    const aptDentistId = getAppointmentDentistUserId(apt)
    if (!aptDentistId) return false
    if (String(aptDentistId) !== String(dentistSelected)) return false
    const aptStart = parseTimeToMinutes(apt.appointment_time)
    const aptDur = Number(apt.duration) || 30
    if (aptStart === null) return false
    // If the apt is the same as the current in-edit appointment (no id or different), still count as conflict
    return intervalsOverlap(startM, duration, aptStart, aptDur)
  })

  if (conflicts.length > 0) {
    conflictingAppointments.value = conflicts
    submitDisabled.value = true
    // Build warning message with 12-hour formatted start and computed end time
    const format12 = (mins) => {
      const h = Math.floor(mins / 60) % 24
      const m = mins % 60
      const period = h >= 12 ? 'PM' : 'AM'
      let hh = h % 12
      if (hh === 0) hh = 12
      const mm = m.toString().padStart(2, '0')
      return `${hh}:${mm} ${period}`
    }

    const entries = conflicts.map(c => {
      const aptStart = parseTimeToMinutes(c.appointment_time)
      const aptDur = Number(c.duration) || 30
      const start12 = aptStart !== null ? format12(aptStart) : (c.appointment_time || 'N/A')
      const end12 = aptStart !== null ? format12(aptStart + aptDur) : `(+${aptDur}m)`
      return `${start12} - ${end12}`
    })

    // If multiple conflicts, join them with "; " otherwise single entry
    const timesText = entries.length === 1 ? entries[0] : entries.join('; ')

    // Build HTML formatted warning: header, line break, italicized message with bold keywords
    conflictWarning.value = `SCHEDULE CONFLICT!<br><i>Selected dentist already has appointment at ${timesText}. Please choose a different <b>Time</b>, different <b>Dentist</b> or select <b>Any</b>.</i>`
  }
}

// Watch relevant fields to re-check conflicts
watch(() => appointmentForm.value.appointment_time, () => {
  // Reset any previous time warning
  timeWarning.value = ''
  // If branch & date are selected, validate the time against branch hours
  if (appointmentForm.value.branch && appointmentForm.value.appointment_date && appointmentForm.value.appointment_time) {
    const ok = isTimeWithinBranchHours(appointmentForm.value.appointment_time)
    if (!ok) {
      // Keep the user's input but warn and prevent submission
      const branch = branches.value.find(b => String(b.id) === String(appointmentForm.value.branch))
      const branchLabel = branch ? (branch.name || branch.title || ('Branch ' + branch.id)) : 'selected branch'
      const hours = branch ? getBranchHoursForDate(branch, appointmentForm.value.appointment_date) : null
      let hoursText = ''
      if (hours && !hours.closed) {
        hoursText = `${formatTime12(hours.openM)} - ${formatTime12(hours.closeM)}`
      }
      timeWarning.value = `Selected time is outside operating hours for ${branchLabel}${hoursText ? (' (' + hoursText + ')') : ''}. Please choose a time within operating hours.`
      submitDisabled.value = true
      return
    }
  }
  // If valid, re-check conflicts
  checkConflicts()
})
watch(() => appointmentForm.value.dentist, () => { checkConflicts() })
watch(() => appointmentForm.value.duration, () => { checkConflicts() })
watch(() => appointmentForm.value.appointment_date, () => { loadDateAppointments(); checkConflicts() })
watch(dateAppointments, () => { checkConflicts() })

// When branch changes, if currently selected dentist isn't in that branch, clear selection
watch(() => appointmentForm.value.branch, (newBranch) => {
  if (!newBranch) return
  const selectedDentist = appointmentForm.value.dentist
  if (!selectedDentist) return

  // check if selected dentist exists in current filtered dentists
  const found = dentists.value.find(e => String(getEmployeeUserId(e)) === String(selectedDentist) || String(e.id) === String(selectedDentist))
  if (!found) {
    appointmentForm.value.dentist = ''
    checkConflicts()
  }
})

// When branch or date changes, if branch has available time slots, set default time to first slot
watch(() => [appointmentForm.value.branch, appointmentForm.value.appointment_date], ([b, d]) => {
  if (!b || !d) return
  // Only auto-fill if user hasn't already entered a time
  if (appointmentForm.value.appointment_time) return
  const slots = availableTimeSlots.value
  if (slots && slots.length > 0) {
    appointmentForm.value.appointment_time = slots[0]
  }
}, { immediate: false })

const loadEmployees = async () => {
  try {
    const response = await api.get('/employees/')
    // Optionally filter to dentist positions; keep full list and let user choose
    employees.value = response.data
  } catch (error) {
    console.error('Error loading employees:', error)
    employees.value = []
  }
}

const positions = ref([])

const loadPositions = async () => {
  try {
    const response = await api.get('/positions/')
    positions.value = response.data
  } catch (error) {
    console.error('Error loading positions:', error)
    positions.value = []
  }
}

const dentistPositionIds = computed(() => {
  return positions.value
    .filter(p => (p.title || p.name || (p.code || '')).toString().toLowerCase().includes('dentist'))
    .map(p => p.id)
})

const dentists = computed(() => {
  return employees.value.filter(emp => {
    if (!emp) return false

    // Determine if employee's position indicates a dentist
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

    // If not yet identified as dentist, check textual title on position
    if (!isDentist) {
      const titleText = (typeof posCandidate === 'string') ? posCandidate : (emp.position && (emp.position.title || emp.position.name)) || ''
      if (titleText && titleText.toString().toLowerCase().includes('dentist')) isDentist = true
    }

    if (!isDentist) return false

    // If a preferred branch is selected, ensure employee is assigned to that branch
    const preferredBranch = appointmentForm.value.branch
    if (preferredBranch) {
      // emp.branch may be an object or an id
      const empBranchRaw = emp.branch || (emp.branch_id || null)
      const empBranchId = empBranchRaw && typeof empBranchRaw === 'object' ? empBranchRaw.id : empBranchRaw
      if (!empBranchId) return false
      if (String(empBranchId) !== String(preferredBranch)) return false
    }

    return true
  })
})

const formatDentistDisplay = (emp) => {
  if (!emp) return ''
  // Title by gender: Male -> Dr., Female -> Dra., Other/unknown -> Dr.
  const title = emp.gender === 'F' ? 'Dra.' : 'Dr.'
  // Build full name using middle initial only when present
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

// Resolve the user id associated with an employee record (handles nested shapes)
const getEmployeeUserId = (emp) => {
  if (!emp) return null
  // emp.user may be an object ({id:...}) or a numeric id, or emp.user_id may exist
  if (emp.user && typeof emp.user === 'object' && emp.user.id) return emp.user.id
  if (emp.user && (typeof emp.user === 'number' || typeof emp.user === 'string')) return emp.user
  if (emp.user_id) return emp.user_id
  return null
}

const getDentistDisplay = (apt) => {
  if (!apt) return 'Unassigned'
  // Normalize dentist value from appointment to the user id (handles nested shapes)
  const rawDentist = (apt && (apt.dentist ?? apt.dentist_id)) || (apt && apt.dentist && apt.dentist.id) || null
  const dentistId = (rawDentist && typeof rawDentist === 'object') ? rawDentist.id : rawDentist
  if (dentistId) {
    // Match employee by linked user id only (employee.user or employee.user.id)
    const emp = employees.value.find(e => e && String(getEmployeeUserId(e)) === String(dentistId))
    const base = emp ? formatDentistDisplay(emp) : (apt.dentist_name || 'Unassigned')
    // Display only the formatted dentist name on the front-end (do not append id)
    return base
  }
  // Fall back to serializer-provided dentist_name or Unassigned
  return apt.dentist_name || 'Unassigned'
}

const selectDentistFromApt = (apt) => {
  if (!apt) return
  // Normalize dentist id from appointment shapes
  const raw = apt.dentist || apt.dentist_id || (apt.dentist && apt.dentist.id) || null
  const dentistUserId = (raw && typeof raw === 'object') ? raw.id : raw
  if (dentistUserId) {
    appointmentForm.value.dentist = dentistUserId
    onPreferredDentistChange()
    checkConflicts()
  }
}

const minDate = computed(() => {
  const tomorrow = new Date()
  tomorrow.setDate(tomorrow.getDate() + 1)
  return tomorrow.toISOString().split('T')[0]
})

const maxPreferredDate = computed(() => {
  const d = new Date()
  d.setDate(d.getDate() + 1 + 14) // tomorrow + 14 days
  return d.toISOString().split('T')[0]
})

onMounted(async () => {
  await loadPatientProfile()
  // preload employees for dentist selection
  // load both employees and positions so we can filter dentists by position_id
  await Promise.all([loadEmployees(), loadPositions(), loadBranches()])
})

const loadPatientProfile = async () => {
  try {
    loading.value = true
    
    // Get current user to find patient ID
    const userResponse = await api.get('/current-user/')
    const username = userResponse.data.username
    
    // Check if user needs to change password
    if (userResponse.data.force_password_change) {
      forcePasswordChange.value = true
      showPasswordModal.value = true
      document.body.classList.add('modal-open')
      
      Swal.fire({
        icon: 'warning',
        title: 'Password Change Required',
        text: 'You must change your password before continuing.',
        allowOutsideClick: false,
        allowEscapeKey: false,
        confirmButtonText: 'OK'
      })
    }
    
    // Get patient by patient_id (which is the username)
    const patientsResponse = await api.get('/patient/patients/', {
      params: { search: username }
    })
    
    if (patientsResponse.data.length > 0) {
      patient.value = patientsResponse.data[0]
      await loadAppointments()
      await loadTreatments()
      await loadUnreadCount()
    }
  } catch (error) {
    console.error('Error loading patient profile:', error)
    Swal.fire({
      icon: 'error',
      title: 'Error',
      text: 'Unable to load your profile. Please try again.'
    })
  } finally {
    loading.value = false
  }
}

const loadAppointments = async (date = '') => {
  try {
    loadingAppointments.value = true
    const params = {}
    if (date) params.appointment_date = date
    const response = await api.get(`/patient/patients/${patient.value.id}/appointments/`, { params })
    let items = (response.data || [])

    // If the backend ignores the appointment_date param, apply a client-side filter
    const filterDate = date || appointmentDateFilter.value || ''
    if (filterDate) {
      items = items.filter(a => {
        if (!a) return false
        const d = String(a.appointment_date || '').split('T')[0]
        return d === String(filterDate)
      })
    }

    appointments.value = items.sort((a, b) => 
      new Date(b.appointment_date) - new Date(a.appointment_date)
    )
  } catch (error) {
    console.error('Error loading appointments:', error)
  } finally {
    loadingAppointments.value = false
  }
}

const refreshAppointments = async () => {
  await loadAppointments(appointmentDateFilter.value || '')
}

// Auto-refresh appointments when the date filter changes (debounced)
watch(() => appointmentDateFilter.value, (newVal) => {
  if (appointmentFilterTimer) clearTimeout(appointmentFilterTimer)
  appointmentFilterTimer = setTimeout(() => {
    refreshAppointments()
  }, 300)
})

const updateAppointment = async (apt) => {
  if (!apt) return
  editingId.value = apt.id
  // Prefill form with appointment data for editing
  appointmentForm.value.appointment_date = apt.appointment_date || ''
  appointmentForm.value.appointment_time = apt.appointment_time || '09:00'
  appointmentForm.value.appointment_type = apt.appointment_type || ''
  appointmentForm.value.other_type = apt.other_type || ''
  appointmentForm.value.dentist = (apt.dentist && apt.dentist.id) || apt.dentist || apt.dentist_id || ''
  appointmentForm.value.duration = apt.duration || 30
  appointmentForm.value.branch = (apt.branch && apt.branch.id) || apt.branch || apt.branch_id || ''
  appointmentForm.value.reason = apt.reason || ''
  appointmentForm.value.notes = apt.notes || ''
  // Open modal for editing
  showAppointmentModal.value = true
  document.body.classList.add('modal-open')
}

const resubmitAppointment = async (apt) => {
  if (!apt) return
  try {
    // If the appointment has an id, update its status to 'requested' instead of creating a duplicate
    const aptId = apt.id || apt.appointment_id || apt.pk
    if (aptId) {
      await api.patch(`/patient/appointments/${aptId}/`, { status: 'requested' })
      Swal.fire({ icon: 'success', title: 'Resubmitted', html: 'Appointment status updated to requested.<br>Our staff will review again and reconfirm your appointment shortly' })
    } else {
      // Fallback: create a new request if no id is available
      const payload = {
        patient: patient.value.id,
        appointment_date: apt.appointment_date,
        appointment_time: apt.appointment_time,
        appointment_type: apt.appointment_type,
        dentist: (apt.dentist && apt.dentist.id) || apt.dentist || apt.dentist_id || null,
        duration: apt.duration || 30,
        reason: apt.reason || '',
        notes: apt.notes || '',
        status: 'requested'
      }
      await api.post('/patient/appointments/', payload)
      Swal.fire({ icon: 'success', title: 'Resubmitted', text: 'Appointment request has been resubmitted.' })
    }
    await loadAppointments(appointmentDateFilter.value || '')
  } catch (err) {
    console.error('Error resubmitting appointment:', err)
    Swal.fire({ icon: 'error', title: 'Error', text: 'Unable to resubmit appointment.' })
  }
}

const loadTreatments = async () => {
  try {
    loadingTreatments.value = true
    const response = await api.get(`/patient/patients/${patient.value.id}/treatments/`)
    treatments.value = response.data.sort((a, b) => 
      new Date(b.treatment_date) - new Date(a.treatment_date)
    )
  } catch (error) {
    console.error('Error loading treatments:', error)
  } finally {
    loadingTreatments.value = false
  }
}

const loadMessages = async () => {
  try {
    loadingMessages.value = true
    const response = await api.get('/patient/messages/inbox/')
    messages.value = response.data
  } catch (error) {
    console.error('Error loading messages:', error)
  } finally {
    loadingMessages.value = false
  }
}

const loadUnreadCount = async () => {
  try {
    const response = await api.get('/patient/messages/unread_count/')
    unreadCount.value = response.data.count
  } catch (error) {
    console.error('Error loading unread count:', error)
  }
}

const handleMessagesTabClick = async () => {
  activeTab.value = 'messages'
  if (messages.value.length === 0) {
    await loadMessages()
  }
}

const loadDateAppointments = async () => {
  if (!appointmentForm.value.appointment_date) {
    dateAppointments.value = []
    return
  }
  
  try {
    loadingDateAppointments.value = true
    const response = await api.get('/patient/appointments/', {
      params: {
        appointment_date: appointmentForm.value.appointment_date
      }
    })
    
    // Filter appointments for this specific date and include only those with status 'scheduled'
    dateAppointments.value = response.data.filter(apt => 
      apt.appointment_date === appointmentForm.value.appointment_date &&
      apt.status === 'scheduled'
    ).sort((a, b) => a.appointment_time.localeCompare(b.appointment_time))
  } catch (error) {
    console.error('Error loading date appointments:', error)
    dateAppointments.value = []
  } finally {
    loadingDateAppointments.value = false
  }
}

// Watch for date changes to load appointments
watch(() => appointmentForm.value.appointment_date, () => {
  loadDateAppointments()
})

const openMessage = async (message) => {
  selectedMessage.value = message
  showMessageModal.value = true
  document.body.classList.add('modal-open')
  
  // Mark as read if unread
  if (!message.is_read) {
    try {
      await api.post(`/patient/messages/${message.id}/mark_read/`)
      message.is_read = true
      unreadCount.value = Math.max(0, unreadCount.value - 1)
    } catch (error) {
      console.error('Error marking message as read:', error)
    }
  }
}

const closeMessageModal = () => {
  showMessageModal.value = false
  selectedMessage.value = null
  document.body.classList.remove('modal-open')
}

const getMessagePreview = (body) => {
  if (!body) return ''
  return body.length > 100 ? body.substring(0, 100) + '...' : body
}

const getMessageTypeBadge = (type) => {
  const classes = {
    message: 'badge badge-primary',
    notification: 'badge badge-info',
    system: 'badge badge-warning'
  }
  return classes[type] || 'badge badge-secondary'
}

const formatDate = (dateString) => {
  if (!dateString) return 'N/A'
  const date = new Date(dateString)
  return date.toLocaleDateString('en-US', { 
    year: 'numeric', 
    month: 'long', 
    day: 'numeric' 
  })
}

const formatStatus = (status) => {
  if (!status) return 'N/A'
  return status.replace(/_/g, ' ').toUpperCase()
}

const capitalizeFirst = (str) => {
  if (!str) return ''
  return str.charAt(0).toUpperCase() + str.slice(1)
}

const getStatusBadgeClass = (status) => {
  const classes = {
    active: 'badge badge-success',
    inactive: 'badge badge-warning',
    archived: 'badge badge-secondary'
  }
  return classes[status] || 'badge badge-secondary'
}

const getAppointmentStatusClass = (status) => {
  const classes = {
    scheduled: 'badge badge-primary',
    confirmed: 'badge badge-info',
    completed: 'badge badge-success',
    cancelled: 'badge badge-danger',
    no_show: 'badge badge-warning'
  }
  return classes[status] || 'badge badge-secondary'
}

const getPaymentStatusClass = (status) => {
  const classes = {
    paid: 'badge badge-success',
    partial: 'badge badge-warning',
    unpaid: 'badge badge-danger'
  }
  return classes[status] || 'badge badge-secondary'
}

const showChangePasswordModal = () => {
  showPasswordModal.value = true
  document.body.classList.add('modal-open')
}

const closeChangePasswordModal = () => {
  // Prevent closing if password change is forced
  if (forcePasswordChange.value) {
    Swal.fire({
      icon: 'warning',
      title: 'Password Change Required',
      text: 'You must change your password before continuing.',
      confirmButtonText: 'OK'
    })
    return
  }
  
  showPasswordModal.value = false
  document.body.classList.remove('modal-open')
  passwordForm.value = {
    current: '',
    new: '',
    confirm: ''
  }
}

const changePassword = async () => {
  if (passwordForm.value.new !== passwordForm.value.confirm) {
    Swal.fire({
      icon: 'error',
      title: 'Error',
      text: 'New passwords do not match'
    })
    return
  }

  if (passwordForm.value.new.length < 6) {
    Swal.fire({
      icon: 'error',
      title: 'Error',
      text: 'Password must be at least 6 characters'
    })
    return
  }

  try {
    await api.post('/change-password/', {
      current_password: passwordForm.value.current,
      new_password: passwordForm.value.new
    })

    // Clear force password change flag
    forcePasswordChange.value = false

    Swal.fire({
      icon: 'success',
      title: 'Success',
      text: 'Password changed successfully'
    })

    showPasswordModal.value = false
    document.body.classList.remove('modal-open')
    passwordForm.value = {
      current: '',
      new: '',
      confirm: ''
    }
  } catch (error) {
    Swal.fire({
      icon: 'error',
      title: 'Error',
      text: error.response?.data?.error || 'Failed to change password'
    })
  }
}

const showRequestAppointmentModal = () => {
  // Reset form
  // Ensure we are not in editing mode when creating a fresh request
  editingId.value = null
  const tomorrow = new Date()
  tomorrow.setDate(tomorrow.getDate() + 1)
  appointmentForm.value = {
    appointment_date: tomorrow.toISOString().split('T')[0],
    appointment_time: '09:00',
    appointment_type: '',
    other_type: '',
    dentist: '',
    duration: 30,
    branch: '',
    reason: '',
    notes: ''
  }
  conflictWarning.value = ''
  conflictingAppointments.value = []
  submitDisabled.value = false
  // Preload holidays and validate the default date
  fetchHolidays().then(() => checkPreferredDateHoliday(appointmentForm.value.appointment_date))
  showAppointmentModal.value = true
  document.body.classList.add('modal-open')
}

const onPreferredDentistChange = () => {
  const selected = appointmentForm.value.dentist || ''
  // Re-evaluate conflicts when preferred dentist changes
  checkConflicts()
}

const closeAppointmentModal = () => {
  showAppointmentModal.value = false
  document.body.classList.remove('modal-open')
  // Reset editing state when closing the modal
  editingId.value = null
  submitDisabled.value = false
}

const submitAppointmentRequest = async () => {
  try {
    const wasEditing = Boolean(editingId.value)
    // Ensure selected date is within allowed range
    checkPreferredDateRange(appointmentForm.value.appointment_date)
    if (dateRangeWarning.value) {
      Swal.fire({ icon: 'warning', title: 'Invalid Date', text: dateRangeWarning.value })
      return
    }
    // Re-check request limits before attempting submission only for new requests
    if (!editingId.value) {
      await checkRequestLimits(appointmentForm.value.appointment_date)
      if (requestLimitWarning.value) {
        Swal.fire({
          icon: 'warning',
          title: 'Request Limit',
          text: requestLimitWarning.value,
          confirmButtonText: 'OK'
        })
        return
      }
    }

    // Prevent submission if selected date is a holiday
    if (dateHolidayWarning.value) {
      Swal.fire({
        icon: 'warning',
        title: 'Holiday Selected',
        html: dateHolidayWarning.value,
        confirmButtonText: 'OK'
      })
      return
    }
    // Validate manual time input against branch hours before attempting submission
    if (appointmentForm.value.branch && appointmentForm.value.appointment_date && appointmentForm.value.appointment_time) {
      const ok = isTimeWithinBranchHours(appointmentForm.value.appointment_time)
      if (!ok) {
        Swal.fire({
          icon: 'error',
          title: 'Invalid Time',
          text: timeWarning.value || 'Selected time is outside operating hours for the chosen branch.'
        })
        return
      }
    }
    // First, check if the time slot is available
    const checkResponse = await api.get('/patient/appointments/', {
      params: {
        appointment_date: appointmentForm.value.appointment_date,
        appointment_time: appointmentForm.value.appointment_time
      }
    })

    // Check if there are any appointments at the same date and time
    const existingAppointments = checkResponse.data.filter(apt => 
      apt.appointment_date === appointmentForm.value.appointment_date &&
      apt.appointment_time === appointmentForm.value.appointment_time &&
      apt.status !== 'cancelled' &&
      apt.status !== 'no_show'
    )

    if (existingAppointments.length > 0) {
      Swal.fire({
        icon: 'warning',
        title: 'Time Slot Not Available',
        text: 'This date and time slot is already booked. Please choose a different time.',
        confirmButtonText: 'OK'
      })
      return
    }

    // Create appointment with patient ID and status as 'requested'
    let appointmentNotes = appointmentForm.value.notes
    
    // If appointment type is 'other', prepend the custom type to notes
    if (appointmentForm.value.appointment_type === 'other' && appointmentForm.value.other_type) {
      appointmentNotes = `Appointment Type: ${appointmentForm.value.other_type}\n\n${appointmentNotes || ''}`
    }
    
    let response
    const payload = {
      patient: patient.value.id,
      appointment_date: appointmentForm.value.appointment_date,
      appointment_time: appointmentForm.value.appointment_time,
      appointment_type: appointmentForm.value.appointment_type,
      dentist: appointmentForm.value.dentist || null,
      duration: appointmentForm.value.duration || 30,
      reason: appointmentForm.value.reason,
      notes: appointmentNotes
    }


    if (wasEditing) {
      response = await api.patch(`/patient/appointments/${editingId.value}/`, payload)
      editingId.value = null
    } else {
      payload.status = 'requested'
      response = await api.post('/patient/appointments/', payload)
    }

    // Show success message; for updates include a newline separator
    if (wasEditing) {
      Swal.fire({
        icon: 'success',
        title: 'Appointment Updated',
        html: 'Appointment updated successfully.<br>You can now resubmit your request.',
        confirmButtonText: 'OK'
      })
    } else {
      Swal.fire({
        icon: 'success',
        title: 'Request Submitted',
        text: 'Your appointment request has been submitted successfully. We will contact you shortly to confirm.',
        confirmButtonText: 'OK'
      })
    }

    closeAppointmentModal()
    
    // Reload appointments if on that tab
    if (activeTab.value === 'appointments') {
      await loadAppointments()
    }
  } catch (error) {
    console.error('Error submitting appointment request:', error)
    
    // Get detailed error message
    let errorMessage = 'Failed to submit appointment request. Please try again.'
    if (error.response?.data) {
      if (typeof error.response.data === 'string') {
        errorMessage = error.response.data
      } else if (error.response.data.error) {
        errorMessage = error.response.data.error
      } else if (error.response.data.detail) {
        errorMessage = error.response.data.detail
      } else {
        // Try to get first error from field errors
        const firstError = Object.values(error.response.data)[0]
        if (Array.isArray(firstError)) {
          errorMessage = firstError[0]
        } else if (typeof firstError === 'string') {
          errorMessage = firstError
        }
      }
    }
    
    Swal.fire({
      icon: 'error',
      title: 'Error',
      text: errorMessage
    })
  }
}

const handleLogout = async () => {
  showUserDropdown.value = false
  const result = await Swal.fire({
    title: 'Logout',
    text: 'Are you sure you want to logout?',
    icon: 'question',
    showCancelButton: true,
    confirmButtonColor: '#3085d6',
    cancelButtonColor: '#d33',
    confirmButtonText: 'Yes, logout'
  })

  if (result.isConfirmed) {
    await authStore.logout()
    router.push('/login')
  }
}

const toggleDropdown = () => {
  showUserDropdown.value = !showUserDropdown.value
}

const getPhotoUrl = (photoPath) => {
  if (!photoPath) return ''
  if (photoPath.startsWith('http')) return photoPath
  return `http://127.0.0.1:8000${photoPath}`
}

const handlePhotoUpload = async (event) => {
  const file = event.target.files[0]
  if (!file) return

  // Validate file type
  if (!file.type.startsWith('image/')) {
    Swal.fire({
      icon: 'error',
      title: 'Invalid File',
      text: 'Please select an image file'
    })
    return
  }

  // Validate file size (max 5MB)
  if (file.size > 5 * 1024 * 1024) {
    Swal.fire({
      icon: 'error',
      title: 'File Too Large',
      text: 'Please select an image smaller than 5MB'
    })
    return
  }

  try {
    uploadingPhoto.value = true
    const formData = new FormData()
    formData.append('photo', file)

    const response = await api.post(`/patient/patients/${patient.value.id}/upload_photo/`, formData, {
      headers: {
        'Content-Type': 'multipart/form-data'
      }
    })

    patient.value = response.data
    
    Swal.fire({
      icon: 'success',
      title: 'Success',
      text: 'Profile photo updated successfully',
      timer: 2000,
      showConfirmButton: false
    })
  } catch (error) {
    console.error('Error uploading photo:', error)
    Swal.fire({
      icon: 'error',
      title: 'Upload Failed',
      text: 'Unable to upload photo. Please try again.'
    })
  } finally {
    uploadingPhoto.value = false
    event.target.value = ''
  }
}
</script>

<style scoped>
.wrapper {
  min-height: 100vh;
  background-color: #f4f6f9;
}

.content-wrapper {
  margin-left: 0 !important;
  min-height: calc(100vh - 57px);
}

.profile-user-img-placeholder {
  margin: 0 auto;
  padding: 10px;
}

.profile-user-img {
  width: 100px;
  height: 100px;
  object-fit: cover;
}

.card-header {
  background-color: #fff !important;
  border-bottom: none !important;
}

.nav-tabs {
  border-bottom: 1px solid #dee2e6;
}

.nav-tabs .nav-link {
  cursor: pointer;
}

.tab-pane {
  animation: fadeIn 0.3s;
}

@keyframes fadeIn {
  from { opacity: 0; }
  to { opacity: 1; }
}

.table-responsive {
  max-height: 400px;
  overflow-y: auto;
}

.appointments-list {
  max-height: 420px;
  overflow-y: auto;
}
.appointment-main {
  min-width: 0;
}
.appointment-header {
  font-size: 1rem;
}
.appointment-actions button { white-space: nowrap; }

.appointment-dentist {
  color: #444;
}
.appointment-notes {
  color: #666;
}
.appointment-dentist strong,
.appointment-notes strong {
  font-weight: 600;
  color: #222;
}

.appointment-actions {
  min-width: 110px;
  max-width: 140px;
}
 .appointment-actions .btn {
  width: 110px;
  min-width: 90px;
  box-sizing: border-box;
  padding: 8px 12px; /* increase horizontal padding to keep icon away from border */
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  overflow: visible;
 }

@media (max-width: 576px) {
  .appointment-actions { min-width: 0; }
  .appointment-actions .btn { 
    width: 100%; 
    display: block;
    box-sizing: border-box;
    padding: 6px 3px 4px 6px;
    white-space: normal;
    text-align: center;
    font-size: 0.95rem;
    min-width: 40px;
    margin-right: 20px;
  }
}

/* Date filter sizing */
.appointment-date-filter {
  min-width: 160px;
  max-width: 320px;
  box-sizing: border-box;
}

@media (max-width: 576px) {
  .appointment-date-filter {
    min-width: 140px;
    max-width: 100%;
  }
}

/* date filter label and wrapper */
.date-filter-wrap { display: inline-flex; align-items: center; gap: 8px; }
.date-filter-label, .date-filter-label-mobile {
  padding-top: 7px;
  font-weight: 600;
  color: #444; /* primary button color */
  font-size: 0.95rem;
}
.date-filter-label-mobile { display: none; }

@media (max-width: 576px) {
  .date-filter-label { display: none; }
  .date-filter-label-mobile { display: inline; font-size: 0.9rem; }
}

/* Button icon & text handling */
.btn-icon { margin-right: 6px; }
.btn-text { display: inline; }

@media (max-width: 576px) {
  .btn-icon { margin-right: 0; font-size: 1.05rem; display: inline-flex; width: 20px; text-align: center; align-items: center; justify-content: center; padding: 0 6px; }
  .btn-text { display: none; }
}

  @media (max-width: 576px) {
    .appointment-header {
      font-size: 0.85rem; /* smaller date/time on mobile */
      line-height: 1.2;
    }
    .appointment-meta {
      font-size: 0.78rem;
    }
  }

/* Mobile responsive - show icons only on small screens */
@media (max-width: 768px) {
  .nav-tabs .tab-text {
    display: none;
  }
  
  .nav-tabs .nav-link {
    padding: 0.5rem 1rem;
    font-size: 1.2rem;
  }
  
  .nav-tabs .nav-link i {
    margin: 0;
  }
}

/* User avatar in navbar */
.user-avatar {
  width: 32px;
  height: 32px;
  border-radius: 50%;
  object-fit: cover;
  border: 2px solid #fff;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

/* Dropdown menu */
.dropdown-menu {
  margin-top: 0.5rem;
}

/* Profile photo upload */
.profile-photo-wrapper {
  position: relative;
  display: inline-block;
}

.photo-upload-overlay {
  position: absolute;
  bottom: 0;
  right: 0;
  background-color: #007bff;
  width: 35px;
  height: 35px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: all 0.3s;
  border: 3px solid #fff;
}

.photo-upload-overlay:hover {
  background-color: #0056b3;
  transform: scale(1.1);
}

.photo-upload-label {
  margin: 0;
  cursor: pointer;
  color: white;
  font-size: 14px;
  display: flex;
  align-items: center;
  justify-content: center;
}

/* Messages */
.message-item {
  padding: 15px;
  border-bottom: 1px solid #dee2e6;
  cursor: pointer;
  transition: background-color 0.2s;
}

.message-item:hover {
  background-color: #f8f9fa;
}

.message-item.unread {
  background-color: #e7f3ff;
}

.message-item.unread:hover {
  background-color: #d0e8ff;
}

.message-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 8px;
}

.message-sender {
  font-size: 14px;
  display: flex;
  align-items: center;
}

.message-subject {
  font-weight: 600;
  margin-bottom: 5px;
  color: #333;
}

.message-preview {
  color: #666;
  font-size: 14px;
  line-height: 1.4;
}

.message-time {
  font-size: 12px;
}

.message-meta {
  background-color: #f8f9fa;
  padding: 15px;
  border-radius: 5px;
}

.message-body {
  padding: 15px 0;
  line-height: 1.6;
}

.brand-section {
  background-color: #2F404A;
  height: 57px;
  display: flex;
  align-items: center;
  padding: 0 20px;
  border-bottom: 3px solid #00B2A9;
}

.brand-box {
  color: white;
  display: inline-flex;
  align-items: center;
  gap: 10px;
}

.brand-logo-top {
  height: 28px;
  width: auto;
  object-fit: contain;
  margin-right: 8px;
}

.brand-box i {
  color: #00B2A9;
  font-size: 1.3rem;
}

.brand-box strong {
  font-size: 1.1rem;
}

.main-header.navbar {
  border-bottom: none !important;
}

.schedule-list {
  max-height: 200px;
  overflow-y: auto;
  margin-bottom: 10px;
}

.schedule-item {
  padding: 5px 0;
  border-bottom: 1px solid rgba(255, 255, 255, 0.2);
  font-size: 0.9rem;
}

.schedule-item:last-child {
  border-bottom: none;
}

.schedule-item i {
  margin-right: 5px;
}
</style>
