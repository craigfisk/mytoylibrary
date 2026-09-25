<template>
  <div class="h-full w-full flex flex-col md:flex-row relative">
    <div id="map-container" class="w-full h-full md:flex-1" ref="mapEl"></div>

    <!-- UI Overlay for Modals -->
    <TransitPlanner v-if="showTransit" @close="showTransit = false" :destinations="libraries" :origin="selectedBase" :initial-destination="selectedDestinationId" />
    <ToyDatabase v-if="showDatabase" @close="showDatabase = false" :library="selectedLibrary" />
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, onUnmounted } from 'vue'
import L from 'leaflet'
import 'leaflet/dist/leaflet.css'
import TransitPlanner from './TransitPlanner.vue'
import ToyDatabase from './ToyDatabase.vue'

const mapEl = ref<HTMLElement | null>(null)
let map: L.Map | null = null

const showTransit = ref(false)
const showDatabase = ref(false)
const selectedLibrary = ref(null)
const selectedBase = ref(null)
const selectedDestinationId = ref<number | null>(null)

const libraries = [
  { id: 1, name: 'Minneapolis Toy Library - Northeast', lat: 45.0039, lng: -93.2570 },
  { id: 2, name: 'Minneapolis Toy Library - South', lat: 44.9602, lng: -93.2324 },
  { id: 3, name: 'St. Paul Toy Library', lat: 44.9387, lng: -93.1557 },
]

const communityCenters = ref<any[]>([])

const customIcon = L.icon({
  iconUrl: 'https://unpkg.com/leaflet@1.9.4/dist/images/marker-icon.png',
  shadowUrl: 'https://unpkg.com/leaflet@1.9.4/dist/images/marker-shadow.png',
  iconSize: [25, 41],
  iconAnchor: [12, 41],
  popupAnchor: [1, -34],
  shadowSize: [41, 41]
});

const redIcon = L.icon({
  iconUrl: 'https://raw.githubusercontent.com/pointhi/leaflet-color-markers/master/img/marker-icon-2x-red.png',
  shadowUrl: 'https://unpkg.com/leaflet@1.9.4/dist/images/marker-shadow.png',
  iconSize: [25, 41],
  iconAnchor: [12, 41],
  popupAnchor: [1, -34],
  shadowSize: [41, 41]
});


const initMap = async () => {
  if (!mapEl.value) return

  map = L.map(mapEl.value).setView([44.9778, -93.2650], 11) // Centered on MSP
  L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '© OpenStreetMap'
  }).addTo(map)

  // Add Library Markers
  libraries.forEach(lib => {
    const marker = L.marker([lib.lat, lib.lng], { icon: redIcon }).addTo(map!)
    marker.bindPopup(`
      <div class="p-2">
        <h3 class="font-bold text-lg mb-2">${lib.name}</h3>
        <button class="bg-blue-600 text-white px-3 py-1 rounded w-full mb-2" onclick="window.dispatchEvent(new CustomEvent('open-transit', { detail: ${lib.id} }))">
          Transit Planner
        </button>
        <button class="bg-green-600 text-white px-3 py-1 rounded w-full" onclick="window.dispatchEvent(new CustomEvent('open-database', { detail: ${lib.id} }))">
          View Toy Database
        </button>
      </div>
    `)
  })

  // Fetch mock community centers
  await fetchCommunityCenters()
}

const fetchCommunityCenters = async () => {
  // Hardcoded list of 15 Community Centers focusing on immigrant/low-income housing & community building
  communityCenters.value = [
    { id: 1001, name: 'Centro Tyrone Guzman', url: 'https://www.centromn.org/', lat: 44.9602, lng: -93.2536 },
    { id: 1002, name: 'Pillsbury United Communities - Brian Coyle Center', url: 'https://pillsburyunited.org/', lat: 44.9687, lng: -93.2427 },
    { id: 1003, name: 'CAPI USA', url: 'https://capiusa.org/', lat: 45.0592, lng: -93.3087 },
    { id: 1004, name: 'Hmong American Partnership (HAP)', url: 'https://www.hmong.org/', lat: 44.9616, lng: -93.1587 },
    { id: 1005, name: 'CLUES St. Paul', url: 'https://clues.org/', lat: 44.9587, lng: -93.0722 },
    { id: 1006, name: 'Hallie Q. Brown Community Center', url: 'https://www.hallieqbrown.org/', lat: 44.9525, lng: -93.1256 },
    { id: 1007, name: 'Sabathani Community Center', url: 'https://sabathani.org/', lat: 44.9403, lng: -93.2678 },
    { id: 1008, name: 'East Side Neighborhood Services', url: 'https://www.esns.org/', lat: 45.0041, lng: -93.2652 },
    { id: 1009, name: 'Project for Pride in Living (PPL)', url: 'https://www.ppl-inc.org/', lat: 44.9654, lng: -93.2571 },
    { id: 1010, name: 'Phyllis Wheatley Community Center', url: 'https://www.phylliswheatley.org/', lat: 44.9926, lng: -93.2965 },
    { id: 1011, name: 'Neighborhood House', url: 'https://neighb.org/', lat: 44.9312, lng: -93.0858 },
    { id: 1012, name: 'Merrick Community Services', url: 'https://merrickcs.org/', lat: 44.9754, lng: -93.0617 },
    { id: 1013, name: 'Appetite for Change', url: 'https://appetiteforchangemn.org/', lat: 45.0003, lng: -93.2842 },
    { id: 1014, name: 'Minneapolis American Indian Center', url: 'https://www.maicnet.org/', lat: 44.9625, lng: -93.2501 },
    { id: 1015, name: 'Karen Organization of Minnesota', url: 'https://www.mnkaren.org/', lat: 44.9818, lng: -93.1091 }
  ];

  communityCenters.value.forEach(center => {
    const marker = L.marker([center.lat, center.lng], { icon: customIcon }).addTo(map!)
    marker.bindPopup(`
      <div class="p-2">
        <h3 class="font-bold">${center.name}</h3>
        <p class="text-sm text-gray-600 mb-2">Community Center</p>
        <a href="${center.url}" target="_blank" class="text-blue-500 underline text-sm mb-2 block">Visit Website</a>
        <button class="bg-indigo-500 text-white px-3 py-1 rounded w-full text-sm mt-1" onclick="window.dispatchEvent(new CustomEvent('set-base', { detail: ${center.id} }))">
          Set as Transit Base
        </button>
      </div>
    `)
  })
}

const handleOpenTransit = (e: any) => {
  selectedDestinationId.value = e.detail
  showTransit.value = true
}

const handleOpenDatabase = (e: any) => {
  selectedLibrary.value = libraries.find(l => l.id === e.detail) as any
  showDatabase.value = true
}

const handleSetBase = (e: any) => {
  selectedBase.value = communityCenters.value.find(c => c.id === e.detail) as any
  alert(`Base set to ${selectedBase.value?.name}`)
}

onMounted(() => {
  initMap()
  window.addEventListener('open-transit', handleOpenTransit)
  window.addEventListener('open-database', handleOpenDatabase)
  window.addEventListener('set-base', handleSetBase)
})

onUnmounted(() => {
  map?.remove()
  window.removeEventListener('open-transit', handleOpenTransit)
  window.removeEventListener('open-database', handleOpenDatabase)
  window.removeEventListener('set-base', handleSetBase)
})
</script>

<style scoped>
/* Optional styling */
</style>