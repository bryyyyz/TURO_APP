<template>
  <div class="student-sessions">
    <div class="page-header">
      <div class="header-text">
        <h1>My Sessions</h1>
        <p>Manage your upcoming and past tutoring sessions.</p>
      </div>
      <div class="header-actions">
        <div class="header-btn date-btn">
          <svg viewBox="0 0 24 24" fill="none" stroke="#64748b" stroke-width="2"><rect x="3" y="4" width="18" height="18" rx="2" ry="2"/><line x1="16" y1="2" x2="16" y2="6"/><line x1="8" y1="2" x2="8" y2="6"/><line x1="3" y1="10" x2="21" y2="10"/></svg>
          <span>Friday, March 15, 2026</span>
          <svg viewBox="0 0 24 24" fill="none" stroke="#94a3b8" stroke-width="2.5" class="chevron"><path d="m6 9 6 6 6-6"/></svg>
        </div>
        <button type="button" class="header-btn notification-btn" @click="openActivityPanel">
          <svg viewBox="0 0 24 24" fill="none" stroke="#f59e0b" stroke-width="2"><path d="M18 8A6 6 0 0 0 6 8c0 7-3 9-3 9h18s-3-2-3-9"/><path d="M13.73 21a2 2 0 0 1-3.46 0"/></svg>
          <span>Notifications</span>
        </button>
      </div>
    </div>

    <!-- Status Tabs -->
    <div class="status-tabs-row">
      <div class="status-tabs">
        <button type="button" class="tab-btn" :class="{ active: activeTab === 'upcoming' }" @click="activeTab = 'upcoming'">
          Upcoming
          <span v-if="pendingTutorConfirm.length" class="tab-dot"></span>
        </button>
        <button type="button" class="tab-btn" :class="{ active: activeTab === 'completed' }" @click="activeTab = 'completed'">Completed</button>
        <button type="button" class="tab-btn" :class="{ active: activeTab === 'cancelled' }" @click="activeTab = 'cancelled'">Cancelled</button>
      </div>
    </div>

    <!-- Sessions List -->
    <div v-if="activeTab === 'upcoming'" class="pending-block" v-show="pendingTutorConfirm.length">
      <p class="pending-heading">Awaiting tutor confirmation</p>
      <p class="pending-sub">These sessions have ended; your tutor will mark them as done soon.</p>
      <div class="sessions-list compact">
        <div class="session-card pending-card" v-for="session in pendingTutorConfirm" :key="'p-' + session.id">
          <div class="tutor-header">
            <img :src="session.tutorPhoto" alt="Tutor" class="tutor-photo" />
            <div class="tutor-info">
              <h3>{{ session.tutorName }}</h3>
              <p>{{ session.subject }}</p>
            </div>
            <span class="status-tag status-pending-verify">Pending</span>
          </div>
          <div class="session-details">
            <div class="detail-item">{{ session.date }}</div>
            <div class="detail-item">{{ session.timeRange }}</div>
          </div>
        </div>
      </div>
    </div>

    <div class="sessions-list animate-scale-in">
      <p v-if="!loading && displayedSessions.length === 0" class="empty-sessions-msg">{{ emptyTabMessage }}</p>
      <div class="session-card" v-for="session in displayedSessions" :key="session.id">
        <div class="tutor-header">
          <div class="tutor-photo-wrap">
            <img :src="session.tutorPhoto" alt="Tutor" class="tutor-photo" @error="onImgError" />
          </div>
          <div class="tutor-info">
            <h3>
              {{ session.tutorName }}
              <svg v-if="session.verified" viewBox="0 0 24 24" fill="#3b82f6" class="verified-icon"><path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm-2 15-5-5 1.41-1.41L10 14.17l7.59-7.59L19 8l-9 9z"/></svg>
              <span :class="['session-tier-badge', tierPillClass(session.tier)]">{{ tierLabel(session.tier) }}</span>
            </h3>
            <p>{{ session.subject }}</p>
          </div>
          <span class="status-tag" :class="session.statusTagClass">{{ session.statusTag }}</span>
        </div>
        
        <div class="session-details">
          <div class="detail-item">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><rect x="3" y="4" width="18" height="18" rx="2" ry="2"/><line x1="16" y1="2" x2="16" y2="6"/><line x1="8" y1="2" x2="8" y2="6"/><line x1="3" y1="10" x2="21" y2="10"/></svg>
            {{ session.date }}
          </div>
          <div class="detail-item">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/></svg>
            {{ activeTab === 'completed' || activeTab === 'cancelled' ? session.timeRange : session.time }}
          </div>
        </div>

        <div class="session-actions" v-if="activeTab === 'upcoming' && session.status === 'confirmed'">
          <button type="button" class="btn-join">Join Session</button>
        </div>
      </div>
    </div>

    <!-- Bottom Grid -->
    <div class="bottom-grid">
      <div class="schedule-section">
        <div class="section-card">
          <div class="card-header">
            <h3>Schedule Sessions</h3>
            <p>Book and manage your upcoming sessions</p>
          </div>
          
          <div class="calendar-card">
            <div class="cal-header">
              <button class="cal-nav">‹</button>
              <div class="cal-title">September 2025</div>
              <button class="cal-nav">›</button>
            </div>
            <div class="cal-grid">
              <div class="cal-day-label" v-for="d in ['Su','Mo','Tu','We','Th','Fr','Sa']" :key="d">{{ d }}</div>
              <div class="cal-day empty"></div>
              <div 
                class="cal-day" 
                v-for="day in 30" 
                :key="day"
                :class="{ today: day === 9, has_session: day === 13 }"
              >
                {{ day }}
              </div>
            </div>
          </div>

          <div class="slot-box">
            <h4>Select a day to see available slots</h4>
            <p>All times shown in your local timezone</p>
          </div>
        </div>
      </div>

      <div class="activities-section">
        <div class="section-card">
          <div class="card-header">
            <h3>Recent Activities</h3>
            <a href="#" class="view-all">View all →</a>
          </div>
          <div class="activity-list">
            <div class="activity-item" v-for="act in recentActivities" :key="act.id">
              <div class="act-icon-wrap" :style="{ backgroundColor: act.color + '15' }">
                <img :src="act.icon" alt="" class="act-icon" />
              </div>
              <div class="act-info">
                <h4>{{ act.title }}</h4>
                <p>{{ act.subtitle }}</p>
              </div>
              <div class="act-val act-val-success">{{ act.value }}</div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, watch, inject } from 'vue';
import { bookingService } from '../../services/api';
import { OPEN_NOTIFICATIONS } from '../../symbols/injectionKeys';

const props = defineProps({ profile: Object });

const openNotifications = inject(OPEN_NOTIFICATIONS, null);
function openActivityPanel() {
  openNotifications?.();
}

const bookings = ref([]);
const loading = ref(true);
const activeTab = ref('upcoming');

function sessionEndMs(b) {
  if (!b?.date) return null;
  const t = b.end_time ? String(b.end_time).slice(0, 8) : '23:59:59';
  const ms = new Date(`${b.date}T${t}`).getTime();
  return Number.isNaN(ms) ? null : ms;
}

watch(() => props.profile, async (p) => {
  if (p && p.user) {
    await fetchBookings(p.user);
  }
}, { immediate: true });

async function fetchBookings(studentId) {
  loading.value = true;
  try {
    const { data } = await bookingService.getStudentBookings(studentId);
    bookings.value = Array.isArray(data) ? data : (data.results || []);
  } catch (e) {
    console.error('Failed to load student bookings', e);
  } finally {
    loading.value = false;
  }
}

function formatTime(t) {
  if (!t) return '';
  const [h, m] = t.split(':');
  const hh = parseInt(h, 10);
  return `${hh % 12 || 12}:${m} ${hh < 12 ? 'AM' : 'PM'}`;
}

function mapBookingCard(b, options = {}) {
  const end = b.end_time ? formatTime(b.end_time) : '';
  const start = formatTime(b.start_time);
  const timeRange = end && start !== end ? `${start} – ${end}` : start;
  const status = b.status;
  let statusTag = 'Scheduled';
  let statusTagClass = '';
  if (status === 'pending') {
    statusTag = 'Pending';
    statusTagClass = 'status-pending';
  } else if (status === 'confirmed') {
    statusTag = 'Confirmed';
    statusTagClass = 'status-confirmed';
  } else if (status === 'completed') {
    statusTag = 'Successful';
    statusTagClass = 'status-done';
  } else if (status === 'cancelled') {
    statusTag = 'Cancelled';
    statusTagClass = 'status-cancelled';
  }
  return {
    id: b.id,
    tutorName: b.tutor_name || 'Tutor',
    subject: b.post_subject || b.post_title || 'Tutoring Session',
    date: new Date(b.date + 'T12:00:00').toLocaleDateString('en-US', { month: 'long', day: 'numeric', year: 'numeric' }),
    time: start,
    timeRange,
    verified: status === 'confirmed' || status === 'completed',
    tutorPhoto: b.tutor_avatar_url || '/images/tutor_avatar.png',
    tier: b.tutor_tier || 'basic',
    status,
    statusTag,
    statusTagClass,
    showJoin: options.showJoin,
  };
}

/** Confirmed sessions that have ended but are not marked completed yet */
const pendingTutorConfirm = computed(() => {
  const now = Date.now();
  return bookings.value
    .filter((b) => b.status === 'confirmed' && sessionEndMs(b) != null && sessionEndMs(b) <= now)
    .sort((a, b) => String(b.date).localeCompare(String(a.date)))
    .map((b) => mapBookingCard(b));
});

const upcomingSessions = computed(() => {
  const now = Date.now();
  return bookings.value
    .filter((b) => {
      if (b.status === 'cancelled' || b.status === 'completed') return false;
      const end = sessionEndMs(b);
      if (end == null) return true;
      return end > now;
    })
    .sort((a, b) => {
      const c = String(a.date).localeCompare(String(b.date));
      if (c !== 0) return c;
      return String(a.start_time || '').localeCompare(String(b.start_time || ''));
    })
    .map((b) => mapBookingCard(b, { showJoin: b.status === 'confirmed' }));
});

const completedSessions = computed(() =>
  bookings.value
    .filter((b) => b.status === 'completed')
    .sort((a, b) => String(b.date).localeCompare(String(a.date)))
    .map((b) => mapBookingCard(b)),
);

const cancelledSessions = computed(() =>
  bookings.value
    .filter((b) => b.status === 'cancelled')
    .sort((a, b) => String(b.date).localeCompare(String(a.date)))
    .map((b) => mapBookingCard(b)),
);

const displayedSessions = computed(() => {
  if (activeTab.value === 'upcoming') return upcomingSessions.value;
  if (activeTab.value === 'completed') return completedSessions.value;
  return cancelledSessions.value;
});

const emptyTabMessage = computed(() => {
  if (activeTab.value === 'upcoming') return 'No upcoming sessions. Book a tutor to get started.';
  if (activeTab.value === 'completed') return 'No completed sessions yet.';
  return 'No cancelled sessions.';
});

const recentActivities = computed(() =>
  bookings.value
    .filter((b) => b.status === 'completed')
    .sort((a, b) => String(b.date).localeCompare(String(a.date)))
    .slice(-5)
    .reverse()
    .map((b) => ({
      id: b.id,
      title: `${b.post_subject || b.post_title || 'Session'} — completed`,
      subtitle: `${b.tutor_name || 'Tutor'} · ${new Date(b.date + 'T12:00:00').toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric' })}`,
      value: 'Success',
      icon: b.tutor_avatar_url || '/images/tutor_avatar.png',
      color: '#059669',
    })),
);

function onImgError(e) {
  if (e.target && !e.target.src.endsWith('/images/tutor_avatar.png'))
    e.target.src = '/images/tutor_avatar.png';
}

function tierLabel(tier) {
  if (tier === 'pro')  return '⭐⭐ Pro';
  if (tier === 'plus') return '⭐ Plus';
  return '';
}
function tierPillClass(tier) {
  if (tier === 'pro')  return 'tier-pro';
  if (tier === 'plus') return 'tier-plus';
  return 'tier-hidden';
}
</script>

<style scoped>
.student-sessions { width: 100%; display: flex; flex-direction: column; gap: 2.5rem; }

/* Header */
.page-header { display: flex; justify-content: space-between; align-items: center; }
.header-text h1 { font-family: var(--font-display); font-size: 2rem; font-weight: 800; color: #0f172a; margin-bottom: 0.25rem; }
.header-text p { color: #64748b; font-weight: 600; font-size: 0.95rem; }

.header-actions { display: flex; gap: 0.75rem; }
.header-btn {
  display: flex; align-items: center; gap: 0.75rem; padding: 0.6rem 1.5rem;
  background: #ffffff; border: 1.5px solid #f1f5f9; border-radius: 2rem;
  font-size: 0.85rem; font-weight: 700; color: #0f172a; cursor: pointer;
  transition: all 0.2s; box-shadow: 0 2px 8px rgba(0,0,0,0.02);
}
.header-btn svg { width: 16px; height: 16px; }
.header-btn .chevron { width: 14px; height: 14px; margin-left: 0.25rem; }
.notification-btn svg { color: #f59e0b; }

/* Tabs */
.status-tabs-row { display: flex; justify-content: flex-start; }
.status-tabs { display: flex; gap: 0.5rem; background: #f1f5f9; padding: 0.4rem; border-radius: 1rem; }
.tab-btn {
  position: relative;
  padding: 0.6rem 1.5rem;
  border-radius: 0.75rem;
  border: none;
  background: transparent;
  font-weight: 700;
  font-size: 0.85rem;
  color: #64748b;
  cursor: pointer;
  transition: all 0.2s;
}
.tab-btn.active { background: #ffffff; color: #0f172a; box-shadow: 0 2px 8px rgba(0,0,0,0.05); }
.tab-dot { display: inline-block; width: 6px; height: 6px; border-radius: 50%; background: #f59e0b; margin-left: 4px; vertical-align: middle; }

.pending-block { margin-bottom: 1rem; }
.pending-heading { font-size: 0.85rem; font-weight: 800; color: #92400e; margin: 0 0 0.25rem; }
.pending-sub { font-size: 0.78rem; color: #a16207; margin: 0 0 0.75rem; font-weight: 600; }
.pending-card { border-color: #fde68a; background: #fffbeb; }
.sessions-list.compact { gap: 0.75rem; }
.empty-sessions-msg { color: #94a3b8; font-weight: 600; font-size: 0.9rem; padding: 1rem 0; }

.status-tag.status-pending { background: #fef3c7; color: #92400e; }
.status-tag.status-confirmed { background: #dbeafe; color: #1e40af; }
.status-tag.status-done { background: #d1fae5; color: #047857; }
.status-tag.status-cancelled { background: #fee2e2; color: #b91c1c; }
.status-tag.status-pending-verify { background: #ffedd5; color: #c2410c; }
.act-val-success { color: #059669; }

/* Sessions List */
.sessions-list { display: flex; flex-direction: column; gap: 1.25rem; }
.session-card { background: #ffffff; border: 1px solid #f1f5f9; border-radius: 1.5rem; padding: 1.5rem 2rem; display: flex; align-items: center; justify-content: space-between; box-shadow: 0 4px 6px -1px rgba(0,0,0,0.02); }

.tutor-header { display: flex; align-items: center; gap: 1.25rem; flex: 1; }
.tutor-photo-wrap { flex-shrink: 0; }
.tutor-photo { width: 56px; height: 56px; border-radius: 50%; object-fit: cover; border: 2px solid #fff; box-shadow: 0 2px 8px rgba(0,0,0,0.10); }
.session-tier-badge {
  display: inline-block; font-size: 0.62rem; font-weight: 800;
  padding: 0.15rem 0.5rem; border-radius: 2rem; vertical-align: middle; margin-left: 0.4rem;
}
.tier-pro  { background: linear-gradient(135deg,#1e3a8a,#3b82f6); color:#fff; }
.tier-plus { background: #fef3c7; color: #92400e; border: 1px solid #fde68a; }
.tier-hidden { display: none; }
.tutor-info h3 { font-size: 1rem; font-weight: 800; color: #0f172a; display: flex; align-items: center; gap: 0.4rem; }
.verified-icon { width: 16px; height: 16px; }
.tutor-info p { font-size: 0.8rem; color: #64748b; font-weight: 700; }
.status-tag { background: #f0fdf4; color: #16a34a; font-size: 0.7rem; font-weight: 800; padding: 0.3rem 0.75rem; border-radius: 0.5rem; margin-left: 1rem; }

.session-details { display: flex; gap: 2rem; flex: 1; justify-content: center; }
.detail-item { display: flex; align-items: center; gap: 0.6rem; font-size: 0.85rem; font-weight: 700; color: #475569; }
.detail-item svg { width: 16px; height: 16px; color: #94a3b8; }

.btn-join { background: #ffffff; color: #0f172a; border: 1.5px solid #f1f5f9; padding: 0.75rem 1.5rem; border-radius: 0.75rem; font-weight: 800; font-size: 0.85rem; cursor: pointer; transition: all 0.2s; }
.btn-join:hover { background: #f8fafc; border-color: #e2e8f0; }

/* Bottom Grid */
.bottom-grid { display: grid; grid-template-columns: 1.8fr 1.2fr; gap: 2rem; }
.section-card { background: #ffffff; border: 1px solid #f1f5f9; border-radius: 1.5rem; padding: 2rem; box-shadow: 0 4px 6px -1px rgba(0,0,0,0.02); height: 100%; }
.section-card h3 { font-size: 1.1rem; font-weight: 800; color: #0f172a; margin-bottom: 0.5rem; }
.section-card p { font-size: 0.85rem; color: #94a3b8; font-weight: 600; margin-bottom: 2rem; }

/* Calendar */
.calendar-card { border: 1.5px solid #f1f5f9; border-radius: 1rem; padding: 1.5rem; margin-bottom: 1.5rem; }
.cal-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 1.5rem; }
.cal-nav { background: none; border: none; font-size: 1.2rem; color: #0f172a; cursor: pointer; font-weight: 800; }
.cal-title { font-weight: 800; color: #0f172a; font-size: 0.95rem; }
.cal-grid { display: grid; grid-template-columns: repeat(7, 1fr); gap: 0.4rem; text-align: center; }
.cal-day-label { font-size: 0.7rem; font-weight: 800; color: #94a3b8; padding-bottom: 0.5rem; }
.cal-day { font-size: 0.85rem; font-weight: 700; color: #475569; padding: 0.6rem; cursor: pointer; border-radius: 0.6rem; transition: all 0.2s; }
.cal-day:hover { background: #f8fafc; }
.cal-day.today { background: #0f172a; color: #ffffff; font-weight: 800; }
.cal-day.has_session { background: #f59e0b15; color: #f59e0b; font-weight: 800; border: 1.5px solid #f59e0b20; }

.slot-box { background: #fbfcfd; border: 1.5px solid #f1f5f9; border-radius: 1rem; padding: 1.5rem; text-align: center; }
.slot-box h4 { font-size: 0.9rem; font-weight: 800; color: #0f172a; margin-bottom: 0.25rem; }
.slot-box p { font-size: 0.75rem; color: #94a3b8; font-weight: 600; }

/* Activities */
.activity-list { display: flex; flex-direction: column; gap: 1.25rem; }
.activity-item { display: flex; align-items: center; gap: 1.25rem; padding: 1rem; background: #fbfcfd; border-radius: 1.25rem; border: 1px solid #f1f5f9; }
.act-icon-wrap { width: 50px; height: 50px; border-radius: 12px; display: flex; align-items: center; justify-content: center; }
.act-icon { width: 28px; height: 28px; object-fit: contain; }
.act-info { flex: 1; }
.act-info h4 { font-size: 0.9rem; font-weight: 800; color: #0f172a; margin-bottom: 0.2rem; }
.act-info p { font-size: 0.75rem; color: #64748b; font-weight: 600; }
.act-val { font-size: 0.9rem; font-weight: 800; color: #059669; }

@media (max-width: 1024px) {
  .session-card { flex-direction: column; align-items: stretch; gap: 1.25rem; }
  .session-details {
    justify-content: flex-start;
    width: 100%;
    flex-wrap: wrap;
    gap: 1rem 1.5rem;
  }
  .bottom-grid { grid-template-columns: 1fr; }
}

/* Phones and narrow tablets */
@media (max-width: 768px) {
  .student-sessions {
    gap: 1.25rem;
    max-width: 100%;
    overflow-x: hidden;
  }

  .page-header {
    flex-direction: column;
    align-items: stretch;
    gap: 1rem;
  }
  .header-text h1 { font-size: 1.35rem; line-height: 1.2; }
  .header-text p { font-size: 0.85rem; }

  .header-actions {
    flex-direction: column;
    width: 100%;
    gap: 0.5rem;
  }
  .header-btn {
    width: 100%;
    justify-content: center;
    padding: 0.65rem 1rem;
    font-size: 0.8rem;
    border-radius: 1rem;
  }
  .header-btn.date-btn span {
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
    min-width: 0;
  }

  .status-tabs-row {
    margin: 0;
    overflow-x: auto;
    -webkit-overflow-scrolling: touch;
    scrollbar-width: none;
    padding-bottom: 2px;
  }
  .status-tabs-row::-webkit-scrollbar { display: none; }
  .status-tabs {
    width: max-content;
    min-width: 100%;
    flex-wrap: nowrap;
    padding: 0.35rem;
    box-sizing: border-box;
  }
  .tab-btn {
    padding: 0.55rem 1rem;
    font-size: 0.78rem;
    white-space: nowrap;
  }

  .pending-heading { font-size: 0.8rem; }
  .pending-sub { font-size: 0.72rem; }

  .sessions-list { gap: 1rem; }

  .session-card {
    padding: 1rem 1.1rem;
    border-radius: 1.1rem;
    align-items: stretch;
  }

  /* Grid: avatar | name+subject; then status under text */
  .tutor-header {
    display: grid;
    grid-template-columns: 48px 1fr;
    grid-template-rows: auto auto;
    gap: 0.5rem 0.85rem;
    align-items: start;
    width: 100%;
  }
  .tutor-photo {
    grid-column: 1;
    grid-row: 1 / span 2;
    align-self: center;
    width: 48px;
    height: 48px;
  }
  .tutor-info {
    grid-column: 2;
    grid-row: 1;
    min-width: 0;
  }
  .tutor-info h3 {
    font-size: 0.92rem;
    flex-wrap: wrap;
    line-height: 1.3;
    word-break: break-word;
  }
  .tutor-info p {
    font-size: 0.75rem;
    word-break: break-word;
  }
  .status-tag {
    grid-column: 2;
    grid-row: 2;
    margin-left: 0;
    justify-self: start;
    align-self: start;
  }

  .session-details {
    flex-direction: column;
    align-items: flex-start;
    gap: 0.65rem;
    width: 100%;
  }
  .detail-item {
    font-size: 0.8rem;
    width: 100%;
  }

  .session-actions {
    width: 100%;
    margin-top: 0.25rem;
  }
  .btn-join {
    width: 100%;
    padding: 0.85rem 1rem;
    text-align: center;
  }

  .bottom-grid { gap: 1.25rem; }

  .section-card {
    padding: 1.25rem 1.1rem;
    border-radius: 1.1rem;
  }
  .section-card p { margin-bottom: 1.25rem; }

  .card-header {
    display: flex;
    flex-direction: column;
    align-items: flex-start;
    gap: 0.35rem;
  }
  .card-header .view-all { align-self: flex-start; }

  .calendar-card {
    padding: 1rem;
    overflow-x: auto;
  }
  .cal-grid {
    gap: 0.2rem;
    min-width: 260px;
  }
  .cal-day-label { font-size: 0.62rem; padding-bottom: 0.35rem; }
  .cal-day {
    font-size: 0.72rem;
    padding: 0.4rem 0.2rem;
  }
  .cal-title { font-size: 0.85rem; }

  .slot-box { padding: 1.1rem; }
  .slot-box h4 { font-size: 0.85rem; }

  .activity-item {
    flex-wrap: wrap;
    gap: 0.75rem;
    padding: 0.85rem;
  }
  .act-info {
    min-width: 0;
    flex: 1 1 140px;
  }
  .act-info h4 { font-size: 0.82rem; word-break: break-word; }
  .act-info p { font-size: 0.7rem; }
  .act-val {
    flex: 1 1 100%;
    text-align: right;
    font-size: 0.82rem;
  }
}
</style>
