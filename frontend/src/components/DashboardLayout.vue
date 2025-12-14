<template>
  <div class="wrapper">
    <!-- Navbar -->
    <nav class="main-header navbar navbar-expand navbar-dark navbar-fixed-top" style="background-color: #2F404A; border-bottom: 3px solid #00B2A9; position: fixed; top: 0; left: 0; right: 0; z-index: 1030;">
      <!-- Left navbar links -->
      <ul class="navbar-nav">
        <li class="nav-item">
          <a class="nav-link text-white" data-widget="pushmenu" href="#" role="button">
            <i class="fas fa-bars"></i>
          </a>
        </li>
      </ul>

      <!-- Center navbar datetime -->
      <div class="navbar-center d-flex justify-content-center w-100">
        <div class="navbar-datetime text-white text-center" >
          <div class="navbar-date small">{{ todayDisplay }}</div>
          <div class="navbar-time small">{{ timeDisplay }}</div>
        </div>
      </div>

      <!-- Right navbar links -->
      <ul class="navbar-nav ml-auto align-items-center">
        <li class="nav-item">
          <a class="nav-link text-white profile-btn logout-btn d-flex align-items-center" href="#" @click.prevent="handleLogout">
            <i class="fas fa-sign-out-alt mr-1"></i>
            <span class="logout-text">Logout</span>
          </a>
        </li>
      </ul>
    </nav>

    <!-- Main Sidebar Container -->
    <aside class="main-sidebar sidebar-fixed elevation-4" style="background-color: #2F404A;">
      <!-- Brand Logo -->
      <a href="/" class="brand-link" style="background-color: rgba(0, 0, 0, 0.2); border-bottom: 1px solid rgba(255, 255, 255, 0.1);">
        <img :src="logoSrc" alt="DentHub" class="brand-logo" />
        <span class="brand-text font-weight-light text-white" style="font-size: 1.8rem;"><b>Dent</b>Hub</span>
      </a>

      <!-- Sidebar -->
      <div class="sidebar sidebar-scrollable">
        <!-- Sidebar user panel -->
        <div class="user-panel mt-3 pb-3 mb-3 d-flex flex-column align-items-center text-center user-panel-fixed">
          <div class="mb-2 d-flex flex-column align-items-center">
            <div>
            <img 
              v-if="userPhoto" 
              :src="userPhoto" 
              class="img-circle elevation-2" 
              alt="User Photo"
              style="width: 80px; height: 80px; object-fit: cover;"
            >
            <i v-else class="fas fa-user-circle fa-5x text-white-50"></i>
            </div>
          </div>
          <div class="info w-100">
            <p class="d-block text-white mb-1" style="font-size: 0.95rem;">
              {{ userFullName }}
            </p>
            <router-link 
              to="/profile" 
              class="btn btn-outline-light btn-sm btn-block profile-btn mb-1" 
              @click="closeSettings"
            >
              <i class="fas fa-user"></i> My Profile
            </router-link>
            <router-link 
              to="/messages" 
              class="btn btn-outline-light btn-sm btn-block profile-btn" 
              @click="closeSettings"
            >
              <i class="fas fa-envelope"></i> Messages
              <span v-if="unreadCount > 0" class="badge badge-danger ml-1">{{ unreadCount }}</span>
            </router-link>
          </div>
        </div>

        <!-- Sidebar Menu -->
        <nav class="mt-2 sidebar-menu-scrollable">
          <ul class="nav nav-pills nav-sidebar flex-column" data-widget="treeview" role="menu" data-accordion="false">
            <li class="nav-item">
              <router-link to="/" class="nav-link" active-class="active" exact-active-class="active" @click="closeSettings">
                <i class="nav-icon fas fa-tachometer-alt"></i>
                <p>Dashboard</p>
              </router-link>
            </li>
            <li class="nav-item">
              <router-link to="/employees" class="nav-link" active-class="active" @click="closeSettings">
                <i class="nav-icon fas fa-users"></i>
                <p>Employees</p>
              </router-link>
            </li>
            <li class="nav-item">
              <router-link to="/users" class="nav-link" active-class="active" @click="closeSettings">
                <i class="nav-icon fas fa-user-shield"></i>
                <p>Users</p>
              </router-link>
            </li>
            <li class="nav-item has-treeview" :class="{ 'menu-open': isSettingsOpen }">
              <a href="#" class="nav-link" :class="{ 'active': isSettingsActive }" @click.prevent="toggleSettings">
                <i class="nav-icon fas fa-cogs"></i>
                <p>
                  Others
                  <i class="right fas fa-angle-left" :class="{ 'rotate-arrow': isSettingsOpen }"></i>
                </p>
              </a>
              <transition name="slide-fade">
                <ul v-show="isSettingsOpen" class="nav nav-treeview">
                  <li class="nav-item">
                    <router-link to="/positions" class="nav-link" active-class="active">
                      <i class="fas fa-briefcase nav-icon"></i>
                      <p>Positions</p>
                    </router-link>
                  </li>
                  <li class="nav-item">
                    <router-link to="/departments" class="nav-link" active-class="active">
                      <i class="fas fa-sitemap nav-icon"></i>
                      <p>Departments</p>
                    </router-link>
                  </li>
                  <li class="nav-item">
                    <router-link to="/branches" class="nav-link" active-class="active">
                      <i class="fas fa-building nav-icon"></i>
                      <p>Branches</p>
                    </router-link>
                  </li>
                  <li class="nav-item">
                    <router-link to="/holidays" class="nav-link" active-class="active">
                      <i class="fas fa-umbrella-beach nav-icon"></i>
                      <p>Holidays</p>
                    </router-link>
                  </li>
                </ul>
              </transition>
            </li>

            <!-- Divider Line -->
            <hr class="sidebar-divider my-3" style="border-top: 1px solid rgba(255,255,255,0.2); margin-left: 1rem; margin-right: 1rem;">

            <!-- Public Website Header -->
            <li class="nav-header" style="color: #17a2b8; font-weight: bold;">PUBLIC WEBSITE</li>

            <!-- Website Content -->
            <li class="nav-item">
              <router-link to="/website-content" class="nav-link" active-class="active" @click="closeSettings">
                <i class="nav-icon fas fa-globe"></i>
                <p>Website Content</p>
              </router-link>
            </li>

            <!-- Divider Line -->
            <hr class="sidebar-divider my-3" style="border-top: 1px solid rgba(255,255,255,0.2); margin-left: 1rem; margin-right: 1rem;">

            <!-- Inventory Header -->
            <li class="nav-header" style="color: #17a2b8; font-weight: bold;">INVENTORY</li>

            <!-- Categories -->
            <li class="nav-item">
              <router-link to="/categories" class="nav-link" active-class="active" @click="closeSettings">
                <i class="nav-icon fas fa-tags"></i>
                <p>Categories</p>
              </router-link>
            </li>

            <!-- Items -->
            <li class="nav-item">
              <router-link to="/items" class="nav-link" active-class="active" @click="closeSettings">
                <i class="nav-icon fas fa-box"></i>
                <p>Items</p>
              </router-link>
            </li>

            <!-- Stock Movements -->
            <li class="nav-item">
              <router-link to="/stock-movements" class="nav-link" active-class="active" @click="closeSettings">
                <i class="nav-icon fas fa-exchange-alt"></i>
                <p>Stock Movements</p>
              </router-link>
            </li>

            <!-- Divider Line -->
            <hr class="sidebar-divider my-3" style="border-top: 1px solid rgba(255,255,255,0.2); margin-left: 1rem; margin-right: 1rem;">

            <!-- Patient Management Header -->
            <li class="nav-header" style="color: #17a2b8; font-weight: bold;">PATIENT MANAGEMENT</li>

            <!-- Patients -->
            <li class="nav-item">
              <router-link to="/patients" class="nav-link" active-class="active" @click="closeSettings">
                <i class="nav-icon fas fa-user-injured"></i>
                <p>Patients</p>
              </router-link>
            </li>

            <!-- Appointments -->
            <li class="nav-item">
              <router-link to="/appointments" class="nav-link" active-class="active" @click="closeSettings">
                <i class="nav-icon fas fa-calendar-check"></i>
                <p>Appointments</p>
              </router-link>
            </li>

            <!-- Treatment Records -->
            <li class="nav-item">
              <router-link to="/treatment-records" class="nav-link" active-class="active" @click="closeSettings">
                <i class="nav-icon fas fa-file-medical"></i>
                <p>Treatment Records</p>
              </router-link>
            </li>
          </ul>
        </nav>
        <!-- Bottom spacing -->
        <div style="height: 60px;"></div>
      </div>
    </aside>

    <!-- Content Wrapper -->
    <div class="content-wrapper" style="margin-top: 57px;">
      <router-view />
    </div>

    <!-- Footer -->
    <footer class="main-footer">
      <strong>DentHub Management System &copy;</strong> <i>All rights reserved 2025.</i> 
      <div class="float-right d-none d-sm-inline-block">
        <b>Version</b> 1.0.0
      </div>
    </footer>
  </div>
</template>

<script setup>
import logoSrc from '../../frontend/src/assets/icon_nobg.png'
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useAuthStore } from '../stores/auth'
import api from '../services/api'
import Swal from 'sweetalert2'

const router = useRouter()
const route = useRoute()
const authStore = useAuthStore()

const isSettingsOpen = ref(false)
const userPhoto = ref(null)
const unreadCount = ref(0)
const userFullName = computed(() => {
  const user = authStore.user
  if (user) {
    const firstName = user.first_name || ''
    const lastName = user.last_name || ''
    return `${firstName} ${lastName}`.trim() || user.username
  }
  return ''
})

const isSettingsActive = computed(() => {
  return ['/positions', '/departments', '/branches'].includes(route.path)
})

// Display today's date (moved to navbar)
const todayDisplay = ref(`${new Date().toLocaleDateString('en-US', { weekday: 'long', month: 'long', day: 'numeric', year: 'numeric' })}`)
// Live clock (shown in navbar)
const timeDisplay = ref(new Date().toLocaleTimeString('en-US', { hour: 'numeric', minute: '2-digit', second: '2-digit' }))
let _clockTimer = null

const toggleSettings = () => {
  isSettingsOpen.value = !isSettingsOpen.value
}

const closeSettings = () => {
  isSettingsOpen.value = false
}



const fetchUserData = async () => {
  try {
    const response = await api.get('/employees/')
    const employee = response.data.find(emp => emp.user === authStore.user?.id)
    if (employee && employee.photo) {
      userPhoto.value = employee.photo
    }
  } catch (error) {
    console.error('Error fetching user data:', error)
  }
}

const fetchUnreadCount = async () => {
  try {
    const response = await api.get('/messages/unread_count/')
    unreadCount.value = response.data.count
  } catch (error) {
    console.error('Error fetching unread count:', error)
  }
}

const handleLogout = async () => {
  const result = await Swal.fire({
    title: 'Are you sure?',
    text: 'You will be logged out of the system',
    icon: 'warning',
    showCancelButton: true,
    confirmButtonColor: '#3085d6',
    cancelButtonColor: '#d33',
    confirmButtonText: 'Yes, logout',
    cancelButtonText: 'Cancel'
  })
  
  if (result.isConfirmed) {
    await authStore.logout()
    router.push('/login')
  }
}

onMounted(() => {
  fetchUserData()
  fetchUnreadCount()

  // Refresh unread count every 30 seconds
  setInterval(fetchUnreadCount, 30000)

  // start live clock (update every second)
  _clockTimer = setInterval(() => {
    timeDisplay.value = new Date().toLocaleTimeString('en-US', { hour: 'numeric', minute: '2-digit', second: '2-digit' })
  }, 1000)
  // initialize immediately
  timeDisplay.value = new Date().toLocaleTimeString('en-US', { hour: 'numeric', minute: '2-digit', second: '2-digit' })

  
})

onUnmounted(() => {
  if (_clockTimer) {
    clearInterval(_clockTimer)
    _clockTimer = null
  }
})
</script>

<style scoped>
.profile-btn {
  transition: all 0.3s ease;
  border-color: rgba(255, 255, 255, 0.5);
}

.profile-btn:hover {
  background-color: #00B2A9 !important;
  border-color: #00B2A9 !important;
  color: white !important;
  transform: translateY(-1px);
  box-shadow: 0 2px 8px rgba(0, 178, 169, 0.4);
}

.nav-link {
  transition: all 0.2s ease;
  color: rgba(255, 255, 255, 0.8) !important;
}

.nav-link:hover {
  background-color: rgba(0, 178, 169, 0.15) !important;
  color: white !important;
}

.nav-link.active {
  background-color: rgba(0, 178, 169, 0.25) !important;
  border-left: 3px solid #00B2A9;
  color: white !important;
}

.sidebar .nav-treeview .nav-link {
  color: rgba(255, 255, 255, 0.7) !important;
}

.sidebar .nav-treeview .nav-link:hover {
  color: white !important;
}

/* Arrow rotation animation */
.right.fa-angle-left {
  transition: transform 0.4s ease-in-out;
  display: inline-block;
}

.right.fa-angle-left.rotate-arrow {
  transform: rotate(-90deg);
}

/* Dropdown slide animation */
.nav-treeview {
  overflow: hidden;
  transition: max-height 0.4s ease-in-out, opacity 0.4s ease-in-out;
  max-height: 0;
  opacity: 0;
}

.menu-open .nav-treeview {
  max-height: 500px;
  opacity: 1;
}

.slide-fade-enter-active,
.slide-fade-leave-active {
  transition: all 0.4s ease-in-out;
}

.slide-fade-enter-from {
  opacity: 0;
}

.slide-fade-enter-to {
  opacity: 1;
}

.slide-fade-leave-from {
  opacity: 1;
}

.slide-fade-leave-to {
  opacity: 0;
}

/* Fixed Sidebar Styles */
.sidebar-fixed {
  position: fixed !important;
  top: 0;
  bottom: 0;
  left: 0;
  z-index: 1038;
}

.sidebar-scrollable {
  height: calc(100vh - 57px); /* Subtract navbar height */
  overflow-y: auto !important;
  overflow-x: hidden;
  -webkit-overflow-scrolling: touch;
}

/* Custom scrollbar for sidebar */
.sidebar-scrollable::-webkit-scrollbar {
  width: 6px;
}

.sidebar-scrollable::-webkit-scrollbar-track {
  background: rgba(0, 0, 0, 0.1);
}

.sidebar-scrollable::-webkit-scrollbar-thumb {
  background: rgba(0, 178, 169, 0.5);
  border-radius: 3px;
}

.sidebar-scrollable::-webkit-scrollbar-thumb:hover {
  background: rgba(0, 178, 169, 0.7);
}

/* Fixed User Panel */
.user-panel-fixed {
  position: sticky;
  top: 0;
  background-color: #2F404A;
  z-index: 10;
  padding-bottom: 1rem !important;
  margin-bottom: 0 !important;
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
}

/* Scrollable Menu */
.sidebar-menu-scrollable {
  overflow-y: auto;
  overflow-x: hidden;
}

/* Sidebar Navigation Link Font Size - Compressed */
.sidebar .nav-link p {
  font-size: 0.78rem !important;
  margin-bottom: 0 !important;
}

.sidebar .nav-link {
  padding: 0.28rem 0.5rem !important;
}

.sidebar .nav-treeview .nav-link {
  padding: 0.22rem 0.5rem 0.22rem 2rem !important;
}

.sidebar .nav-treeview .nav-link p {
  font-size: 0.72rem !important;
}

.sidebar .nav-header {
  font-size: 0.72rem !important;
  padding: 0.22rem 1rem !important;
  margin-top: 0.35rem !important;
}

.sidebar .nav-icon {
  font-size: 0.87rem !important;
  margin-right: 0.3rem !important;
}

.sidebar .nav-item {
  margin-bottom: 0 !important;
}

/* Compress dividers */
.sidebar-divider {
  margin-top: 0.35rem !important;
  margin-bottom: 0.35rem !important;
}

/* Compress user panel */
.user-panel-fixed {
  padding-top: 0.3rem !important;
  padding-bottom: 0.3rem !important;
  margin-bottom: 0 !important;
}

.user-panel-fixed img,
.user-panel-fixed .fa-user-circle {
  font-size: 5rem !important;
  width: 80px !important;
  height: 80px !important;
}

.user-panel-fixed .info p {
  font-size: 0.95rem !important;
  margin-bottom: 0.25rem !important;
}

.user-panel-fixed .info a {
  font-size: 0.85rem !important;
}

.date-top {
  background: rgba(0, 178, 169, 0.12);
  color: #eaffff;
  padding: 2px 8px;
  border-radius: 6px;
  font-weight: 600;
}

.time-top {
  color: #dffaf7;
  font-weight: 500;
  font-size: 0.88rem;
  margin-top: 2px;
}

/* Centered navbar datetime */
.navbar-center {
  position: absolute;
  left: 50%;
  transform: translateX(-50%);
  top: 8px; /* align vertically within navbar */
  pointer-events: none; /* allow clicks through to underlying elements */
}
.navbar-datetime {
  pointer-events: auto;
}
.navbar-datetime {
  max-width: calc(100% - 140px);
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}
.navbar-date {
  font-weight: 700;
  letter-spacing: 0.2px;
}
.navbar-time {
  font-weight: 500;
  font-size: 0.9rem;
}

/* Prevent overlap on small screens: hide date and allow time only */
@media (max-width: 575.98px) {
  .navbar-date { font-size: 0.55rem; }
  .navbar-time { font-size: 0.95rem; }
  .navbar-datetime { max-width: calc(100% - 90px); }
}

/* Logout button styling in navbar */
.logout-btn {
  padding: 0.28rem 0.6rem;
  border-radius: 0.35rem;
  border: 1px solid rgba(255,255,255,0.08);
  background: transparent;
  color: rgba(255,255,255,0.95) !important;
  gap: 6px;
}
.logout-btn .fa-sign-out-alt {
  font-size: 0.95rem;
}
.logout-btn .logout-text {
  display: inline-block;
  font-size: 0.95rem;
}
.logout-btn:hover {
  background-color: rgba(0, 178, 169, 0.12);
  color: #ffffff !important;
  transform: translateY(-1px);
  text-decoration: none;
}
.logout-btn:focus {
  outline: none;
  box-shadow: 0 0 0 3px rgba(0,178,169,0.08);
}

/* Brand link compression */
.brand-link {
  padding: 0.5rem 0.5rem !important;
  height: 57px !important;
  display: flex !important;
  align-items: center !important;
}

.brand-text {
  font-size: 1.3rem !important;
}

/* Brand logo image on sidebar */
.brand-logo {
  height: 34px;
  width: auto;
  margin-right: 10px;
  object-fit: contain;
}
</style>
