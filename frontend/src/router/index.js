import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '../stores/auth'
import LoginView from '../views/LoginView.vue'
import DashboardLayout from '../components/DashboardLayout.vue'
import DashboardView from '../views/DashboardView.vue'
import EmployeesView from '../views/EmployeesView.vue'
import PositionsView from '../views/PositionsView.vue'
import DepartmentsView from '../views/DepartmentsView.vue'
import BranchesView from '../views/BranchesView.vue'
import UsersView from '../views/UsersView.vue'
import ProfileView from '../views/ProfileView.vue'
import CategoriesView from '../views/CategoriesView.vue'
import ItemsView from '../views/ItemsView.vue'
import StockMovementsView from '../views/StockMovementsView.vue'
import MessagesView from '../views/MessagesView.vue'
import PatientsView from '../views/PatientsView.vue'
import AppointmentsView from '../views/AppointmentsView.vue'
import TreatmentRecordsView from '../views/TreatmentRecordsView.vue'
import PatientProfileView from '../views/PatientProfileView.vue'
import WebsiteContentView from '../views/WebsiteContentView.vue'
import HolidaysView from '../views/HolidaysView.vue'

const routes = [
  {
    path: '/login',
    name: 'login',
    component: LoginView,
    meta: { requiresGuest: true }
  },
  {
    path: '/patient-profile',
    name: 'patient-profile',
    component: PatientProfileView,
    meta: { 
      requiresAuth: true,
      requiresPatient: true 
    }
  },
  {
    path: '/',
    component: DashboardLayout,
    meta: { 
      requiresAuth: true,
      requiresStaff: true 
    },
    children: [
      {
        path: '',
        name: 'dashboard',
        component: DashboardView
      },
      {
        path: 'employees',
        name: 'employees',
        component: EmployeesView
      },
      {
        path: 'users',
        name: 'users',
        component: UsersView
      },
      {
        path: 'profile',
        name: 'profile',
        component: ProfileView
      },
      {
        path: 'positions',
        name: 'positions',
        component: PositionsView
      },
      {
        path: 'departments',
        name: 'departments',
        component: DepartmentsView
      },
      {
        path: 'branches',
        name: 'branches',
        component: BranchesView
      },
      {
        path: 'categories',
        name: 'categories',
        component: CategoriesView
      },
      {
        path: 'items',
        name: 'items',
        component: ItemsView
      },
      {
        path: 'stock-movements',
        name: 'stock-movements',
        component: StockMovementsView
      },
      {
        path: 'messages',
        name: 'messages',
        component: MessagesView
      },
      {
        path: 'patients',
        name: 'patients',
        component: PatientsView
      },
      {
        path: 'appointments',
        name: 'appointments',
        component: AppointmentsView
      },
      {
        path: 'treatment-records',
        name: 'treatment-records',
        component: TreatmentRecordsView
      },
      {
        path: 'website-content',
        name: 'website-content',
        component: WebsiteContentView
      }
      ,
      {
        path: 'holidays',
        name: 'holidays',
        component: HolidaysView
      }
    ]
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

// Navigation guard
router.beforeEach(async (to, from, next) => {
  const authStore = useAuthStore()
  
  // Only check auth once if we have a remembered session and not already authenticated
  if (!authStore.isAuthenticated && localStorage.getItem('rememberSession') === 'true') {
    await authStore.checkAuth()
  }
  
  // If checkAuth failed and we're trying to access a protected route, redirect to login
  if (to.meta.requiresAuth && !authStore.isAuthenticated) {
    // Clear any stale localStorage data
    localStorage.removeItem('rememberSession')
    localStorage.removeItem('sessionUser')
    next('/login')
    return
  }
  
  // Redirect authenticated users away from login
  if (to.meta.requiresGuest && authStore.isAuthenticated) {
    // Check if user is a patient
    const isPatient = authStore.user?.group_names?.includes('patient')
    if (isPatient) {
      next('/patient-profile')
    } else {
      next('/')
    }
    return
  }
  
  // Check if route requires patient role
  if (to.meta.requiresPatient) {
    const isPatient = authStore.user?.group_names?.includes('patient')
    if (!isPatient) {
      next('/')
      return
    }
  }
  
  // Check if route requires staff role (non-patient users)
  if (to.meta.requiresStaff) {
    const isPatient = authStore.user?.group_names?.includes('patient')
    if (isPatient) {
      next('/patient-profile')
      return
    }
  }
  
  next()
})

export default router
