&lt;template>
  &lt;div
    class="fixed bottom-4 right-4 z-50 flex flex-col gap-2"
    style="max-height: 100vh; overflow-y: auto"
  >
    &lt;TransitionGroup name="notification">
      &lt;div
        v-for="notification in notifications"
        :key="notification.id"
        class="min-w-[300px] p-4 rounded-lg shadow-lg transform transition-all duration-300"
        :class="{
          'bg-green-50 dark:bg-green-900/20 border border-green-200 dark:border-green-800': notification.type === 'success',
          'bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-800': notification.type === 'error',
          'bg-blue-50 dark:bg-blue-900/20 border border-blue-200 dark:border-blue-800': notification.type === 'info'
        }"
      >
        &lt;div class="flex items-start gap-3">
          &lt;div class="flex-shrink-0">
            &lt;Icon
              :name="getIcon(notification.type)"
              class="h-5 w-5"
              :class="{
                'text-green-500 dark:text-green-400': notification.type === 'success',
                'text-red-500 dark:text-red-400': notification.type === 'error',
                'text-blue-500 dark:text-blue-400': notification.type === 'info'
              }"
            />
          &lt;/div>
          &lt;div class="flex-1">
            &lt;p
              class="text-sm font-medium"
              :class="{
                'text-green-800 dark:text-green-200': notification.type === 'success',
                'text-red-800 dark:text-red-200': notification.type === 'error',
                'text-blue-800 dark:text-blue-200': notification.type === 'info'
              }"
            >
              {{ notification.message }}
            &lt;/p>
          &lt;/div>
          &lt;button
            @click="removeNotification(notification.id)"
            class="flex-shrink-0 ml-4 text-gray-400 hover:text-gray-500 focus:outline-none"
          >
            &lt;Icon name="lucide:x" class="h-4 w-4" />
          &lt;/button>
        &lt;/div>
      &lt;/div>
    &lt;/TransitionGroup>
  &lt;/div>
&lt;/template>

&lt;script setup lang="ts">
import { ref } from 'vue'

interface Notification {
  id: number
  type: 'success' | 'error' | 'info'
  message: string
}

const notifications = ref<Notification[]>([])
let notificationId = 0

const getIcon = (type: string) => {
  switch (type) {
    case 'success':
      return 'lucide:check-circle'
    case 'error':
      return 'lucide:x-circle'
    default:
      return 'lucide:info'
  }
}

const addNotification = (type: 'success' | 'error' | 'info', message: string) => {
  const id = notificationId++
  notifications.value.push({ id, type, message })
  setTimeout(() => removeNotification(id), 5000)
}

const removeNotification = (id: number) => {
  const index = notifications.value.findIndex(n => n.id === id)
  if (index !== -1) {
    notifications.value.splice(index, 1)
  }
}

defineExpose({
  addNotification
})
&lt;/script>

&lt;style scoped>
.notification-enter-active,
.notification-leave-active {
  transition: all 0.3s ease;
}

.notification-enter-from {
  opacity: 0;
  transform: translateX(30px);
}

.notification-leave-to {
  opacity: 0;
  transform: translateX(30px);
}
&lt;/style>
