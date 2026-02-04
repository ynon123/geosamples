<template>
  <div class="map-wrap">
    <div ref="mapEl" class="map"></div>

    <div class="draw-ui">
      <div class="toolbar">
        <button
          class="btn"
          :class="{ active: mode === 'draw' }"
          type="button"
          @click="toggleDraw"
        >
          Polygon
        </button>

        <button
          class="btn"
          :class="{ active: mode === 'edit' }"
          type="button"
          :disabled="!hasPolygon"
          @click="toggleEdit"
        >
          Edit
        </button>

        <button
          class="btn"
          :class="{ active: mode === 'delete' }"
          type="button"
          :disabled="!hasPolygon"
          @click="toggleDelete"
        >
          Delete
        </button>
      </div>

      <div v-if="mode !== 'idle'" class="actions">
        <template v-if="mode === 'draw'">
          <span class="hint">סגור פוליגון בלחיצה על הנקודה הראשונה</span>
          <button class="btn secondary" type="button" @click="cancelMode">Cancel</button>
        </template>

        <template v-else-if="mode === 'edit'">
          <button class="btn" type="button" @click="saveEdit">Save</button>
          <button class="btn secondary" type="button" @click="cancelEdit">Cancel</button>
        </template>

        <template v-else-if="mode === 'delete'">
          <button class="btn danger" type="button" @click="confirmDelete">Delete</button>
          <button class="btn secondary" type="button" @click="cancelDelete">Cancel</button>
        </template>
      </div>
    </div>
  </div>
</template>

<script setup>
import { onMounted, onBeforeUnmount, ref, watch, nextTick } from "vue";

import L from "leaflet";
import "leaflet/dist/leaflet.css";

import "leaflet-draw";
import "leaflet-draw/dist/leaflet.draw.css";

import markerIcon2x from "leaflet/dist/images/marker-icon-2x.png";
import markerIcon from "leaflet/dist/images/marker-icon.png";
import markerShadow from "leaflet/dist/images/marker-shadow.png";

const props = defineProps({
  samples: { type: Array, default: () => [] },
  polygon: { type: Object, default: null },
  selectedId: { type: [String, Number], default: null },
});
const emit = defineEmits(["polygonChanged"]);

const mapEl = ref(null);

let map = null;
let markersLayer = null;
let drawnItems = null;

let drawPolygonHandler = null;
let editHandler = null;
let deleteHandler = null;

const markerById = new Map();

const mode = ref("idle");
const hasPolygon = ref(false);

function fixLeafletMarkerAssets() {
  L.Icon.Default.mergeOptions({
    iconRetinaUrl: markerIcon2x,
    iconUrl: markerIcon,
    shadowUrl: markerShadow,
  });
}

function updateHasPolygon() {
  const n = drawnItems?.getLayers?.()?.length ?? 0;
  hasPolygon.value = n > 0;
}

function stopAllModes() {
  try { drawPolygonHandler?.disable?.(); } catch {}
  try { editHandler?.disable?.(); } catch {}
  try { deleteHandler?.disable?.(); } catch {}
  mode.value = "idle";
}

function initMap() {
  map = L.map(mapEl.value, { tap: false }).setView([32.08, 34.78], 12);

  L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
    attribution: "© OpenStreetMap",
    maxZoom: 19,
  }).addTo(map);

  markersLayer = L.layerGroup().addTo(map);

  drawnItems = new L.FeatureGroup();
  map.addLayer(drawnItems);
}

function initHandlers() {
  drawPolygonHandler = new L.Draw.Polygon(map, {
    allowIntersection: false,
    showArea: false,
    repeatMode: false,
  });

  editHandler = new L.EditToolbar.Edit(map, {
    featureGroup: drawnItems,
    selectedPathOptions: {
      dashArray: "6,4",
      fillOpacity: 0.25,
      maintainColor: true,
    },
  });

  deleteHandler = new L.EditToolbar.Delete(map, {
    featureGroup: drawnItems,
  });

  map.on(L.Draw.Event.CREATED, (e) => {
    drawnItems.clearLayers();
    drawnItems.addLayer(e.layer);

    updateHasPolygon();
    emitPolygonFromDrawnItems();

    stopAllModes();
  });

  map.on(L.Draw.Event.EDITED, () => {
    emitPolygonFromDrawnItems();
    stopAllModes();
  });

  map.on(L.Draw.Event.DELETED, () => {
    updateHasPolygon();
    emit("polygonChanged", null);
    stopAllModes();
  });
}

function toggleDraw() {
  if (mode.value === "draw") return stopAllModes();
  stopAllModes();

  mode.value = "draw";
  try { drawPolygonHandler.enable(); } catch {}
}

function toggleEdit() {
  if (!hasPolygon.value) return;
  if (mode.value === "edit") return stopAllModes();
  stopAllModes();

  mode.value = "edit";
  try { editHandler.enable(); } catch {}
}

function toggleDelete() {
  if (!hasPolygon.value) return;
  if (mode.value === "delete") return stopAllModes();
  stopAllModes();

  mode.value = "delete";
  try { deleteHandler.enable(); } catch {}
}

function cancelMode() {
  stopAllModes();
}

function saveEdit() {
  try { editHandler.save(); } catch {}
  emitPolygonFromDrawnItems();
  stopAllModes();
}

function cancelEdit() {
  try { editHandler.revertLayers(); } catch {}
  stopAllModes();
}

function confirmDelete() {
  try { deleteHandler.save(); } catch {}
  stopAllModes();
}

function cancelDelete() {
  try { deleteHandler.revertLayers(); } catch {}
  stopAllModes();
}

function emitPolygonFromDrawnItems() {
  const layers = drawnItems?.getLayers?.() ?? [];
  if (!layers.length) {
    emit("polygonChanged", null);
    return;
  }
  const gj = layers[0].toGeoJSON();
  emit("polygonChanged", gj.geometry ?? null);
}

function syncPolygonFromProps() {
  if (!map || !drawnItems) return;

  if (mode.value !== "idle") stopAllModes();

  drawnItems.clearLayers();
  if (!props.polygon) {
    updateHasPolygon();
    return;
  }

  const feature = { type: "Feature", geometry: props.polygon, properties: {} };
  L.geoJSON(feature, { interactive: true }).eachLayer((layer) => drawnItems.addLayer(layer));

  updateHasPolygon();
}

function renderMarkers() {
  if (!map || !markersLayer) return;

  markersLayer.clearLayers();
  markerById.clear();

  for (const s of props.samples || []) {
    const lat = Number(s.latitude);
    const lon = Number(s.longitude);
    if (!Number.isFinite(lat) || !Number.isFinite(lon)) continue;

    const isSel = props.selectedId != null && String(s.id) === String(props.selectedId);

    const m = L.marker([lat, lon], {
      opacity: isSel ? 1 : 0.95,
      riseOnHover: true,
      keyboard: false,
    }).addTo(markersLayer);

    markerById.set(String(s.id), m);
  }
}

function applySelected() {
  if (!map || props.selectedId == null) return;
  const m = markerById.get(String(props.selectedId));
  if (!m) return;
  try { map.panTo(m.getLatLng(), { animate: true }); } catch {}
}

onMounted(async () => {
  await nextTick();
  if (!mapEl.value) return;

  fixLeafletMarkerAssets();
  initMap();
  initHandlers();

  syncPolygonFromProps();
  renderMarkers();
  applySelected();

  setTimeout(() => {
    try { map.invalidateSize(); } catch {}
  }, 50);
});

watch(() => props.polygon, syncPolygonFromProps, { deep: true });

watch(
  () => props.samples,
  () => {
    renderMarkers();
    applySelected();
  },
  { deep: true }
);

watch(() => props.selectedId, applySelected);

onBeforeUnmount(() => {
  try {
    stopAllModes();
    map?.off?.();
    map?.remove?.();
  } catch {}
  map = null;
});
</script>

<style scoped>
.map-wrap {
  height: 100%;
  width: 100%;
  border-radius: 24px;
  overflow: hidden;
  border: 1px solid rgba(255, 255, 255, 0.1);
  position: relative;
}
.map {
  height: 100%;
  width: 100%;
}

.draw-ui {
  position: absolute;
  top: 12px;
  right: 12px;
  z-index: 6000;
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.toolbar,
.actions {
  display: flex;
  gap: 8px;
  align-items: center;
  background: rgba(20, 20, 25, 0.75);
  border: 1px solid rgba(255, 255, 255, 0.12);
  border-radius: 14px;
  padding: 8px;
  backdrop-filter: blur(6px);
}

.btn {
  border: 1px solid rgba(255, 255, 255, 0.18);
  background: rgba(255, 255, 255, 0.08);
  color: white;
  padding: 6px 10px;
  border-radius: 10px;
  font-size: 13px;
  cursor: pointer;
  user-select: none;
}
.btn:hover {
  background: rgba(255, 255, 255, 0.12);
}
.btn:disabled {
  opacity: 0.45;
  cursor: not-allowed;
}
.btn.active {
  background: rgba(96, 165, 250, 0.25);
  border-color: rgba(96, 165, 250, 0.5);
}
.btn.secondary {
  background: rgba(255, 255, 255, 0.06);
}
.btn.danger {
  background: rgba(239, 68, 68, 0.18);
  border-color: rgba(239, 68, 68, 0.5);
}
.hint {
  font-size: 12px;
  color: rgba(255, 255, 255, 0.75);
  padding: 0 6px;
}
</style>
