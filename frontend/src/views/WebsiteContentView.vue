<template>
  <div class="content-wrapper">
    <section class="content-header">
      <div class="container-fluid">
        <div class="row mb-2">
          <div class="col-sm-6">
            <h1>Website Content Management</h1>
          </div>
        </div>
      </div>
    </section>

    <section class="content">
      <div class="container-fluid">
        <!-- Tabs -->
        <ul class="nav nav-tabs" role="tablist">
          <li class="nav-item">
            <a class="nav-link" :class="{ active: activeTab === 'hero' }" @click.prevent="activeTab = 'hero'" href="#" role="tab">
              <i class="fas fa-home"></i> Hero Section
            </a>
          </li>
          <li class="nav-item">
            <a class="nav-link" :class="{ active: activeTab === 'services' }" @click.prevent="activeTab = 'services'" href="#" role="tab">
              <i class="fas fa-tooth"></i> Services
            </a>
          </li>
          <li class="nav-item">
            <a class="nav-link" :class="{ active: activeTab === 'about' }" @click.prevent="activeTab = 'about'" href="#" role="tab">
              <i class="fas fa-info-circle"></i> About
            </a>
          </li>
          <li class="nav-item">
            <a class="nav-link" :class="{ active: activeTab === 'contact' }" @click.prevent="activeTab = 'contact'" href="#" role="tab">
              <i class="fas fa-envelope"></i> Contact
            </a>
          </li>
          <li class="nav-item">
            <a class="nav-link" :class="{ active: activeTab === 'settings' }" @click.prevent="activeTab = 'settings'" href="#" role="tab">
              <i class="fas fa-cog"></i> Site Settings
            </a>
          </li>
        </ul>

        <div class="tab-content p-3">
          <!-- Hero Section Tab -->
          <div class="tab-pane fade" :class="{ 'show active': activeTab === 'hero' }" role="tabpanel">
            <div class="card">
              <div class="card-header">
                <h3 class="card-title">Hero Carousel Slides</h3>
                <div class="card-tools">
                  <button class="btn btn-success btn-sm" @click="showAddHeroModal">
                    <i class="fas fa-plus"></i> Add Slide
                  </button>
                </div>
              </div>
              <div class="card-body">
                <table class="table table-bordered table-hover">
                  <thead>
                    <tr>
                      <th>Order</th>
                      <th>Image</th>
                      <th>Title</th>
                      <th>Subtitle</th>
                      <th>Active</th>
                      <th>Actions</th>
                    </tr>
                  </thead>
                  <tbody>
                    <tr v-for="hero in heroSlides" :key="hero.id">
                      <td>{{ hero.order }}</td>
                      <td>
                        <img v-if="hero.background_image" :src="hero.background_image" alt="Hero Image" style="width: 60px; height: 40px; object-fit: cover; border-radius: 4px;">
                        <span v-else class="badge badge-secondary">Default</span>
                      </td>
                      <td>{{ hero.title }}</td>
                      <td>{{ hero.subtitle.substring(0, 50) }}...</td>
                      <td>
                        <span class="badge" :class="hero.is_active ? 'badge-success' : 'badge-secondary'">
                          {{ hero.is_active ? 'Active' : 'Inactive' }}
                        </span>
                      </td>
                      <td>
                        <button class="btn btn-sm btn-info" @click="editHero(hero)">
                          <i class="fas fa-edit"></i>
                        </button>
                        <button class="btn btn-sm btn-danger" @click="deleteHero(hero.id)">
                          <i class="fas fa-trash"></i>
                        </button>
                      </td>
                    </tr>
                  </tbody>
                </table>
                
                <!-- Carousel Settings -->
                <div class="mt-4 p-3 border rounded bg-light">
                  <h5><i class="fas fa-cog"></i> Carousel Settings</h5>
                  <div class="row">
                    <div class="col-md-6">
                      <div class="form-group">
                        <label>Auto-Slide Interval (milliseconds)</label>
                        <input 
                          type="number" 
                          class="form-control" 
                          v-model.number="settingsData.carousel_interval" 
                          min="1000" 
                          step="1000"
                          @change="saveSiteSettings"
                        >
                        <small class="form-text text-muted">
                          Time between automatic slide transitions (e.g., 5000 = 5 seconds)
                        </small>
                      </div>
                    </div>
                    <div class="col-md-6 d-flex align-items-end">
                      <button type="button" class="btn btn-primary mb-3" @click="saveSiteSettings">
                        <i class="fas fa-save"></i> Save Interval
                      </button>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <!-- Services Tab -->
          <div class="tab-pane fade" :class="{ 'show active': activeTab === 'services' }" role="tabpanel">
            <div class="card">
              <div class="card-header">
                <h3 class="card-title">Services</h3>
                <div class="card-tools">
                  <button class="btn btn-success btn-sm" @click="showAddServiceModal">
                    <i class="fas fa-plus"></i> Add Service
                  </button>
                </div>
              </div>
              <div class="card-body">
                <table class="table table-bordered table-hover">
                  <thead>
                    <tr>
                      <th>Order</th>
                      <th>Icon</th>
                      <th>Title</th>
                      <th>Description</th>
                      <th>Active</th>
                      <th>Actions</th>
                    </tr>
                  </thead>
                  <tbody>
                    <tr v-for="service in services" :key="service.id">
                      <td>{{ service.order }}</td>
                      <td><i class="fas" :class="service.icon"></i></td>
                      <td>{{ service.title }}</td>
                      <td>{{ service.description.substring(0, 50) }}...</td>
                      <td>
                        <span class="badge" :class="service.is_active ? 'badge-success' : 'badge-secondary'">
                          {{ service.is_active ? 'Active' : 'Inactive' }}
                        </span>
                      </td>
                      <td>
                        <button class="btn btn-sm btn-info" @click="editService(service)">
                          <i class="fas fa-edit"></i>
                        </button>
                        <button class="btn btn-sm btn-danger" @click="deleteService(service.id)">
                          <i class="fas fa-trash"></i>
                        </button>
                      </td>
                    </tr>
                  </tbody>
                </table>
              </div>
            </div>
          </div>

          <!-- About Tab -->
          <div class="tab-pane fade" :class="{ 'show active': activeTab === 'about' }" role="tabpanel">
            <div class="card">
              <div class="card-header">
                <h3 class="card-title">About Section Content</h3>
              </div>
              <div class="card-body">
                <form @submit.prevent="saveAboutSection">
                  <div class="form-group">
                    <label>Title</label>
                    <input type="text" class="form-control" v-model="aboutData.title" required>
                  </div>
                  <div class="form-group">
                    <label>Description</label>
                    <textarea class="form-control" rows="4" v-model="aboutData.description" required></textarea>
                  </div>
                  
                  <h5 class="mt-4">Statistics</h5>
                  <div class="row">
                    <div class="col-md-6">
                      <div class="form-group">
                        <label>Patients Count</label>
                        <input type="text" class="form-control" v-model="aboutData.patients_count" required>
                      </div>
                    </div>
                    <div class="col-md-6">
                      <div class="form-group">
                        <label>Patients Label</label>
                        <input type="text" class="form-control" v-model="aboutData.patients_label" required>
                      </div>
                    </div>
                  </div>
                  <div class="row">
                    <div class="col-md-6">
                      <div class="form-group">
                        <label>Years Count</label>
                        <input type="text" class="form-control" v-model="aboutData.years_count" required>
                      </div>
                    </div>
                    <div class="col-md-6">
                      <div class="form-group">
                        <label>Years Label</label>
                        <input type="text" class="form-control" v-model="aboutData.years_label" required>
                      </div>
                    </div>
                  </div>
                  <div class="row">
                    <div class="col-md-6">
                      <div class="form-group">
                        <label>Dentists Count</label>
                        <input type="text" class="form-control" v-model="aboutData.dentists_count" required>
                      </div>
                    </div>
                    <div class="col-md-6">
                      <div class="form-group">
                        <label>Dentists Label</label>
                        <input type="text" class="form-control" v-model="aboutData.dentists_label" required>
                      </div>
                    </div>
                  </div>

                  <h5 class="mt-4">Features <small class="text-muted">(Drag to reorder)</small></h5>
                  <div 
                    v-for="(feature, index) in aboutFeatures" 
                    :key="index" 
                    class="input-group mb-2 feature-item"
                    draggable="true"
                    @dragstart="dragStart(index)"
                    @dragover.prevent
                    @drop="dropFeature(index)"
                    style="cursor: move;"
                  >
                    <div class="input-group-prepend">
                      <span class="input-group-text" style="cursor: move;">
                        <i class="fas fa-grip-vertical"></i>
                      </span>
                    </div>
                    <input type="text" class="form-control" v-model="feature.text" placeholder="Feature text">
                    <div class="input-group-append">
                      <button type="button" class="btn btn-danger" @click="removeFeature(index)">
                        <i class="fas fa-times"></i>
                      </button>
                    </div>
                  </div>
                  <button type="button" class="btn btn-secondary btn-sm mb-3" @click="addFeature">
                    <i class="fas fa-plus"></i> Add Feature
                  </button>

                  <div class="form-group">
                    <div class="custom-control custom-switch">
                      <input type="checkbox" class="custom-control-input" id="aboutActive" v-model="aboutData.is_active">
                      <label class="custom-control-label" for="aboutActive">Active</label>
                    </div>
                  </div>
                  <button type="submit" class="btn btn-primary">
                    <i class="fas fa-save"></i> Save About Section
                  </button>
                </form>
              </div>
            </div>
          </div>

          <!-- Contact Tab -->
          <div class="tab-pane fade" :class="{ 'show active': activeTab === 'contact' }" role="tabpanel">
            <div class="card">
              <div class="card-header">
                <h3 class="card-title">Contact Information</h3>
              </div>
              <div class="card-body">
                <form @submit.prevent="saveContactInfo">
                  <div class="form-group">
                    <label>Section Title</label>
                    <input type="text" class="form-control" v-model="contactData.section_title" required>
                  </div>
                  <div class="form-group">
                    <label>Section Subtitle</label>
                    <textarea class="form-control" rows="2" v-model="contactData.section_subtitle" required></textarea>
                  </div>
                  
                  <h5 class="mt-4">Social Media Links</h5>
                  <div class="form-group">
                    <label><i class="fab fa-facebook"></i> Facebook URL</label>
                    <input type="url" class="form-control" v-model="contactData.facebook_url" placeholder="https://facebook.com/...">
                  </div>
                  <div class="form-group">
                    <label><i class="fab fa-twitter"></i> Twitter URL</label>
                    <input type="url" class="form-control" v-model="contactData.twitter_url" placeholder="https://twitter.com/...">
                  </div>
                  <div class="form-group">
                    <label><i class="fab fa-instagram"></i> Instagram URL</label>
                    <input type="url" class="form-control" v-model="contactData.instagram_url" placeholder="https://instagram.com/...">
                  </div>
                  <div class="form-group">
                    <label><i class="fab fa-linkedin"></i> LinkedIn URL</label>
                    <input type="url" class="form-control" v-model="contactData.linkedin_url" placeholder="https://linkedin.com/...">
                  </div>
                  
                  <div class="form-group">
                    <label>Footer Text</label>
                    <textarea class="form-control" rows="2" v-model="contactData.footer_text" required></textarea>
                  </div>
                  
                  <div class="form-group">
                    <div class="custom-control custom-switch">
                      <input type="checkbox" class="custom-control-input" id="contactActive" v-model="contactData.is_active">
                      <label class="custom-control-label" for="contactActive">Active</label>
                    </div>
                  </div>
                  <button type="submit" class="btn btn-primary">
                    <i class="fas fa-save"></i> Save Contact Information
                  </button>
                </form>
              </div>
            </div>
          </div>

          <!-- Site Settings Tab -->
          <div class="tab-pane fade" :class="{ 'show active': activeTab === 'settings' }" role="tabpanel">
            <div class="card">
              <div class="card-header">
                <h3 class="card-title">Site Settings</h3>
              </div>
              <div class="card-body">
                <form @submit.prevent="saveSiteSettings">
                  <div class="form-group">
                    <label>Site Name</label>
                    <input type="text" class="form-control" v-model="settingsData.site_name" required>
                  </div>
                  <div class="form-group">
                    <label>Patient Portal URL</label>
                    <input type="url" class="form-control" v-model="settingsData.patient_portal_url" required>
                  </div>
                  <div class="row">
                    <div class="col-md-6">
                      <div class="form-group">
                        <label>Primary Color</label>
                        <div class="input-group">
                          <input type="color" class="form-control" v-model="settingsData.primary_color" required>
                          <input type="text" class="form-control" v-model="settingsData.primary_color" required>
                        </div>
                      </div>
                    </div>
                    <div class="col-md-6">
                      <div class="form-group">
                        <label>Secondary Color</label>
                        <div class="input-group">
                          <input type="color" class="form-control" v-model="settingsData.secondary_color" required>
                          <input type="text" class="form-control" v-model="settingsData.secondary_color" required>
                        </div>
                      </div>
                    </div>
                  </div>
                  <button type="submit" class="btn btn-primary">
                    <i class="fas fa-save"></i> Save Site Settings
                  </button>
                </form>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- Service Modal -->
    <div v-if="showServiceModal" class="modal fade show" style="display: block;" tabindex="-1" role="dialog">
      <div class="modal-dialog" role="document">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">{{ serviceModalTitle }}</h5>
            <button type="button" class="close" @click="closeServiceModal">
              <span>&times;</span>
            </button>
          </div>
          <form @submit.prevent="saveService">
            <div class="modal-body">
              <div class="form-group">
                <label>Title</label>
                <input type="text" class="form-control" v-model="serviceForm.title" required>
              </div>
              <div class="form-group">
                <label>Description</label>
                <textarea class="form-control" rows="3" v-model="serviceForm.description" required></textarea>
              </div>
              <div class="form-group">
                <label>Icon</label>
                <select class="form-control" v-model="serviceForm.icon" required>
                  <option value="fa-teeth">Teeth</option>
                  <option value="fa-smile-beam">Smile Beam</option>
                  <option value="fa-tooth">Tooth</option>
                  <option value="fa-user-md">Doctor</option>
                  <option value="fa-crown">Crown</option>
                  <option value="fa-child">Child</option>
                  <option value="fa-x-ray">X-Ray</option>
                  <option value="fa-syringe">Syringe</option>
                </select>
                <small class="form-text text-muted">
                  <i class="fas" :class="serviceForm.icon"></i> Preview
                </small>
              </div>
              <div class="form-group">
                <label>Order</label>
                <input type="number" class="form-control" v-model.number="serviceForm.order" required>
              </div>
              <div class="form-group">
                <div class="custom-control custom-switch">
                  <input type="checkbox" class="custom-control-input" id="serviceActive" v-model="serviceForm.is_active">
                  <label class="custom-control-label" for="serviceActive">Active</label>
                </div>
              </div>
            </div>
            <div class="modal-footer">
              <button type="button" class="btn btn-secondary" @click="closeServiceModal">Cancel</button>
              <button type="submit" class="btn btn-primary">Save</button>
            </div>
          </form>
        </div>
      </div>
    </div>
    <div v-if="showServiceModal" class="modal-backdrop fade show"></div>

    <!-- Hero Slide Modal -->
    <div v-if="showHeroModal" class="modal fade show" style="display: block;" tabindex="-1" role="dialog">
      <div class="modal-dialog modal-lg modal-dialog-scrollable" role="document">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">{{ heroModalTitle }}</h5>
            <button type="button" class="close" @click="closeHeroModal">
              <span>&times;</span>
            </button>
          </div>
          <form @submit.prevent="saveHero">
            <div class="modal-body" style="max-height: 70vh; overflow-y: auto;">
              <div class="form-group">
                <label>Background Image (HD)</label>
                <input type="file" class="form-control-file" @change="handleHeroImageUpload" accept="image/*">
                <small class="form-text text-muted">Upload HD background image. Leave empty to use default gradient background.</small>
                <div v-if="heroImagePreview || heroForm.background_image" class="mt-2">
                  <img :src="heroImagePreview || heroForm.background_image" alt="Preview" style="max-width: 100%; max-height: 200px; object-fit: cover; border-radius: 8px;">
                  <button type="button" class="btn btn-sm btn-danger mt-2" @click="removeHeroImage">
                    <i class="fas fa-trash"></i> Remove Image
                  </button>
                </div>
              </div>
              <div class="form-group">
                <label>Title</label>
                <input type="text" class="form-control" v-model="heroForm.title" required>
              </div>
              <div class="form-group">
                <label>Subtitle</label>
                <textarea class="form-control" rows="3" v-model="heroForm.subtitle" required></textarea>
              </div>
              <div class="row">
                <div class="col-md-6">
                  <div class="form-group">
                    <label>Primary Button Text</label>
                    <input type="text" class="form-control" v-model="heroForm.primary_button_text" required>
                  </div>
                </div>
                <div class="col-md-6">
                  <div class="form-group">
                    <label>Primary Button Link</label>
                    <input type="text" class="form-control" v-model="heroForm.primary_button_link" required>
                  </div>
                </div>
              </div>
              <div class="row">
                <div class="col-md-6">
                  <div class="form-group">
                    <label>Secondary Button Text</label>
                    <input type="text" class="form-control" v-model="heroForm.secondary_button_text" required>
                  </div>
                </div>
                <div class="col-md-6">
                  <div class="form-group">
                    <label>Secondary Button Link</label>
                    <input type="text" class="form-control" v-model="heroForm.secondary_button_link" required>
                  </div>
                </div>
              </div>
              <div class="form-group">
                <label>Icon (Shown when no background image)</label>
                <select class="form-control" v-model="heroForm.icon" required>
                  <option value="fa-tooth">Tooth</option>
                  <option value="fa-teeth">Teeth</option>
                  <option value="fa-smile-beam">Smile Beam</option>
                  <option value="fa-user-md">Doctor</option>
                  <option value="fa-star">Star</option>
                  <option value="fa-heart">Heart</option>
                  <option value="fa-shield-alt">Shield</option>
                  <option value="fa-award">Award</option>
                  <option value="fa-magic">Magic</option>
                  <option value="fa-crown">Crown</option>
                </select>
                <small class="form-text text-muted">
                  <i class="fas" :class="heroForm.icon" style="font-size: 2rem; margin-top: 10px;"></i> Icon Preview
                </small>
              </div>
              <div class="form-group">
                <label>Order (0-4)</label>
                <input type="number" class="form-control" v-model.number="heroForm.order" min="0" max="4" required>
                <small class="form-text text-muted">Maximum 5 slides allowed (order 0-4). Lower numbers appear first.</small>
              </div>
              <div class="form-group">
                <div class="custom-control custom-switch">
                  <input type="checkbox" class="custom-control-input" id="heroActive" v-model="heroForm.is_active">
                  <label class="custom-control-label" for="heroActive">Active</label>
                </div>
              </div>
            </div>
            <div class="modal-footer">
              <button type="button" class="btn btn-secondary" @click="closeHeroModal">Cancel</button>
              <button type="submit" class="btn btn-primary">Save</button>
            </div>
          </form>
        </div>
      </div>
    </div>
    <div v-if="showHeroModal" class="modal-backdrop fade show"></div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import api from '../services/api'
import Swal from 'sweetalert2'

const activeTab = ref('hero')
const showServiceModal = ref(false)
const showHeroModal = ref(false)

const heroSlides = ref([])
const heroForm = ref({
  id: null,
  title: '',
  subtitle: '',
  primary_button_text: '',
  primary_button_link: '',
  secondary_button_text: '',
  secondary_button_link: '',
  background_image: null,
  icon: 'fa-tooth',
  order: 0,
  is_active: true
})
const heroImageFile = ref(null)
const heroImagePreview = ref(null)

const services = ref([])
const serviceForm = ref({
  id: null,
  title: '',
  description: '',
  icon: 'fa-tooth',
  order: 0,
  is_active: true
})

const aboutData = ref({
  id: null,
  title: '',
  description: '',
  patients_count: '',
  patients_label: '',
  years_count: '',
  years_label: '',
  dentists_count: '',
  dentists_label: '',
  is_active: true
})
const aboutFeatures = ref([])
let draggedFeatureIndex = null

const contactData = ref({
  id: null,
  section_title: '',
  section_subtitle: '',
  facebook_url: '',
  twitter_url: '',
  instagram_url: '',
  linkedin_url: '',
  footer_text: '',
  is_active: true
})

const settingsData = ref({
  id: null,
  site_name: '',
  patient_portal_url: '',
  primary_color: '#00B2A9',
  secondary_color: '#0097A7',
  carousel_interval: 5000
})

const heroModalTitle = ref('Add Hero Slide')
const serviceModalTitle = ref('Add Service')

const fetchHeroSlides = async () => {
  try {
    const response = await api.get('/website/hero/')
    heroSlides.value = response.data
  } catch (error) {
    console.error('Error fetching hero slides:', error)
  }
}

const showAddHeroModal = () => {
  heroModalTitle.value = 'Add Hero Slide'
  const nextOrder = Math.min(heroSlides.value.length, 4) // Max 5 slides (0-4)
  heroForm.value = {
    id: null,
    title: '',
    subtitle: '',
    primary_button_text: 'Book Appointment',
    primary_button_link: '#contact',
    secondary_button_text: 'Our Services',
    secondary_button_link: '#services',
    background_image: null,
    icon: 'fa-tooth',
    order: nextOrder,
    is_active: true
  }
  heroImageFile.value = null
  heroImagePreview.value = null
  showHeroModal.value = true
}

const editHero = (hero) => {
  heroModalTitle.value = 'Edit Hero Slide'
  heroForm.value = { ...hero }
  heroImageFile.value = null
  heroImagePreview.value = null
  showHeroModal.value = true
}

const closeHeroModal = () => {
  showHeroModal.value = false
  heroImageFile.value = null
  heroImagePreview.value = null
}

const handleHeroImageUpload = (event) => {
  const file = event.target.files[0]
  if (file) {
    heroImageFile.value = file
    const reader = new FileReader()
    reader.onload = (e) => {
      heroImagePreview.value = e.target.result
    }
    reader.readAsDataURL(file)
  }
}

const removeHeroImage = () => {
  heroImageFile.value = null
  heroImagePreview.value = null
  heroForm.value.background_image = null
}

const saveHero = async () => {
  try {
    // Validate max 5 slides
    if (!heroForm.value.id && heroSlides.value.filter(h => h.is_active).length >= 5) {
      Swal.fire('Error', 'Maximum of 5 hero slides allowed. Please deactivate or delete an existing slide first.', 'error')
      return
    }
    
    const formData = new FormData()
    formData.append('title', heroForm.value.title)
    formData.append('subtitle', heroForm.value.subtitle)
    formData.append('primary_button_text', heroForm.value.primary_button_text)
    formData.append('primary_button_link', heroForm.value.primary_button_link)
    formData.append('secondary_button_text', heroForm.value.secondary_button_text)
    formData.append('secondary_button_link', heroForm.value.secondary_button_link)
    formData.append('icon', heroForm.value.icon)
    formData.append('order', Math.min(heroForm.value.order, 4)) // Ensure max order is 4
    formData.append('is_active', heroForm.value.is_active)
    
    if (heroImageFile.value) {
      formData.append('background_image', heroImageFile.value)
    } else if (heroForm.value.background_image === null && heroForm.value.id) {
      // If removing image from existing slide
      formData.append('background_image', '')
    }
    
    if (heroForm.value.id) {
      await api.put(`/website/hero/${heroForm.value.id}/`, formData, {
        headers: { 'Content-Type': 'multipart/form-data' }
      })
    } else {
      await api.post('/website/hero/', formData, {
        headers: { 'Content-Type': 'multipart/form-data' }
      })
    }
    Swal.fire('Success', 'Hero slide saved successfully!', 'success')
    closeHeroModal()
    await fetchHeroSlides()
  } catch (error) {
    Swal.fire('Error', 'Failed to save hero slide.', 'error')
    console.error('Error saving hero slide:', error)
  }
}

const deleteHero = async (id) => {
  const result = await Swal.fire({
    title: 'Are you sure?',
    text: "You won't be able to revert this!",
    icon: 'warning',
    showCancelButton: true,
    confirmButtonColor: '#3085d6',
    cancelButtonColor: '#d33',
    confirmButtonText: 'Yes, delete it!'
  })
  
  if (result.isConfirmed) {
    try {
      await api.delete(`/website/hero/${id}/`)
      Swal.fire('Deleted!', 'Hero slide has been deleted.', 'success')
      await fetchHeroSlides()
    } catch (error) {
      Swal.fire('Error', 'Failed to delete hero slide.', 'error')
      console.error('Error deleting hero slide:', error)
    }
  }
}

const fetchServices = async () => {
  try {
    const response = await api.get('/website/services/')
    services.value = response.data
  } catch (error) {
    console.error('Error fetching services:', error)
  }
}

const showAddServiceModal = () => {
  serviceModalTitle.value = 'Add Service'
  serviceForm.value = {
    id: null,
    title: '',
    description: '',
    icon: 'fa-tooth',
    order: services.value.length,
    is_active: true
  }
  showServiceModal.value = true
}

const editService = (service) => {
  serviceModalTitle.value = 'Edit Service'
  serviceForm.value = { ...service }
  showServiceModal.value = true
}

const closeServiceModal = () => {
  showServiceModal.value = false
}

const saveService = async () => {
  try {
    if (serviceForm.value.id) {
      await api.put(`/website/services/${serviceForm.value.id}/`, serviceForm.value)
    } else {
      await api.post('/website/services/', serviceForm.value)
    }
    closeServiceModal()
    fetchServices()
    Swal.fire('Success', 'Service saved successfully!', 'success')
  } catch (error) {
    Swal.fire('Error', 'Failed to save service.', 'error')
    console.error('Error saving service:', error)
  }
}

const deleteService = async (id) => {
  const result = await Swal.fire({
    title: 'Are you sure?',
    text: 'This service will be deleted.',
    icon: 'warning',
    showCancelButton: true,
    confirmButtonColor: '#d33',
    cancelButtonColor: '#3085d6',
    confirmButtonText: 'Yes, delete it!'
  })
  
  if (result.isConfirmed) {
    try {
      await api.delete(`/website/services/${id}/`)
      fetchServices()
      Swal.fire('Deleted!', 'Service has been deleted.', 'success')
    } catch (error) {
      Swal.fire('Error', 'Failed to delete service.', 'error')
      console.error('Error deleting service:', error)
    }
  }
}

const fetchAboutSection = async () => {
  try {
    const response = await api.get('/website/about/')
    if (response.data.length > 0) {
      aboutData.value = response.data[0]
      aboutFeatures.value = aboutData.value.features || []
    }
  } catch (error) {
    console.error('Error fetching about section:', error)
  }
}

const addFeature = () => {
  aboutFeatures.value.push({ text: '', order: aboutFeatures.value.length })
}

const removeFeature = (index) => {
  aboutFeatures.value.splice(index, 1)
}

const dragStart = (index) => {
  draggedFeatureIndex = index
}

const dropFeature = (dropIndex) => {
  if (draggedFeatureIndex === null || draggedFeatureIndex === dropIndex) return
  
  const features = [...aboutFeatures.value]
  const draggedItem = features[draggedFeatureIndex]
  
  // Remove from old position
  features.splice(draggedFeatureIndex, 1)
  
  // Insert at new position
  features.splice(dropIndex, 0, draggedItem)
  
  aboutFeatures.value = features
  draggedFeatureIndex = null
}

const saveAboutSection = async () => {
  try {
    if (aboutData.value.id) {
      await api.put(`/website/about/${aboutData.value.id}/`, aboutData.value)
    } else {
      const response = await api.post('/website/about/', aboutData.value)
      aboutData.value.id = response.data.id
    }
    
    // Save features
    const existingFeatures = aboutData.value.features || []
    for (let i = 0; i < aboutFeatures.value.length; i++) {
      const feature = aboutFeatures.value[i]
      feature.order = i
      feature.about_section = aboutData.value.id
      
      if (feature.id) {
        await api.put(`/website/about-features/${feature.id}/`, feature)
      } else {
        await api.post('/website/about-features/', feature)
      }
    }
    
    // Delete removed features
    for (const existingFeature of existingFeatures) {
      if (!aboutFeatures.value.find(f => f.id === existingFeature.id)) {
        await api.delete(`/website/about-features/${existingFeature.id}/`)
      }
    }
    
    fetchAboutSection()
    Swal.fire('Success', 'About section updated successfully!', 'success')
  } catch (error) {
    Swal.fire('Error', 'Failed to save about section.', 'error')
    console.error('Error saving about section:', error)
  }
}

const fetchContactInfo = async () => {
  try {
    const response = await api.get('/website/contact/')
    if (response.data.length > 0) {
      contactData.value = response.data[0]
    }
  } catch (error) {
    console.error('Error fetching contact info:', error)
  }
}

const saveContactInfo = async () => {
  try {
    if (contactData.value.id) {
      await api.put(`/website/contact/${contactData.value.id}/`, contactData.value)
    } else {
      const response = await api.post('/website/contact/', contactData.value)
      contactData.value.id = response.data.id
    }
    Swal.fire('Success', 'Contact information updated successfully!', 'success')
  } catch (error) {
    Swal.fire('Error', 'Failed to save contact information.', 'error')
    console.error('Error saving contact info:', error)
  }
}

const fetchSiteSettings = async () => {
  try {
    const response = await api.get('/website/settings/')
    if (response.data.length > 0) {
      settingsData.value = response.data[0]
    }
  } catch (error) {
    console.error('Error fetching site settings:', error)
  }
}

const saveSiteSettings = async () => {
  try {
    if (settingsData.value.id) {
      await api.put(`/website/settings/${settingsData.value.id}/`, settingsData.value)
    } else {
      const response = await api.post('/website/settings/', settingsData.value)
      settingsData.value.id = response.data.id
    }
    Swal.fire('Success', 'Site settings updated successfully!', 'success')
  } catch (error) {
    Swal.fire('Error', 'Failed to save site settings.', 'error')
    console.error('Error saving site settings:', error)
  }
}

onMounted(() => {
  fetchHeroSlides()
  fetchServices()
  fetchAboutSection()
  fetchContactInfo()
  fetchSiteSettings()
})
</script>

<style scoped>
.content-wrapper {
  min-height: calc(100vh - 60px);
}

.feature-item {
  transition: background-color 0.2s ease;
}

.feature-item:hover {
  background-color: #f8f9fa;
}

.feature-item:active {
  opacity: 0.5;
}
</style>
