<template>
  <div class="location-picker-wrap">
    <!-- Search Bar -->
    <div class="lp-search-row">
      <div class="lp-search-box">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="11" cy="11" r="8"/><line x1="21" y1="21" x2="16.65" y2="16.65"/></svg>
        <input
          v-model="searchQuery"
          type="text"
          placeholder="Search a location in the Philippines..."
          @keydown.enter.prevent="searchLocation"
          @input="onSearchInput"
        />
        <button v-if="searchQuery" class="lp-clear-btn" type="button" @click="clearSearch">✕</button>
      </div>
      <button class="lp-search-btn" type="button" @click="searchLocation" :disabled="searching">
        {{ searching ? '...' : 'Search' }}
      </button>
    </div>

    <!-- Search Results Dropdown -->
    <div v-if="searchResults.length" class="lp-results">
      <div
        v-for="r in searchResults"
        :key="r.place_id"
        class="lp-result-item"
        @click="selectResult(r)"
      >
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0z"/><circle cx="12" cy="10" r="3"/></svg>
        <span>{{ r.display_name }}</span>
      </div>
    </div>

    <!-- Map Container -->
    <div class="lp-map-container">
      <div ref="mapRef" class="lp-map"></div>
      <div v-if="geocoding" class="lp-geocoding-overlay">
        <span class="lp-spinner"></span> Getting location details...
      </div>
      <button class="lp-locate-btn" type="button" @click="centerOnPhilippines" title="Reset view to Philippines">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"/><line x1="12" y1="8" x2="12" y2="12"/><line x1="12" y1="16" x2="12.01" y2="16"/></svg>
      </button>
    </div>

    <!-- Resolved Address Fields -->
    <div class="lp-address-fields" v-if="localBarangay || localMunicipality || localProvince">
      <div class="lp-address-header">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0z"/><circle cx="12" cy="10" r="3"/></svg>
        Detected Location
      </div>
      <div class="lp-address-grid">
        <div class="lp-address-item">
          <label>Barangay</label>
          <input v-model="localBarangay" type="text" placeholder="Barangay" @input="emitChange" />
        </div>
        <div class="lp-address-item">
          <label>City / Municipality</label>
          <input v-model="localMunicipality" type="text" placeholder="City / Municipality" @input="emitChange" />
        </div>
        <div class="lp-address-item">
          <label>Province</label>
          <input v-model="localProvince" type="text" placeholder="Province / Region" @input="emitChange" />
        </div>
      </div>
      <p class="lp-hint">📍 You can manually correct any field above after dropping the pin.</p>
    </div>
    <div class="lp-empty-hint" v-else>
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0z"/><circle cx="12" cy="10" r="3"/></svg>
      Click anywhere on the map to set your location
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted, watch } from 'vue';

const props = defineProps({
  barangay:    { type: String, default: '' },
  municipality:{ type: String, default: '' },
  province:    { type: String, default: '' },
  lat:         { type: Number, default: null },
  lng:         { type: Number, default: null },
});

const emit = defineEmits(['update:barangay', 'update:municipality', 'update:province', 'update:lat', 'update:lng', 'change']);

const mapRef    = ref(null);
const geocoding = ref(false);
const searching = ref(false);
const searchQuery   = ref('');
const searchResults = ref([]);

const localBarangay    = ref(props.barangay    || '');
const localMunicipality= ref(props.municipality || '');
const localProvince    = ref(props.province    || '');

let map    = null;
let marker = null;
let L      = null;

// Philippines bounds
const PH_CENTER = [12.8797, 121.7740];
const PH_ZOOM   = 6;

async function loadLeaflet() {
  if (window.L) return window.L;

  // Inject CSS
  if (!document.getElementById('leaflet-css')) {
    const link = document.createElement('link');
    link.id   = 'leaflet-css';
    link.rel  = 'stylesheet';
    link.href = 'https://unpkg.com/leaflet@1.9.4/dist/leaflet.css';
    document.head.appendChild(link);
  }

  // Inject JS
  await new Promise((resolve, reject) => {
    if (window.L) return resolve();
    const script = document.createElement('script');
    script.src = 'https://unpkg.com/leaflet@1.9.4/dist/leaflet.js';
    script.onload  = resolve;
    script.onerror = reject;
    document.head.appendChild(script);
  });

  return window.L;
}

function buildIcon(leaflet) {
  return leaflet.divIcon({
    className: '',
    html: `<div class="lp-custom-marker">
      <svg viewBox="0 0 24 24" fill="#e11d48" width="32" height="32">
        <path d="M12 2C8.13 2 5 5.13 5 9c0 5.25 7 13 7 13s7-7.75 7-13c0-3.87-3.13-7-7-7z"/>
        <circle cx="12" cy="9" r="2.5" fill="white"/>
      </svg>
    </div>`,
    iconSize:   [32, 40],
    iconAnchor: [16, 40],
  });
}

async function initMap() {
  L = await loadLeaflet();
  if (!mapRef.value) return;

  map = L.map(mapRef.value, {
    center: PH_CENTER,
    zoom: PH_ZOOM,
    zoomControl: true,
  });

  L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '© <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a>',
    maxZoom: 19,
  }).addTo(map);

  // If we have existing coords, drop pin immediately
  if (props.lat && props.lng) {
    dropPin(props.lat, props.lng, false);
  }

  map.on('click', async (e) => {
    await dropPin(e.latlng.lat, e.latlng.lng, true);
  });
}

async function dropPin(lat, lng, geocode = true) {
  if (!map || !L) return;

  if (marker) {
    marker.setLatLng([lat, lng]);
  } else {
    marker = L.marker([lat, lng], { icon: buildIcon(L), draggable: true }).addTo(map);
    marker.on('dragend', async () => {
      const pos = marker.getLatLng();
      await reverseGeocode(pos.lat, pos.lng);
      emit('update:lat', pos.lat);
      emit('update:lng', pos.lng);
    });
  }

  map.setView([lat, lng], Math.max(map.getZoom(), 14));
  emit('update:lat', lat);
  emit('update:lng', lng);

  if (geocode) await reverseGeocode(lat, lng);
}

async function reverseGeocode(lat, lng) {
  geocoding.value = true;
  try {
    const res  = await fetch(
      `https://nominatim.openstreetmap.org/reverse?format=json&lat=${lat}&lon=${lng}&addressdetails=1`,
      { headers: { 'Accept-Language': 'en' } }
    );
    const data = await res.json();
    const addr = data.address || {};

    // Map OSM fields to PH admin hierarchy
    localBarangay.value     = addr.village || addr.suburb || addr.neighbourhood || addr.quarter || '';
    localMunicipality.value = addr.city || addr.town || addr.municipality || addr.county || '';
    localProvince.value     = addr.state || addr.province || addr.region || '';

    emitChange();

    if (marker) {
      const label = [localBarangay.value, localMunicipality.value, localProvince.value].filter(Boolean).join(', ');
      marker.bindPopup(`<strong>📍 ${label || 'Pinned location'}</strong>`).openPopup();
    }
  } catch (e) {
    console.warn('Reverse geocode failed', e);
  } finally {
    geocoding.value = false;
  }
}

async function searchLocation() {
  const q = searchQuery.value.trim();
  if (!q) return;
  searching.value   = true;
  searchResults.value = [];
  try {
    const res = await fetch(
      `https://nominatim.openstreetmap.org/search?format=json&q=${encodeURIComponent(q + ', Philippines')}&addressdetails=1&limit=6&countrycodes=ph`,
      { headers: { 'Accept-Language': 'en' } }
    );
    const data = await res.json();
    searchResults.value = data;
  } catch (e) {
    console.warn('Search failed', e);
  } finally {
    searching.value = false;
  }
}

async function selectResult(r) {
  searchResults.value = [];
  searchQuery.value   = '';
  await dropPin(parseFloat(r.lat), parseFloat(r.lon), false);
  // Populate from the search result address directly
  const addr = r.address || {};
  localBarangay.value     = addr.village || addr.suburb || addr.neighbourhood || addr.quarter || '';
  localMunicipality.value = addr.city || addr.town || addr.municipality || addr.county || '';
  localProvince.value     = addr.state || addr.province || addr.region || '';
  emitChange();
  if (marker) {
    const label = [localBarangay.value, localMunicipality.value, localProvince.value].filter(Boolean).join(', ');
    marker.bindPopup(`<strong>📍 ${label || r.display_name}</strong>`).openPopup();
  }
}

function clearSearch() {
  searchQuery.value    = '';
  searchResults.value  = [];
}

function onSearchInput() {
  if (!searchQuery.value.trim()) searchResults.value = [];
}

function centerOnPhilippines() {
  if (map) map.setView(PH_CENTER, PH_ZOOM);
}

function emitChange() {
  emit('update:barangay',     localBarangay.value);
  emit('update:municipality', localMunicipality.value);
  emit('update:province',     localProvince.value);
  emit('change', {
    barangay:     localBarangay.value,
    municipality: localMunicipality.value,
    province:     localProvince.value,
  });
}

// Sync from parent
watch(() => props.barangay,     v => { localBarangay.value     = v || ''; });
watch(() => props.municipality, v => { localMunicipality.value = v || ''; });
watch(() => props.province,     v => { localProvince.value     = v || ''; });

onMounted(() => initMap());
onUnmounted(() => { if (map) { map.remove(); map = null; } });
</script>

<style scoped>
.location-picker-wrap {
  display: flex;
  flex-direction: column;
  gap: 0.85rem;
}

/* Search */
.lp-search-row {
  display: flex;
  gap: 0.5rem;
}
.lp-search-box {
  flex: 1;
  display: flex;
  align-items: center;
  background: #f8fafc;
  border: 1.5px solid #e2e8f0;
  border-radius: 0.75rem;
  padding: 0 0.85rem;
  gap: 0.5rem;
}
.lp-search-box svg { width: 16px; height: 16px; color: #94a3b8; flex-shrink: 0; }
.lp-search-box input {
  flex: 1;
  border: none;
  background: transparent;
  font-size: 0.88rem;
  font-weight: 600;
  color: #0f172a;
  padding: 0.65rem 0;
  outline: none;
}
.lp-search-box input::placeholder { color: #94a3b8; }
.lp-clear-btn {
  background: none;
  border: none;
  color: #94a3b8;
  font-size: 0.85rem;
  cursor: pointer;
  padding: 0.25rem;
  line-height: 1;
}
.lp-search-btn {
  background: #0f172a;
  color: #fff;
  border: none;
  border-radius: 0.75rem;
  padding: 0 1.25rem;
  font-size: 0.85rem;
  font-weight: 700;
  cursor: pointer;
  white-space: nowrap;
}
.lp-search-btn:disabled { opacity: 0.6; cursor: not-allowed; }

/* Results */
.lp-results {
  background: #fff;
  border: 1.5px solid #e2e8f0;
  border-radius: 0.75rem;
  overflow: hidden;
  box-shadow: 0 8px 24px rgba(0,0,0,0.08);
  z-index: 1000;
}
.lp-result-item {
  display: flex;
  align-items: flex-start;
  gap: 0.65rem;
  padding: 0.75rem 1rem;
  cursor: pointer;
  font-size: 0.83rem;
  font-weight: 600;
  color: #334155;
  border-bottom: 1px solid #f1f5f9;
  transition: background 0.15s;
}
.lp-result-item:last-child { border-bottom: none; }
.lp-result-item:hover { background: #f8fafc; }
.lp-result-item svg { width: 14px; height: 14px; color: #e11d48; flex-shrink: 0; margin-top: 2px; }

/* Map */
.lp-map-container {
  position: relative;
  border-radius: 1rem;
  overflow: hidden;
  border: 1.5px solid #e2e8f0;
  box-shadow: 0 4px 16px rgba(0,0,0,0.06);
}
.lp-map {
  width: 100%;
  height: 340px;
}
.lp-geocoding-overlay {
  position: absolute;
  inset: 0;
  background: rgba(255,255,255,0.7);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 0.85rem;
  font-weight: 700;
  color: #0f172a;
  gap: 0.5rem;
  z-index: 500;
  backdrop-filter: blur(2px);
}
.lp-spinner {
  width: 16px;
  height: 16px;
  border: 2px solid #e2e8f0;
  border-top-color: #0f172a;
  border-radius: 50%;
  animation: spin 0.7s linear infinite;
  display: inline-block;
}
@keyframes spin { to { transform: rotate(360deg); } }

.lp-locate-btn {
  position: absolute;
  bottom: 12px;
  right: 12px;
  width: 38px;
  height: 38px;
  background: #fff;
  border: 1.5px solid #e2e8f0;
  border-radius: 0.6rem;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  z-index: 500;
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
}
.lp-locate-btn svg { width: 18px; height: 18px; color: #0f172a; }
.lp-locate-btn:hover { background: #f8fafc; }

/* Address Fields */
.lp-address-header {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 0.8rem;
  font-weight: 800;
  color: #0f172a;
  text-transform: uppercase;
  letter-spacing: 0.04em;
}
.lp-address-header svg { width: 15px; height: 15px; color: #e11d48; }
.lp-address-grid {
  display: grid;
  grid-template-columns: 1fr 1fr 1fr;
  gap: 0.75rem;
  margin-top: 0.5rem;
}
.lp-address-item label {
  display: block;
  font-size: 0.72rem;
  font-weight: 800;
  color: #64748b;
  text-transform: uppercase;
  margin-bottom: 0.3rem;
}
.lp-address-item input {
  width: 100%;
  background: #f8fafc;
  border: 1.5px solid #e2e8f0;
  border-radius: 0.6rem;
  padding: 0.55rem 0.75rem;
  font-size: 0.88rem;
  font-weight: 600;
  color: #0f172a;
  outline: none;
  transition: border-color 0.2s;
}
.lp-address-item input:focus { border-color: #0f172a; background: #fff; }
.lp-hint {
  font-size: 0.78rem;
  color: #64748b;
  font-weight: 600;
  margin-top: 0.35rem;
}
.lp-empty-hint {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 0.85rem;
  color: #94a3b8;
  font-weight: 600;
  padding: 0.75rem 1rem;
  background: #f8fafc;
  border-radius: 0.75rem;
  border: 1.5px dashed #e2e8f0;
}
.lp-empty-hint svg { width: 16px; height: 16px; color: #94a3b8; flex-shrink: 0; }

/* Mobile */
@media (max-width: 768px) {
  .lp-address-grid { grid-template-columns: 1fr; }
  .lp-map { height: 260px; }
}
</style>

<style>
/* Global — custom marker (not scoped so Leaflet can see it) */
.lp-custom-marker {
  display: flex;
  align-items: flex-end;
  justify-content: center;
}
.leaflet-popup-content-wrapper {
  border-radius: 0.75rem !important;
  box-shadow: 0 8px 24px rgba(0,0,0,0.12) !important;
}
.leaflet-popup-content {
  font-family: 'Inter', sans-serif !important;
  font-size: 0.85rem !important;
  font-weight: 600 !important;
  color: #0f172a !important;
}
</style>
