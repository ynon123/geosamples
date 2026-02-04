<template>
  <div class="rounded-3xl border border-white/10 bg-slate-900/40 backdrop-blur p-5 shadow-xl">
    <div class="flex items-center justify-between">
      <div class="text-sm font-semibold">Filters</div>
      <div class="text-xs text-slate-300">{{ status }}</div>
    </div>

    <div class="mt-4 grid grid-cols-2 gap-3">
      <div>
        <label class="text-xs text-slate-300">From</label>
        <input
          type="datetime-local"
          v-model="localFrom"
          :max="localTo || undefined"
          class="mt-1 w-full rounded-2xl bg-slate-950/60 border border-white/10 px-3 py-2 text-sm outline-none focus:ring-2 focus:ring-indigo-500/60"
        />
      </div>

      <div>
        <label class="text-xs text-slate-300">To</label>
        <input
          type="datetime-local"
          v-model="localTo"
          :min="localFrom || undefined"
          class="mt-1 w-full rounded-2xl bg-slate-950/60 border border-white/10 px-3 py-2 text-sm outline-none focus:ring-2 focus:ring-indigo-500/60"
        />
      </div>
    </div>

    <div class="mt-4 grid grid-cols-2 gap-3">
      <button
        class="rounded-2xl bg-indigo-500/90 hover:bg-indigo-500 px-4 py-2 text-sm font-semibold shadow-lg shadow-indigo-500/20"
        @click="apply"
      >
        Apply
      </button>

      <button
        class="rounded-2xl border border-white/10 bg-white/5 hover:bg-white/10 px-4 py-2 text-sm"
        @click="clearDates"
      >
        Clear dates
      </button>

      <button
        class="rounded-2xl border border-white/10 bg-white/5 hover:bg-white/10 px-4 py-2 text-sm"
        @click="last24h"
      >
        Last 24h
      </button>

      <button
        class="rounded-2xl border border-white/10 bg-white/5 hover:bg-white/10 px-4 py-2 text-sm"
        @click="emit('clearPolygon')"
      >
        Clear polygon
      </button>
    </div>
  </div>
</template>

<script setup>
import { ref, watch } from "vue";

const props = defineProps({
  fromTime: { type: String, default: "" },
  toTime: { type: String, default: "" },
  status: { type: String, default: "" },
});

const emit = defineEmits([
  "update:fromTime",
  "update:toTime",
  "apply",
  "clearDates",
  "last24h",
  "clearPolygon",
]);

const localFrom = ref(props.fromTime || "");
const localTo = ref(props.toTime || "");

watch(() => props.fromTime, v => (localFrom.value = v || ""));
watch(() => props.toTime, v => (localTo.value = v || ""));

function apply() {
  emit("update:fromTime", localFrom.value);
  emit("update:toTime", localTo.value);
  emit("apply");
}

function clearDates() {
  localFrom.value = "";
  localTo.value = "";
  emit("update:fromTime", "");
  emit("update:toTime", "");
  emit("clearDates");
}

function last24h() {
  emit("last24h");
}
</script>
