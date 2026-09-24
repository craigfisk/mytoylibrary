<template>
  <div class="absolute inset-0 bg-black bg-opacity-50 flex items-center justify-center z-[2000] p-4">
    <div class="bg-white rounded-lg shadow-2xl w-full max-w-4xl max-h-full flex flex-col overflow-hidden">
      <div class="p-4 bg-green-600 text-white flex justify-between items-center">
        <div>
          <h2 class="text-2xl font-bold">Toy Database</h2>
          <p class="text-sm opacity-90" v-if="library">{{ library.name }}</p>
        </div>
        <button @click="$emit('close')" class="text-white hover:text-gray-200">
          <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
          </svg>
        </button>
      </div>

      <div class="p-4 flex-1 overflow-y-auto">
        <div class="flex justify-between items-center mb-6">
          <h3 class="text-xl font-bold">Available Inventory</h3>
          <div class="bg-green-100 text-green-800 px-3 py-1 rounded-full text-sm font-semibold">
            Holds Placed: {{ activeHolds.length }} / 3
          </div>
        </div>

        <div v-if="loading" class="text-center py-10">
          Loading inventory...
        </div>

        <div v-else class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          <div v-for="toy in inventory" :key="toy.id" class="border rounded-lg overflow-hidden flex flex-col shadow-sm hover:shadow-md transition">
            <div class="h-48 bg-gray-200 flex items-center justify-center text-gray-500 font-medium">
              <!-- Placeholder for toy image -->
              [Image: {{ toy.category }}]
            </div>
            <div class="p-4 flex-1 flex flex-col">
              <h4 class="font-bold text-lg mb-1">{{ toy.name }}</h4>
              <p class="text-sm text-gray-500 mb-2">Ages: {{ toy.ages }}</p>
              <p class="text-sm mb-4 flex-1">{{ toy.description }}</p>
              
              <button 
                @click="placeHold(toy)" 
                :disabled="isHeld(toy.id) || activeHolds.length >= 3"
                :class="[
                  'w-full py-2 rounded font-bold transition',
                  isHeld(toy.id) ? 'bg-gray-300 text-gray-600 cursor-not-allowed' : 
                  activeHolds.length >= 3 ? 'bg-gray-300 text-gray-600 cursor-not-allowed' : 
                  'bg-green-600 hover:bg-green-700 text-white'
                ]"
              >
                {{ isHeld(toy.id) ? 'Hold Placed' : (activeHolds.length >= 3 ? 'Hold Limit Reached' : 'Place Hold') }}
              </button>
            </div>
          </div>
        </div>
      </div>

      <div class="p-4 border-t bg-gray-50" v-if="activeHolds.length > 0">
        <h3 class="font-bold mb-2">My Current Holds (Expires in 1 week)</h3>
        <ul class="space-y-2">
          <li v-for="hold in activeHolds" :key="hold.id" class="flex justify-between items-center text-sm bg-white p-2 border rounded">
            <span>{{ hold.name }}</span>
            <button @click="removeHold(hold.id)" class="text-red-500 hover:text-red-700 font-semibold">Remove</button>
          </li>
        </ul>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'

const props = defineProps({
  library: { type: Object, default: null }
})

const emit = defineEmits(['close'])

const loading = ref(true)
const inventory = ref<any[]>([])
const activeHolds = ref<any[]>([])

const fetchInventory = () => {
  loading.value = true
  setTimeout(() => {
    // Mock inventory data
    inventory.value = [
      { id: 1, name: 'Wooden Train Set', category: 'Building', ages: '3-5', description: 'Classic wooden train set with 50 pieces.' },
      { id: 2, name: 'Shape Sorter Cube', category: 'Educational', ages: '1-3', description: 'Helps with color and shape recognition.' },
      { id: 3, name: 'Magnet Tiles', category: 'Building', ages: '3+', description: 'Magnetic building tiles for creative play.' },
      { id: 4, name: 'Interactive Learning Globe', category: 'Educational', ages: '5-8', description: 'Explore the world with an interactive pen.' },
      { id: 5, name: 'Duplo Basic Bricks', category: 'Building', ages: '1.5-3', description: 'Large Lego bricks for toddlers.' },
      { id: 6, name: 'Dollhouse with Furniture', category: 'Pretend Play', ages: '3-6', description: 'Three-story dollhouse with wooden furniture.' }
    ]
    loading.value = false
  }, 800)
}

const placeHold = (toy: any) => {
  if (activeHolds.value.length < 3 && !isHeld(toy.id)) {
    activeHolds.value.push(toy)
  }
}

const removeHold = (id: number) => {
  activeHolds.value = activeHolds.value.filter(t => t.id !== id)
}

const isHeld = (id: number) => {
  return activeHolds.value.some(t => t.id === id)
}

onMounted(() => {
  fetchInventory()
})
</script>