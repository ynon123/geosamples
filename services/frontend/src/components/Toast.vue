<template>
  <div class="fixed top-5 right-5 z-[9999] space-y-2">
    <div v-for="t in toasts" :key="t.id"
      class="rounded-2xl shadow-xl border border-white/10 bg-slate-900/90 backdrop-blur px-4 py-3 text-slate-100 w-[360px]">
      <div class="flex items-start gap-3">
        <div class="mt-0.5 h-2.5 w-2.5 rounded-full" :class="t.kind === 'error' ? 'bg-red-400' : 'bg-emerald-400'"></div>
        <div class="flex-1">
          <div class="text-sm font-semibold">{{ t.title }}</div>
          <div class="text-xs text-slate-300 mt-0.5 whitespace-pre-wrap">{{ t.message }}</div>
        </div>
        <button class="text-slate-400 hover:text-slate-200" @click="remove(t.id)">✕</button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { reactive } from "vue";
const toasts = reactive([]);
function push({ title, message, kind = "ok", ttl = 3500 }) {
  const id = Math.random().toString(16).slice(2);
  toasts.push({ id, title, message, kind });
  setTimeout(() => remove(id), ttl);
}
function remove(id) {
  const idx = toasts.findIndex(t => t.id === id);
  if (idx >= 0) toasts.splice(idx, 1);
}
defineExpose({ push });
</script>
