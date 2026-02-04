<template>
  <div class="rounded-3xl border border-white/10 bg-slate-900/40 backdrop-blur p-6 shadow-xl h-full min-h-0 flex flex-col overflow-hidden">
    <div class="flex items-center justify-between shrink-0">
      <div class="text-base font-semibold">Latest samples</div>
      <div class="text-xs text-slate-400">{{ rows.length }} shown</div>
    </div>

    <div class="mt-4 flex-1 min-h-0 overflow-hidden rounded-2xl border border-white/10">
      <div class="h-full overflow-y-auto">
        <table class="w-full text-sm">
          <thead class="bg-slate-950/50 text-slate-300 sticky top-0 z-10">
            <tr>
              <th class="px-4 py-3 text-left font-semibold">Time</th>
              <th class="px-4 py-3 text-left font-semibold">Signal</th>
              <th class="px-4 py-3 text-left font-semibold">Lat/Lon</th>
            </tr>
          </thead>

          <tbody class="divide-y divide-white/5">
            <tr v-for="r in rows" :key="r.id" class="hover:bg-white/5">
              <td class="px-4 py-3 font-mono text-xs text-slate-200">{{ fmtTs(r.timestamp) }}</td>
              <td class="px-4 py-3 font-semibold text-slate-100">{{ r.signal_strength }}</td>
              <td class="px-4 py-3">
                <button
                  class="rounded-xl border border-white/10 bg-white/5 hover:bg-white/10 px-3 py-1.5 text-xs font-mono"
                  @click="emit('focus', r)"
                  title="Focus on map"
                >
                  {{ fmt(r.latitude) }}, {{ fmt(r.longitude) }}
                </button>
              </td>
            </tr>

            <tr v-if="rows.length === 0">
              <td colspan="3" class="px-4 py-6 text-center text-slate-400 text-sm">
                No samples for the current filters.
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</template>

<script setup>
defineProps({ rows: { type: Array, default: () => [] } });
const emit = defineEmits(["focus"]);
function fmtTs(iso) {
  if (!iso) return "";
  const d = new Date(iso);
  if (Number.isNaN(d.getTime())) return String(iso);
  return d.toLocaleString("he-IL", {
    year: "numeric",
    month: "2-digit",
    day: "2-digit",
    hour: "2-digit",
    minute: "2-digit",
    second: "2-digit",
    hour12: false,
  });
}

function fmt(x) {
  if (x === null || x === undefined) return "";
  const n = Number(x);
  if (Number.isNaN(n)) return String(x);
  return n.toFixed(5);
}
</script>
