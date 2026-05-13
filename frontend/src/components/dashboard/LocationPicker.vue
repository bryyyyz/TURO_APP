<template>
  <div class="location-picker-wrap">

    <!-- GPS Button + Search Row -->
    <div class="lp-top-row">
      <button class="lp-gps-btn" type="button" @click="useMyLocation" :disabled="gpsLoading">
        <span v-if="gpsLoading" class="lp-spinner"></span>
        <svg v-else viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <circle cx="12" cy="12" r="3"/><path d="M12 1v4M12 19v4M4.22 4.22l2.83 2.83M16.95 16.95l2.83 2.83M1 12h4M19 12h4M4.22 19.78l2.83-2.83M16.95 7.05l2.83-2.83"/>
        </svg>
        {{ gpsLoading ? 'Detecting...' : 'Use My Current Location' }}
      </button>

      <div class="lp-search-box">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="11" cy="11" r="8"/><line x1="21" y1="21" x2="16.65" y2="16.65"/></svg>
        <input
          v-model="searchQuery"
          type="text"
          placeholder="Search barangay, city, province..."
          @keydown.enter.prevent="searchLocation"
          @input="onSearchInput"
        />
        <button v-if="searchQuery" class="lp-clear-btn" type="button" @click="clearSearch">✕</button>
        <button class="lp-search-inner-btn" type="button" @click="searchLocation" :disabled="searching">
          {{ searching ? '...' : 'Search' }}
        </button>
      </div>
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
        <span class="lp-spinner"></span> Getting precise location...
      </div>
      <button class="lp-reset-btn" type="button" @click="centerOnPhilippines" title="Reset view">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M3 12a9 9 0 1 0 9-9 9.75 9.75 0 0 0-6.74 2.74L3 8"/><path d="M3 3v5h5"/></svg>
      </button>
    </div>

    <!-- Resolved Address Fields -->
    <div class="lp-address-fields" v-if="localBarangay || localMunicipality || localProvince">
      <div class="lp-address-header">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0z"/><circle cx="12" cy="10" r="3"/></svg>
        Auto-detected Location
        <span class="lp-editable-badge">Editable</span>
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
          <input v-model="localProvince" type="text" placeholder="Province" @input="emitChange" />
        </div>
      </div>
      <p class="lp-hint">📍 Fields are auto-filled from the pin. You can manually correct them if needed.</p>
    </div>

    <div class="lp-empty-hint" v-else>
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0z"/><circle cx="12" cy="10" r="3"/></svg>
      Use "My Current Location" or click anywhere on the map
    </div>

    <!-- GPS error message -->
    <div v-if="gpsError" class="lp-gps-error">
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"/><line x1="12" y1="8" x2="12" y2="12"/><line x1="12" y1="16" x2="12.01" y2="16"/></svg>
      {{ gpsError }}
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

const mapRef     = ref(null);
const geocoding  = ref(false);
const searching  = ref(false);
const gpsLoading = ref(false);
const gpsError   = ref('');
const searchQuery   = ref('');
const searchResults = ref([]);

const localBarangay    = ref(props.barangay    || '');
const localMunicipality= ref(props.municipality || '');
const localProvince    = ref(props.province    || '');

let map    = null;
let marker = null;
let L      = null;

const PH_CENTER = [12.8797, 121.7740];
const PH_ZOOM   = 6;

// ─── Leaflet Loader ──────────────────────────────────────────────────────────
async function loadLeaflet() {
  if (window.L) return window.L;
  if (!document.getElementById('leaflet-css')) {
    const link = document.createElement('link');
    link.id   = 'leaflet-css';
    link.rel  = 'stylesheet';
    link.href = 'https://unpkg.com/leaflet@1.9.4/dist/leaflet.css';
    document.head.appendChild(link);
  }
  await new Promise((resolve, reject) => {
    if (window.L) return resolve();
    const script = document.createElement('script');
    script.src = 'https://unpkg.com/leaflet@1.9.4/dist/leaflet.js';
    script.onload = resolve;
    script.onerror = reject;
    document.head.appendChild(script);
  });
  return window.L;
}

function buildIcon(leaflet) {
  return leaflet.divIcon({
    className: '',
    html: `<div class="lp-custom-marker">
      <svg viewBox="0 0 24 24" fill="#e11d48" width="36" height="36">
        <path d="M12 2C8.13 2 5 5.13 5 9c0 5.25 7 13 7 13s7-7.75 7-13c0-3.87-3.13-7-7-7z"/>
        <circle cx="12" cy="9" r="2.5" fill="white"/>
      </svg>
    </div>`,
    iconSize:   [36, 44],
    iconAnchor: [18, 44],
  });
}

// ─── Map Init ─────────────────────────────────────────────────────────────────
async function initMap() {
  L = await loadLeaflet();
  if (!mapRef.value) return;

  map = L.map(mapRef.value, { center: PH_CENTER, zoom: PH_ZOOM, zoomControl: true });

  L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '© <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a>',
    maxZoom: 19,
  }).addTo(map);

  if (props.lat && props.lng) dropPin(props.lat, props.lng, false);

  map.on('click', async (e) => {
    await dropPin(e.latlng.lat, e.latlng.lng, true);
  });
}

// ─── Pin Drop ─────────────────────────────────────────────────────────────────
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
  map.setView([lat, lng], Math.max(map.getZoom(), 16));
  emit('update:lat', lat);
  emit('update:lng', lng);
  if (geocode) await reverseGeocode(lat, lng);
}

// ─── Philippine Address Extractor ────────────────────────────────────────────
// Nominatim returns different field names for Philippine admin levels.
// This function maps them to barangay / municipality / province correctly.
function extractPhAddress(addr) {
  /*
   * Philippine OSM admin hierarchy (from finest to coarsest):
   *   admin_level 10 → Barangay (village / hamlet / suburb)
   *   admin_level 6  → City / Municipality (city / town / city_district / county)
   *   admin_level 4  → Province (state / province)
   *   admin_level 3  → Region (region — fallback if province missing)
   *
   * Nominatim flattens these into named keys. We try the most specific
   * ones first for each level.
   */

  // BARANGAY — finest grain
  const barangay =
    addr.village        ||  // typical OSM barangay
    addr.hamlet         ||
    addr.suburb         ||
    addr.neighbourhood  ||
    addr.quarter        ||
    addr.residential    ||
    '';

  // MUNICIPALITY / CITY
  const municipality =
    addr.city           ||  // chartered cities (e.g. Makati City)
    addr.town           ||
    addr.municipality   ||
    addr.city_district  ||  // some component cities
    addr.county         ||  // fallback
    '';

  // PROVINCE
  const province =
    addr.province       ||  // some PH entries tag this directly
    addr.state          ||  // most PH provinces map to OSM "state"
    addr.region         ||  // fallback for NCR / BARMM which have no province
    '';

  return { barangay, municipality, province };
}

// ─── Reverse Geocode ──────────────────────────────────────────────────────────
async function reverseGeocode(lat, lng) {
  geocoding.value = true;
  try {
    // zoom=18 gives the finest possible detail (street/barangay level)
    const res  = await fetch(
      `https://nominatim.openstreetmap.org/reverse?format=json&lat=${lat}&lon=${lng}&addressdetails=1&zoom=18`,
      { headers: { 'Accept-Language': 'en' } }
    );
    const data = await res.json();
    const addr = data.address || {};

    const { barangay, municipality, province } = extractPhAddress(addr);
    localBarangay.value     = barangay;
    localMunicipality.value = municipality;
    localProvince.value     = province;

    emitChange();
    updatePopup();
  } catch (e) {
    console.warn('Reverse geocode failed', e);
  } finally {
    geocoding.value = false;
  }
}

function updatePopup() {
  if (!marker) return;
  const label = [localBarangay.value, localMunicipality.value, localProvince.value]
    .filter(Boolean).join(', ');
  marker.bindPopup(`<strong>📍 ${label || 'Pinned location'}</strong>`).openPopup();
}

// ─── GPS — Use My Current Location ───────────────────────────────────────────
async function useMyLocation() {
  gpsError.value = '';
  if (!navigator.geolocation) {
    gpsError.value = 'Geolocation is not supported by your browser.';
    return;
  }
  gpsLoading.value = true;
  navigator.geolocation.getCurrentPosition(
    async (pos) => {
      const lat = pos.coords.latitude;
      const lng = pos.coords.longitude;
      await dropPin(lat, lng, true);
      gpsLoading.value = false;
    },
    (err) => {
      gpsLoading.value = false;
      if (err.code === 1)
        gpsError.value = 'Location access denied. Please allow location in your browser settings.';
      else if (err.code === 2)
        gpsError.value = 'Could not detect your position. Please click on the map manually.';
      else
        gpsError.value = 'Location detection timed out. Please click on the map manually.';
    },
    { enableHighAccuracy: true, timeout: 12000, maximumAge: 0 }
  );
}

// ─── Search ───────────────────────────────────────────────────────────────────
async function searchLocation() {
  const q = searchQuery.value.trim();
  if (!q) return;
  searching.value = true;
  searchResults.value = [];
  try {
    const res = await fetch(
      `https://nominatim.openstreetmap.org/search?format=json&q=${encodeURIComponent(q + ', Philippines')}&addressdetails=1&limit=6&countrycodes=ph`,
      { headers: { 'Accept-Language': 'en' } }
    );
    searchResults.value = await res.json();
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
  const { barangay, municipality, province } = extractPhAddress(r.address || {});
  localBarangay.value     = barangay;
  localMunicipality.value = municipality;
  localProvince.value     = province;
  emitChange();
  updatePopup();
}

function clearSearch()  { searchQuery.value = ''; searchResults.value = []; }
function onSearchInput() { if (!searchQuery.value.trim()) searchResults.value = []; }
function centerOnPhilippines() { if (map) map.setView(PH_CENTER, PH_ZOOM); }

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

watch(() => props.barangay,     v => { localBarangay.value     = v || ''; });
watch(() => props.municipality, v => { localMunicipality.value = v || ''; });
watch(() => props.province,     v => { localProvince.value     = v || ''; });

onMounted(() => initMap());
onUnmounted(() => { if (map) { map.remove(); map = null; } });
</script>

<style scoped>
.location-picker-wrap { display: flex; flex-direction: column; gap: 0.85rem; }

/* Top row: GPS + Search */
.lp-top-row { display: flex; flex-direction: column; gap: 0.5rem; }

.lp-gps-btn {
  display: flex; align-items: center; justify-content: center; gap: 0.55rem;
  width: 100%; padding: 0.75rem 1rem;
  background: linear-gradient(135deg, #0f172a, #1e3a5f);
  color: #fff; border: none; border-radius: 0.75rem;
  font-size: 0.88rem; font-weight: 700; cursor: pointer;
  transition: opacity 0.2s; letter-spacing: 0.01em;
}
.lp-gps-btn:hover:not(:disabled) { opacity: 0.88; }
.lp-gps-btn:disabled { opacity: 0.6; cursor: not-allowed; }
.lp-gps-btn svg { width: 16px; height: 16px; flex-shrink: 0; }

.lp-search-box {
  display: flex; align-items: center;
  background: #f8fafc; border: 1.5px solid #e2e8f0;
  border-radius: 0.75rem; padding: 0 0.75rem; gap: 0.4rem;
}
.lp-search-box svg { width: 15px; height: 15px; color: #94a3b8; flex-shrink: 0; }
.lp-search-box input {
  flex: 1; border: none; background: transparent;
  font-size: 0.87rem; font-weight: 600; color: #0f172a;
  padding: 0.65rem 0; outline: none;
}
.lp-search-box input::placeholder { color: #94a3b8; }
.lp-clear-btn { background: none; border: none; color: #94a3b8; font-size: 0.85rem; cursor: pointer; padding: 0.2rem; }
.lp-search-inner-btn {
  background: #0f172a; color: #fff; border: none;
  border-radius: 0.55rem; padding: 0.4rem 0.85rem;
  font-size: 0.8rem; font-weight: 700; cursor: pointer; white-space: nowrap;
}
.lp-search-inner-btn:disabled { opacity: 0.6; cursor: not-allowed; }

/* Results */
.lp-results { background: #fff; border: 1.5px solid #e2e8f0; border-radius: 0.75rem; overflow: hidden; box-shadow: 0 8px 24px rgba(0,0,0,0.08); }
.lp-result-item { display: flex; align-items: flex-start; gap: 0.65rem; padding: 0.7rem 1rem; cursor: pointer; font-size: 0.82rem; font-weight: 600; color: #334155; border-bottom: 1px solid #f1f5f9; transition: background 0.15s; }
.lp-result-item:last-child { border-bottom: none; }
.lp-result-item:hover { background: #f8fafc; }
.lp-result-item svg { width: 13px; height: 13px; color: #e11d48; flex-shrink: 0; margin-top: 2px; }

/* Map */
.lp-map-container { position: relative; border-radius: 1rem; overflow: hidden; border: 1.5px solid #e2e8f0; box-shadow: 0 4px 16px rgba(0,0,0,0.06); }
.lp-map { width: 100%; height: 340px; }
.lp-geocoding-overlay { position: absolute; inset: 0; background: rgba(255,255,255,0.75); display: flex; align-items: center; justify-content: center; font-size: 0.85rem; font-weight: 700; color: #0f172a; gap: 0.5rem; z-index: 500; backdrop-filter: blur(3px); }
.lp-spinner { width: 15px; height: 15px; border: 2px solid #e2e8f0; border-top-color: #0f172a; border-radius: 50%; animation: spin 0.7s linear infinite; display: inline-block; flex-shrink: 0; }
@keyframes spin { to { transform: rotate(360deg); } }

.lp-reset-btn { position: absolute; bottom: 12px; right: 12px; width: 36px; height: 36px; background: #fff; border: 1.5px solid #e2e8f0; border-radius: 0.55rem; display: flex; align-items: center; justify-content: center; cursor: pointer; z-index: 500; box-shadow: 0 2px 8px rgba(0,0,0,0.1); }
.lp-reset-btn svg { width: 16px; height: 16px; color: #0f172a; }
.lp-reset-btn:hover { background: #f8fafc; }

/* Address fields */
.lp-address-header { display: flex; align-items: center; gap: 0.5rem; font-size: 0.78rem; font-weight: 800; color: #0f172a; text-transform: uppercase; letter-spacing: 0.04em; }
.lp-address-header svg { width: 14px; height: 14px; color: #e11d48; flex-shrink: 0; }
.lp-editable-badge { background: #f0fdf4; color: #16a34a; font-size: 0.65rem; font-weight: 800; padding: 0.15rem 0.5rem; border-radius: 2rem; border: 1px solid #bbf7d0; }
.lp-address-grid { display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 0.75rem; margin-top: 0.5rem; }
.lp-address-item label { display: block; font-size: 0.72rem; font-weight: 800; color: #64748b; text-transform: uppercase; margin-bottom: 0.3rem; }
.lp-address-item input { width: 100%; background: #f8fafc; border: 1.5px solid #e2e8f0; border-radius: 0.6rem; padding: 0.55rem 0.75rem; font-size: 0.88rem; font-weight: 600; color: #0f172a; outline: none; transition: border-color 0.2s; font-family: inherit; }
.lp-address-item input:focus { border-color: #0f172a; background: #fff; }
.lp-hint { font-size: 0.76rem; color: #64748b; font-weight: 600; margin-top: 0.35rem; }
.lp-empty-hint { display: flex; align-items: center; gap: 0.5rem; font-size: 0.84rem; color: #94a3b8; font-weight: 600; padding: 0.75rem 1rem; background: #f8fafc; border-radius: 0.75rem; border: 1.5px dashed #e2e8f0; }
.lp-empty-hint svg { width: 15px; height: 15px; color: #94a3b8; flex-shrink: 0; }
.lp-gps-error { display: flex; align-items: center; gap: 0.5rem; font-size: 0.82rem; color: #b91c1c; font-weight: 600; padding: 0.7rem 1rem; background: #fef2f2; border-radius: 0.75rem; border: 1.5px solid #fecaca; }
.lp-gps-error svg { width: 15px; height: 15px; flex-shrink: 0; }

@media (max-width: 768px) {
  .lp-address-grid { grid-template-columns: 1fr; }
  .lp-map { height: 260px; }
}
</style>

<style>
.lp-custom-marker { display: flex; align-items: flex-end; justify-content: center; }
.leaflet-popup-content-wrapper { border-radius: 0.75rem !important; box-shadow: 0 8px 24px rgba(0,0,0,0.12) !important; }
.leaflet-popup-content { font-family: 'Inter', sans-serif !important; font-size: 0.85rem !important; font-weight: 600 !important; color: #0f172a !important; }
</style>
