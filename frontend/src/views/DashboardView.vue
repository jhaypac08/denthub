<template>
  <div class="content-header">
    <div class="container-fluid">
      <div class="row mb-2">
        <div class="col-sm-6">
          <h1 class="m-0">Dashboard</h1>
        </div>
      </div>
    </div>
  </div>

  <section class="content">
    <div class="container-fluid">
      <!-- Stats Row -->
      <div class="row">
        <div class="col-lg-3 col-6">
          <div class="small-box bg-info" @click="navigateTo('/patients')" style="cursor: pointer;">
            <div class="inner">
              <h3>{{ stats.patientCount }}</h3>
              <p>Total Patients</p>
            </div>
            <div class="icon">
              <i class="fas fa-user-injured"></i>
            </div>
            <a href="#" class="small-box-footer" @click.prevent>
              More info <i class="fas fa-arrow-circle-right"></i>
            </a>
          </div>
        </div>

        <div class="col-lg-3 col-6">
          <div class="small-box bg-success" @click="navigateTo('/employees')" style="cursor: pointer;">
            <div class="inner">
              <h3>{{ stats.active }}</h3>
              <p>Active Employees</p>
            </div>
            <div class="icon">
              <i class="fas fa-user-check"></i>
            </div>
            <a href="#" class="small-box-footer" @click.prevent>
              More info <i class="fas fa-arrow-circle-right"></i>
            </a>
          </div>
        </div>

        <div class="col-lg-3 col-6">
          <div class="small-box bg-warning" @click="navigateTo('/appointments')" style="cursor: pointer;">
            <div class="inner">
              <h3>{{ stats.todayAppointments }}</h3>
              <p>Today's Appointments</p>
            </div>
            <div class="icon">
              <i class="fas fa-calendar-day"></i>
            </div>
            <a href="#" class="small-box-footer" @click.prevent>
              More info <i class="fas fa-arrow-circle-right"></i>
            </a>
          </div>
        </div>

        <div class="col-lg-3 col-6">
          <div class="small-box bg-danger" @click="navigateTo('/branches')" style="cursor: pointer;">
            <div class="inner">
              <h3>{{ branches.length }}</h3>
              <p>Branches</p>
            </div>
            <div class="icon">
              <i class="fas fa-building"></i>
            </div>
            <a href="#" class="small-box-footer" @click.prevent>
              More info <i class="fas fa-arrow-circle-right"></i>
            </a>
          </div>
        </div>
      </div>

      <!-- Welcome Card -->
      <div class="row">
        <div class="col-12">
          <div class="card">
            <div class="card-header">
              <h3 class="card-title">Welcome to DentHub Employee Management</h3>
            </div>
            <div class="card-body">
              <p>Welcome, {{ authStore.user?.first_name || authStore.user?.username }}!</p>
              <p>This is your employee management dashboard. Use the sidebar to navigate through the application.</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  </section>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth'
import api from '../services/api'

const router = useRouter()
const authStore = useAuthStore()

const stats = ref({
  patientCount: 0,
  active: 0,
  todayAppointments: 0
})

const branches = ref([])

const navigateTo = (path) => {
  router.push(path)
}

const fetchStats = async () => {
  try {
    const [employeesRes, branchesRes, patientsRes, appointmentsRes] = await Promise.all([
      api.get('/employees/'),
      api.get('/branches/'),
      api.get('/patient/patients/'),
      api.get('/patient/appointments/')
    ])
    
    const employees = employeesRes.data
    const patients = patientsRes.data
    const appointments = appointmentsRes.data
    
    // Count total patients
    stats.value.patientCount = patients.length
    stats.value.active = employees.filter(e => e.status === 'active').length
    
    // Count today's appointments
    const today = new Date().toISOString().split('T')[0]
    stats.value.todayAppointments = appointments.filter(a => a.appointment_date === today).length
    
    branches.value = branchesRes.data
  } catch (error) {
    console.error('Error fetching stats:', error)
  }
}

onMounted(() => {
  fetchStats()
})
</script>
