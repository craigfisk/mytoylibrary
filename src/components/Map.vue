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
    { id: 1001, name: 'Centro Tyrone Guzman', url: 'https://www.centromn.org/', address: '1915 Chicago Ave, Minneapolis, MN 55404', focus: 'Centro Tyrone Guzman is the oldest and largest multi-service Latine organization in Minneapolis, focusing on community building, education, and health for low-income Latine families.', lat: 44.9602, lng: -93.2536 },
    { id: 1002, name: 'Pillsbury United Communities - Brian Coyle Center', url: 'https://pillsburyunited.org/', address: '420 15th Ave S, Minneapolis, MN 55454', focus: 'Located in the Cedar-Riverside neighborhood, the Brian Coyle Center serves a large East African immigrant population, providing youth programs, food shelf services, and community-building initiatives.', lat: 44.9687, lng: -93.2427 },
    { id: 1003, name: 'CAPI USA', url: 'https://capiusa.org/', address: '5930 Brooklyn Blvd, Brooklyn Center, MN 55429', focus: 'CAPI USA empowers immigrants and refugees, particularly Asian immigrants, by guiding them toward economic independence through workforce development, basic needs support, and housing assistance.', lat: 45.0592, lng: -93.3087 },
    { id: 1004, name: 'Hmong American Partnership (HAP)', url: 'https://www.hmong.org/', address: '1075 Arcade St, St. Paul, MN 55106', focus: 'HAP is a prominent social service and community development organization focusing on the economic and social integration of Hmong and other immigrant and refugee communities.', lat: 44.9616, lng: -93.1587 },
    { id: 1005, name: 'CLUES St. Paul', url: 'https://clues.org/', address: '797 E 7th St, St. Paul, MN 55106', focus: 'Comunidades Latinas Unidas En Servicio (CLUES) is Minnesota\'s largest Latino-led organization, focusing on connecting families to resources, skills, and institutions to advance equity and well-being.', lat: 44.9587, lng: -93.0722 },
    { id: 1006, name: 'Hallie Q. Brown Community Center', url: 'https://www.hallieqbrown.org/', address: '270 N Kent St, St. Paul, MN 55102', focus: 'Historically serving the African American community in the Rondo neighborhood, this center provides human services, food security, and early childhood education to improve the quality of life for low-income residents.', lat: 44.9525, lng: -93.1256 },
    { id: 1007, name: 'Sabathani Community Center', url: 'https://sabathani.org/', address: '310 E 38th St, Minneapolis, MN 55409', focus: 'Founded by community members in South Minneapolis, Sabathani focuses on providing basic needs, housing, and family resources primarily to African American and low-income populations.', lat: 44.9403, lng: -93.2678 },
    { id: 1008, name: 'East Side Neighborhood Services', url: 'https://www.esns.org/', address: '1700 2nd St NE, Minneapolis, MN 55413', focus: 'Serving Northeast and Southeast Minneapolis, this organization builds pathways toward equity by supporting individuals and families across all stages of life with employment, housing, and food assistance.', lat: 45.0041, lng: -93.2652 },
    { id: 1009, name: 'Project for Pride in Living (PPL)', url: 'https://www.ppl-inc.org/', address: '1035 E Franklin Ave, Minneapolis, MN 55404', focus: 'PPL focuses on empowering lower-income individuals and families to build self-reliance through deeply affordable housing and targeted employment training programs.', lat: 44.9654, lng: -93.2571 },
    { id: 1010, name: 'Phyllis Wheatley Community Center', url: 'https://www.phylliswheatley.org/', address: '1301 10th Ave N, Minneapolis, MN 55411', focus: 'Located in North Minneapolis, this historic center provides comprehensive services, early childhood development, and supportive programming for African American families and other marginalized groups.', lat: 44.9926, lng: -93.2965 },
    { id: 1011, name: 'Neighborhood House', url: 'https://neighb.org/', address: '179 Robie St E, St. Paul, MN 55107', focus: 'A long-standing multi-cultural center in St. Paul that supports immigrants, refugees, and low-income families in transitioning from surviving to thriving through food, housing, and education support.', lat: 44.9312, lng: -93.0858 },
    { id: 1012, name: 'Merrick Community Services', url: 'https://merrickcs.org/', address: '1669 Arcade St, St. Paul, MN 55106', focus: 'Operating on the East Side of St. Paul, Merrick empowers individuals and families to overcome poverty and become self-sufficient through food access, employment, and youth services.', lat: 44.9754, lng: -93.0617 },
    { id: 1013, name: 'Appetite for Change', url: 'https://appetiteforchangemn.org/', address: '1200 W Broadway Ave, Minneapolis, MN 55411', focus: 'Located in North Minneapolis, this organization uses food as a tool for health, wealth, and social change, engaging the community in urban agriculture and culinary training to build food sovereignty.', lat: 45.0003, lng: -93.2842 },
    { id: 1014, name: 'Minneapolis American Indian Center', url: 'https://www.maicnet.org/', address: '1530 E Franklin Ave, Minneapolis, MN 55404', focus: 'This center is a community hub that preserves and supports Native American cultural values while providing educational, social, and economic services to a large urban Native population.', lat: 44.9625, lng: -93.2501 },
    { id: 1015, name: 'Karen Organization of Minnesota', url: 'https://www.mnkaren.org/', address: '2353 Rice St #240, Roseville, MN 55113', focus: 'The first Karen-led social service agency in the U.S., it focuses on assisting Karen and other refugees from Burma in settling into their new communities through employment, health, and youth services.', lat: 44.9818, lng: -93.1091 }
  ];

  communityCenters.value.forEach(center => {
    const marker = L.marker([center.lat, center.lng], { icon: customIcon }).addTo(map!)
    marker.bindPopup(`
      <div class="p-2 w-64">
        <h3 class="font-bold text-base mb-1">${center.name}</h3>
        <a href="${center.url}" target="_blank" class="text-blue-500 underline text-sm mb-1 block">${center.url}</a>
        <p class="text-xs text-gray-700 mb-2">${center.address}</p>
        <p class="text-xs text-gray-800 mb-3 border-t pt-2"><strong>Focus:</strong> ${center.focus}</p>
        <button class="bg-indigo-500 hover:bg-indigo-600 text-white px-3 py-1.5 rounded w-full text-sm mt-1 transition-colors" onclick="window.dispatchEvent(new CustomEvent('set-base', { detail: ${center.id} }))">
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