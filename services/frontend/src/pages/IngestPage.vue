<template>
  <div class="h-full min-h-0 overflow-hidden">
    <Toast ref="toastRef" />

    <div class="h-full min-h-0 grid grid-cols-12 gap-6 overflow-hidden">
      <section class="col-span-12 lg:col-span-5 h-full min-h-0 overflow-hidden">
        <div class="h-full min-h-0 rounded-3xl border border-white/10 bg-slate-900/40 backdrop-blur p-6 shadow-xl overflow-auto">
          <div class="text-lg font-semibold">Ingest sample</div>

          <div class="mt-6 grid grid-cols-2 gap-3">
            <div>
              <label class="text-xs text-slate-300">Latitude</label>
              <input
                v-model.number="lat"
                type="number"
                step="0.000001"
                class="mt-1 w-full rounded-2xl bg-slate-950/60 border border-white/10 px-3 py-2 text-sm outline-none focus:ring-2 focus:ring-indigo-500/60"
              />
            </div>

            <div>
              <label class="text-xs text-slate-300">Longitude</label>
              <input
                v-model.number="lon"
                type="number"
                step="0.000001"
                class="mt-1 w-full rounded-2xl bg-slate-950/60 border border-white/10 px-3 py-2 text-sm outline-none focus:ring-2 focus:ring-indigo-500/60"
              />
            </div>

            <div>
              <label class="text-xs text-slate-300">Signal strength</label>
              <input
                v-model.number="signal"
                type="number"
                step="0.1"
                class="mt-1 w-full rounded-2xl bg-slate-950/60 border border-white/10 px-3 py-2 text-sm outline-none focus:ring-2 focus:ring-indigo-500/60"
              />
            </div>

            <div>
              <label class="text-xs text-slate-300">Timestamp</label>
              <input
                v-model="tsLocal"
                type="datetime-local"
                class="mt-1 w-full rounded-2xl bg-slate-950/60 border border-white/10 px-3 py-2 text-sm outline-none focus:ring-2 focus:ring-indigo-500/60"
              />
            </div>
          </div>

          <div class="mt-5 flex gap-3">
            <button
              class="flex-1 rounded-2xl bg-emerald-500/90 hover:bg-emerald-500 px-4 py-2 text-sm font-semibold shadow-lg shadow-emerald-500/20"
              @click="submit"
            >
              Submit
            </button>
            <button
              class="flex-1 rounded-2xl border border-white/10 bg-white/5 hover:bg-white/10 px-4 py-2 text-sm"
              @click="reset"
            >
              Reset
            </button>
          </div>
        </div>
      </section>

      <section class="col-span-12 lg:col-span-7 h-full min-h-0 overflow-hidden">
        <MapPicker class="h-full w-full" :lat="lat" :lon="lon" @picked="onPicked" />
      </section>
    </div>
  </div>
</template>

<script setup>
import {onMounted, ref} from "vue";
import Toast from "../components/Toast.vue";
import MapPicker from "../components/MapPicker.vue";
import {ingestSamples} from "../lib/api";

const toastRef = ref(null);

function toastOk(title, message) {
  toastRef.value?.push?.({title, message, kind: "ok"});
}

function toastErr(title, message) {
  toastRef.value?.push?.({title, message, kind: "error", ttl: 6000});
}

const lat = ref(32.0853);
const lon = ref(34.7818);
const signal = ref(-70.0);
const tsLocal = ref("");

function pad(n) {
  return String(n).padStart(2, "0");
}

function toLocalInput(d) {
  return `${d.getFullYear()}-${pad(d.getMonth() + 1)}-${pad(d.getDate())}T${pad(d.getHours())}:${pad(d.getMinutes())}`;
}

function nowLocalInput() {
  return toLocalInput(new Date());
}

function toIsoFromLocal(localInput) {
  if (!localInput) return new Date().toISOString();
  const d = new Date(localInput);
  if (Number.isNaN(d.getTime())) return new Date().toISOString();
  return d.toISOString();
}

function onPicked({latitude, longitude}) {
  lat.value = latitude;
  lon.value = longitude;
}

async function submit() {
  try {
    const payload = {
      latitude: lat.value,
      longitude: lon.value,
      signal_strength: signal.value,
      timestamp: toIsoFromLocal(tsLocal.value),
    };
    const res = await ingestSamples(payload);
    toastOk("Ingested", `Inserted ${res.inserted} sample`);
  } catch (e) {
    const msg = String(e?.message || e);
    toastErr("Ingest error", msg.length > 180 ? msg.slice(0, 180) + "…" : msg);
  }
}

function reset() {
  signal.value = -70.0;
  tsLocal.value = nowLocalInput();
}

onMounted(() => {
  tsLocal.value = nowLocalInput();
});
</script>
