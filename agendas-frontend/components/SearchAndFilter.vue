&lt;template>
  &lt;div class="flex flex-col md:flex-row gap-4 mb-6">
    &lt;div class="flex-1">
      &lt;Input
        v-model="searchQuery"
        placeholder="Pesquisar agendas..."
        class="w-full"
      >
        &lt;template #prefix>
          &lt;Icon name="lucide:search" class="h-4 w-4 text-gray-500" />
        &lt;/template>
      &lt;/Input>
    &lt;/div>
    
    &lt;div class="flex gap-2">
      &lt;Select v-model="selectedStatus" class="w-40">
        &lt;option value="">Todos os status&lt;/option>
        &lt;option value="CONFIRMADO">Confirmado&lt;/option>
        &lt;option value="PENDENTE">Pendente&lt;/option>
        &lt;option value="CANCELADO">Cancelado&lt;/option>
      &lt;/Select>
      
      &lt;DatePicker v-model="selectedDate" class="w-40" />
      
      &lt;Button @click="clearFilters" variant="outline">
        &lt;Icon name="lucide:x" class="h-4 w-4 mr-2" />
        Limpar
      &lt;/Button>
    &lt;/div>
  &lt;/div>
&lt;/template>

&lt;script setup lang="ts">
import { ref, watch } from 'vue'
import debounce from 'lodash-es/debounce'

const searchQuery = ref('')
const selectedStatus = ref('')
const selectedDate = ref('')

const emit = defineEmits(['filter'])

const emitFilters = debounce(() => {
  emit('filter', {
    query: searchQuery.value,
    status: selectedStatus.value,
    date: selectedDate.value
  })
}, 300)

watch([searchQuery, selectedStatus, selectedDate], emitFilters)

const clearFilters = () => {
  searchQuery.value = ''
  selectedStatus.value = ''
  selectedDate.value = ''
  emitFilters()
}
&lt;/script>
