<template>
  <div>
    <div class="content-header">
      <div class="container-fluid">
        <div class="row mb-2">
          <div class="col-sm-6">
            <h1 class="m-0">Holidays</h1>
            <p class="text-muted small">Manage clinic holidays (client-side scaffold).</p>
          </div>
        </div>
      </div>
    </div>

    <section class="content">
      <div class="container-fluid">
        <div class="card">
          <div class="card-header d-flex justify-content-between align-items-center">
            <!-- <h5 class="mb-0">Holiday Dates</h5> -->
            <div class="d-flex align-items-center">
              <div class="search-box d-flex align-items-center mr-2">
                <input v-model="searchTerm" placeholder="Search holidays" class="form-control form-control-sm border-0" style="width: 200px; background:transparent;" />
                <button class="btn btn-sm btn-outline-secondary ml-2" @click="refresh">Refresh</button>
              </div>
              <div class="add-panel d-flex align-items-center ml-2">
                <input type="text" v-model="newName" placeholder="Holiday name" class="form-control form-control-sm mr-2" style="width: 220px;" />
                <input type="date" v-model="newDate" class="form-control form-control-sm mr-2" style="width: 170px;" />
                <div class="form-check mr-2 mb-0">
                  <input class="form-check-input" type="checkbox" v-model="newRecurring" id="recurringCheck">
                  <label class="form-check-label small text-white-75" for="recurringCheck">Recurring (Annual)</label>
                </div>
                <button class="btn btn-sm add-btn-border ml-2" @click="addHoliday">Add Holiday</button>
              </div>
            </div>
          </div>
          <div class="card-body">
            <div v-if="holidays.length === 0" class="text-center py-4 text-muted">
              No holidays defined yet.
            </div>
            <ul class="list-group" v-else>
              <li v-for="h in filteredHolidays" :key="h.id" class="list-group-item">
                <div class="d-flex justify-content-between align-items-start">
                  <div style="flex:1">
                    <template v-if="editingId !== h.id">
                      <strong class="d-block">{{ h.name }}</strong>
                      <div class="small text-muted">
                        <div>
                          <span v-if="h.is_recurring">
                            <span v-if="h.month && h.day">{{ formatRecurring(h.month, h.day) }} • Annual</span>
                            <span v-else>Movable / varies • Annual</span>
                          </span>
                          <span v-else>
                            Specific: {{ formatDate(h.specific_date) }}
                          </span>
                        </div>
                        <div>Type: <strong>{{ formatType(h.holiday_type) }}</strong> • Pay: <strong>{{ formatPay(h.pay_multiplier) }}</strong></div>
                        <div v-if="h.computed_date">Computed date: <strong>{{ formatDate(h.computed_date) }}</strong></div>
                        <div v-if="h.notes" class="text-muted">Notes: {{ h.notes }}</div>
                      </div>
                    </template>
                    <template v-else>
                      <div class="mb-1">
                        <input v-model="editCopy.name" class="form-control form-control-sm" />
                      </div>
                      <div class="d-flex mb-1">
                        <div class="mr-2">
                          <label class="small">Recurring</label>
                          <input type="checkbox" v-model="editCopy.is_recurring" />
                        </div>
                        <div class="mr-2">
                          <label class="small">Date</label>
                          <input v-if="editCopy.is_recurring" type="date" v-model="editCopy._date_rec" class="form-control form-control-sm" />
                          <input v-else type="date" v-model="editCopy.specific_date" class="form-control form-control-sm" />
                        </div>
                        <div>
                          <label class="small">Pay</label>
                          <input type="number" step="0.01" v-model.number="editCopy.pay_multiplier" class="form-control form-control-sm" style="width:100px" />
                        </div>
                      </div>
                      <div class="mb-1">
                        <label class="small">Type</label>
                        <select v-model="editCopy.holiday_type" class="form-control form-control-sm">
                          <option value="regular">Regular Holiday</option>
                          <option value="special_non_working">Special (Non-Working)</option>
                          <option value="special_working">Special (Working)</option>
                        </select>
                      </div>
                      <div>
                        <label class="small">Notes</label>
                        <input v-model="editCopy.notes" class="form-control form-control-sm" />
                      </div>
                    </template>
                  </div>
                  <div class="ml-3 text-center" style="min-width:120px">
                    <template v-if="editingId !== h.id">
                      <div class="btn-stack">
                        <button class="btn btn-sm btn-secondary" @click="startEdit(h)">Edit</button>
                        <button class="btn btn-sm btn-danger" @click="removeHoliday(h.id)">Remove</button>
                      </div>
                    </template>
                    <template v-else>
                      <div>
                        <button class="btn btn-sm btn-success mr-1" @click="saveEdit(h.id)">Save</button>
                        <button class="btn btn-sm btn-outline-secondary" @click="cancelEdit">Cancel</button>
                      </div>
                    </template>
                  </div>
                </div>
              </li>
            </ul>
          </div>
          <div class="card-footer text-right">
            <small class="text-muted">This page is currently a frontend scaffold. Persist to backend if needed.</small>
          </div>
        </div>
      </div>
    </section>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import api from '../services/api'
import Swal from 'sweetalert2'

const holidays = ref([])
const newDate = ref('')
const newName = ref('')
const newRecurring = ref(true)
const searchTerm = ref('')
const editingId = ref(null)
const editCopy = ref(null)

const formatDate = (date) => {
  if (!date) return ''
  return new Date(date).toLocaleDateString('en-US', { year: 'numeric', month: 'long', day: 'numeric' })
}

const loadHolidays = async () => {
  try {
    const resp = await api.get('/website/holidays/')
    holidays.value = resp.data
  } catch (err) {
    console.error('Failed to load holidays', err)
    holidays.value = []
  }
}

const refresh = async () => {
  await loadHolidays()
  Swal.fire({ toast: true, position: 'top-end', icon: 'info', title: 'Refreshed', showConfirmButton: false, timer: 900 })
}

const addHoliday = async () => {
  if (!newDate.value || !newName.value) {
    Swal.fire('Missing', 'Please provide a name and date', 'warning')
    return
  }

  // Prepare payload depending on recurring flag
  const payload = { name: newName.value, is_recurring: !!newRecurring.value }
  const d = new Date(newDate.value)
  if (newRecurring.value) {
    payload.month = d.getMonth() + 1
    payload.day = d.getDate()
  } else {
    payload.specific_date = newDate.value
  }

  try {
    await api.post('/website/holidays/', payload)
    await loadHolidays()
    newDate.value = ''
    newName.value = ''
    newRecurring.value = true
    Swal.fire({ toast: true, position: 'top-end', icon: 'success', title: 'Holiday added', showConfirmButton: false, timer: 1400 })
  } catch (err) {
    console.error('Failed to add holiday', err)
    Swal.fire('Error', 'Failed to add holiday', 'error')
  }
}

const removeHoliday = async (id) => {
  const res = await Swal.fire({
    title: 'Remove holiday?',
    icon: 'warning',
    showCancelButton: true,
    confirmButtonText: 'Remove',
  })
  if (!res.isConfirmed) return
  try {
    await api.delete(`/website/holidays/${id}/`)
    await loadHolidays()
    Swal.fire({ toast: true, position: 'top-end', icon: 'success', title: 'Removed', showConfirmButton: false, timer: 1200 })
  } catch (err) {
    console.error('Failed to remove holiday', err)
    Swal.fire('Error', 'Failed to remove holiday', 'error')
  }
}

const sortedHolidays = computed(() => {
  // Sort by an actual calendar date: prefer computed_date, then specific_date, then recurring month/day (current year)
  const year = new Date().getFullYear()
  const getSortDate = (h) => {
    if (!h) return new Date(9999,0,1)
    if (h.computed_date) return new Date(h.computed_date)
    if (!h.is_recurring && h.specific_date) return new Date(h.specific_date)
    if (h.is_recurring && h.month && h.day) {
      try { return new Date(year, Number(h.month) - 1, Number(h.day)) } catch(e) { return new Date(9999,0,1) }
    }
    return new Date(9999,0,1)
  }

  return (holidays.value || []).slice().sort((a,b) => {
    const da = getSortDate(a).valueOf()
    const db = getSortDate(b).valueOf()
    if (da === db) return (a.name || '').localeCompare(b.name || '')
    return da - db
  })
})

const filteredHolidays = computed(() => {
  const q = (searchTerm.value || '').toLowerCase().trim()
  const list = sortedHolidays.value || []
  if (!q) return list
  return list.filter(h => {
    return (h.name || '').toLowerCase().includes(q) || (h.notes || '').toLowerCase().includes(q) || (h.holiday_type || '').toLowerCase().includes(q)
  })
})

onMounted(() => {
  loadHolidays()
})

const formatRecurring = (month, day) => {
  if (!month || !day) return ''
  const d = new Date(2000, month - 1, day)
  // short month with period
  const rawMonth = d.toLocaleDateString('en-US', { month: 'short' })
  const monthStr = rawMonth.endsWith('.') ? rawMonth : `${rawMonth}.`
  return `${monthStr} ${d.getDate()}`
}

const formatType = (t) => {
  if (!t) return 'Unknown'
  if (t === 'regular') return 'Regular Holiday'
  if (t === 'special_non_working') return 'Special (Non-Working)'
  if (t === 'special_working') return 'Special (Working)'
  return t
}

const formatPay = (p) => {
  if (!p) return '1.00'
  return Number(p).toFixed(2)
}

const startEdit = (h) => {
  editingId.value = h.id
  // create a copy for editing; add _date_rec helper for recurring date input
  const copy = JSON.parse(JSON.stringify(h))
  if (copy.is_recurring && copy.month && copy.day) {
    const d = new Date(2000, copy.month - 1, copy.day)
    copy._date_rec = `${d.getFullYear()}-${String(d.getMonth()+1).padStart(2,'0')}-${String(d.getDate()).padStart(2,'0')}`
  } else {
    copy._date_rec = ''
  }
  editCopy.value = copy
}

const cancelEdit = () => {
  editingId.value = null
  editCopy.value = null
}

const saveEdit = async (id) => {
  if (!editCopy.value) return
  const payload = {
    name: editCopy.value.name,
    is_recurring: !!editCopy.value.is_recurring,
    notes: editCopy.value.notes || '',
    holiday_type: editCopy.value.holiday_type,
    pay_multiplier: Number(editCopy.value.pay_multiplier) || 1.0,
  }
  if (editCopy.value.is_recurring) {
    // parse _date_rec if provided
    if (editCopy.value._date_rec) {
      const d = new Date(editCopy.value._date_rec)
      payload.month = d.getMonth() + 1
      payload.day = d.getDate()
      payload.specific_date = null
    }
  } else {
    payload.specific_date = editCopy.value.specific_date || null
    payload.month = null
    payload.day = null
  }

  try {
    await api.patch(`/website/holidays/${id}/`, payload)
    await loadHolidays()
    Swal.fire({ toast: true, position: 'top-end', icon: 'success', title: 'Saved', showConfirmButton: false, timer: 1000 })
    cancelEdit()
  } catch (err) {
    console.error('Failed to save', err)
    Swal.fire('Error', 'Failed to save holiday', 'error')
  }
}
</script>

<style scoped>
.card-header .form-control-sm { display: inline-block; vertical-align: middle; }

/* Header controls responsive layout */
.card-header .d-flex { flex-wrap: wrap; gap: 8px; }
.search-box {
  border: 1px solid #e0e0e0;
  padding: 6px 8px;
  border-radius: 6px;
  background: #fff;
  flex: 0 0 auto;
  display: flex;
  align-items: center;
  gap: 8px;
}
.search-box input.form-control { box-shadow: none; flex: 1 1 auto; min-width: 0; }

.add-panel {
  border: 1px solid rgba(255,255,255,0.18);
  padding: 6px 8px;
  border-radius: 6px;
  background: transparent;
  flex: 1 1 480px;
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  align-items: center;
}
.add-panel input.form-control {
  background: rgba(255,255,255,0.95);
  border: 1px solid rgba(0,0,0,0.08);
  color: #111;
  box-shadow: none;
  padding: 6px 8px;
  border-radius: 4px;
  flex: 1 1 140px;
  min-width: 120px;
}
.add-panel input[type="date"] {
  background: rgba(255,255,255,0.95);
  border: 1px solid rgba(0,0,0,0.08);
  color: #111;
  flex: 1 1 140px;
  min-width: 120px;
}
.add-panel .form-check { flex: 0 0 auto; display:flex; align-items:center; }
.add-btn-border {
  border: 1px solid rgba(0,0,0,0.12);
  background: transparent !important;
  color: #ffffff;
  padding: 6px 10px;
  border-radius: 6px;
  transition: background-color 200ms ease, color 200ms ease, box-shadow 200ms ease, transform 120ms ease;
}

.add-btn-border:hover {
  background: #0d6efd !important;
  color: #fff !important;
  border-color: #0d6efd;
  box-shadow: 0 6px 18px rgba(13,110,253,0.18);
  transform: translateY(-1px);
}

.add-btn-border:active {
  transform: translateY(0);
}

.add-panel {
  border: 1px solid rgba(255,255,255,0.18);
  padding: 6px 8px;
  border-radius: 6px;
  background: transparent;
}
.add-panel .form-control {
  background: rgba(255,255,255,0.95);
  border: 1px solid rgba(0,0,0,0.08);
  color: #111;
  box-shadow: none;
  padding: 6px 8px;
  border-radius: 4px;
}
.add-panel input[type="date"] {
  background: rgba(255,255,255,0.95);
  border: 1px solid rgba(0,0,0,0.08);
  color: #111;
}
.add-panel .form-check-label { color: #fff; }
.add-panel .form-control::placeholder { color: rgba(0,0,0,0.45); }
.btn-stack { display: flex; flex-direction: column; gap: 6px; align-items: center; }
.btn-stack button { display: block; width: 100%; }
@media (max-width: 768px) {
    .add-panel {
        margin-left: 0px !important;
    }
    
    input[type="date"].form-control-sm {
        width: 100% !important;
    }
}
</style>
