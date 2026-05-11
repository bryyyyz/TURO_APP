<template>
  <div class="overview-container">
    <!-- Desktop header -->
    <div class="welcome-header desktop-only">
      <div class="welcome-text">
        <div class="greeting">
          <h1>Good day, {{ profile?.first_name || 'Tutor' }}!</h1>
        </div>
        <p>Here's what's happening with your tutoring business today.</p>
      </div>
      <div class="header-actions">
        <div class="header-btn date-btn">
          <TuroIcon name="calendar" :size="18" class="hdr-ic-muted" />
          <span>{{ formattedDate }}</span>
          <TuroIcon name="chevronDown" :size="14" stroke-width="2.5" class="chevron hdr-ic-chevr" />
        </div>
      </div>
    </div>

    <!-- Mobile header -->
    <div class="mobile-greeting-row mobile-only">
      <div class="greeting-text">
        <h2>Good day, {{ profile?.first_name || 'Tutor' }}!</h2>
        <p>What are we teaching today?</p>
      </div>
      <button type="button" class="mobile-action-btn" @click="emit('navigate-post')">
        <TuroIcon name="plus" :size="14" stroke-width="2.5" />
        Post
      </button>
    </div>

    <!-- Stats grid -->
    <div class="stats-grid">
      <div class="stat-card" v-for="s in stats" :key="s.label" :class="s.cls">
        <div class="stat-icon-wrap" aria-hidden="true">
          <TuroIcon :name="s.icon" :size="22" class="stat-turo-ic" />
        </div>
        <div class="stat-info">
          <span class="stat-label">{{ s.label }}</span>
          <h2 class="stat-value">{{ s.value }}</h2>
          <span class="stat-trend" :class="s.trendClass">
            {{ s.delta }}
          </span>
        </div>
        <div class="stat-progress-container desktop-only">
          <div class="stat-progress-bar">
            <div class="progress-fill" :style="{ width: s.progress + '%', background: s.progressColor }"></div>
          </div>
        </div>
      </div>
    </div>

    <!-- Mobile-only sections -->
    <div class="mobile-only mobile-sections">
      <!-- Pending Requests -->
      <div class="section-group">
        <div class="section-header">
          <div class="section-title">Pending Requests</div>
          <span class="header-badge">{{ pendingRequests.length }} new</span>
        </div>
        <div class="horizontal-scroll">
          <div class="request-card-mobile" v-for="req in pendingRequests" :key="req.id">
            <div class="req-top">
              <div class="req-av">JD</div>
              <div class="req-meta">
                <strong>{{ req.name }}</strong>
                <span>{{ req.subject }}</span>
              </div>
            </div>
            <div class="req-time">{{ req.time }}</div>
            <div class="req-btns">
              <button type="button" class="btn-acc" @click="handleAccept(req.id)">Accept</button>
              <button type="button" class="btn-dec" @click="handleDecline(req.id)">Decline</button>
            </div>
          </div>
        </div>
      </div>

      <!-- Performance Banner -->
      <div class="mobile-performance-banner">
        <div class="perf-icon" aria-hidden="true"><TuroIcon name="award" :size="22" class="perf-ic" /></div>
        <div class="perf-text">
          <strong>Top Rated Tutor</strong>
          <span>Rank #3 · Mathematics</span>
        </div>
        <TuroIcon name="chevronRight" :size="16" stroke-width="2.5" class="perf-chev" />
      </div>

      <!-- Earnings Activity -->
      <div class="section-group">
        <div class="section-header">
          <div class="section-title">Earnings Activity</div>
          <a class="section-link">View all →</a>
        </div>
        <div class="earnings-list-mobile">
          <div class="earning-item-mobile" v-for="item in earnings" :key="item.id">
            <div class="item-icon" aria-hidden="true"><TuroIcon name="ledger" :size="20" class="earn-ic" /></div>
            <div class="item-info">
              <strong>{{ item.name }}</strong>
              <span>{{ item.subject }}</span>
            </div>
            <div class="item-amount">₱{{ item.amount }}</div>
          </div>
        </div>
      </div>
    </div>

    <!-- Desktop grid -->
    <div class="dashboard-rows desktop-only">
      <div class="dashboard-row">
        <!-- Earnings Table -->
        <div class="content-card">
          <div class="card-header">
            <h3>Total Earnings</h3>
            <a href="#" class="view-all">Full view →</a>
          </div>
          <div class="earnings-list">
            <div class="earning-item" v-for="e in earnings" :key="e.id">
              <div class="item-time">10:00 <span>AM</span></div>
              <div class="item-main">
                <strong>{{ e.name }}</strong>
                <span>{{ e.subject }} · Grade 10</span>
              </div>
              <div class="item-price">₱{{ e.amount }}</div>
              <div class="item-actions">
                <button class="btn-sm btn-outline">View</button>
                <button class="btn-sm btn-outline">Receipt</button>
              </div>
            </div>
          </div>
        </div>

        <!-- Performance Metrics -->
        <div class="content-card">
          <div class="card-header">
            <h3>Performance Metrics</h3>
          </div>
          <div class="metrics-list">
            <div class="metric-item" v-for="m in metrics" :key="m.label">
              <div class="metric-top">
                <span>{{ m.label }}</span>
                <strong>{{ m.value }}</strong>
              </div>
              <div class="metric-bar"><div class="bar-fill" :class="m.color" :style="{ width: m.progress + '%' }"></div></div>
            </div>
          </div>
          <div class="top-rated-banner">
            <div class="banner-icon" aria-hidden="true"><TuroIcon name="award" :size="22" class="banner-ic" /></div>
            <div class="banner-text">
              <strong>Top Rated Tutor</strong>
              <span>Rank #3 · Math Category</span>
            </div>
            <TuroIcon name="chevronRight" :size="16" stroke-width="2.5" class="banner-chevron" />
          </div>
        </div>
      </div>

      <div class="dashboard-row dashboard-row-full">
        <!-- Pending Requests -->
        <div class="content-card">
          <div class="card-header">
            <h3>Pending Requests</h3>
            <span class="header-badge">{{ pendingRequests.length }} awaiting</span>
          </div>
          <div class="requests-list">
            <div class="request-item" v-for="req in pendingRequests" :key="req.id">
              <img :src="req.avatar || '/images/student_avatar.png'" alt="Student" class="avatar-sq" />
              <div class="request-main">
                <div class="req-title-row">
                  <strong>{{ req.name }}</strong>
                  <span class="status-pill">Pending</span>
                </div>
                <span>{{ req.detail }}</span>
                <div class="request-btns">
                  <button class="btn-confirm" type="button" @click="handleAccept(req.id)"><TuroIcon name="check" :size="14" stroke-width="3" /> Accept</button>
                  <button class="btn-cancel" type="button" @click="handleDecline(req.id)"><TuroIcon name="x" :size="14" stroke-width="3" /> Decline</button>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, watch } from 'vue';
import { TuroIcon } from '../icons';
import { bookingService, paymentService } from '../../services/api';
import { useToast } from '../../composables/useToast';

const props = defineProps({ profile: Object });
const { showToast } = useToast();

const loading         = ref(false);
const pendingRequests = ref([]);
const earnings        = ref([]);

const stats = ref([
  { cls: 'card-earnings',       label: 'Total Earnings',   value: '₱0',   delta: 'All time',          trendClass: 'trend-up',      progress: 0,  progressColor: '#f59e0b', icon: 'ledger' },
  { cls: 'card-this-month',     label: 'This Month',       value: '₱0',   delta: 'Current month',     trendClass: 'trend-up',      progress: 0,  progressColor: '#1e3a8a', icon: 'calendar' },
  { cls: 'card-pending',        label: 'Pending Requests', value: '0',    delta: 'Awaiting response', trendClass: 'trend-warning',  progress: 30, progressColor: '#10b981', icon: 'bell' },
  { cls: 'card-sessions-billed',label: 'Sessions Billed',  value: '0',    delta: 'All time',          trendClass: 'trend-up',      progress: 80, progressColor: '#0f172a', icon: 'users' },
]);

const metrics = [
  { label: 'Student Satisfaction', value: '95%', progress: 95, color: 'bg-yellow' },
  { label: 'Session Completion',   value: '88%', progress: 88, color: 'bg-green'  },
  { label: 'Lesson Quality',       value: '92%', progress: 92, color: 'bg-purple' },
];

const emit = defineEmits(['navigate-post']);

const formattedDate = computed(() =>
  new Date().toLocaleDateString('en-US', { weekday: 'long', year: 'numeric', month: 'long', day: 'numeric' })
);

watch(() => props.profile, async (p) => {
  if (!p?.user) return;
  loading.value = true;
  try {
    const [bRes, pRes] = await Promise.all([
      bookingService.getTutorBookings(p.user),
      paymentService.getTutorPayments(p.user),
    ]);

    const bookings = Array.isArray(bRes.data) ? bRes.data : (bRes.data?.results || []);
    const payments = Array.isArray(pRes.data) ? pRes.data : (pRes.data?.results || []);

    // Pending requests
    pendingRequests.value = bookings
      .filter(b => b.status === 'pending')
      .map(b => {
        const datePart = b.date
          ? new Date(b.date + 'T12:00:00').toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric' })
          : '';
        const timePart = b.start_time ? String(b.start_time).slice(0, 5) : '';
        const detail = [b.post_subject || b.post_title || 'Tutoring Session', datePart, timePart].filter(Boolean).join(' • ');
        return {
          id:      b.id,
          name:    b.student_name || 'Student',
          avatar:  b.student_avatar_url || '/images/student_avatar.png',
          subject: b.post_subject || b.post_title || 'Tutoring Session',
          time:    datePart + (timePart ? ' · ' + timePart : ''),
          detail,
        };
      });

    // Recent earnings list
    earnings.value = payments.slice(0, 5).map(p => ({
      id:      p.id,
      name:    p.student_name || 'Student',
      subject: p.post_subject || p.post_title || 'Session',
      amount:  parseFloat(p.amount || 0).toFixed(2),
    }));

    // Stats
    const total = payments.reduce((s, p) => s + parseFloat(p.amount || 0), 0);
    const now   = new Date();
    const thisMonthKey = now.getFullYear() + '-' + String(now.getMonth() + 1).padStart(2, '0');
    const monthTotal   = payments
      .filter(p => p.booking_date?.startsWith(thisMonthKey))
      .reduce((s, p) => s + parseFloat(p.amount || 0), 0);

    stats.value[0].value    = '₱' + total.toFixed(2);
    stats.value[0].delta    = payments.length + ' payment(s)';
    stats.value[0].progress = Math.min(payments.length * 10, 100);

    stats.value[1].value    = '₱' + monthTotal.toFixed(2);
    stats.value[1].delta    = 'This month';
    stats.value[1].progress = total > 0 ? Math.min((monthTotal / total) * 100, 100) : 0;

    stats.value[2].value    = pendingRequests.value.length.toString();
    stats.value[2].delta    = pendingRequests.value.length > 0 ? 'Need response' : 'All clear';
    stats.value[2].progress = Math.min(pendingRequests.value.length * 20, 100);

    stats.value[3].value    = bookings.filter(b => b.status === 'confirmed').length.toString();
    stats.value[3].delta    = 'Confirmed sessions';
    stats.value[3].progress = Math.min(bookings.length * 5, 100);

  } catch (error) {
    console.error('[Overview] fetch error:', error);
  } finally {
    loading.value = false;
  }
}, { immediate: true });

const handleAccept = async (id) => {
  try {
    await bookingService.updateBooking(id, { status: 'confirmed' });
    showToast('Booking accepted!', 'success');
    pendingRequests.value = pendingRequests.value.filter(r => r.id !== id);
    stats.value[2].value = pendingRequests.value.length.toString();
    stats.value[2].delta = pendingRequests.value.length > 0 ? 'Need response' : 'All clear';
    stats.value[3].value = String(parseInt(stats.value[3].value, 10) + 1);
  } catch (error) {
    showToast('Failed to accept booking', 'error');
  }
};

const handleDecline = async (id) => {
  try {
    await bookingService.updateBooking(id, { status: 'cancelled' });
    showToast('Booking declined', 'info');
    pendingRequests.value = pendingRequests.value.filter(r => r.id !== id);
    stats.value[2].value = pendingRequests.value.length.toString();
    stats.value[2].delta = pendingRequests.value.length > 0 ? 'Need response' : 'All clear';
  } catch (error) {
    showToast('Failed to decline booking', 'error');
  }
};
</script>


<style scoped>
.overview-container { display: flex; flex-direction: column; gap: 2.5rem; }

/* Desktop-only Helpers */
.desktop-only { display: block; }
.mobile-only { display: none; }

/* Welcome Header Desktop */
.welcome-header { display: flex; justify-content: space-between; align-items: center; }
.greeting { display: flex; align-items: center; gap: 0.5rem; margin-bottom: 0.25rem; }
.greeting h1 { font-family: var(--font-display); font-size: 1.8rem; font-weight: 800; color: #0f172a; }
.wave { font-size: 1.5rem; }
.welcome-text p { color: #64748b; font-weight: 600; font-size: 0.95rem; }
.header-actions { display: flex; gap: 0.75rem; }
.header-btn {
  display: flex; align-items: center; gap: 0.75rem; padding: 0.6rem 1.5rem;
  background: #ffffff; border: 1.5px solid #f1f5f9; border-radius: 2rem;
  font-size: 0.85rem; font-weight: 700; color: #0f172a; cursor: pointer;
}
.header-btn svg { width: 16px; height: 16px; }
.hdr-ic-muted { color: #64748b; }
.hdr-ic-chevr { color: #94a3b8; }
.hdr-ic-warn { color: #f59e0b; }

/* Stats Grid */
.stats-grid { display: grid; grid-template-columns: repeat(4, 1fr); gap: 1.5rem; }
.stat-card {
  padding: 1.5rem 1.5rem 2.5rem; border-radius: 1.5rem; position: relative;
  border: 1px solid #f1f5f9; transition: transform 0.2s; background: #ffffff;
}
.card-earnings { background: #fffdf5; }
.card-this-month { background: #f5f9ff; }
.card-pending { background: #f6fdf9; }
.card-sessions-billed { background: #f9f8ff; }
.stat-label { font-size: 0.8rem; font-weight: 700; color: #64748b; display: block; margin-bottom: 0.75rem; }
.stat-value { font-size: 2.4rem; font-weight: 800; color: #0f172a; }
.stat-trend { font-size: 0.8rem; font-weight: 700; margin-top: 0.75rem; display: flex; align-items: center; gap: 0.25rem; }
.trend-up { color: #10b981; }
.trend-warning { color: #d97706; }
.stat-icon-wrap {
  position: absolute; top: 1.25rem; right: 1.25rem; width: 48px; height: 48px;
  background: #ffffff; border-radius: 14px; display: flex; align-items: center; justify-content: center;
  box-shadow: 0 4px 12px rgba(0,0,0,0.06);
}
.stat-turo-ic { color: #0f172a; }

/* Desktop Grid Rows */
.dashboard-rows { display: flex; flex-direction: column; gap: 2rem; }
.dashboard-row { display: grid; grid-template-columns: 1.8fr 1.2fr; gap: 2rem; }
.dashboard-row-full { grid-template-columns: 1fr; }
.content-card { background: #ffffff; border-radius: 1.5rem; padding: 1.75rem; border: 1px solid #f1f5f9; }
.card-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 1.5rem; }
.card-header h3 { font-size: 1.1rem; font-weight: 800; color: #0f172a; }
.view-all { font-size: 0.8rem; font-weight: 700; color: #64748b; text-decoration: none; }

/* Earnings List Desktop */
.earnings-list { display: flex; flex-direction: column; gap: 0.75rem; }
.earning-item { display: flex; align-items: center; padding: 1.25rem; background: #fdfdfd; border: 1px solid #f1f5f9; border-radius: 1rem; }
.item-time { width: 80px; font-size: 1.1rem; font-weight: 800; color: #f59e0b; text-align: center; }
.item-time span { font-size: 0.65rem; color: #94a3b8; display: block; }
.item-main { flex: 1; padding-left: 1rem; border-left: 2px solid #f1f5f9; }
.item-main strong { display: block; font-size: 1.05rem; line-height: 1.15; }
.item-main span { display: block; margin-top: 0.2rem; font-size: 0.86rem; color: #64748b; font-weight: 600; }
.item-price { font-size: 1.1rem; font-weight: 800; color: #10b981; margin: 0 1.5rem; }

/* Metrics Desktop */
.metrics-list { display: flex; flex-direction: column; gap: 1.25rem; margin-bottom: 1.5rem; }
.metric-item { display: flex; flex-direction: column; gap: 0.5rem; }
.metric-top { display: flex; justify-content: space-between; align-items: center; }
.metric-top span { font-size: 0.82rem; font-weight: 600; color: #64748b; }
.metric-top strong { font-size: 0.9rem; font-weight: 800; color: #0f172a; }
.metric-bar { width: 100%; height: 8px; background: #f1f5f9; border-radius: 4px; overflow: hidden; }
.bar-fill { height: 100%; border-radius: 4px; transition: width 0.6s ease; }
.bg-green { background: #10b981; }
.bg-blue { background: #3b82f6; }
.bg-yellow { background: #f59e0b; }
.bg-purple { background: #8b5cf6; }

/* Top Rated Banner */
.top-rated-banner {
  display: flex; align-items: center; gap: 0.85rem;
  background: linear-gradient(135deg, #07193f, #0d2859);
  border-radius: 1rem; padding: 1rem 1.25rem; color: #ffffff;
}
.banner-icon { flex-shrink: 0; display: flex; align-items: center; justify-content: center; }
.banner-ic { color: #ffffff; }
.banner-text { flex: 1; }
.banner-text strong { font-size: 0.9rem; font-weight: 800; display: block; }
.banner-text span { font-size: 0.72rem; opacity: 0.7; font-weight: 600; }
.banner-chevron { color: rgba(255,255,255,0.5); flex-shrink: 0; }
.perf-icon { display: flex; align-items: center; justify-content: center; flex-shrink: 0; font-size: 0; }
.perf-ic { color: #ffffff; }
.perf-chev { color: rgba(255,255,255,0.85); }
.item-icon { display: flex; align-items: center; justify-content: center; font-size: 0; }
.earn-ic { color: #f59e0b; }

/* Pending Requests Desktop */
.requests-list { display: flex; flex-direction: column; gap: 1rem; }
.request-item { display: flex; align-items: flex-start; gap: 1rem; padding: 1.1rem; background: #f8fafc; border: 1px solid #f1f5f9; border-radius: 1rem; }
.avatar-sq { width: 46px; height: 46px; border-radius: 10px; object-fit: cover; flex-shrink: 0; }
.request-main { flex: 1; min-width: 0; }
.req-title-row { display: flex; align-items: center; justify-content: space-between; margin-bottom: 0.3rem; }
.req-title-row strong { font-size: 0.95rem; font-weight: 800; color: #0f172a; }
.status-pill { background: #fffbeb; color: #d97706; font-size: 0.7rem; font-weight: 800; padding: 3px 8px; border-radius: 20px; border: 1px solid #fde68a; }
.request-main > span { font-size: 0.8rem; color: #64748b; font-weight: 600; display: block; margin-bottom: 0.75rem; }
.request-btns { display: flex; gap: 0.5rem; }
.btn-confirm {
  display: flex; align-items: center; gap: 0.35rem;
  background: #0f172a; color: #ffffff; border: none;
  padding: 0.45rem 1rem; border-radius: 0.5rem;
  font-size: 0.78rem; font-weight: 700; cursor: pointer;
}
.btn-confirm svg { width: 12px; height: 12px; }
.btn-cancel {
  display: flex; align-items: center; gap: 0.35rem;
  background: #fff0f0; color: #ef4444; border: 1px solid #fecaca;
  padding: 0.45rem 1rem; border-radius: 0.5rem;
  font-size: 0.78rem; font-weight: 700; cursor: pointer;
}
.btn-cancel svg { width: 12px; height: 12px; }

/* Earnings item action buttons */
.item-actions { display: flex; gap: 0.5rem; }
.btn-sm { padding: 0.4rem 0.85rem; border-radius: 0.5rem; font-size: 0.75rem; font-weight: 700; cursor: pointer; border: none; }
.btn-outline { background: #f1f5f9; color: #334155; border: 1px solid #e2e8f0; }
.btn-outline:hover { background: #e2e8f0; }

/* Mobile layout */
@media (max-width: 768px) {
  .desktop-only { display: none !important; }
  .mobile-only { display: block !important; }
  .overview-container { gap: 1.5rem; }

  /* Mobile Greeting */
  .mobile-greeting-row { display: flex; align-items: center; justify-content: space-between; }
  .greeting-text h2 { font-family: var(--font-display); font-size: 24px; font-weight: 800; color: #0f172a; line-height: 1.1; }
  .greeting-text p { font-size: 14px; color: #64748b; margin-top: 4px; font-weight: 500; }
  .mobile-action-btn {
    background: #0f172a; color: #ffffff; border: none; border-radius: 50px;
    padding: 10px 16px; font-size: 13px; font-weight: 700;
    display: flex; align-items: center; gap: 6px;
  }

  /* Card system: match mobile design used in tutor Students list */
  .stat-card,
  .request-card-mobile,
  .earning-item-mobile,
  .mobile-performance-banner {
    border: 1px solid #f1f5f9;
    border-radius: 1rem;
    box-shadow: 0 4px 10px rgba(15, 23, 42, 0.04);
    background: #ffffff;
  }

  /* Stats Grid Mobile */
  .stats-grid { grid-template-columns: 1fr 1fr; gap: 10px; width: 100%; }
  .stat-card { padding: 1rem 1.05rem; }
  .stat-icon-wrap { position: static; width: 32px; height: 32px; background: #f4f6fb; border-radius: 8px; margin-bottom: 8px; box-shadow: none; }
  .stat-turo-ic { width: 17px !important; height: 17px !important; }
  .stat-label { font-size: 9px; color: #a0aec0; letter-spacing: 0.5px; margin-bottom: 2px; text-transform: uppercase; font-weight: 700; }
  .stat-value { font-family: var(--font-display); font-size: 26px; font-weight: 800; margin: 0; line-height: 1; }
  .stat-trend { font-size: 10px; font-weight: 700; margin-top: 4px; }

  /* Mobile Sections Group */
  .mobile-sections { display: flex; flex-direction: column; gap: 24px; }
  .section-header { display: flex; align-items: center; justify-content: space-between; margin-bottom: 12px; }
  .section-title { font-family: var(--font-display); font-size: 18px; font-weight: 800; color: #0f172a; }
  .section-link { font-size: 13px; color: #f59e0b; font-weight: 700; }
  .header-badge { background: #fffbeb; color: #d97706; font-size: 11px; font-weight: 800; padding: 4px 8px; border-radius: 6px; }

  /* Horizontal Scroll */
  .horizontal-scroll { display: flex; gap: 12px; overflow-x: auto; padding: 4px 0; scrollbar-width: none; }
  .horizontal-scroll::-webkit-scrollbar { display: none; }

  /* Request Card Mobile */
  .request-card-mobile { padding: 1rem 1.05rem; min-width: 260px; }
  .req-top { display: flex; gap: 10px; align-items: center; margin-bottom: 10px; }
  .req-av { width: 38px; height: 38px; border-radius: 50%; background: #0f172a; color: #fff; display: flex; align-items: center; justify-content: center; font-weight: 800; font-size: 13px; }
  .req-meta strong { font-size: 14px; color: #0f172a; display: block; }
  .req-meta span { font-size: 11px; color: #a0aec0; font-weight: 600; }
  .req-time { font-size: 12px; color: #4a5568; font-weight: 700; margin-bottom: 12px; }
  .req-btns { display: flex; gap: 8px; }
  .btn-acc { flex: 1; background: #0f172a; color: #fff; border: none; border-radius: 8px; padding: 8px; font-size: 12px; font-weight: 700; }
  .btn-dec { flex: 1; background: #f4f6fb; color: #ef4444; border: none; border-radius: 8px; padding: 8px; font-size: 12px; font-weight: 700; }

  /* Performance Banner Mobile */
  .mobile-performance-banner {
    background: linear-gradient(135deg, #0f172a, #1a2f5e);
    padding: 1rem 1.05rem;
    display: flex;
    align-items: center;
    gap: 14px;
    color: #fff;
    box-shadow: 0 6px 16px rgba(15, 23, 42, 0.16);
    border-color: rgba(255, 255, 255, 0.12);
  }
  .perf-icon { font-size: 24px; }
  .perf-text { flex: 1; }
  .perf-text strong { font-size: 15px; display: block; }
  .perf-text span { font-size: 11px; color: rgba(255,255,255,0.6); font-weight: 600; }

  /* Earnings Mobile */
  .earnings-list-mobile { display: flex; flex-direction: column; gap: 10px; }
  .earning-item-mobile {
    display: flex; align-items: center; gap: 12px; background: #fff;
    padding: 1rem 1.05rem;
  }
  .item-icon { font-size: 20px; width: 40px; height: 40px; background: #fffbeb; display: flex; align-items: center; justify-content: center; border-radius: 10px; }
  .item-info { flex: 1; }
  .item-info strong { font-size: 14px; color: #0f172a; display: block; }
  .item-info span { font-size: 11px; color: #a0aec0; font-weight: 600; }
  .item-amount { font-size: 15px; font-weight: 800; color: #10b981; }
}
</style>
