<template>
  <div class="relative h-full w-full">
    <div ref="mapEl" class="h-full w-full rounded-3xl overflow-hidden border border-white/10"></div>
    <div class="absolute bottom-4 left-4 pointer-events-none">
      <div class="rounded-2xl border border-white/10 bg-slate-950/70 backdrop-blur px-4 py-3 text-slate-200 text-xs">
        <div class="font-semibold">Pick a point</div>
        <div class="text-slate-300 mt-1">Click anywhere on the map to set latitude/longitude.</div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { onMounted, onBeforeUnmount, ref, watch } from "vue";
import L from "leaflet";
import "leaflet/dist/leaflet.css";

import markerIcon2x from "leaflet/dist/images/marker-icon-2x.png";
import markerIcon from "leaflet/dist/images/marker-icon.png";
import markerShadow from "leaflet/dist/images/marker-shadow.png";

const props = defineProps({
  lat: { type: Number, default: null },
  lon: { type: Number, default: null },
});
const emit = defineEmits(["picked"]);

const mapEl = ref(null);
let map = null;
let marker = null;

function fixLeafletMarkerAssets() {
  L.Icon.Default.mergeOptions({
    iconRetinaUrl: markerIcon2x,
    iconUrl: markerIcon,
    shadowUrl: markerShadow,
  });
}

function setMarker(lat, lon) {
  if (!map) return;

  if (marker) {
    marker.setLatLng([lat, lon]);
    return;
  }

  marker = L.marker([lat, lon], {
    riseOnHover: true,
    keyboard: false,
  }).addTo(map);
}

onMounted(() => {
  fixLeafletMarkerAssets();

  map = L.map(mapEl.value).setView([32.08, 34.78], 12);
  L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
    attribution: "© OpenStreetMap",
    maxZoom: 19,
  }).addTo(map);

  map.on("click", (e) => {
    const {lat, lng} = e.latlng;
    setMarker(lat, lng);
    emit("picked", {latitude: lat, longitude: lng});
  });

  if (props.lat != null && props.lon != null) setMarker(props.lat, props.lon);
});

watch(
    () => [props.lat, props.lon],
    ([lat, lon]) => {
      if (lat != null && lon != null) setMarker(lat, lon);
    }
);

onBeforeUnmount(() => {
  try {
    map?.remove?.();
  } catch {
  }
  map = null;
});
</script>
