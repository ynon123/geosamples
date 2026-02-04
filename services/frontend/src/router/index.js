import { createRouter, createWebHistory } from "vue-router";
import MapPage from "../pages/MapPage.vue";
import IngestPage from "../pages/IngestPage.vue";

export default createRouter({
  history: createWebHistory(),
  routes: [
    { path: "/", redirect: "/map" },
    { path: "/map", component: MapPage },
    { path: "/ingest", component: IngestPage },
  ],
});
