<template>
  <div class="absolute top-0 right-0 w-full md:w-96 h-full bg-white shadow-xl z-[1000] flex flex-col transform transition-transform border-l">
    <div class="p-4 bg-blue-600 text-white flex justify-between items-center shadow">
      <h2 class="text-xl font-bold">Transit Planner</h2>
      <button @click="$emit('close')" class="text-white hover:text-gray-200">
        <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
        </svg>
      </button>
    </div>

    <div class="p-4 flex-1 overflow-y-auto">
      <div class="mb-4">
        <label class="block text-sm font-medium text-gray-700 mb-1">Origin</label>
        <select v-model="originType" class="w-full border-gray-300 rounded-md shadow-sm focus:border-blue-500 focus:ring-blue-500 border p-2">
          <option value="current">Current Location (Geolocation)</option>
          <option value="base">Saved Base: {{ origin ? origin.name : 'None Selected' }}</option>
        </select>
        <p v-if="originType === 'base' && !origin" class="text-red-500 text-sm mt-1">Please select a community center on the map as your base.</p>
      </div>

      <div class="mb-4">
        <label class="block text-sm font-medium text-gray-700 mb-1">Destination (Toy Library)</label>
        <select v-model="selectedDestination" class="w-full border-gray-300 rounded-md shadow-sm focus:border-blue-500 focus:ring-blue-500 border p-2">
          <option v-for="dest in destinations" :key="dest.id" :value="dest.id">
            {{ dest.name }}
          </option>
        </select>
      </div>

      <div class="mb-4 border-t pt-4">
        <label class="block text-sm font-medium text-gray-700 mb-2">Departure/Arrival Time</label>
        <div class="flex gap-2 mb-2">
          <label class="inline-flex items-center">
            <input type="radio" v-model="timeMode" value="now" class="text-blue-600">
            <span class="ml-2 text-sm">Now</span>
          </label>
          <label class="inline-flex items-center">
            <input type="radio" v-model="timeMode" value="depart" class="text-blue-600">
            <span class="ml-2 text-sm">Depart At</span>
          </label>
          <label class="inline-flex items-center">
            <input type="radio" v-model="timeMode" value="arrive" class="text-blue-600">
            <span class="ml-2 text-sm">Arrive By</span>
          </label>
        </div>

        <div v-if="timeMode !== 'now'" class="flex gap-2">
          <input type="date" v-model="customDate" class="w-1/2 border-gray-300 rounded-md border p-2 text-sm">
          <input type="time" v-model="customTime" class="w-1/2 border-gray-300 rounded-md border p-2 text-sm">
        </div>
      </div>

      <button @click="planRoute" class="w-full bg-blue-600 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded transition">
        Find Routes
      </button>

      <div v-if="loading" class="mt-4 text-center text-gray-600">
        Finding routes...
      </div>

      <div v-if="results" class="mt-6 border-t pt-4">
        <h3 class="font-bold text-lg mb-3">Outbound Route</h3>
        <div class="bg-gray-50 border p-3 rounded mb-4">
          <p class="text-sm font-semibold text-blue-800">{{ results.outbound.summary }}</p>
          <p class="text-xs text-gray-600 mt-1">Departs: {{ results.outbound.departTime }}</p>
          <p class="text-xs text-gray-600">Arrives: {{ results.outbound.arriveTime }}</p>
        </div>

        <h3 class="font-bold text-lg mb-3">Return Route</h3>
        <div class="bg-gray-50 border p-3 rounded">
          <p class="text-sm font-semibold text-blue-800">{{ results.return.summary }}</p>
          <p class="text-xs text-gray-600 mt-1">Departs: {{ results.return.departTime }}</p>
          <p class="text-xs text-gray-600">Arrives: {{ results.return.arriveTime }}</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'

const props = defineProps<{
  destinations: any[]
  origin?: any
  initialDestination?: number | null
}>()

const emit = defineEmits(['close'])

const originType = ref('current')
const selectedDestination = ref(props.initialDestination || (props.destinations.length ? props.destinations[0].id : null))
const timeMode = ref('now')
const customDate = ref('')
const customTime = ref('')
const loading = ref(false)
const results = ref<any>(null)

const planRoute = () => {
  loading.value = true
  results.value = null
  
  // Simulate API delay
  setTimeout(() => {
    loading.value = false
    // Mock results for prototype
    results.value = {
      outbound: {
        summary: 'Bus Route 2 -> Light Rail Blue Line',
        departTime: timeMode.value === 'now' ? 'In 5 mins' : `${customDate.value} ${customTime.value}`,
        arriveTime: '45 mins later'
      },
      return: {
        summary: 'Light Rail Blue Line -> Bus Route 2',
        departTime: '1 hour 30 mins later',
        arriveTime: '2 hours 15 mins later'
      }
    }
  }, 1000)
}
</script>