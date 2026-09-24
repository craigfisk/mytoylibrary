<template>
  <div class="h-screen w-full flex flex-col font-sans">
    <header class="bg-indigo-700 text-white p-4 shadow-md z-[2000] relative flex justify-between items-center">
      <div>
        <h1 class="text-2xl font-bold">MNToys Planner</h1>
        <p class="text-sm opacity-90">Find Toy Libraries & Plan Your Visit</p>
      </div>
    </header>
    <main class="flex-1 relative overflow-hidden">
      <Map />
    </main>
  </div>
</template>

<script setup lang="ts">
import Map from './components/Map.vue'
</script>

<style>
/* Global styles handled by tailwind in style.css */
</style>