<template>
  <div class="student-overview">
    <!-- Desktop greeting -->
    <div class="welcome-header desktop-only">
      <div class="welcome-text">
        <div class="greeting">
          <h1>Hello, {{ profile?.first_name || 'Student' }}!</h1>
          <span class="wave" aria-hidden="true">👋</span>
        </div>
        <p>Ready to learn something new today?</p>
      </div>
      <div class="header-actions">
        <div class="header-btn date-btn">
          <TuroIcon name="calendar" :size="18" class="hdr-ic-muted" />
          <span>{{ formattedDate }}</span>
          <TuroIcon name="chevronDown" :size="14" stroke-width="2.5" class="chevron hdr-ic-chevr" />
        </div>
        <button type="button" class="header-btn notification-btn" @click="openActivityPanel">
          <TuroIcon name="bell" :size="18" class="hdr-ic-warn" />
          <span>Notifications</span>
        </button>
      </div>
    </div>

    <!-- Mobile greeting -->
    <div class="mobile-greeting-row mobile-only">
      <div class="greeting-text">
        <h2>Hello, {{ profile?.first_name || 'Student' }}! <span class="wave" aria-hidden="true">👋</span></h2>
        <p>Ready to learn something new today?</p>
      </div>
      <button type="button" class="mobile-book-btn" @click="emit('navigate-discover')">
        <TuroIcon name="calendar" :size="14" stroke-width="2.5" />
        Book
      </button>
    </div>

    <!-- Stats grid -->
    <div class="stats-grid">
      <div class="stat-card c1" v-for="s in stats" :key="s.label" :class="s.cls">
        <div class="stat-icon-wrap" aria-hidden="true">
          <TuroIcon :name="s.icon" :size="22" class="stat-turo-ic" />
        </div>
        <div class="stat-info">
          <span class="stat-label">{{ s.label }}</span>
          <h2 class="stat-value">{{ s.value }}</h2>
          <span class="stat-trend" :class="s.trendClass">
            <span v-if="s.trendClass === 'trend-up'">▲</span>
            {{ s.delta }}
          </span>
        </div>
        <!-- Progress bar (Desktop style) -->
        <div class="stat-progress-container desktop-only">
          <div class="stat-progress-bar">
            <div class="fill" :style="{ width: s.progress + '%', background: s.progressColor }"></div>
          </div>
        </div>
      </div>
    </div>

    <!-- Mobile-only sections -->
    <div class="mobile-only mobile-sections">
      <!-- Upcoming Session -->
      <div class="section-group">
        <div class="section-header">
          <div class="section-title">Upcoming Session</div>
          <a class="section-link">View all →</a>
        </div>
        <div v-if="upcomingSession" class="session-card-mobile">
          <div class="session-avatar">{{ upcomingSession.initial }}</div>
          <div class="session-info">
            <div class="session-subject">{{ upcomingSession.subject }}</div>
            <div class="session-tutor">{{ upcomingSession.tutorName }}</div>
            <div class="session-time">
              <TuroIcon name="clock" :size="12" stroke-width="2" class="session-clock-ic" />
              {{ upcomingSession.dateLabel }}, {{ upcomingSession.timeLabel }} · {{ upcomingSession.durationLabel }}
            </div>
          </div>
          <button type="button" class="join-btn-mobile" @click="emit('navigate-discover')">{{ upcomingSession.cta }}</button>
        </div>
        <div v-else class="session-empty-mobile">
          <p>No upcoming sessions. Browse tutors to book your next lesson.</p>
          <button type="button" class="join-btn-mobile session-empty-btn" @click="emit('navigate-discover')">Find a tutor</button>
        </div>
      </div>

      <!-- Activity Chart (Mobile Specific Styling) -->
      <div class="content-card chart-card-mobile">
        <div class="section-header">
          <div class="section-title">Sessions Activity</div>
          <div class="chart-controls">
            <button class="chip" :class="{ active: chartRange === '3m' }" @click="chartRange = '3m'">3M</button>
            <button class="chip" :class="{ active: chartRange === '6m' }" @click="chartRange = '6m'">6M</button>
          </div>
        </div>
        <div class="chart-legend-mobile">
          <div class="legend-item"><div class="legend-dot" style="background:var(--color-accent-orange)"></div>Sessions</div>
          <div class="legend-item"><div class="legend-dot" style="background:var(--color-primary-dark)"></div>Hours</div>
        </div>
        <div class="chart-bars-mobile">
          <div class="bar-group-mobile" v-for="m in filteredActivity" :key="m.name">
            <div class="bar-pair">
              <div class="bar navy" :style="{ height: m.hours + 'px' }"></div>
              <div class="bar gold" :style="{ height: m.sessions + 'px' }"></div>
            </div>
            <div class="bar-label">{{ m.name }}</div>
          </div>
        </div>
      </div>

      <!-- My Tutors Scroll -->
      <div class="section-group">
        <div class="section-header">
          <div class="section-title">My Tutors</div>
          <a class="section-link">View all →</a>
        </div>
        <div class="horizontal-scroll tutors-scroll">
          <div class="tutor-card-mini" v-for="t in tutors" :key="t.id">
            <div class="tutor-av" :style="{ background: t.color || 'var(--color-primary-dark)' }">{{ t.name.charAt(0) }}</div>
            <div class="tutor-name">{{ t.name }}</div>
            <div class="tutor-subject">{{ t.subject }}</div>
            <div class="tutor-stars"><TuroIcon name="star" :size="12" filled class="mini-star" /> {{ t.rating }}</div>
            <div class="tutor-rate">₱450/hr</div>
            <button class="book-small-btn">Book Session</button>
          </div>
        </div>
      </div>

      <!-- Achievements Scroll -->
      <div class="section-group">
        <div class="section-header">
          <div class="section-title">Achievements</div>
          <a class="section-link">View all →</a>
        </div>
        <div class="horizontal-scroll achievements-scroll">
          <div class="achievement-card-mini" v-for="a in achievements" :key="a.id" :class="{ locked: !a.earned }">
            <span class="achievement-icon"><TuroIcon :name="a.icon" :size="26" class="achievement-ic" /></span>
            <div class="achievement-name">{{ a.title }}</div>
            <div class="achievement-status">{{ a.earned ? 'Earned' : 'Locked' }}</div>
          </div>
        </div>
      </div>

      <!-- Promo Card -->
      <div class="mobile-promo-card">
        <div class="promo-text">
          <h4>Earn while<br>you teach!</h4>
          <p>Join our community of tutors and inspire learners.</p>
        </div>
        <button class="promo-btn-mobile">Become a Tutor</button>
      </div>
    </div>

    <!-- Desktop grid -->
    <div class="dashboard-grid desktop-only">
      <!-- Left Column -->
      <div class="grid-left">
        <!-- Sessions Activity -->
        <div class="content-card">
          <div class="card-header">
            <h3>Sessions Activity</h3>
            <select class="time-filter">
              <option>Last 6 Months</option>
              <option>Last Year</option>
            </select>
          </div>
          <div class="chart-container">
            <div class="chart-bars">
              <div class="bar-group" v-for="month in activityData" :key="month.name">
                <div class="bars">
                  <div class="bar sessions" :style="{ height: month.sessions + '%' }"></div>
                  <div class="bar hours" :style="{ height: month.hours + '%' }"></div>
                </div>
                <span>{{ month.name }}</span>
              </div>
            </div>
            <div class="chart-legend">
              <span class="legend-item"><span class="dot sessions"></span> Sessions</span>
              <span class="legend-item"><span class="dot hours"></span> Hours</span>
            </div>
          </div>
        </div>

        <!-- My Tutors -->
        <div class="content-card">
          <div class="card-header">
            <h3>My Tutors</h3>
            <a href="#" class="view-all">View all →</a>
          </div>
          <div class="tutor-list">
            <div class="tutor-item" v-for="tutor in tutors" :key="tutor.id">
              <img src="/images/student_avatar.png" alt="Avatar" class="t-avatar" />
              <div class="tutor-info">
                <h4>{{ tutor.name }}</h4>
                <p>{{ tutor.subject }}</p>
              </div>
              <div class="tutor-meta">
                <span class="rating"><TuroIcon name="star" :size="14" filled class="rating-star" /> {{ tutor.rating }}</span>
                <span class="sessions">{{ tutor.sessions }} Sessions</span>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Right Column -->
      <div class="grid-right">
        <!-- Next upcoming session -->
        <div class="content-card next-session-desktop">
          <div class="card-header">
            <h3>Next session</h3>
            <button type="button" class="view-all" @click="emit('navigate-discover')">Book</button>
          </div>
          <div v-if="upcomingSession" class="next-session-body">
            <div class="next-avatar">{{ upcomingSession.initial }}</div>
            <div>
              <div class="next-subject">{{ upcomingSession.subject }}</div>
              <div class="next-tutor">{{ upcomingSession.tutorName }}</div>
              <div class="next-meta">
                {{ upcomingSession.dateLabel }} · {{ upcomingSession.timeLabel }} · {{ upcomingSession.durationLabel }}
              </div>
              <span class="next-status">{{ upcomingSession.status }}</span>
            </div>
          </div>
          <p v-else class="next-session-empty">No upcoming sessions yet. Explore tutors and book your first lesson.</p>
        </div>

        <!-- Achievements -->
        <div class="content-card achievements-card">
          <div class="card-header">
            <h3>Achievements</h3>
            <a href="#" class="view-all">View all →</a>
          </div>
          <div class="achievements-grid">
            <div class="achievement-badge" v-for="badge in achievements" :key="badge.id" :class="{ locked: !badge.earned }">
              <div class="badge-icon" :style="{ backgroundColor: badge.color }">
                <TuroIcon :name="badge.icon" :size="22" class="badge-ic-symbol" />
              </div>
              <strong>{{ badge.title }}</strong>
              <span>{{ badge.status }}</span>
            </div>
          </div>
        </div>

        <!-- Learning Progress -->
        <div class="content-card">
          <div class="card-header">
            <h3>Learning Progress</h3>
          </div>
          <div class="progress-list">
            <div class="progress-item" v-for="item in progress" :key="item.subject">
              <div class="progress-label">
                <span>{{ item.subject }}</span>
                <span>{{ item.value }}%</span>
              </div>
              <div class="progress-bar-bg">
                <div class="progress-bar-fill" :style="{ width: item.value + '%', backgroundColor: item.color }"></div>
              </div>
            </div>
          </div>
          <button class="btn-full-progress">View full progress →</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, watch, inject } from 'vue';
import { TuroIcon } from '../icons';
import { bookingService, paymentService } from '../../services/api';
import { OPEN_NOTIFICATIONS, REFRESH_TRIGGER } from '../../symbols/injectionKeys';

const props = defineProps({ profile: Object });
const emit = defineEmits(['navigate-discover']);

const openNotifications = inject(OPEN_NOTIFICATIONS, null);
const refreshTrigger = inject(REFRESH_TRIGGER, null);

function openActivityPanel() {
  openNotifications?.();
}

function sessionEndMs(b) {
  if (!b?.date) return null;
  const t = b.end_time ? String(b.end_time).slice(0, 8) : '23:59:59';
  const ms = new Date(`${b.date}T${t}`).getTime();
  return Number.isNaN(ms) ? null : ms;
}

function bookingDurationHours(b) {
  if (!b?.start_time || !b?.end_time) return 1;
  const parse = (t) => {
    const p = String(t).slice(0, 8).split(':').map(Number);
    return (p[0] || 0) * 60 + (p[1] || 0);
  };
  const m = parse(b.end_time) - parse(b.start_time);
  return Math.max(m / 60, 0.25);
}

function formatClock(timeVal) {
  if (!timeVal) return 'Time TBD';
  const parts = String(timeVal).slice(0, 8).split(':').map(Number);
  const h = parts[0];
  const mi = parts[1] ?? 0;
  if (Number.isNaN(h)) return 'Time TBD';
  const d = new Date();
  d.setHours(h, mi, 0, 0);
  return d.toLocaleTimeString('en-US', { hour: 'numeric', minute: '2-digit' });
}

const formattedDate = computed(() =>
  new Date().toLocaleDateString('en-US', { weekday: 'long', year: 'numeric', month: 'long', day: 'numeric' })
);

const chartRange  = ref('6m');
const loading     = ref(false);
const allBookings = ref([]);
const allPayments = ref([]);

const MONTHS = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'];

const stats = ref([
  { cls: 'bg-cream',    label: 'Sessions Completed', value: '0',  delta: 'None yet',   trendClass: 'trend-neutral', progress: 0, progressColor: '#f59e0b', icon: 'calendarCheck' },
  { cls: 'bg-blue',     label: 'Hours Learned',      value: '0',  delta: '—',          trendClass: 'trend-neutral', progress: 0, progressColor: '#1e3a8a', icon: 'clock' },
  { cls: 'bg-mint',     label: 'Active Tutors',      value: '0',  delta: 'No tutors',  trendClass: 'trend-neutral', progress: 0, progressColor: '#10b981', icon: 'users' },
  { cls: 'bg-lavender', label: 'Total Spent',        value: '₱0', delta: 'All time',   trendClass: 'trend-neutral', progress: 0, progressColor: '#0f172a', icon: 'creditCardThin' },
]);

const tutors         = ref([]);
const upcomingSession = ref(null);
const activityData   = ref(Array.from({ length: 6 }, (_, i) => ({ name: MONTHS[i], sessions: 0, hours: 0 })));
const achievements   = ref([
  { id: 1, title: 'First Session', status: 'Locked', earned: false, icon: 'graduationCap', color: '#f5f9ff' },
  { id: 2, title: '5 Sessions',    status: 'Locked', earned: false, icon: 'star', color: '#fffdf5' },
  { id: 3, title: '10 Sessions',   status: 'Locked', earned: false, icon: 'list', color: '#fff5f5' },
  { id: 4, title: '20 Sessions',   status: 'Locked', earned: false, icon: 'award', color: '#f6fdf9' },
]);

async function fetchStudentDashboardData() {
  const p = props.profile;
  if (!p?.user) return;
  loading.value = true;
  try {
    const [bRes, pRes] = await Promise.all([
      bookingService.getStudentBookings(p.user),
      paymentService.getStudentPayments(p.user),
    ]);

    const list = Array.isArray(bRes.data) ? bRes.data : (bRes.data?.results || []);
    const pmts = Array.isArray(pRes.data) ? pRes.data : (pRes.data?.results || []);
    allBookings.value = list;
    allPayments.value = pmts;

    const completedSessions = list.filter((b) => b.status === 'completed');
    const hoursLearned = completedSessions.reduce((s, b) => s + bookingDurationHours(b), 0);
    const uniqueIds    = [...new Set(list.map(b => b.tutor).filter(Boolean))];
    const totalSpent   = pmts.reduce((s, p) => s + parseFloat(p.amount || 0), 0);

    stats.value[0].value     = completedSessions.length.toString();
    stats.value[0].delta     = completedSessions.length > 0 ? completedSessions.length + ' sessions' : 'None yet';
    stats.value[0].progress  = Math.min(completedSessions.length * 10, 100);
    stats.value[0].trendClass = completedSessions.length > 0 ? 'trend-up' : 'trend-neutral';

    stats.value[1].value =
      hoursLearned >= 10 ? Math.round(hoursLearned).toString() : hoursLearned.toFixed(1);
    stats.value[1].delta =
      hoursLearned > 0 ? `~${hoursLearned.toFixed(1)} hr(s)` : 'Start learning!';
    stats.value[1].progress = Math.min(Math.round(hoursLearned * 10), 100);

    stats.value[2].value    = uniqueIds.length.toString();
    stats.value[2].delta    = uniqueIds.length > 0 ? uniqueIds.length + ' tutor(s)' : 'No tutors';
    stats.value[2].progress = Math.min(uniqueIds.length * 25, 100);

    stats.value[3].value    = '₱' + totalSpent.toFixed(2);
    stats.value[3].delta    = pmts.length + ' payment(s)';
    stats.value[3].progress = Math.min(pmts.length * 15, 100);

    tutors.value = uniqueIds.slice(0, 3).map((id) => {
      const b = list.find((x) => x.tutor === id);
      const sessionCount = list.filter((x) => x.tutor === id && x.status === 'completed').length;
      return {
        id,
        name: b?.tutor_name || 'Tutor',
        subject: b?.post_subject || b?.post_title || 'Session',
        rating: '4.9',
        sessions: sessionCount,
      };
    });

    const now = Date.now();
    const upcomingPool = list
      .filter((b) => {
        if (b.status === 'cancelled' || b.status === 'completed') return false;
        if (!b.date) return false;
        const end = sessionEndMs(b);
        if (end == null) return true;
        return end > now;
      })
      .sort((a, b) => {
        const c = String(a.date).localeCompare(String(b.date));
        if (c !== 0) return c;
        return String(a.start_time || '').localeCompare(String(b.start_time || ''));
      });
    const today = new Date().toISOString().split('T')[0];
    const next = upcomingPool[0];
    const nextDur = next ? bookingDurationHours(next) : 0;
    upcomingSession.value = next
      ? {
          tutorName: next.tutor_name || 'Tutor',
          subject: next.post_subject || next.post_title || 'Session',
          initial: (next.tutor_name || 'T').charAt(0).toUpperCase(),
          dateLabel:
            next.date === today
              ? 'Today'
              : new Date(next.date + 'T12:00:00').toLocaleDateString('en-US', {
                  month: 'short',
                  day: 'numeric',
                }),
          timeLabel: formatClock(next.start_time),
          durationLabel: `${Math.round(nextDur * 60)} min`,
          status: next.status,
          cta: next.status === 'confirmed' ? 'Join →' : 'Details →',
        }
      : null;

    const chartNow = new Date();
    activityData.value = Array.from({ length: 6 }, (_, i) => {
      const d = new Date(chartNow.getFullYear(), chartNow.getMonth() - 5 + i, 1);
      const key = d.getFullYear() + '-' + String(d.getMonth() + 1).padStart(2, '0');
      const monthBookings = list.filter((b) => b.date?.startsWith(key) && b.status === 'completed');
      const cnt = monthBookings.length;
      const monthHours = monthBookings.reduce((s, b) => s + bookingDurationHours(b), 0);
      return {
        name: MONTHS[d.getMonth()],
        sessions: Math.min(cnt * 20, 100),
        hours: Math.min(Math.round(monthHours * 25), 100),
      };
    });

    const c = completedSessions.length;
    achievements.value[0].earned = c >= 1;  achievements.value[0].status = c >= 1  ? 'Earned' : 'Locked';
    achievements.value[1].earned = c >= 5;  achievements.value[1].status = c >= 5  ? 'Earned' : c + '/5';
    achievements.value[2].earned = c >= 10; achievements.value[2].status = c >= 10 ? 'Earned' : c + '/10';
    achievements.value[3].earned = c >= 20; achievements.value[3].status = c >= 20 ? 'Earned' : c + '/20';

  } catch (err) {
    console.error('[StudentOverview]', err);
  } finally {
    loading.value = false;
  }
}

watch(() => props.profile, fetchStudentDashboardData, { immediate: true });
watch(refreshTrigger, fetchStudentDashboardData);

const filteredActivity = computed(() =>
  chartRange.value === '3m' ? activityData.value.slice(-3) : activityData.value
);

const progress = computed(() => {
  const map   = {};
  allBookings.value.forEach(b => { const s = b.post_subject || b.post_title || 'General'; map[s] = (map[s] || 0) + 1; });
  const total  = allBookings.value.length || 1;
  const colors = ['#1e293b', '#f59e0b', '#10b981'];
  return Object.entries(map).slice(0, 3).map(([subject, count], i) => ({ subject, value: Math.round((count / total) * 100), color: colors[i] }));
});
</script>


<style scoped>
.student-overview { width: 100%; display: flex; flex-direction: column; gap: 2.5rem; }

/* Desktop-only Helpers */
.desktop-only { display: block; }
.mobile-only { display: none; }

/* Desktop Header */
.welcome-header { display: flex; justify-content: space-between; align-items: center; }
.greeting { display: flex; align-items: center; gap: 0.75rem; margin-bottom: 0.25rem; }
.greeting h1 { font-family: var(--font-display); font-size: 1.8rem; font-weight: 800; color: #0f172a; }
.wave { font-size: 1.5rem; }
.welcome-text p { color: #64748b; font-weight: 600; font-size: 0.95rem; }

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
.hdr-ic-muted { color: #64748b; }
.hdr-ic-chevr { color: #94a3b8; }
.hdr-ic-warn { color: #f59e0b; }

/* Stats Grid */
.stats-grid { display: grid; grid-template-columns: repeat(4, 1fr); gap: 1.5rem; }
.stat-card {
  padding: 1.5rem 1.5rem 2.5rem; border-radius: 1.5rem; display: flex; flex-direction: column;
  position: relative; box-shadow: 0 4px 6px -1px rgba(0,0,0,0.02); border: 1px solid #f1f5f9;
  transition: transform 0.2s; background: #ffffff;
}
.stat-card:hover { transform: translateY(-4px); }

.bg-cream { background: #fffdf5; }
.bg-blue { background: #f5f9ff; }
.bg-mint { background: #f6fdf9; }
.bg-lavender { background: #f9f8ff; }

.stat-info .stat-label { font-size: 0.75rem; font-weight: 800; color: #64748b; text-transform: uppercase; display: block; margin-bottom: 0.5rem; }
.stat-info .stat-value { font-size: 2.2rem; font-weight: 800; color: #0f172a; margin: 0.5rem 0; }
.stat-info .stat-trend { font-size: 0.8rem; font-weight: 700; }
.trend-up { color: #10b981; }
.trend-neutral { color: #64748b; }

.stat-icon-wrap {
  position: absolute; top: 1.25rem; right: 1.25rem; width: 48px; height: 48px;
  background: #ffffff; border-radius: 14px; display: flex; align-items: center;
  justify-content: center; box-shadow: 0 4px 12px rgba(0,0,0,0.06);
}
.stat-turo-ic { color: #0f172a; }
.session-time { display: flex; align-items: center; gap: 4px; }
.session-clock-ic { color: #ffc85a; flex-shrink: 0; }
.tutor-stars { display: flex; align-items: center; gap: 4px; }
.mini-star { color: #f59e0b; }
.rating { display: inline-flex; align-items: center; gap: 4px; }
.rating-star { color: #f59e0b; }
.achievement-icon { display: flex; align-items: center; justify-content: center; }
.achievement-ic { color: #0f172a; }
.badge-icon {
  width: 50px;
  height: 50px;
  border-radius: 12px;
  margin-bottom: 0.25rem;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.04);
  display: flex;
  align-items: center;
  justify-content: center;
}
.badge-ic-symbol { color: #0f172a; }

.stat-progress-container { position: absolute; bottom: 1.5rem; left: 1.5rem; right: 1.5rem; }
.stat-progress-bar { width: 100%; height: 6px; background: rgba(0,0,0,0.05); border-radius: 10px; overflow: hidden; }
.stat-progress-bar .fill { height: 100%; border-radius: 10px; }

/* Desktop Grid */
.dashboard-grid { display: grid; grid-template-columns: 1.8fr 1.2fr; gap: 2rem; }
.content-card { background: #ffffff; border: 1px solid #f1f5f9; border-radius: 1.5rem; padding: 2rem; box-shadow: 0 4px 6px -1px rgba(0,0,0,0.02); }
.card-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 2rem; }
.card-header h3 { font-size: 1.1rem; font-weight: 800; color: #0f172a; }
.time-filter { background: #f8fafc; border: 1.5px solid #f1f5f9; padding: 0.4rem 0.75rem; border-radius: 0.75rem; font-weight: 700; color: #64748b; outline: none; }
.view-all { font-size: 0.85rem; font-weight: 700; color: #3b82f6; text-decoration: none; }

/* Chart Desktop */
.chart-container { height: 220px; display: flex; flex-direction: column; justify-content: flex-end; }
.chart-bars { display: flex; justify-content: space-between; align-items: flex-end; height: 100%; border-bottom: 2px solid #f1f5f9; padding-bottom: 1rem; }
.bar-group { display: flex; flex-direction: column; align-items: center; gap: 0.5rem; flex: 1; }
.bars { display: flex; gap: 4px; align-items: flex-end; height: 140px; }
.bar { width: 10px; border-radius: 4px 4px 0 0; }
.bar.sessions { background: #0f172a; }
.bar.hours { background: #f59e0b; }
.bar-group span { font-size: 0.7rem; font-weight: 800; color: #94a3b8; }
.chart-legend { display: flex; justify-content: center; gap: 2rem; margin-top: 1rem; }
.legend-item { display: flex; align-items: center; gap: 0.5rem; font-size: 0.75rem; font-weight: 800; color: #64748b; }
.dot { width: 10px; height: 10px; border-radius: 2px; }
.dot.sessions { background: #0f172a; }
.dot.hours { background: #f59e0b; }

/* Tutor List Desktop */
.tutor-list { display: flex; flex-direction: column; gap: 1rem; }
.tutor-item { display: flex; align-items: center; padding: 1.25rem; background: #fbfcfd; border-radius: 1.25rem; border: 1px solid #f1f5f9; }
.t-avatar { width: 50px; height: 50px; border-radius: 50%; object-fit: cover; margin-right: 1.25rem; border: 2px solid #fff; box-shadow: 0 2px 8px rgba(0,0,0,0.05); }
.tutor-info { flex: 1; }
.tutor-info h4 { font-size: 0.95rem; font-weight: 800; color: #0f172a; margin-bottom: 0.25rem; }
.tutor-info p { font-size: 0.8rem; color: #64748b; font-weight: 600; }
.tutor-meta { text-align: right; display: flex; flex-direction: column; gap: 0.25rem; }
.rating { font-size: 0.85rem; font-weight: 800; color: #f59e0b; }
.sessions { font-size: 0.75rem; font-weight: 700; color: #94a3b8; }

/* Achievements Desktop */
.achievements-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 1rem; }
.achievement-badge { text-align: center; padding: 1.5rem 1rem; border-radius: 1.25rem; display: flex; flex-direction: column; align-items: center; gap: 0.5rem; background: #fbfcfd; border: 1px solid #f1f5f9; }
.achievement-badge strong { font-size: 0.85rem; font-weight: 800; color: #0f172a; }
.achievement-badge span { font-size: 0.75rem; color: #64748b; font-weight: 700; }
.achievement-badge.locked { filter: grayscale(1); opacity: 0.5; }

.next-session-body { display: flex; gap: 1rem; align-items: flex-start; }
.next-avatar {
  width: 48px; height: 48px; border-radius: 50%;
  background: linear-gradient(135deg, #0f172a, #1e3a5f); color: #fff;
  font-weight: 800; font-size: 1.1rem; display: flex; align-items: center; justify-content: center;
  flex-shrink: 0;
}
.next-subject { font-size: 0.72rem; font-weight: 800; text-transform: uppercase; letter-spacing: 0.04em; color: #94a3b8; }
.next-tutor { font-size: 1rem; font-weight: 800; color: #0f172a; margin-top: 0.2rem; }
.next-meta { font-size: 0.8rem; color: #64748b; font-weight: 600; margin-top: 0.35rem; }
.next-status {
  display: inline-block; margin-top: 0.5rem; font-size: 0.72rem; font-weight: 800;
  text-transform: capitalize; padding: 0.2rem 0.5rem; border-radius: 6px;
  background: #fffbeb; color: #b45309; border: 1px solid #fde68a;
}
.next-session-empty { font-size: 0.88rem; color: #64748b; font-weight: 600; margin: 0; line-height: 1.5; }

/* Progress Desktop */
.progress-list { display: flex; flex-direction: column; gap: 1.25rem; margin-bottom: 1.5rem; }
.progress-item { display: flex; flex-direction: column; gap: 0.6rem; }
.progress-label { display: flex; justify-content: space-between; font-size: 0.85rem; font-weight: 700; color: #334155; }
.progress-bar-bg { height: 6px; background: #f1f5f9; border-radius: 10px; overflow: hidden; }
.progress-bar-fill { height: 100%; border-radius: 10px; }
.btn-full-progress { width: 100%; padding: 0.85rem; background: #fbfcfd; border: 1.5px solid #f1f5f9; border-radius: 1rem; color: #0f172a; font-weight: 800; font-size: 0.85rem; cursor: pointer; transition: all 0.2s; }

/* Mobile layout */
@media (max-width: 768px) {
  .desktop-only { display: none !important; }
  .mobile-only { display: block !important; }
  .student-overview { gap: 1.5rem; }

  /* Mobile Greeting */
  .mobile-greeting-row { display: flex; align-items: center; justify-content: space-between; }
  .greeting-text h2 { font-family: var(--font-display); font-size: 24px; font-weight: 800; color: #0f172a; line-height: 1.1; }
  .greeting-text p { font-size: 14px; color: #64748b; margin-top: 4px; font-weight: 500; }
  .mobile-book-btn {
    background: #0f172a; color: #ffffff; border: none; border-radius: 50px;
    padding: 10px 16px; font-size: 13px; font-weight: 700;
    display: flex; align-items: center; gap: 6px; box-shadow: 0 4px 12px rgba(15,22,41,0.1);
  }

  /* Stats Grid Mobile */
  .stats-grid { grid-template-columns: 1fr 1fr; gap: 10px; width: 100%; }
  .stat-card { padding: 14px; box-shadow: 0 2px 10px rgba(15,22,41,0.06); border-radius: 16px; border: none; }
  .stat-icon-wrap { position: static; width: 32px; height: 32px; background: #f4f6fb; border-radius: 8px; margin-bottom: 8px; box-shadow: none; }
  .stat-icon-wrap :deep(.stat-card-svg),
  .stat-icon-wrap :deep(svg) { width: 17px; height: 17px; }
  .stat-label { font-size: 9px; color: #a0aec0; letter-spacing: 0.5px; margin-bottom: 2px; font-weight: 700; }
  .stat-value { font-family: var(--font-display); font-size: 26px; font-weight: 800; margin: 0; line-height: 1; }
  .stat-trend { font-size: 10px; font-weight: 700; margin-top: 4px; display: block; }

  /* Mobile Sections Group */
  .mobile-sections { display: flex; flex-direction: column; gap: 24px; }
  .section-header { display: flex; align-items: center; justify-content: space-between; margin-bottom: 12px; }
  .section-title { font-family: var(--font-display); font-size: 18px; font-weight: 800; color: #0f172a; }
  .section-link { font-size: 13px; color: #f59e0b; font-weight: 700; }

  /* Upcoming Session Mobile */
  .session-card-mobile {
    background: linear-gradient(135deg, #0f172a, #1a2f5e); border-radius: 16px;
    padding: 16px; display: flex; align-items: center; gap: 12px; position: relative; overflow: hidden;
  }
  .session-avatar { width: 44px; height: 44px; border-radius: 50%; background: #ffc107; display: flex; align-items: center; justify-content: center; font-family: var(--font-display); font-size: 16px; font-weight: 800; color: #0f172a; border: 2px solid rgba(255,255,255,0.2); }
  .session-subject { font-size: 10px; color: rgba(255,255,255,0.5); font-weight: 700; text-transform: uppercase; letter-spacing: 0.5px; }
  .session-tutor { font-family: var(--font-display); font-size: 15px; font-weight: 700; color: #ffffff; margin: 1px 0; }
  .session-time { font-size: 11px; color: #ffc85a; display: flex; align-items: center; gap: 4px; font-weight: 600; }
  .join-btn-mobile { background: #ffc107; color: #0f172a; border: none; border-radius: 50px; padding: 6px 12px; font-size: 11px; font-weight: 800; }

  /* Activity Chart Mobile */
  .chart-card-mobile { border-radius: 18px; padding: 18px; border: none; box-shadow: 0 2px 12px rgba(15,22,41,0.08); }
  .chip { font-size: 12px; font-weight: 700; padding: 5px 12px; border-radius: 50px; border: 1.5px solid #e2e8f0; background: none; color: #4a5568; }
  .chip.active { background: #0f172a; color: #ffffff; border-color: #0f172a; }
  .chart-legend-mobile { display: flex; gap: 16px; margin: 14px 0 10px; }
  .chart-bars-mobile { display: flex; align-items: flex-end; gap: 8px; height: 100px; padding: 0 2px; }
  .bar-group-mobile { flex: 1; display: flex; align-items: flex-end; gap: 3px; flex-direction: column; justify-content: flex-end; height: 100%; }
  .bar-pair { display: flex; gap: 3px; align-items: flex-end; width: 100%; }
  .bar-label { text-align: center; font-size: 10px; color: #a0aec0; margin-top: 6px; width: 100%; font-weight: 700; }

  /* Horizontal Scrolls */
  .horizontal-scroll { display: flex; gap: 12px; overflow-x: auto; padding: 4px 0; scrollbar-width: none; }
  .horizontal-scroll::-webkit-scrollbar { display: none; }

  /* Tutor Card Mini */
  .tutor-card-mini { background: #ffffff; border-radius: 18px; padding: 16px; min-width: 150px; box-shadow: 0 2px 12px rgba(15,22,41,0.08); text-align: center; }
  .tutor-av { width: 52px; height: 52px; border-radius: 50%; margin: 0 auto 10px; display: flex; align-items: center; justify-content: center; font-family: var(--font-display); font-size: 18px; font-weight: 800; color: #ffffff; }
  .tutor-name { font-family: var(--font-display); font-size: 13px; font-weight: 800; color: #0f172a; }
  .tutor-subject { font-size: 11px; color: #a0aec0; margin: 2px 0; font-weight: 600; }
  .tutor-stars { font-size: 11px; color: #f59e0b; font-weight: 700; }
  .tutor-rate { font-size: 11px; color: #4a5568; margin-top: 8px; font-weight: 700; }
  .book-small-btn { margin-top: 10px; width: 100%; background: #f4f6fb; border: 1.5px solid #e2e8f0; border-radius: 50px; padding: 7px; font-size: 12px; font-weight: 700; color: #0f172a; }

  /* Achievement Card Mini */
  .achievement-card-mini { background: #ffffff; border-radius: 18px; padding: 18px 14px; min-width: 120px; text-align: center; box-shadow: 0 2px 12px rgba(15,22,41,0.08); flex-shrink: 0; position: relative; overflow: hidden; }
  .achievement-card-mini::before { content: ''; position: absolute; top: 0; left: 0; right: 0; height: 40px; background: linear-gradient(135deg, rgba(245,166,35,0.08), rgba(78,205,196,0.08)); }
  .achievement-icon { font-size: 30px; margin-bottom: 8px; display: block; position: relative; z-index: 1; }
  .achievement-name { font-family: var(--font-display); font-size: 13px; font-weight: 800; color: #0f172a; position: relative; z-index: 1; }
  .achievement-status { font-size: 11px; color: #a0aec0; margin-top: 3px; font-weight: 700; position: relative; z-index: 1; }
  .achievement-card-mini.locked { filter: grayscale(1); opacity: 0.5; }

  /* Promo Card Mobile */
  .mobile-promo-card {
    background: linear-gradient(135deg, #1a2340, #0f3460); border-radius: 18px;
    padding: 20px; display: flex; align-items: center; gap: 16px; box-shadow: 0 4px 20px rgba(15,22,41,0.1);
  }
  .promo-text h4 { font-family: var(--font-display); font-size: 15px; font-weight: 800; color: #ffffff; line-height: 1.2; }
  .promo-text p { font-size: 12px; color: rgba(255,255,255,0.5); margin-top: 4px; font-weight: 500; }
  .promo-btn-mobile { background: #ffc107; color: #0f172a; border: none; border-radius: 50px; padding: 9px 16px; font-size: 12px; font-weight: 800; white-space: nowrap; }

  .session-empty-mobile {
    background: #f8fafc; border-radius: 16px; padding: 18px;
    border: 1px solid #f1f5f9; text-align: center;
  }
  .session-empty-mobile p {
    margin: 0 0 12px 0; font-size: 14px; font-weight: 600; color: #64748b; line-height: 1.4;
  }
  .session-empty-btn { width: auto; margin: 0 auto; display: inline-block; }
}
</style>
