<template>
  <div class="schedule-tab">

    <div class="page-header desktop-only">
      <div>
        <h1>My Schedule</h1>
        <p>Monthly view of your confirmed bookings and available session slots.</p>
      </div>
    </div>

    <!-- Month Navigation -->
    <div class="month-nav">
      <button class="nav-btn" @click="prevMonth">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><path d="m15 18-6-6 6-6"/></svg>
      </button>
      <div class="month-title">
        <span class="month-name">{{ monthLabel }}</span>
      </div>
      <button class="nav-btn" @click="nextMonth">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><path d="m9 18 6-6-6-6"/></svg>
      </button>
    </div>

    <!-- Stats Strip -->
    <div class="stats-strip">
      <div class="strip-stat" v-for="s in stripStats" :key="s.label">
        <span class="strip-dot" :style="{ background: s.color }"></span>
        <span class="strip-val">{{ s.value }}</span>
        <span class="strip-label">{{ s.label }}</span>
      </div>
    </div>

    <!-- Legend -->
    <div class="legend">
      <span class="leg-item"><span class="leg-dot available"></span>Available</span>
      <span class="leg-item"><span class="leg-dot booking"></span>Booked by Student</span>
      <span class="leg-item"><span class="leg-dot today"></span>Today</span>
    </div>

    <!-- Calendar -->
    <div class="calendar-card" v-if="!loading">
      <div class="dow-row">
        <div v-for="d in ['Sun','Mon','Tue','Wed','Thu','Fri','Sat']" :key="d" class="dow">{{ d }}</div>
      </div>
      <div class="cal-body">
        <div v-for="blank in calendarBlanks" :key="'b'+blank" class="cal-cell empty"></div>
        <div
          v-for="day in calendarDays"
          :key="day.date"
          :class="['cal-cell',
            { today: day.isToday,
              'has-slots': day.slots.length > 0 || day.bookings.length > 0,
              'has-bookings': day.bookings.length > 0,
              selected: selectedDate === day.date }]"
          @click="selectDay(day)"
        >
          <span class="day-num">{{ day.n }}</span>
          <div class="slot-dots" v-if="day.slots.length || day.bookings.length">
            <!-- Booking dots (orange) -->
            <span
              v-for="(b, i) in day.bookings.slice(0,2)"
              :key="'bk'+i"
              class="slot-dot booking"
            ></span>
            <!-- Available slot dots (green) -->
            <span
              v-for="(s, i) in day.slots.filter(sl => !sl.is_booked).slice(0,2)"
              :key="'sl'+i"
              class="slot-dot available"
            ></span>
          </div>
        </div>
      </div>
    </div>

    <!-- Loading -->
    <div class="loading-state" v-if="loading">
      <div class="spinner"></div><p>Loading schedule...</p>
    </div>

    <!-- Day Detail Panel -->
    <transition name="slide">
      <div class="day-panel" v-if="selectedDate && (selectedDaySlots.length > 0 || selectedDayBookings.length > 0)">
        <div class="panel-header">
          <h3>{{ formatDayTitle(selectedDate) }}</h3>
          <button @click="selectedDate = null">✕</button>
        </div>

        <!-- Confirmed Bookings Section -->
        <div v-if="selectedDayBookings.length" class="panel-section">
          <p class="panel-section-title">📌 Student Bookings</p>
          <div class="slot-list">
            <div class="slot-row booking-row" v-for="b in selectedDayBookings" :key="'bk'+b.id">
              <div class="booking-info">
                <div class="slot-time">
                  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" width="13" height="13"><circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/></svg>
                  {{ formatTime(b.start_time) }} – {{ formatTime(b.end_time) }}
                </div>
                <div class="booking-meta">
                  <span class="booking-student">👤 {{ b.student_name }}</span>
                  <span class="booking-post">{{ b.post_title }} · Session {{ b.session_number }}</span>
                </div>
                <p v-if="studentFullAddress(b)" class="student-location">
                  <span class="loc-label">Student location</span>
                  {{ studentFullAddress(b) }}
                </p>
                <p v-else class="student-location muted">No address on file for this student.</p>
                <button
                  v-if="canMarkComplete(b)"
                  type="button"
                  class="btn-mark-done"
                  :disabled="markingBookingId === b.id"
                  @click="markBookingComplete(b)"
                >
                  {{ markingBookingId === b.id ? 'Saving…' : 'Mark session as done' }}
                </button>
              </div>
              <span :class="['slot-status', b.status]">{{ statusLabel(b.status) }}</span>
            </div>
          </div>
        </div>

        <!-- Available Slots Section -->
        <div v-if="selectedDaySlots.filter(s => !s.is_booked).length" class="panel-section">
          <p class="panel-section-title">🟢 Available Slots</p>
          <div class="slot-list">
            <div class="slot-row" v-for="s in selectedDaySlots.filter(sl => !sl.is_booked)" :key="'sl'+s.id">
              <div class="slot-time">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" width="13" height="13"><circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/></svg>
                {{ formatTime(s.start_time) }} – {{ formatTime(s.end_time) }}
              </div>
              <div class="slot-post">{{ s.post_title }} · Session {{ s.session_number }}</div>
              <span class="slot-status free">Open</span>
            </div>
          </div>
        </div>
      </div>
      <div class="day-panel empty-panel" v-else-if="selectedDate">
        <p>No sessions on {{ formatDayTitle(selectedDate) }}.</p>
      </div>
    </transition>

  </div>
</template>

<script setup>
import { ref, computed, watch } from 'vue';
import { sessionSlotService, bookingService } from '../../services/api';

const props = defineProps({ profile: Object });

const today = new Date();
const todayStr = today.toISOString().split('T')[0];
const viewYear = ref(today.getFullYear());
const viewMonth = ref(today.getMonth());
const allSlots = ref([]);
const allBookings = ref([]);
const loading = ref(true);
const selectedDate = ref(null);
const currentTutorId = ref(null);
const markingBookingId = ref(null);

watch(() => props.profile, async (p) => {
  if (p && p.user) {
    currentTutorId.value = p.user;
    await fetchData();
  }
}, { immediate: true });

async function fetchData() {
  if (!currentTutorId.value) return;
  loading.value = true;
  try {
    const [slotsRes, bookingsRes] = await Promise.all([
      sessionSlotService.getSlots({ tutor_id: currentTutorId.value }),
      bookingService.getTutorBookings(currentTutorId.value)
    ]);
    allSlots.value = Array.isArray(slotsRes.data) ? slotsRes.data : (slotsRes.data.results || []);
    allBookings.value = Array.isArray(bookingsRes.data) ? bookingsRes.data : (bookingsRes.data.results || []);
  } catch (e) {
    console.error('Failed to load schedule', e);
  } finally {
    loading.value = false;
  }
}

const monthLabel = computed(() =>
  new Date(viewYear.value, viewMonth.value, 1)
    .toLocaleDateString('en-US', { month: 'long', year: 'numeric' })
);

function prevMonth() {
  if (viewMonth.value === 0) { viewMonth.value = 11; viewYear.value--; }
  else viewMonth.value--;
  selectedDate.value = null;
}
function nextMonth() {
  if (viewMonth.value === 11) { viewMonth.value = 0; viewYear.value++; }
  else viewMonth.value++;
  selectedDate.value = null;
}

const calendarBlanks = computed(() =>
  new Date(viewYear.value, viewMonth.value, 1).getDay()
);

const calendarDays = computed(() => {
  const daysInMonth = new Date(viewYear.value, viewMonth.value + 1, 0).getDate();
  return Array.from({ length: daysInMonth }, (_, i) => {
    const n = i + 1;
    const date = `${viewYear.value}-${String(viewMonth.value+1).padStart(2,'0')}-${String(n).padStart(2,'0')}`;
    const slots = allSlots.value.filter(s => s.date === date);
    const bookings = allBookings.value.filter(b => b.date === date);
    return { n, date, isToday: date === todayStr, slots, bookings };
  });
});

const slotsInMonth = computed(() => {
  const prefix = `${viewYear.value}-${String(viewMonth.value+1).padStart(2,'0')}`;
  return allSlots.value.filter(s => s.date.startsWith(prefix));
});
const bookingsInMonth = computed(() => {
  const prefix = `${viewYear.value}-${String(viewMonth.value+1).padStart(2,'0')}`;
  return allBookings.value.filter(b => b.date && b.date.startsWith(prefix));
});

const stripStats = computed(() => [
  { label: 'Available', value: slotsInMonth.value.filter(s => !s.is_booked).length, color: '#10b981' },
  { label: 'Booked', value: bookingsInMonth.value.length, color: '#f59e0b' },
  { label: 'Total Sessions', value: slotsInMonth.value.length, color: '#0f172a' },
]);

const selectedDaySlots = computed(() =>
  allSlots.value.filter(s => s.date === selectedDate.value)
);
const selectedDayBookings = computed(() =>
  allBookings.value.filter(b => b.date === selectedDate.value)
);

function selectDay(day) {
  selectedDate.value = selectedDate.value === day.date ? null : day.date;
}
function formatDayTitle(dateStr) {
  return new Date(dateStr + 'T00:00:00').toLocaleDateString('en-US', { weekday:'long', month:'long', day:'numeric', year:'numeric' });
}
function formatTime(t) {
  if (!t) return '';
  const [h, m] = t.split(':');
  const hh = parseInt(h);
  return `${hh % 12 || 12}:${m} ${hh < 12 ? 'AM' : 'PM'}`;
}

function sessionEndMs(b) {
  if (!b?.date) return null;
  const t = b.end_time ? String(b.end_time).slice(0, 8) : '23:59:59';
  return new Date(`${b.date}T${t}`).getTime();
}

function canMarkComplete(b) {
  if (!b || b.status !== 'confirmed') return false;
  const end = sessionEndMs(b);
  if (end == null || Number.isNaN(end)) return false;
  return end <= Date.now();
}

function studentFullAddress(b) {
  const parts = [b.student_barangay, b.student_municipality, b.student_province]
    .map((x) => (x && String(x).trim()) || '')
    .filter(Boolean);
  return parts.length ? parts.join(', ') : '';
}

function statusLabel(s) {
  if (s === 'completed') return 'Done';
  return s || '';
}

async function markBookingComplete(b) {
  if (!currentTutorId.value || !b?.id) return;
  markingBookingId.value = b.id;
  try {
    await bookingService.updateBooking(b.id, {
      status: 'completed',
      tutor_id: currentTutorId.value,
    });
    await fetchData();
  } catch (e) {
    console.error('Mark complete failed', e);
    const msg =
      e?.response?.data?.status?.[0] ||
      e?.response?.data?.detail ||
      (typeof e?.response?.data === 'string' ? e.response.data : null) ||
      'Could not mark session as done.';
    window.alert(msg);
  } finally {
    markingBookingId.value = null;
  }
}
</script>

<style scoped>
.schedule-tab { display: flex; flex-direction: column; gap: 1.25rem; }
.page-header h1 { font-size: 2rem; font-weight: 800; color: #0f172a; }
.page-header p { color: #64748b; margin-top: 0.2rem; }

/* Month nav */
.month-nav { display: flex; align-items: center; justify-content: space-between; background: white; border-radius: 1rem; padding: 1rem 1.5rem; border: 1px solid #f1f5f9; box-shadow: 0 2px 8px rgba(0,0,0,0.03); }
.nav-btn { background: #f8fafc; border: 1px solid #f1f5f9; border-radius: 0.6rem; width: 36px; height: 36px; display: flex; align-items: center; justify-content: center; cursor: pointer; }
.nav-btn svg { width: 16px; height: 16px; color: #0f172a; }
.month-name { font-size: 1.2rem; font-weight: 800; color: #0f172a; }

/* Stats */
.stats-strip { display: flex; gap: 1.5rem; }
.strip-stat { display: flex; align-items: center; gap: 0.5rem; background: white; border-radius: 0.75rem; padding: 0.75rem 1.25rem; border: 1px solid #f1f5f9; }
.strip-dot { width: 10px; height: 10px; border-radius: 50%; }
.strip-val { font-size: 1.25rem; font-weight: 800; color: #0f172a; }
.strip-label { font-size: 0.75rem; color: #94a3b8; font-weight: 600; }

/* Legend */
.legend { display: flex; gap: 1.25rem; align-items: center; }
.leg-item { display: flex; align-items: center; gap: 0.4rem; font-size: 0.78rem; font-weight: 600; color: #64748b; }
.leg-dot { width: 10px; height: 10px; border-radius: 50%; }
.leg-dot.available { background: #10b981; }
.leg-dot.booking { background: #f59e0b; }
.leg-dot.today { background: #0f172a; }

/* Calendar */
.calendar-card { background: white; border-radius: 1.25rem; border: 1px solid #f1f5f9; overflow: hidden; box-shadow: 0 4px 16px rgba(0,0,0,0.04); }
.dow-row { display: grid; grid-template-columns: repeat(7,1fr); background: #0f172a; }
.dow { text-align: center; padding: 0.75rem 0; font-size: 0.72rem; font-weight: 700; color: rgba(255,255,255,0.7); }

.cal-body { display: grid; grid-template-columns: repeat(7,1fr); }
.cal-cell {
  min-height: 80px; border-right: 1px solid #f8fafc; border-bottom: 1px solid #f8fafc;
  padding: 0.5rem; cursor: pointer; transition: background 0.15s; position: relative;
}
.cal-cell.empty { cursor: default; background: #fafafa; }
.cal-cell:hover:not(.empty) { background: #f8fafc; }
.cal-cell.today { background: #eff6ff; }
.cal-cell.today .day-num { background: #0f172a; color: #fff; border-radius: 50%; width: 24px; height: 24px; display: flex; align-items: center; justify-content: center; }
.cal-cell.selected { background: #f0fdf4; outline: 2px solid #10b981; outline-offset: -2px; }
.day-num { font-size: 0.8rem; font-weight: 700; color: #0f172a; display: inline-flex; align-items: center; justify-content: center; width: 24px; height: 24px; }
.slot-dots { display: flex; flex-wrap: wrap; gap: 2px; margin-top: 0.35rem; }
.slot-dot { width: 7px; height: 7px; border-radius: 50%; }
.slot-dot.available { background: #10b981; }
.slot-dot.booking { background: #f59e0b; }
.slot-more { font-size: 0.6rem; color: #94a3b8; font-weight: 700; }
/* Day panel */
.day-panel { background: white; border-radius: 1.25rem; border: 1px solid #f1f5f9; padding: 1.25rem 1.5rem; box-shadow: 0 4px 16px rgba(0,0,0,0.04); }
.empty-panel { color: #94a3b8; font-size: 0.9rem; }
.panel-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 1rem; }
.panel-header h3 { font-size: 1rem; font-weight: 800; color: #0f172a; }
.panel-header button { background: none; border: none; font-size: 1.1rem; cursor: pointer; color: #94a3b8; }
.panel-section { display: flex; flex-direction: column; gap: 0.75rem; margin-bottom: 1.5rem; }
.panel-section:last-child { margin-bottom: 0; }
.panel-section-title { font-size: 0.85rem; font-weight: 800; color: #0f172a; margin: 0; }
.slot-list { display: flex; flex-direction: column; gap: 0.75rem; }
.slot-row { display: flex; align-items: center; gap: 1rem; padding: 0.75rem 1rem; background: #f8fafc; border-radius: 0.75rem; border: 1px solid #f1f5f9; }
.booking-row { background: #fffbeb; border-color: #fef3c7; }
.booking-info { display: flex; flex-direction: column; gap: 0.2rem; flex: 1; }
.booking-meta { display: flex; align-items: center; gap: 0.5rem; font-size: 0.75rem; color: #92400e; font-weight: 600; flex-wrap: wrap; }
.booking-student { font-weight: 800; color: #b45309; }
.student-location {
  margin: 0.35rem 0 0;
  font-size: 0.72rem;
  font-weight: 600;
  color: #78350f;
  line-height: 1.35;
}
.student-location.muted { color: #a8a29e; font-style: italic; }
.loc-label { display: block; font-size: 0.65rem; font-weight: 800; text-transform: uppercase; letter-spacing: 0.04em; color: #92400e; margin-bottom: 0.15rem; }
.btn-mark-done {
  margin-top: 0.65rem;
  align-self: flex-start;
  padding: 0.45rem 0.85rem;
  border-radius: 0.5rem;
  border: none;
  background: #0f172a;
  color: #fff;
  font-size: 0.72rem;
  font-weight: 800;
  cursor: pointer;
  transition: background 0.2s;
}
.btn-mark-done:hover:not(:disabled) { background: #1e293b; }
.btn-mark-done:disabled { opacity: 0.6; cursor: not-allowed; }
.slot-time { display: flex; align-items: center; gap: 0.4rem; font-size: 0.85rem; font-weight: 700; color: #0f172a; min-width: 140px; }
.slot-post { flex: 1; font-size: 0.82rem; color: #64748b; font-weight: 600; }
.slot-status { font-size: 0.7rem; font-weight: 800; padding: 0.25rem 0.65rem; border-radius: 2rem; text-transform: capitalize; }
.slot-status.free { background: #dcfce7; color: #16a34a; }
.slot-status.pending { background: #fef3c7; color: #92400e; }
.slot-status.confirmed { background: #dbeafe; color: #1e3a8a; }
.slot-status.completed { background: #d1fae5; color: #047857; }
.slot-status.cancelled { background: #fee2e2; color: #b91c1c; }

.loading-state { display: flex; flex-direction: column; align-items: center; gap: 1rem; padding: 4rem; color: #94a3b8; }
.spinner { width: 36px; height: 36px; border: 3px solid #f1f5f9; border-top-color: #0f172a; border-radius: 50%; animation: spin 0.7s linear infinite; }
@keyframes spin { to { transform: rotate(360deg); } }

.slide-enter-active, .slide-leave-active { transition: all 0.3s ease; }
.slide-enter-from, .slide-leave-to { opacity: 0; transform: translateY(-10px); }

@media (max-width: 768px) {
  .desktop-only { display: none !important; }
  .stats-strip { flex-wrap: wrap; gap: 0.75rem; }
  .strip-stat { flex: 1; min-width: 80px; }
  .cal-cell { min-height: 52px; padding: 0.3rem; }
  .dow { font-size: 0.6rem; padding: 0.5rem 0; }
}
</style>
