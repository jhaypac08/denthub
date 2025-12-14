<template>
  <div class="row mt-3">
    <div class="col-sm-12 col-md-5">
      <div class="dataTables_info">
        Showing {{ startItem }} to {{ endItem }} of {{ total }} entries
      </div>
    </div>
    <div class="col-sm-12 col-md-7">
      <div class="dataTables_paginate paging_simple_numbers float-right">
        <ul class="pagination">
          <li class="paginate_button page-item previous" :class="{ disabled: currentPage === 1 }">
            <a href="javascript:void(0)" class="page-link" @click="goToPage(currentPage - 1)">Previous</a>
          </li>
          
          <li v-for="page in visiblePages" :key="page" class="paginate_button page-item" :class="{ active: page === currentPage }">
            <a href="javascript:void(0)" class="page-link" @click="goToPage(page)">{{ page }}</a>
          </li>
          
          <li class="paginate_button page-item next" :class="{ disabled: currentPage === totalPages }">
            <a href="javascript:void(0)" class="page-link" @click="goToPage(currentPage + 1)">Next</a>
          </li>
        </ul>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  currentPage: {
    type: Number,
    required: true
  },
  perPage: {
    type: Number,
    required: true
  },
  total: {
    type: Number,
    required: true
  }
})

const emit = defineEmits(['page-change'])

const totalPages = computed(() => Math.ceil(props.total / props.perPage))

const startItem = computed(() => {
  if (props.total === 0) return 0
  return (props.currentPage - 1) * props.perPage + 1
})

const endItem = computed(() => {
  const end = props.currentPage * props.perPage
  return end > props.total ? props.total : end
})

const visiblePages = computed(() => {
  const pages = []
  const total = totalPages.value
  const current = props.currentPage
  
  if (total <= 7) {
    for (let i = 1; i <= total; i++) {
      pages.push(i)
    }
  } else {
    if (current <= 4) {
      for (let i = 1; i <= 5; i++) {
        pages.push(i)
      }
      pages.push('...')
      pages.push(total)
    } else if (current >= total - 3) {
      pages.push(1)
      pages.push('...')
      for (let i = total - 4; i <= total; i++) {
        pages.push(i)
      }
    } else {
      pages.push(1)
      pages.push('...')
      for (let i = current - 1; i <= current + 1; i++) {
        pages.push(i)
      }
      pages.push('...')
      pages.push(total)
    }
  }
  
  return pages.filter(p => p !== '...' || pages.indexOf(p) === pages.lastIndexOf(p))
})

const goToPage = (page) => {
  if (page < 1 || page > totalPages.value || page === props.currentPage) {
    return
  }
  emit('page-change', page)
}
</script>

<style scoped>
.dataTables_info {
  padding-top: 0.85em;
}

.pagination {
  margin-bottom: 0;
}

.page-item.disabled .page-link {
  cursor: not-allowed;
}

.page-item.active .page-link {
  background-color: #007bff;
  border-color: #007bff;
  color: #ffffff !important;
}

.page-link {
  color: #007bff;
}

.page-link:hover {
  color: #0056b3;
}
</style>
