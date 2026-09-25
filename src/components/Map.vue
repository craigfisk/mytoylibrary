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
    { id: 1001, name: 'Centro Tyrone Guzman', url: 'https://www.centromn.org/', address: '1915 Chicago Ave, Minneapolis, MN 55404', description: 'Multiservice organization serving Latine families in Minneapolis.', lat: 44.9602, lng: -93.2536 },
    { id: 1002, name: 'Pillsbury United Communities - Brian Coyle Center', url: 'https://pillsburyunited.org/', address: '420 15th Ave S, Minneapolis, MN 55454', description: 'Community center providing services for East African immigrants and others in Cedar-Riverside.', lat: 44.9687, lng: -93.2427 },
    { id: 1003, name: 'CAPI USA', url: 'https://capiusa.org/', address: '5930 Brooklyn Blvd, Brooklyn Center, MN 55429', description: 'Guiding refugees and immigrants in their journey toward self-determination.', lat: 45.0592, lng: -93.3087 },
    { id: 1004, name: 'Hmong American Partnership (HAP)', url: 'https://www.hmong.org/', address: '1075 Arcade St, St Paul, MN 55106', description: 'Empowering the community to embrace the strengths of our cultures while achieving our potential.', lat: 44.9616, lng: -93.1587 },
    { id: 1005, name: 'CLUES St. Paul', url: 'https://clues.org/', address: '797 E 7th St, St Paul, MN 55106', description: 'Linguistic and cultural resources to advance the capacity of Latino families.', lat: 44.9587, lng: -93.0722 },
    { id: 1006, name: 'Hallie Q. Brown Community Center', url: 'https://www.hallieqbrown.org/', address: '270 N Kent St, St Paul, MN 55102', description: 'An African American, nonprofit social service agency providing programming for all ages.', lat: 44.9525, lng: -93.1256 },
    { id: 1007, name: 'Sabathani Community Center', url: 'https://sabathani.org/', address: '310 E 38th St, Minneapolis, MN 55409', description: 'One of Minnesota’s oldest African American-founded nonprofits, offering various services.', lat: 44.9403, lng: -93.2678 },
    { id: 1008, name: 'East Side Neighborhood Services', url: 'https://www.esns.org/', address: '1700 2nd St NE, Minneapolis, MN 55413', description: 'Fostering the healthy development and well-being of individuals and families.', lat: 45.0041, lng: -93.2652 },
    { id: 1009, name: 'Project for Pride in Living (PPL)', url: 'https://www.ppl-inc.org/', address: '1035 E Franklin Ave, Minneapolis, MN 55404', description: 'Builds the hope, assets, and self-reliance of individuals and families.', lat: 44.9654, lng: -93.2571 },
    { id: 1010, name: 'Phyllis Wheatley Community Center', url: 'https://www.phylliswheatley.org/', address: '1301 10th Ave N, Minneapolis, MN 55411', description: 'Comprehensive, quality programs for life-long learning and community empowerment.', lat: 44.9926, lng: -93.2965 },
    { id: 1011, name: 'Neighborhood House', url: 'https://neighb.org/', address: '179 Robie St E, St Paul, MN 55107', description: 'Helping people transition from surviving to thriving in diverse communities.', lat: 44.9312, lng: -93.0858 },
    { id: 1012, name: 'Merrick Community Services', url: 'https://merrickcs.org/', address: '1669 Arcade St, St Paul, MN 55106', description: 'Supporting East Side Saint Paul residents to empower themselves and their community.', lat: 44.9754, lng: -93.0617 },
    { id: 1013, name: 'Appetite for Change', url: 'https://appetiteforchangemn.org/', address: '1200 W Broadway Ave, Minneapolis, MN 55411', description: 'Using food as a tool to build health, wealth, and social change in North Minneapolis.', lat: 45.0003, lng: -93.2842 },
    { id: 1014, name: 'Minneapolis American Indian Center', url: 'https://www.maicnet.org/', address: '1530 E Franklin Ave, Minneapolis, MN 55404', description: 'Providing services to the Native American urban community of Minneapolis.', lat: 44.9625, lng: -93.2501 },
    { id: 1015, name: 'Karen Organization of Minnesota', url: 'https://www.mnkaren.org/', address: '2353 Rice St #240, Roseville, MN 55113', description: 'Enhancing the quality of life for Karen and other refugees from Burma in Minnesota.', lat: 44.9818, lng: -93.1091 }
  ];

  communityCenters.value.forEach(center => {
    const marker = L.marker([center.lat, center.lng], { icon: customIcon }).addTo(map!)
    marker.bindPopup(`
      <div class="p-2">
        <h3 class="font-bold">${center.name}</h3>
        <a href="${center.url}" target="_blank" class="text-blue-500 underline text-sm mb-1 block">${center.url}</a>
        <p class="text-sm text-gray-700 mb-1">${center.address}</p>
        <p class="text-sm text-gray-600 mb-2">${center.description}</p>
        <button class="bg-indigo-500 text-white px-3 py-1 rounded w-full text-sm mt-1" onclick="window.dispatchEvent(new CustomEvent('set-base', { detail: ${center.id} }))">
          Set as Transit Base
        </button>
      </div>
    `)
    marker.on('mouseover', function(this: any) {
      this.openPopup()
    })
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