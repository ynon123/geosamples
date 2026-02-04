<template>
  <header class="sticky top-0 z-50 border-b border-white/10 bg-slate-950/70 backdrop-blur">
    <div class="mx-auto max-w-7xl px-6 py-4 flex items-center gap-4">
      <div class="h-10 w-10 rounded-2xl bg-gradient-to-br from-indigo-500 to-fuchsia-500 shadow-lg"></div>
      <div class="flex-1">
        <div class="text-lg font-semibold tracking-tight">Geo Samples</div>
        <div class="text-xs text-slate-300">Polygon filtering + time range (FastAPI + PostGIS)</div>
      </div>

      <nav class="flex items-center gap-3">
        <RouterLink to="/map" class="rounded-2xl border border-white/10 px-5 py-2.5 text-sm font-semibold"
          :class="$route.path === '/map' ? 'bg-white/10' : 'bg-white/5 hover:bg-white/10'">Map</RouterLink>
        <RouterLink to="/ingest" class="rounded-2xl border border-white/10 px-5 py-2.5 text-sm font-semibold"
          :class="$route.path === '/ingest' ? 'bg-white/10' : 'bg-white/5 hover:bg-white/10'">Ingest</RouterLink>
      </nav>
    </div>
  </header>
</template>

<script setup>
import { RouterLink, useRoute } from "vue-router";
const $route = useRoute();
</script>
