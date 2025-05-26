<template>
  <div class="calendar-wrapper">
    <div class="flex flex-col md:flex-row justify-between items-center mb-4 gap-4">
      <div class="flex items-center gap-2">
        <Button variant="outline" size="icon" @click="previousPeriod">
          <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="h-4 w-4">
            <path d="m15 18-6-6 6-6"/>
          </svg>
        </Button>
        <h2 class="text-2xl font-bold text-gray-900 dark:text-white">{{ currentPeriodLabel }}</h2>
        <Button variant="outline" size="icon" @click="nextPeriod">
          <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="h-4 w-4">
            <path d="m9 18 6-6-6-6"/>
          </svg>
        </Button>
        <Button variant="outline" size="sm" @click="currentDate = new Date()" class="ml-2">
          Hoje
        </Button>
      </div>
      <div class="flex space-x-2">
        <Button @click="currentView = 'month'" :variant="currentView === 'month' ? 'default' : 'outline'" size="sm">
          Mês
        </Button>
        <Button @click="currentView = 'week'" :variant="currentView === 'week' ? 'default' : 'outline'" size="sm">
          Semana
        </Button>
        <Button @click="currentView = 'day'" :variant="currentView === 'day' ? 'default' : 'outline'" size="sm">
          Dia
        </Button>
      </div>
    </div>
    
    <Card class="shadow-lg">
      <CardContent class="p-0">
        <!-- Month View -->
        <div v-if="currentView === 'month'" class="calendar-grid">
          <!-- Calendar Header -->
          <div class="calendar-header grid grid-cols-7 bg-gray-50 dark:bg-gray-900 border-b border-gray-200 dark:border-gray-700">
            <div v-for="day in weekDays" :key="day" class="p-2 text-center text-sm font-medium text-gray-700 dark:text-gray-300">
              {{ day }}
            </div>
          </div>
          
          <!-- Calendar Body -->
          <div class="calendar-body grid grid-cols-7 bg-white dark:bg-gray-800">
            <div
              v-for="date in monthDates"
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
              <div class="mt-1 space-y-1 max-h-[80px] overflow-y-auto">
                <div
                  v-for="event in getEventsForDate(date)"
                  :key="event.id"
                  class="text-xs p-1 rounded truncate cursor-pointer flex items-center gap-1"
                  :class="getEventClasses(event.status)"
                  @click.stop="handleEventClick(event)"
                >
                  <div class="w-1 h-1 rounded-full" :class="getStatusDotClass(event.status)"></div>
                  <span>{{ formatTime(event.start) }}</span>
                  <span class="truncate">{{ event.title }}</span>
                </div>
              </div>
              
              <!-- More indicator if there are too many events -->
              <div v-if="getEventsForDate(date).length > 3" class="text-xs text-center mt-1 text-gray-500 dark:text-gray-400">
                + {{ getEventsForDate(date).length - 3 }} mais
              </div>
            </div>
          </div>
        </div>
        
        <!-- Week View -->
        <div v-else-if="currentView === 'week'" class="week-view">
          <div class="grid grid-cols-8 bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-700">
            <!-- Time column -->
            <div class="border-r border-gray-200 dark:border-gray-700">
              <div class="h-12 border-b border-gray-200 dark:border-gray-700"></div>
              <div v-for="hour in 24" :key="hour" class="h-16 border-b border-gray-200 dark:border-gray-700 text-xs text-gray-500 dark:text-gray-400 p-1">
                {{ hour - 1 }}:00
              </div>
            </div>
            
            <!-- Days columns -->
            <div v-for="date in weekDates" :key="date.toISOString()" class="relative border-r border-gray-200 dark:border-gray-700 last:border-r-0">
              <!-- Day header -->
              <div 
                class="h-12 border-b border-gray-200 dark:border-gray-700 text-center py-2 sticky top-0 z-10 bg-gray-50 dark:bg-gray-900"
                :class="{ 'bg-blue-50 dark:bg-blue-900/20': isToday(date) }"
              >
                <div class="text-sm font-medium">{{ format(date, 'EEE', { locale: ptBR }) }}</div>
                <div 
                  class="text-sm" 
                  :class="{ 'font-bold': isToday(date) }"
                >
                  {{ date.getDate() }}
                </div>
              </div>
              
              <!-- Hours grid -->
              <div>
                <div v-for="hour in 24" :key="hour" class="h-16 border-b border-gray-200 dark:border-gray-700"></div>
              </div>
              
              <!-- Events -->
              <div class="absolute top-12 left-0 right-0 pointer-events-none">
                <div
                  v-for="event in getEventsForDate(date)"
                  :key="event.id"
                  class="absolute mx-1 rounded text-xs p-1 cursor-pointer overflow-hidden pointer-events-auto"
                  :class="getEventClasses(event.status)"
                  :style="getEventPositionStyle(event)"
                  @click.stop="handleEventClick(event)"
                >
                  <div class="font-medium">{{ event.title }}</div>
                  <div>{{ formatTimeRange(event.start, event.end) }}</div>
                </div>
              </div>
            </div>
          </div>
        </div>
        
        <!-- Day View -->
        <div v-else-if="currentView === 'day'" class="day-view">
          <div class="grid grid-cols-2 bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-700">
            <!-- Time column -->
            <div class="border-r border-gray-200 dark:border-gray-700 col-span-1">
              <div class="h-12 border-b border-gray-200 dark:border-gray-700 bg-gray-50 dark:bg-gray-900 text-center py-2">
                <div class="text-sm font-medium">{{ format(currentDate, 'EEEE', { locale: ptBR }) }}</div>
                <div class="text-sm font-bold">{{ format(currentDate, 'dd/MM/yyyy') }}</div>
              </div>
              <div v-for="hour in 24" :key="hour" class="h-16 border-b border-gray-200 dark:border-gray-700 text-xs text-gray-500 dark:text-gray-400 p-1">
                {{ hour - 1 }}:00
              </div>
            </div>
            
            <!-- Events column -->
            <div class="relative col-span-1">
              <!-- Day header -->
              <div class="h-12 border-b border-gray-200 dark:border-gray-700 bg-gray-50 dark:bg-gray-900"></div>
              
              <!-- Hours grid -->
              <div>
                <div v-for="hour in 24" :key="hour" class="h-16 border-b border-gray-200 dark:border-gray-700"></div>
              </div>
              
              <!-- Events -->
              <div class="absolute top-12 left-0 right-0 pointer-events-none">
                <div
                  v-for="event in getEventsForDate(currentDate)"
                  :key="event.id"
                  class="absolute mx-1 rounded text-xs p-1 cursor-pointer overflow-hidden pointer-events-auto"
                  :class="getEventClasses(event.status)"
                  :style="getEventPositionStyle(event)"
                  @click.stop="handleEventClick(event)"
                >
                  <div class="font-medium">{{ event.title }}</div>
                  <div>{{ formatTimeRange(event.start, event.end) }}</div>
                  <div class="text-xs truncate">{{ event.location || 'Sem local' }}</div>
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
import { 
  format, formatISO, parse, parseISO,
  startOfMonth, endOfMonth, eachDayOfInterval, 
  startOfWeek, endOfWeek, isSameMonth, isToday as isDateToday,
  addMonths, subMonths, addWeeks, subWeeks, addDays, subDays,
  differenceInMinutes, getHours, getMinutes
} from 'date-fns'
import { ptBR } from 'date-fns/locale'
import type { Agenda } from '~/types/agenda'

const props = defineProps<{
  agendas: Agenda[]
}>()

const currentView = ref('month')
const currentDate = ref(new Date())

// Navigation functions
const nextPeriod = () => {
  if (currentView.value === 'month') {
    currentDate.value = addMonths(currentDate.value, 1)
  } else if (currentView.value === 'week') {
    currentDate.value = addWeeks(currentDate.value, 1)
  } else if (currentView.value === 'day') {
    currentDate.value = addDays(currentDate.value, 1)
  }
}

const previousPeriod = () => {
  if (currentView.value === 'month') {
    currentDate.value = subMonths(currentDate.value, 1)
  } else if (currentView.value === 'week') {
    currentDate.value = subWeeks(currentDate.value, 1)
  } else if (currentView.value === 'day') {
    currentDate.value = subDays(currentDate.value, 1)
  }
}

// Period label
const currentPeriodLabel = computed(() => {
  if (currentView.value === 'month') {
    return format(currentDate.value, 'MMMM yyyy', { locale: ptBR })
  } else if (currentView.value === 'week') {
    const weekStart = startOfWeek(currentDate.value)
    const weekEnd = endOfWeek(currentDate.value)
    if (weekStart.getMonth() === weekEnd.getMonth()) {
      return `${format(weekStart, 'dd')} - ${format(weekEnd, 'dd')} de ${format(weekStart, 'MMMM yyyy', { locale: ptBR })}`
    } else {
      return `${format(weekStart, 'dd MMM')} - ${format(weekEnd, 'dd MMM yyyy', { locale: ptBR })}`
    }
  } else {
    return format(currentDate.value, 'dd MMMM yyyy', { locale: ptBR })
  }
})

const weekDays = computed(() => {
  const days = []
  const date = startOfWeek(new Date())
  for (let i = 0; i < 7; i++) {
    days.push(format(date, 'EEE', { locale: ptBR }))
    date.setDate(date.getDate() + 1)
  }
  return days
})

// Different date calculations for different views
const monthDates = computed(() => {
  const start = startOfWeek(startOfMonth(currentDate.value))
  const end = endOfWeek(endOfMonth(currentDate.value))
  return eachDayOfInterval({ start, end })
})

const weekDates = computed(() => {
  const start = startOfWeek(currentDate.value)
  const end = endOfWeek(currentDate.value)
  return eachDayOfInterval({ start, end })
})

const isCurrentMonth = (date: Date) => {
  return isSameMonth(date, currentDate.value)
}

const isToday = (date: Date) => {
  return isDateToday(date)
}

// Format helpers
const formatTime = (date: Date) => {
  return format(date, 'HH:mm')
}

const formatTimeRange = (start: Date, end: Date) => {
  return `${formatTime(start)} - ${formatTime(end)}`
}

// Event styling helpers
const getEventClasses = (status: string) => {
  switch (status) {
    case 'CONFIRMADO':
      return 'bg-green-100 dark:bg-green-900/20 text-green-800 dark:text-green-200'
    case 'ATENDIDO':
      return 'bg-blue-100 dark:bg-blue-900/20 text-blue-800 dark:text-blue-200'
    case 'CANCELADO':
      return 'bg-red-100 dark:bg-red-900/20 text-red-800 dark:text-red-200'
    default: // RECEBIDO
      return 'bg-gray-100 dark:bg-gray-700 text-gray-800 dark:text-gray-200'
  }
}

const getStatusDotClass = (status: string) => {
  switch (status) {
    case 'CONFIRMADO':
      return 'bg-green-500'
    case 'ATENDIDO':
      return 'bg-blue-500'
    case 'CANCELADO':
      return 'bg-red-500'
    default: // RECEBIDO
      return 'bg-gray-500'
  }
}

// Position calculation for week/day views
const getEventPositionStyle = (event: any) => {
  const startHour = getHours(event.start)
  const startMinute = getMinutes(event.start)
  const durationMinutes = differenceInMinutes(event.end, event.start)
  
  const top = (startHour * 16) + (startMinute / 60 * 16) // 16px per hour
  const height = (durationMinutes / 60) * 16 // Convert minutes to hours, then to pixels
  
  return {
    top: `${top}px`,
    height: `${Math.max(height, 16)}px`, // Minimum height of 16px
    left: '0',
    right: '0'
  }
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
      description: agenda.descricao,
      location: agenda.local,
      status: agenda.estadoAtualAgenda, // Changed from status to estadoAtualAgenda to match API
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
