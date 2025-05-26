&lt;template>
  &lt;div class="mb-6 space-y-4">
    &lt;div class="flex flex-col md:flex-row gap-4">
      &lt;div class="flex-1">
        &lt;Input
          v-model="searchQuery"
          placeholder="Pesquisar por título, descrição ou local..."
          class="w-full"
        >
          &lt;template #prefix>
            &lt;svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="h-4 w-4 text-gray-500">
              &lt;circle cx="11" cy="11" r="8"/>
              &lt;path d="m21 21-4.3-4.3"/>
            &lt;/svg>
          &lt;/template>
        &lt;/Input>
      &lt;/div>
      
      &lt;div class="flex gap-2">
        &lt;Select v-model="selectedStatus" class="w-40">
          &lt;option value="">Todos os status&lt;/option>
          &lt;option value="RECEBIDO">Recebido&lt;/option>
          &lt;option value="CONFIRMADO">Confirmado&lt;/option>
          &lt;option value="ATENDIDO">Atendido&lt;/option>
          &lt;option value="CANCELADO">Cancelado&lt;/option>
        &lt;/Select>
        
        &lt;Button @click="toggleAdvancedFilters" variant="outline" size="icon" class="h-10 w-10">
          &lt;svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="h-4 w-4">
            &lt;path d="M3 6h18"/>
            &lt;path d="M7 12h10"/>
            &lt;path d="M10 18h4"/>
          &lt;/svg>
        &lt;/Button>
        
        &lt;Button @click="clearFilters" variant="outline" size="icon" class="h-10 w-10">
          &lt;svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="h-4 w-4">
            &lt;path d="M18 6 6 18"/>
            &lt;path d="m6 6 12 12"/>
          &lt;/svg>
        &lt;/Button>
      &lt;/div>
    &lt;/div>
    
    &lt;div v-if="showAdvancedFilters" class="grid grid-cols-1 md:grid-cols-3 gap-4 p-4 bg-gray-50 dark:bg-gray-800 rounded-lg border border-gray-200 dark:border-gray-700">
      &lt;div>
        &lt;label class="block text-sm font-medium mb-1 dark:text-gray-300">Período&lt;/label>
        &lt;div class="flex gap-2">
          &lt;div class="flex-1">
            &lt;label class="block text-xs text-gray-500 dark:text-gray-400 mb-1">De&lt;/label>
            &lt;Input type="date" v-model="startDate" class="w-full" />
          &lt;/div>
          &lt;div class="flex-1">
            &lt;label class="block text-xs text-gray-500 dark:text-gray-400 mb-1">Até&lt;/label>
            &lt;Input type="date" v-model="endDate" class="w-full" />
          &lt;/div>
        &lt;/div>
      &lt;/div>
      
      &lt;div>
        &lt;label class="block text-sm font-medium mb-1 dark:text-gray-300">Data específica&lt;/label>
        &lt;Input type="date" v-model="selectedDate" class="w-full" />
      &lt;/div>
      
      &lt;div class="flex items-end">
        &lt;Button @click="applyAdvancedFilters" class="w-full">
          Aplicar Filtros
        &lt;/Button>
      &lt;/div>
    &lt;/div>
    
    &lt;div v-if="hasActiveFilters" class="flex flex-wrap gap-2">
      &lt;div v-if="searchQuery" class="inline-flex items-center bg-gray-100 dark:bg-gray-700 text-sm px-3 py-1 rounded-full">
        Pesquisa: {{ searchQuery }}
        &lt;button @click="searchQuery = ''; emitFilters()" class="ml-2 text-gray-500 hover:text-gray-700 dark:text-gray-400 dark:hover:text-gray-200">
          &lt;svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="h-3 w-3">
            &lt;path d="M18 6 6 18"/>
            &lt;path d="m6 6 12 12"/>
          &lt;/svg>
        &lt;/button>
      &lt;/div>
      
      &lt;div v-if="selectedStatus" class="inline-flex items-center bg-gray-100 dark:bg-gray-700 text-sm px-3 py-1 rounded-full">
        Status: {{ getStatusDisplay(selectedStatus) }}
        &lt;button @click="selectedStatus = ''; emitFilters()" class="ml-2 text-gray-500 hover:text-gray-700 dark:text-gray-400 dark:hover:text-gray-200">
          &lt;svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="h-3 w-3">
            &lt;path d="M18 6 6 18"/>
            &lt;path d="m6 6 12 12"/>
          &lt;/svg>
        &lt;/button>
      &lt;/div>
      
      &lt;div v-if="selectedDate" class="inline-flex items-center bg-gray-100 dark:bg-gray-700 text-sm px-3 py-1 rounded-full">
        Data: {{ formatDate(selectedDate) }}
        &lt;button @click="selectedDate = ''; emitFilters()" class="ml-2 text-gray-500 hover:text-gray-700 dark:text-gray-400 dark:hover:text-gray-200">
          &lt;svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="h-3 w-3">
            &lt;path d="M18 6 6 18"/>
            &lt;path d="m6 6 12 12"/>
          &lt;/svg>
        &lt;/button>
      &lt;/div>
      
      &lt;div v-if="startDate || endDate" class="inline-flex items-center bg-gray-100 dark:bg-gray-700 text-sm px-3 py-1 rounded-full">
        Período: {{ startDate ? formatDate(startDate) : 'Início' }} - {{ endDate ? formatDate(endDate) : 'Fim' }}
        &lt;button @click="startDate = ''; endDate = ''; emitFilters()" class="ml-2 text-gray-500 hover:text-gray-700 dark:text-gray-400 dark:hover:text-gray-200">
          &lt;svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="h-3 w-3">
            &lt;path d="M18 6 6 18"/>
            &lt;path d="m6 6 12 12"/>
          &lt;/svg>
        &lt;/button>
      &lt;/div>
    &lt;/div>
  &lt;/div>
&lt;/template>

&lt;script setup lang="ts">
import { ref, computed, watch } from 'vue'
import debounce from 'lodash-es/debounce'
import { format, parseISO } from 'date-fns'
import { ptBR } from 'date-fns/locale'

const searchQuery = ref('')
const selectedStatus = ref('')
const selectedDate = ref('')
const startDate = ref('')
const endDate = ref('')
const showAdvancedFilters = ref(false)

const emit = defineEmits(['filter'])

const hasActiveFilters = computed(() => {
  return searchQuery.value || selectedStatus.value || selectedDate.value || startDate.value || endDate.value
})

const emitFilters = debounce(() => {
  emit('filter', {
    search: searchQuery.value,
    estado: selectedStatus.value,
    date: selectedDate.value,
    start_date: startDate.value,
    end_date: endDate.value
  })
}, 300)

watch([searchQuery, selectedStatus, selectedDate], emitFilters)

const applyAdvancedFilters = () => {
  emitFilters()
  showAdvancedFilters.value = false
}

const toggleAdvancedFilters = () => {
  showAdvancedFilters.value = !showAdvancedFilters.value
}

const clearFilters = () => {
  searchQuery.value = ''
  selectedStatus.value = ''
  selectedDate.value = ''
  startDate.value = ''
  endDate.value = ''
  showAdvancedFilters.value = false
  emitFilters()
}

const formatDate = (dateString: string) => {
  if (!dateString) return ''
  try {
    return format(parseISO(dateString), 'dd/MM/yyyy', { locale: ptBR })
  } catch (e) {
    return dateString
  }
}

const getStatusDisplay = (status: string) => {
  const statusMap: Record<string, string> = {
    'RECEBIDO': 'Recebido',
    'CONFIRMADO': 'Confirmado',
    'ATENDIDO': 'Atendido',
    'CANCELADO': 'Cancelado'
  }
  return statusMap[status] || status
}
&lt;/script>
