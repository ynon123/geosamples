<template>
  <div class="h-full min-h-0 overflow-hidden">
    <Toast ref="toastRef" />

    <div class="h-full min-h-0 grid grid-cols-12 gap-6 overflow-hidden">
      <div class="col-span-12 lg:col-span-4 min-h-0 flex flex-col gap-6 overflow-hidden">
        <FilterCard
          :fromTime="fromTime"
          :toTime="toTime"
          :status="statusText"
          @update:fromTime="(v) => (fromTime = v)"
          @update:toTime="(v) => (toTime = v)"
          @apply="applyFilters"
          @clearDates="clearDates"
          @last24h="setLast24h"
          @clearPolygon="clearPolygon"
        />

        <div class="flex-1 min-h-0 overflow-hidden">
          <SamplesTable :rows="samples.slice(0, 10)" @focus="focusSample" />
        </div>
      </div>

      <div class="col-span-12 lg:col-span-8 min-h-0 overflow-hidden">
        <MapView
          class="h-full w-full"
          :samples="samples"
          :polygon="polygonGeoJson"
          :selectedId="selectedSampleId"
          @polygonChanged="onPolygonChanged"
        />
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed, onMounted, ref, watch } from "vue";

import Toast from "../components/Toast.vue";
import FilterCard from "../components/FilterCard.vue";
import MapView from "../components/MapView.vue";
import SamplesTable from "../components/SamplesTable.vue";
import { getSamples, filterSamples } from "../lib/api";

const toastRef = ref(null);
function toastOk(title, message) { toastRef.value?.push?.({ title, message, kind: "ok" }); }
function toastErr(title, message) { toastRef.value?.push?.({ title, message, kind: "error", ttl: 6000 }); }

const LS_KEY = "geosamples.map.filters.v2";
const fromTime = ref("");
const toTime = ref("");
const polygonGeoJson = ref(null);

const samples = ref([]);
const selectedSampleId = ref(null);

const statusText = computed(() => `Loaded ${samples.value.length}`);

function pad(n) { return String(n).padStart(2, "0"); }
function toLocalInput(d) {
  return `${d.getFullYear()}-${pad(d.getMonth()+1)}-${pad(d.getDate())}T${pad(d.getHours())}:${pad(d.getMinutes())}`;
}
function last24hDefaults() {
  const to = new Date();
  const from = new Date(Date.now() - 24*60*60*1000);
  return { from: toLocalInput(from), to: toLocalInput(to) };
}
function toIsoOrNull(localInput) {
  if (!localInput) return null;
  const d = new Date(localInput);
  if (Number.isNaN(d.getTime())) return null;
  return d.toISOString();
}

function persist() {
  try {
    localStorage.setItem(LS_KEY, JSON.stringify({
      fromTime: fromTime.value || "",
      toTime: toTime.value || "",
      polygon: polygonGeoJson.value || null
    }));
  } catch {}
}
function restore() {
  try {
    const raw = localStorage.getItem(LS_KEY);
    if (!raw) return false;
    const obj = JSON.parse(raw);
    fromTime.value = obj.fromTime || "";
    toTime.value = obj.toTime || "";
    polygonGeoJson.value = obj.polygon || null;
    return true;
  } catch { return false; }
}
watch([fromTime, toTime, polygonGeoJson], persist, { deep: true });

async function fetchSamples() {
  try {
    if (polygonGeoJson.value) {
      const res = await filterSamples({
        polygon: polygonGeoJson.value,
        from_time: toIsoOrNull(fromTime.value),
        to_time: toIsoOrNull(toTime.value),
        limit: 1000,
        offset: 0,
      });
      samples.value = Array.isArray(res) ? res : (res.items || []);
      return;
    }

    const res = await getSamples({
      limit: 1000,
      offset: 0,
      from_time: toIsoOrNull(fromTime.value),
      to_time: toIsoOrNull(toTime.value),
    });
    samples.value = Array.isArray(res) ? res : (res.items || []);
  } catch (e) {
    toastErr("API error", e?.message || String(e));
  }
}

function isInvalidRange() {
  if (!fromTime.value || !toTime.value) return false;
  const a = new Date(fromTime.value);
  const b = new Date(toTime.value);
  if (Number.isNaN(a.getTime()) || Number.isNaN(b.getTime())) return false;
  return b.getTime() < a.getTime();
}

async function applyFilters() {
  if (isInvalidRange()) {
    toastErr("Invalid time range", "End time must be after start time");
    return;
  }
  await fetchSamples();
  toastOk("Applied", "Filters applied");
}

async function clearPolygon() {
  polygonGeoJson.value = null;
  selectedSampleId.value = null;
  await fetchSamples();
}
async function clearDates() {
  fromTime.value = "";
  toTime.value = "";
  await fetchSamples();
}
async function setLast24h() {
  const def = last24hDefaults();
  fromTime.value = def.from;
  toTime.value = def.to;
  await fetchSamples();
}

function onPolygonChanged(geo) {
  polygonGeoJson.value = geo;
  fetchSamples();
}
function focusSample(r) {
  selectedSampleId.value = r?.id ?? null;
}

onMounted(async () => {
  const ok = restore();
  if (!ok) {
    const def = last24hDefaults();
    fromTime.value = def.from;
    toTime.value = def.to;
  }
  await fetchSamples();
});
</script>
