<template>
  <div class="content-header">
    <div class="container-fluid">
      <div class="row mb-2">
        <div class="col-sm-6">
          <h1 class="m-0">
            <i class="fas fa-envelope"></i> Messages 
            <span v-if="unreadCount > 0" class="badge badge-danger ml-2">{{ unreadCount }}</span>
          </h1>
        </div>
        <div class="col-sm-6">
          <button class="btn btn-info float-right ml-2" @click="refreshMessages" title="Refresh">
            <i class="fas fa-sync-alt"></i>
          </button>
          <button class="btn btn-primary float-right" @click="openComposeModal">
            <i class="fas fa-paper-plane"></i> Compose
          </button>
        </div>
      </div>
    </div>
  </div>

  <section class="content">
    <div class="container-fluid">
      <div class="card">
        <div class="card-header p-2">
          <ul class="nav nav-pills">
            <li class="nav-item">
              <a 
                class="nav-link" 
                :class="{ active: activeTab === 'inbox' }" 
                href="#" 
                @click.prevent="activeTab = 'inbox'; fetchMessages()"
              >
                <i class="fas fa-inbox"></i> Inbox 
                <span v-if="unreadCount > 0" class="badge badge-danger ml-1">{{ unreadCount }}</span>
              </a>
            </li>
            <li class="nav-item">
              <a 
                class="nav-link" 
                :class="{ active: activeTab === 'sent' }" 
                href="#" 
                @click.prevent="activeTab = 'sent'; fetchMessages()"
              >
                <i class="fas fa-paper-plane"></i> Sent
              </a>
            </li>
          </ul>
        </div>

        <div class="card-body">
          <div class="d-flex justify-content-between align-items-center mb-3">
            <div class="input-group input-group-sm" style="width: 300px;">
              <input 
                type="text" 
                v-model="searchQuery"
                class="form-control" 
                placeholder="Search messages"
              >
              <div class="input-group-append">
                <button class="btn btn-default">
                  <i class="fas fa-search"></i>
                </button>
              </div>
            </div>
            
            <div v-if="selectedMessages.length > 0" class="btn-group">
              <span class="badge badge-info mr-2 p-2">{{ selectedMessages.length }} selected</span>
              <button 
                v-if="activeTab === 'inbox'"
                class="btn btn-sm btn-secondary" 
                @click="markSelectedAsRead"
                title="Mark as Read"
              >
                <i class="far fa-envelope-open"></i> Mark Read
              </button>
              <button 
                v-if="activeTab === 'inbox'"
                class="btn btn-sm btn-secondary ml-1" 
                @click="markSelectedAsUnread"
                title="Mark as Unread"
              >
                <i class="fas fa-envelope"></i> Mark Unread
              </button>
              <button 
                class="btn btn-sm btn-danger ml-1" 
                @click="deleteSelected"
                title="Delete Selected"
              >
                <i class="fas fa-trash"></i> Delete
              </button>
              <button 
                class="btn btn-sm btn-default ml-1" 
                @click="clearSelection"
                title="Clear Selection"
              >
                <i class="fas fa-times"></i>
              </button>
            </div>
          </div>

          <div class="table-responsive">
            <table class="table table-hover">
              <thead>
                <tr>
                  <th style="width: 40px;">
                    <input 
                      type="checkbox" 
                      @change="toggleSelectAll"
                      :checked="selectedMessages.length === filteredMessages.length && filteredMessages.length > 0"
                    >
                  </th>
                  <th style="width: 40px;"></th>
                  <th style="width: 200px;">{{ activeTab === 'inbox' ? 'From' : 'To' }}</th>
                  <th>Subject</th>
                  <th style="width: 100px;">Priority</th>
                  <th style="width: 120px;">Type</th>
                  <th style="width: 150px;">Date</th>
                  <th style="width: 120px;">Actions</th>
                </tr>
              </thead>
              <tbody>
                <tr 
                  v-for="message in filteredMessages" 
                  :key="message.id"
                  :class="{ 'table-active': activeTab === 'inbox' && !message.is_read }"
                >
                  <td class="align-middle text-center" @click.stop>
                    <input 
                      type="checkbox" 
                      :value="message.id"
                      v-model="selectedMessages"
                    >
                  </td>
                  <td class="align-middle text-center" @click="viewMessage(message)" style="cursor: pointer;">
                    <i 
                      v-if="activeTab === 'inbox'" 
                      :class="message.is_read ? 'far fa-envelope-open' : 'fas fa-envelope'"
                      :title="message.is_read ? 'Read' : 'Unread'"
                    ></i>
                  </td>
                  <td class="align-middle" @click="viewMessage(message)" style="cursor: pointer;">
                    <strong v-if="activeTab === 'inbox' && !message.is_read">
                      {{ message.sender_name }}
                    </strong>
                    <span v-else>{{ activeTab === 'inbox' ? message.sender_name : message.receiver_name }}</span>
                  </td>
                  <td class="align-middle" @click="viewMessage(message)" style="cursor: pointer;">
                    <strong v-if="activeTab === 'inbox' && !message.is_read">
                      {{ message.subject }}
                    </strong>
                    <span v-else>{{ message.subject }}</span>
                  </td>
                  <td class="align-middle" @click="viewMessage(message)" style="cursor: pointer;">
                    <span 
                      :class="{
                        'badge badge-secondary': message.priority === 'low',
                        'badge badge-info': message.priority === 'normal',
                        'badge badge-warning': message.priority === 'high',
                        'badge badge-danger': message.priority === 'urgent'
                      }"
                    >
                      {{ message.priority }}
                    </span>
                  </td>
                  <td class="align-middle" @click="viewMessage(message)" style="cursor: pointer;">
                    <span class="badge badge-light">{{ message.message_type }}</span>
                  </td>
                  <td class="align-middle" @click="viewMessage(message)" style="cursor: pointer;">
                    <small>{{ message.time_ago }}</small>
                  </td>
                  <td class="align-middle">
                    <button 
                      class="btn btn-sm btn-danger" 
                      @click.stop="deleteMessage(message.id)"
                      title="Delete"
                    >
                      <i class="fas fa-trash"></i>
                    </button>
                  </td>
                </tr>
                <tr v-if="filteredMessages.length === 0">
                  <td colspan="8" class="text-center">No messages found</td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </div>
  </section>

  <!-- Compose Modal -->
  <div class="modal fade" id="composeModal" tabindex="-1">
    <div class="modal-dialog modal-lg">
      <div class="modal-content">
        <div class="modal-header">
          <h4 class="modal-title"><i class="fas fa-paper-plane"></i> Compose Message</h4>
          <button type="button" class="close" @click="closeComposeModal">
            <span>&times;</span>
          </button>
        </div>
        <form @submit.prevent="sendMessage">
          <div class="modal-body">
            <div class="row">
              <div class="col-md-8">
                <div class="form-group">
                  <label>To <span class="text-danger">*</span></label>
                  <select 
                    v-model="composeForm.receiver" 
                    class="form-control" 
                    required
                  >
                    <option value="">Select Recipient</option>
                    <option v-for="user in users" :key="user.id" :value="user.id">
                      {{ user.first_name }} {{ user.last_name }} ({{ user.username }})
                    </option>
                  </select>
                </div>
              </div>
              <div class="col-md-4">
                <div class="form-group">
                  <label>Priority</label>
                  <select v-model="composeForm.priority" class="form-control">
                    <option value="low">Low</option>
                    <option value="normal">Normal</option>
                    <option value="high">High</option>
                    <option value="urgent">Urgent</option>
                  </select>
                </div>
              </div>
            </div>

            <div class="form-group">
              <label>Subject <span class="text-danger">*</span></label>
              <input 
                type="text" 
                v-model="composeForm.subject" 
                class="form-control" 
                required
                maxlength="200"
              >
            </div>

            <div class="form-group">
              <label>Message <span class="text-danger">*</span></label>
              <textarea 
                v-model="composeForm.body" 
                class="form-control" 
                rows="8"
                required
              ></textarea>
            </div>

            <div class="form-group">
              <label>Type</label>
              <select v-model="composeForm.message_type" class="form-control">
                <option value="message">Message</option>
                <option value="notification">Notification</option>
                <option value="system">System Alert</option>
              </select>
            </div>
          </div>
          <div class="modal-footer">
            <button type="button" class="btn btn-default" @click="closeComposeModal">Cancel</button>
            <button type="submit" class="btn btn-primary">
              <i class="fas fa-paper-plane"></i> Send
            </button>
          </div>
        </form>
      </div>
    </div>
  </div>

  <!-- View Message Modal -->
  <div class="modal fade" id="viewMessageModal" tabindex="-1">
    <div class="modal-dialog modal-lg">
      <div class="modal-content">
        <div class="modal-header">
          <h4 class="modal-title">
            <span 
              :class="{
                'badge badge-secondary': viewData.priority === 'low',
                'badge badge-info': viewData.priority === 'normal',
                'badge badge-warning': viewData.priority === 'high',
                'badge badge-danger': viewData.priority === 'urgent'
              }"
            >
              {{ viewData.priority }}
            </span>
            {{ viewData.subject }}
          </h4>
          <button type="button" class="close" @click="closeViewModal">
            <span>&times;</span>
          </button>
        </div>
        <div class="modal-body">
          <div class="mb-3">
            <strong>From:</strong> {{ viewData.sender_name }}<br>
            <strong>To:</strong> {{ viewData.receiver_name }}<br>
            <strong>Date:</strong> {{ viewData.time_ago }}<br>
            <strong>Type:</strong> <span class="badge badge-light">{{ viewData.message_type }}</span>
          </div>
          <hr>
          <div style="white-space: pre-wrap;">{{ viewData.body }}</div>
        </div>
        <div class="modal-footer">
          <button 
            v-if="activeTab === 'inbox'" 
            type="button" 
            class="btn btn-primary" 
            @click="replyToMessage"
          >
            <i class="fas fa-reply"></i> Reply
          </button>
          <button 
            v-if="activeTab === 'inbox' && viewData.is_read" 
            type="button" 
            class="btn btn-secondary" 
            @click="markAsUnread(viewData.id)"
          >
            <i class="far fa-envelope"></i> Mark as Unread
          </button>
          <button type="button" class="btn btn-default" @click="closeViewModal">Close</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import api from '../services/api'
import Swal from 'sweetalert2'

const messages = ref([])
const users = ref([])
const activeTab = ref('inbox')
const searchQuery = ref('')
const unreadCount = ref(0)
const selectedMessages = ref([])

const composeForm = ref({
  receiver: '',
  subject: '',
  body: '',
  priority: 'normal',
  message_type: 'message'
})

const viewData = ref({
  id: null,
  sender: null,
  sender_name: '',
  receiver_name: '',
  subject: '',
  body: '',
  priority: '',
  message_type: '',
  time_ago: '',
  is_read: false
})

// Clear selection when switching tabs
watch(activeTab, () => {
  selectedMessages.value = []
})

const filteredMessages = computed(() => {
  if (!searchQuery.value) return messages.value
  
  const query = searchQuery.value.toLowerCase()
  return messages.value.filter(message => 
    message.subject.toLowerCase().includes(query) ||
    message.body.toLowerCase().includes(query) ||
    (message.sender_name && message.sender_name.toLowerCase().includes(query)) ||
    (message.receiver_name && message.receiver_name.toLowerCase().includes(query))
  )
})

const fetchMessages = async () => {
  try {
    const endpoint = activeTab.value === 'inbox' ? '/messages/inbox/' : '/messages/sent/'
    const response = await api.get(endpoint)
    messages.value = response.data
    
    if (activeTab.value === 'inbox') {
      await fetchUnreadCount()
    }
  } catch (error) {
    console.error('Error fetching messages:', error)
    Swal.fire({
      icon: 'error',
      title: 'Error',
      text: 'Failed to fetch messages'
    })
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

const fetchUsers = async () => {
  try {
    const response = await api.get('/users/')
    users.value = response.data.filter(u => u.is_active)
  } catch (error) {
    console.error('Error fetching users:', error)
  }
}

const refreshMessages = async () => {
  const button = event.target.closest('button')
  const icon = button.querySelector('i')
  icon.classList.add('fa-spin')
  
  await fetchMessages()
  
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
    title: 'Messages refreshed'
  })
}

const openComposeModal = () => {
  resetComposeForm()
  showComposeModal()
}

const sendMessage = async () => {
  try {
    await api.post('/messages/', composeForm.value)
    
    Swal.fire({
      icon: 'success',
      title: 'Success!',
      text: 'Message sent successfully',
      timer: 1500,
      showConfirmButton: false
    })
    
    await fetchMessages()
    closeComposeModal()
  } catch (error) {
    console.error('Error sending message:', error)
    Swal.fire({
      icon: 'error',
      title: 'Error',
      text: error.response?.data?.message || 'Failed to send message'
    })
  }
}

const viewMessage = async (message) => {
  viewData.value = { ...message }
  
  // Mark as read if it's in inbox and unread
  if (activeTab.value === 'inbox' && !message.is_read) {
    try {
      await api.post(`/messages/${message.id}/mark_as_read/`)
      message.is_read = true
      await fetchUnreadCount()
    } catch (error) {
      console.error('Error marking as read:', error)
    }
  }
  
  showViewModal()
}

const markAsUnread = async (id) => {
  try {
    await api.post(`/messages/${id}/mark_as_unread/`)
    
    const message = messages.value.find(m => m.id === id)
    if (message) {
      message.is_read = false
    }
    
    await fetchUnreadCount()
    closeViewModal()
    
    Swal.fire({
      toast: true,
      position: 'top-end',
      icon: 'success',
      title: 'Marked as unread',
      showConfirmButton: false,
      timer: 2000
    })
  } catch (error) {
    console.error('Error marking as unread:', error)
  }
}

const replyToMessage = () => {
  const senderId = viewData.value.sender
  
  closeViewModal()
  
  composeForm.value = {
    receiver: senderId,
    subject: viewData.value.subject.startsWith('Re: ') 
      ? viewData.value.subject 
      : `Re: ${viewData.value.subject}`,
    body: '',
    priority: 'normal',
    message_type: 'message'
  }
  
  showComposeModal()
}

const toggleSelectAll = () => {
  if (selectedMessages.value.length === filteredMessages.value.length) {
    selectedMessages.value = []
  } else {
    selectedMessages.value = filteredMessages.value.map(m => m.id)
  }
}

const clearSelection = () => {
  selectedMessages.value = []
}

const markSelectedAsRead = async () => {
  if (selectedMessages.value.length === 0) return
  
  try {
    for (const id of selectedMessages.value) {
      await api.post(`/messages/${id}/mark_as_read/`)
    }
    
    await fetchMessages()
    selectedMessages.value = []
    
    Swal.fire({
      toast: true,
      position: 'top-end',
      icon: 'success',
      title: 'Messages marked as read',
      showConfirmButton: false,
      timer: 2000
    })
  } catch (error) {
    console.error('Error marking messages as read:', error)
    Swal.fire({
      icon: 'error',
      title: 'Error',
      text: 'Failed to mark messages as read'
    })
  }
}

const markSelectedAsUnread = async () => {
  if (selectedMessages.value.length === 0) return
  
  try {
    for (const id of selectedMessages.value) {
      await api.post(`/messages/${id}/mark_as_unread/`)
    }
    
    await fetchMessages()
    selectedMessages.value = []
    
    Swal.fire({
      toast: true,
      position: 'top-end',
      icon: 'success',
      title: 'Messages marked as unread',
      showConfirmButton: false,
      timer: 2000
    })
  } catch (error) {
    console.error('Error marking messages as unread:', error)
    Swal.fire({
      icon: 'error',
      title: 'Error',
      text: 'Failed to mark messages as unread'
    })
  }
}

const deleteSelected = async () => {
  if (selectedMessages.value.length === 0) return
  
  const result = await Swal.fire({
    title: 'Are you sure?',
    text: `Delete ${selectedMessages.value.length} message(s)?`,
    icon: 'warning',
    showCancelButton: true,
    confirmButtonColor: '#d33',
    cancelButtonColor: '#3085d6',
    confirmButtonText: 'Yes, delete them!'
  })
  
  if (result.isConfirmed) {
    try {
      for (const id of selectedMessages.value) {
        await api.delete(`/messages/${id}/`)
      }
      
      await fetchMessages()
      selectedMessages.value = []
      
      Swal.fire('Deleted!', 'Messages have been deleted.', 'success')
    } catch (error) {
      console.error('Error deleting messages:', error)
      Swal.fire({
        icon: 'error',
        title: 'Error',
        text: 'Failed to delete messages'
      })
    }
  }
}

const deleteMessage = async (id) => {
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
      await api.delete(`/messages/${id}/`)
      Swal.fire('Deleted!', 'Message has been deleted.', 'success')
      await fetchMessages()
    } catch (error) {
      console.error('Error deleting message:', error)
      Swal.fire({
        icon: 'error',
        title: 'Error',
        text: 'Failed to delete message'
      })
    }
  }
}

const resetComposeForm = () => {
  composeForm.value = {
    receiver: '',
    subject: '',
    body: '',
    priority: 'normal',
    message_type: 'message'
  }
}

const showComposeModal = () => {
  const modal = document.getElementById('composeModal')
  modal.classList.add('show')
  modal.style.display = 'block'
  document.body.classList.add('modal-open')
  
  const backdrop = document.createElement('div')
  backdrop.className = 'modal-backdrop fade show'
  backdrop.id = 'compose-modal-backdrop'
  document.body.appendChild(backdrop)
}

const closeComposeModal = () => {
  const modal = document.getElementById('composeModal')
  modal.classList.remove('show')
  modal.style.display = 'none'
  document.body.classList.remove('modal-open')
  
  const backdrop = document.getElementById('compose-modal-backdrop')
  if (backdrop) {
    backdrop.remove()
  }
  
  resetComposeForm()
}

const showViewModal = () => {
  const modal = document.getElementById('viewMessageModal')
  modal.classList.add('show')
  modal.style.display = 'block'
  document.body.classList.add('modal-open')
  
  const backdrop = document.createElement('div')
  backdrop.className = 'modal-backdrop fade show'
  backdrop.id = 'view-modal-backdrop'
  document.body.appendChild(backdrop)
}

const closeViewModal = () => {
  const modal = document.getElementById('viewMessageModal')
  modal.classList.remove('show')
  modal.style.display = 'none'
  document.body.classList.remove('modal-open')
  
  const backdrop = document.getElementById('view-modal-backdrop')
  if (backdrop) {
    backdrop.remove()
  }
}

onMounted(() => {
  fetchMessages()
  fetchUsers()
  
  // Auto-refresh messages every 10 seconds
  setInterval(() => {
    fetchMessages()
  }, 10000)
})
</script>

<style scoped>
.table-active {
  font-weight: bold;
}
</style>
