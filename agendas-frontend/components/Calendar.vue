<template>
  <div class="calendar-wrapper">
    <div class="flex justify-between items-center mb-4">
      <h2 class="text-2xl font-bold text-gray-900 dark:text-white">Calendário de Agendas</h2>
      <div class="flex space-x-2">
        <Button @click="currentView = 'month'" :variant="currentView === 'month' ? 'default' : 'outline'">
          Mês
        </Button>
        <Button @click="currentView = 'week'" :variant="currentView === 'week' ? 'default' : 'outline'">
          Semana
        </Button>
        <Button @click="currentView = 'day'" :variant="currentView === 'day' ? 'default' : 'outline'">
          Dia
        </Button>
      </div>
    </div>
    
    <Card class="shadow-lg">
      <CardContent class="p-0">
        <div class="calendar-grid">
          <!-- Calendar Header -->
          <div class="calendar-header grid grid-cols-7 bg-gray-50 dark:bg-gray-900 border-b border-gray-200 dark:border-gray-700">
            <div v-for="day in weekDays" :key="day" class="p-2 text-center text-sm font-medium text-gray-700 dark:text-gray-300">
              {{ day }}
            </div>
          </div>
          
          <!-- Calendar Body -->
          <div class="calendar-body grid grid-cols-7 bg-white dark:bg-gray-800">
            <div
              v-for="date in calendarDates"
              :key="date.toISOString()"
              class="min-h-[100px] p-2 border-b border-r border-gray-200 dark:border-gray-700 relative"
              :class="{
                'bg-gray-50 dark:bg-gray-900': !isCurrentMonth(date),
                'bg-blue-50 dark:bg-blue-900/20': isToday(date)
              }"
              @click="handleDateClick(date)"
            >
              <span
                class="text-sm"
                :class="{
                  'text-gray-400 dark:text-gray-600': !isCurrentMonth(date),
                  'font-bold': isToday(date)
                }"
              >
                {{ date.getDate() }}
              </span>
              
              <!-- Events for this date -->
              <div class="mt-1 space-y-1">
                <div
                  v-for="event in getEventsForDate(date)"
                  :key="event.id"
                  class="text-xs p-1 rounded truncate cursor-pointer"
                  :class="{
                    'bg-green-100 dark:bg-green-900/20 text-green-800 dark:text-green-200': event.status === 'CONFIRMADO',
                    'bg-gray-100 dark:bg-gray-700 text-gray-800 dark:text-gray-200': event.status !== 'CONFIRMADO'
                  }"
                  @click.stop="handleEventClick(event)"
                >
                  {{ event.title }}
                </div>
              </div>
            </div>
          </div>
        </div>
      </CardContent>
    </Card>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import { format, startOfMonth, endOfMonth, eachDayOfInterval, startOfWeek, endOfWeek, isSameMonth, isToday as isDateToday } from 'date-fns'
import { ptBR } from 'date-fns/locale'
import type { Agenda } from '~/types/agenda'

const props = defineProps<{
  agendas: Agenda[]
}>()

const currentView = ref('month')
const currentDate = ref(new Date())

const weekDays = computed(() => {
  const days = []
  const date = startOfWeek(new Date())
  for (let i = 0; i < 7; i++) {
    days.push(format(date, 'EEE', { locale: ptBR }))
    date.setDate(date.getDate() + 1)
  }
  return days
})

const calendarDates = computed(() => {
  const start = startOfWeek(startOfMonth(currentDate.value))
  const end = endOfWeek(endOfMonth(currentDate.value))
  return eachDayOfInterval({ start, end })
})

const isCurrentMonth = (date: Date) => {
  return isSameMonth(date, currentDate.value)
}

const isToday = (date: Date) => {
  return isDateToday(date)
}

const getEventsForDate = (date: Date) => {
  return props.agendas
    .filter(agenda => {
      const eventDate = new Date(agenda.dataInicio)
      return eventDate.getDate() === date.getDate() &&
             eventDate.getMonth() === date.getMonth() &&
             eventDate.getFullYear() === date.getFullYear()
    })
    .map(agenda => ({
      id: agenda.id,
      title: agenda.titulo,
      status: agenda.status,
      start: new Date(agenda.dataInicio),
      end: new Date(agenda.dataFim)
    }))
}

const emit = defineEmits(['event-click', 'date-click'])

const handleEventClick = (event: any) => {
  emit('event-click', event)
}

const handleDateClick = (date: Date) => {
  emit('date-click', date)
}
</script>

<style scoped>
.calendar-grid {
  @apply border border-gray-200 dark:border-gray-700 rounded-lg overflow-hidden;
}

.calendar-header {
  @apply sticky top-0 z-10;
}

.calendar-body > div:nth-child(7n) {
  @apply border-r-0;
}

.calendar-body > div:nth-last-child(-n+7) {
  @apply border-b-0;
}
</style>
