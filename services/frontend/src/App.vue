<template>
  <div class="h-screen bg-slate-950 text-slate-100 flex flex-col overflow-hidden">
    <TopBar class="shrink-0" />

    <main class="flex-1 min-h-0 overflow-hidden mx-auto w-full max-w-7xl px-6 py-6 flex">
      <RouterView class="flex-1 min-h-0 overflow-hidden" />
    </main>
  </div>
</template>

<script setup>
import { RouterView } from "vue-router";
import TopBar from "./components/TopBar.vue";
</script>
