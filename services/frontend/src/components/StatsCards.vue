<template>
  <div class="grid grid-cols-2 gap-4">
    <div class="rounded-3xl border border-white/10 bg-slate-900/40 p-5 shadow-xl">
      <div class="text-xs text-slate-300">Shown</div>
      <div class="mt-2 text-2xl font-semibold">{{ shown }}</div>
    </div>
    <div class="rounded-3xl border border-white/10 bg-slate-900/40 p-5 shadow-xl">
      <div class="text-xs text-slate-300">Mode</div>
      <div class="mt-2 text-sm font-semibold">{{ modeLabel }}</div>
      <div class="mt-1 text-xs text-slate-400">{{ modeHint }}</div>
    </div>
  </div>
</template>

<script setup>
defineProps({ shown: Number, modeLabel: String, modeHint: String });
</script>
