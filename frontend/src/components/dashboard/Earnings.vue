<template>
  <div class="earnings-container">

    <!-- Desktop Header -->
    <div class="page-header desktop-only">
      <h1>Earnings</h1>
      <p>Track your revenue, payouts, and rate configuration.</p>
    </div>

    <!-- Stats Grid -->
    <div class="earnings-stats">
      <div class="e-card bg-cream">
        <div class="e-icon-wrap">
          <svg viewBox="0 0 24 24" fill="none" stroke="#0f172a" stroke-width="2"><path d="M12 1v22M17 5H9.5a3.5 3.5 0 0 0 0 7h5a3.5 3.5 0 0 1 0 7H6"/></svg>
        </div>
        <span class="e-label">Total Earnings</span>
        <h2 class="e-value">₱{{ totalEarnings }}</h2>
        <span class="e-trend trend-up">All time</span>
      </div>
      <div class="e-card bg-blue">
        <div class="e-icon-wrap">
          <svg viewBox="0 0 24 24" fill="none" stroke="#0f172a" stroke-width="2"><rect x="3" y="4" width="18" height="18" rx="2"/><line x1="16" y1="2" x2="16" y2="6"/><line x1="8" y1="2" x2="8" y2="6"/><line x1="3" y1="10" x2="21" y2="10"/></svg>
        </div>
        <span class="e-label">This Month</span>
        <h2 class="e-value">₱{{ thisMonthEarnings }}</h2>
        <span class="e-trend trend-up">Current month</span>
      </div>
      <div class="e-card bg-mint">
        <div class="e-icon-wrap">
          <svg viewBox="0 0 24 24" fill="none" stroke="#0f172a" stroke-width="2"><path d="M4 19.5A2.5 2.5 0 0 1 6.5 17H20"/><path d="M6.5 2H20v20H6.5A2.5 2.5 0 0 1 4 19.5v-15A2.5 2.5 0 0 1 6.5 2z"/></svg>
        </div>
        <span class="e-label">Pending Payout</span>
        <h2 class="e-value">₱{{ pendingPayout }}</h2>
        <span class="e-trend trend-neutral">Processing</span>
      </div>
      <div class="e-card bg-lavender">
        <div class="e-icon-wrap">
          <svg viewBox="0 0 24 24" fill="none" stroke="#0f172a" stroke-width="2"><path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M23 21v-2a4 4 0 0 0-3-3.87"/><path d="M16 3.13a4 4 0 0 1 0 7.75"/></svg>
        </div>
        <span class="e-label">Sessions Billed</span>
        <h2 class="e-value">{{ sessionsBilled }}</h2>
        <span class="e-trend trend-up">From payments</span>
      </div>
    </div>

    <!-- Chart + Rate Config -->
    <div class="revenue-row">
      <div class="chart-card">
        <div class="card-header">
          <h3>Monthly Revenue</h3>
          <select class="time-filter">
            <option>6 Months</option>
            <option>1 Year</option>
          </select>
        </div>
        <div class="chart-area">
          <svg viewBox="0 0 600 200" class="revenue-svg" preserveAspectRatio="none">
            <line x1="0" y1="170" x2="600" y2="170" stroke="#f1f5f9" />
            <line x1="0" y1="120" x2="600" y2="120" stroke="#f1f5f9" />
            <line x1="0" y1="70" x2="600" y2="70" stroke="#f1f5f9" />
            <path :d="bluePath" fill="none" stroke="#3b82f6" stroke-width="2.5" />
            <path :d="goldPath" fill="none" stroke="#f59e0b" stroke-width="2.5" />
            <circle v-for="p in bluePoints" :key="'b'+p.x" :cx="p.x" :cy="p.y" r="4" fill="#3b82f6"/>
            <circle v-for="p in goldPoints" :key="'g'+p.x" :cx="p.x" :cy="p.y" r="4" fill="#f59e0b"/>
          </svg>
          <div class="chart-labels">
            <span v-for="d in chartData" :key="d.label">{{ d.label }}</span>
          </div>
        </div>
        <div class="chart-legend">
          <div class="leg-item"><span class="leg-dot blue"></span> Earnings</div>
          <div class="leg-item"><span class="leg-dot gold"></span> Payouts</div>
        </div>
      </div>

      <div class="rate-card">
        <h3>Rate Config</h3>
        <div class="rate-content">
          <div class="rate-item">
            <span class="label">Hourly Rate</span>
            <span class="value gold">₱{{ hourlyRate }}/hr</span>
          </div>
          <div class="rate-item">
            <span class="label">Platform Fee</span>
            <span class="value orange">{{ platformFeePercent }}%</span>
          </div>
          <div class="rate-item total">
            <span class="label">Net Rate</span>
            <span class="value green">₱{{ netRate }}/hr</span>
          </div>
          <button class="btn-update">Update Rate</button>
        </div>
      </div>
    </div>

    <!-- Payout History -->
    <div class="payout-card">
      <div class="card-header">
        <h3>Payout History</h3>
      </div>

      <!-- Mobile: Card List -->
      <div class="payout-card-list mobile-only">
        <div class="payout-item" v-for="p in payoutList" :key="p.id">
          <img :src="p.avatar" alt="" class="mini-avatar" />
          <div class="payout-info">
            <strong>{{ p.student }}</strong>
            <span>{{ p.subject }} · {{ p.date }}</span>
          </div>
          <div class="payout-right">
            <span class="payout-amount">₱{{ p.amount }}</span>
            <span :class="['status-pill', p.status.toLowerCase()]">{{ p.status }}</span>
          </div>
        </div>
      </div>

      <!-- Desktop: Table -->
      <div class="table-container desktop-only">
        <table class="payout-table">
          <thead>
            <tr><th>STUDENT / SUBJECT</th><th>DATE</th><th>AMOUNT</th><th>STATUS</th></tr>
          </thead>
          <tbody>
            <tr v-for="p in payoutList" :key="p.id">
              <td>
                <div class="payout-cell">
                  <img :src="p.avatar" alt="" class="mini-avatar" />
                  <div class="cell-info"><strong>{{ p.student }}</strong><span>{{ p.subject }}</span></div>
                </div>
              </td>
              <td class="text-bold">{{ p.date }}</td>
              <td class="amount-cell">₱{{ p.amount }}</td>
              <td><span :class="['status-pill', p.status.toLowerCase()]">{{ p.status }}</span></td>
            </tr>
          </tbody>
        </table>
      </div>

      <div class="table-footer">
        <a href="#" class="view-all">View all payout history →</a>
      </div>
    </div>

  </div>
</template>

<script setup>
import { ref, computed, watch, inject } from 'vue';
import { paymentService, postService } from '../../services/api';
import { REFRESH_TRIGGER } from '../../symbols/injectionKeys';
import { formatCurrency } from '../../utils/format';

const props = defineProps({ profile: Object });

const payments = ref([]);
const posts    = ref([]);
const loading  = ref(false);
const refreshTrigger = inject(REFRESH_TRIGGER, null);

async function fetchEarnings() {
  const p = props.profile;
  if (p?.user) {
    loading.value = true;
    try {
      const [pmtRes, postRes] = await Promise.all([
        paymentService.getTutorPayments(p.user),
        postService.getAllPosts({ tutor_id: p.user })
      ]);
      payments.value = Array.isArray(pmtRes.data) ? pmtRes.data : (pmtRes.data.results || []);
      posts.value    = Array.isArray(postRes.data) ? postRes.data : (postRes.data.results || []);
    } catch (e) {
      console.error('Failed to fetch earnings', e);
    } finally {
      loading.value = false;
    }
  }
}

watch(() => props.profile, fetchEarnings, { immediate: true });
watch(refreshTrigger, fetchEarnings);

const totalEarnings = computed(() =>
  formatCurrency(
    payments.value
      .filter(p => p.status === 'completed')
      .reduce((s, p) => s + parseFloat(p.amount || 0), 0)
  )
);

const thisMonthEarnings = computed(() => {
  const now = new Date();
  const month = now.getMonth();
  const year = now.getFullYear();
  return formatCurrency(
    payments.value
      .filter(p => {
        if (p.status !== 'completed') return false;
        const d = new Date(p.paid_at || p.booking_date);
        return d.getMonth() === month && d.getFullYear() === year;
      })
      .reduce((s, p) => s + parseFloat(p.amount || 0), 0)
  );
});

const pendingPayout = computed(() =>
  formatCurrency(
    payments.value
      .filter(p => p.status === 'pending')
      .reduce((s, p) => s + parseFloat(p.amount || 0), 0)
  )
);

const sessionsBilled = computed(() => payments.value.filter(p => p.status === 'completed').length);

const hourlyRate = computed(() => {
  if (posts.value.length === 0) return 0;
  return parseFloat(posts.value[0].hourly_rate || 0);
});

const platformFeePercent = ref(10); // Standard 10%
const platformFeeAmount = computed(() => (hourlyRate.value * (platformFeePercent.value / 100)));
const netRate = computed(() => formatCurrency(hourlyRate.value - platformFeeAmount.value));

const MONTH_NAMES = ['JAN', 'FEB', 'MAR', 'APR', 'MAY', 'JUN', 'JUL', 'AUG', 'SEP', 'OCT', 'NOV', 'DEC'];

const chartData = computed(() => {
  const now = new Date();
  const last6Months = Array.from({ length: 6 }, (_, i) => {
    const d = new Date(now.getFullYear(), now.getMonth() - 5 + i, 1);
    return {
      month: d.getMonth(),
      year: d.getFullYear(),
      label: MONTH_NAMES[d.getMonth()],
      earnings: 0,
      payouts: 0
    };
  });

  payments.value.forEach(p => {
    const d = new Date(p.paid_at || p.booking_date);
    const m = d.getMonth();
    const y = d.getFullYear();
    const found = last6Months.find(x => x.month === m && x.year === y);
    if (found) {
      if (p.status === 'completed') found.earnings += parseFloat(p.amount || 0);
      else if (p.status === 'pending') found.payouts += parseFloat(p.amount || 0);
    }
  });

  return last6Months;
});

const bluePoints = computed(() => {
  const max = Math.max(...chartData.value.map(d => d.earnings), 1000);
  return chartData.value.map((d, i) => ({
    x: 50 + i * 100,
    y: 170 - (d.earnings / max) * 100
  }));
});

const goldPoints = computed(() => {
  const max = Math.max(...chartData.value.map(d => d.payouts), 1000);
  return chartData.value.map((d, i) => ({
    x: 50 + i * 100,
    y: 170 - (d.payouts / max) * 100
  }));
});

const bluePath = computed(() => {
  if (bluePoints.value.length < 2) return '';
  return `M ${bluePoints.value.map(p => `${p.x} ${p.y}`).join(' L ')}`;
});

const goldPath = computed(() => {
  if (goldPoints.value.length < 2) return '';
  return `M ${goldPoints.value.map(p => `${p.x} ${p.y}`).join(' L ')}`;
});

const payoutList = computed(() =>
  payments.value.map(p => ({
    id: p.id,
    student: p.student_name || 'Student',
    subject: p.post_subject || p.post_title || 'Session',
    date: p.booking_date
      ? new Date(p.booking_date + 'T00:00:00').toLocaleDateString('en-US', { month: 'short', day: 'numeric' })
      : (p.paid_at ? new Date(p.paid_at).toLocaleDateString('en-US', { month: 'short', day: 'numeric' }) : '—'),
    amount: formatCurrency(p.amount),
    status: p.status === 'completed' ? 'PAID' : p.status.toUpperCase(),
    avatar: p.student_avatar_url || '/images/student_avatar.png',
  }))
);
</script>

<style scoped>
.earnings-container { display: flex; flex-direction: column; gap: 1.5rem; }

.desktop-only { display: block; }
.mobile-only { display: none; }

.page-header h1 { font-family: var(--font-display); font-size: 2rem; font-weight: 800; color: #0f172a; }
.page-header p { color: #64748b; font-size: 0.95rem; margin-top: 0.25rem; }

/* Stats */
.earnings-stats { display: grid; grid-template-columns: repeat(4, 1fr); gap: 1.25rem; }
.e-card { padding: 1.25rem 1.25rem 2rem; border-radius: 1.25rem; display: flex; flex-direction: column; position: relative; border: 1px solid #f1f5f9; transition: transform 0.2s; }
.e-card:hover { transform: translateY(-3px); }
.bg-cream { background: #fffdf5; }
.bg-blue { background: #f5f9ff; }
.bg-mint { background: #f6fdf9; }
.bg-lavender { background: #f9f8ff; }
.e-icon-wrap { width: 40px; height: 40px; background: #fff; border-radius: 12px; display: flex; align-items: center; justify-content: center; box-shadow: 0 2px 8px rgba(0,0,0,0.05); margin-bottom: 0.75rem; }
.e-icon-wrap svg { width: 18px; height: 18px; }
.e-label { font-size: 0.7rem; font-weight: 800; color: #94a3b8; text-transform: uppercase; }
.e-value { font-family: var(--font-display); font-size: 2.4rem; font-weight: 800; color: #0f172a; margin: 0.25rem 0; }
.e-trend { font-size: 0.72rem; font-weight: 700; }
.trend-up { color: #10b981; }
.trend-neutral { color: #d97706; }

/* Revenue Row */
.revenue-row { display: grid; grid-template-columns: 2fr 1fr; gap: 1.5rem; }
.chart-card, .rate-card { background: #fff; border-radius: 1.25rem; padding: 1.5rem; border: 1px solid #f1f5f9; }
.card-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 1.5rem; }
.card-header h3 { font-size: 1rem; font-weight: 800; color: #0f172a; }
.time-filter { background: #f8fafc; border: 1.5px solid #f1f5f9; padding: 0.35rem 0.65rem; border-radius: 0.65rem; font-weight: 700; color: #64748b; outline: none; font-size: 0.82rem; }
.chart-area { padding-bottom: 1rem; }
.revenue-svg { width: 100%; height: 160px; display: block; }
.chart-labels { display: flex; justify-content: space-between; padding: 0.5rem 0 0; font-size: 0.68rem; font-weight: 800; color: #94a3b8; }
.chart-legend { display: flex; gap: 1.5rem; justify-content: center; margin-top: 0.75rem; }
.leg-item { display: flex; align-items: center; gap: 0.4rem; font-size: 0.78rem; font-weight: 700; color: #64748b; }
.leg-dot { width: 8px; height: 8px; border-radius: 50%; }
.leg-dot.blue { background: #3b82f6; }
.leg-dot.gold { background: #f59e0b; }

.rate-card h3 { font-size: 1rem; font-weight: 800; color: #0f172a; margin-bottom: 1.25rem; }
.rate-content { display: flex; flex-direction: column; gap: 0.75rem; }
.rate-item { display: flex; flex-direction: column; gap: 0.3rem; padding: 1rem; background: #fdfdfd; border: 1px solid #f8fafc; border-radius: 0.85rem; }
.rate-item .label { font-size: 0.8rem; font-weight: 700; color: #64748b; }
.rate-item .value { font-size: 1.15rem; font-weight: 800; }
.value.gold { color: #f59e0b; }
.value.orange { color: #d97706; }
.value.green { color: #10b981; }
.rate-item.total { background: #fffcf0; border-color: #fef3c7; }
.btn-update { background: #fffcf0; border: 1.5px solid #fef3c7; color: #d97706; padding: 0.75rem; border-radius: 0.75rem; font-weight: 800; font-size: 0.85rem; cursor: pointer; width: 100%; margin-top: 0.25rem; }

/* Payout */
.payout-card { background: #fff; border-radius: 1.25rem; padding: 1.5rem; border: 1px solid #f1f5f9; }
.payout-card h3 { font-size: 1rem; font-weight: 800; color: #0f172a; margin-bottom: 1.25rem; }
.table-container { overflow-x: auto; }
.payout-table { width: 100%; border-collapse: collapse; }
.payout-table th { text-align: left; padding: 1rem; font-size: 0.72rem; font-weight: 800; color: #94a3b8; border-bottom: 1px solid #f1f5f9; }
.payout-table td { padding: 1.1rem 1rem; border-bottom: 1px solid #f8fafc; }
.payout-cell { display: flex; align-items: center; gap: 0.85rem; }
.mini-avatar { width: 38px; height: 38px; border-radius: 50%; object-fit: cover; flex-shrink: 0; }
.cell-info { display: flex; flex-direction: column; }
.cell-info strong { font-size: 0.88rem; color: #0f172a; font-weight: 800; }
.cell-info span { font-size: 0.72rem; color: #94a3b8; font-weight: 600; }
.text-bold { font-weight: 700; color: #475569; font-size: 0.82rem; }
.amount-cell { font-size: 1rem; font-weight: 800; color: #f59e0b; }
.status-pill { padding: 0.25rem 0.65rem; border-radius: 0.45rem; font-size: 0.65rem; font-weight: 800; display: inline-block; }
.status-pill.paid { background: #ecfdf5; color: #059669; }
.status-pill.pending { background: #fffbeb; color: #d97706; }
.table-footer { margin-top: 1.25rem; text-align: center; }
.view-all { font-size: 0.82rem; font-weight: 700; color: #3b82f6; text-decoration: none; }

/* ── MOBILE ── */
@media (max-width: 768px) {
  .desktop-only { display: none !important; }
  .mobile-only { display: flex !important; }

  .earnings-stats { grid-template-columns: 1fr 1fr; gap: 0.75rem; }
  .e-card { padding: 1rem; border-radius: 1rem; }
  .e-icon-wrap { width: 32px; height: 32px; border-radius: 10px; margin-bottom: 0.5rem; }
  .e-icon-wrap svg { width: 14px; height: 14px; }
  .e-label { font-size: 0.62rem; }
  .e-value { font-size: 26px; font-weight: 800; }
  .e-trend { font-size: 0.62rem; }

  .revenue-row { grid-template-columns: 1fr; gap: 1rem; }
  .chart-card, .rate-card { border-radius: 1rem; padding: 1.1rem; }
  .revenue-svg { height: 120px; }

  .rate-content { gap: 0.5rem; }
  .rate-item { padding: 0.75rem; border-radius: 0.75rem; }
  .rate-item .value { font-size: 1rem; }

  .payout-card { border-radius: 1rem; padding: 1.1rem; }
  .payout-card-list { flex-direction: column; gap: 0.65rem; }
  .payout-item { display: flex; align-items: center; gap: 0.75rem; padding: 0.85rem; background: #f8fafc; border-radius: 0.85rem; }
  .payout-info { flex: 1; min-width: 0; }
  .payout-info strong { font-size: 0.82rem; font-weight: 800; color: #0f172a; display: block; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
  .payout-info span { font-size: 0.68rem; color: #94a3b8; font-weight: 600; }
  .payout-right { display: flex; flex-direction: column; align-items: flex-end; gap: 0.25rem; flex-shrink: 0; }
  .payout-amount { font-size: 0.95rem; font-weight: 800; color: #f59e0b; }
}
</style>
