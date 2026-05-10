<template>
  <div class="student-payments">

    <!-- Desktop Header -->
    <div class="page-header desktop-only">
      <h1>Payments</h1>
      <p>Manage your billing, payment methods, and history.</p>
    </div>

    <!-- Stats Grid -->
    <div class="stats-grid">
      <div class="stat-card bg-cream">
        <div class="stat-icon-wrap">
          <svg viewBox="0 0 24 24" fill="none" stroke="#0f172a" stroke-width="2"><rect x="2" y="5" width="20" height="14" rx="2"/><line x1="2" y1="10" x2="22" y2="10"/></svg>
        </div>
        <span class="stat-label">This Month</span>
        <h2 class="stat-value">₱{{ totalSpent }}</h2>
        <span class="stat-trend trend-up">All time</span>
      </div>
      <div class="stat-card bg-blue">
        <div class="stat-icon-wrap">
          <svg viewBox="0 0 24 24" fill="none" stroke="#0f172a" stroke-width="2"><path d="M16 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"/><circle cx="8.5" cy="7" r="4"/><polyline points="17 11 19 13 23 9"/></svg>
        </div>
        <span class="stat-label">Sessions</span>
        <h2 class="stat-value">{{ sessionCount }}</h2>
        <span class="stat-trend trend-up">Total booked</span>
      </div>
      <div class="stat-card bg-mint">
        <div class="stat-icon-wrap">
          <svg viewBox="0 0 24 24" fill="none" stroke="#0f172a" stroke-width="2"><path d="M3 12a9 9 0 1 0 9-9 9.75 9.75 0 0 0-6.74 2.74L3 8"/><path d="M3 3v5h5"/></svg>
        </div>
        <span class="stat-label">Refunds</span>
        <h2 class="stat-value">₱0</h2>
        <span class="stat-trend trend-neutral">None active</span>
      </div>
      <div class="stat-card bg-lavender">
        <div class="stat-icon-wrap">
          <svg viewBox="0 0 24 24" fill="none" stroke="#0f172a" stroke-width="2"><path d="M12 1v22M17 5H9.5a3.5 3.5 0 0 0 0 7h5a3.5 3.5 0 0 1 0 7H6"/></svg>
        </div>
        <span class="stat-label">Total Spent</span>
        <h2 class="stat-value">₱{{ totalSpent }}</h2>
        <span class="stat-trend">All time</span>
      </div>
    </div>

    <!-- Payment Grid: methods + billing -->
    <div class="payment-grid">
      <div class="card methods-card">
        <div class="card-header">
          <h3>Payment Methods</h3>
          <button class="btn-action">+ Add</button>
        </div>
        <div class="methods-list">
          <div class="method-item">
            <div class="card-brand visa">VISA</div>
            <div class="method-info">
              <strong>•••• 4242</strong>
              <span>Expires 06/27 · Jayson Dela Cruz</span>
            </div>
            <span class="badge-default">Default</span>
          </div>
          <div class="method-item">
            <div class="card-brand gcash">GCash</div>
            <div class="method-info">
              <strong>+63 991 ••89</strong>
              <span>GCash Wallet · Linked</span>
            </div>
            <button class="btn-text">Manage</button>
          </div>
        </div>
      </div>

      <div class="card billing-card">
        <div class="card-header">
          <h3>Billing Info</h3>
          <button class="btn-action">Edit</button>
        </div>
        <div class="billing-details">
          <div class="detail-row"><span>Name</span><strong>Jayson Dela Cruz</strong></div>
          <div class="detail-row"><span>Email</span><strong>jayson@example.com</strong></div>
          <div class="detail-row"><span>Country</span><strong>Philippines</strong></div>
          <div class="detail-row"><span>Currency</span><strong>₱ PHP</strong></div>
        </div>
      </div>
    </div>

    <!-- Transaction History -->
    <div class="card history-card">
      <div class="card-header">
        <div>
          <h3>Transactions</h3>
          <p>All billing activity</p>
        </div>
      </div>

      <!-- Mobile: Card list -->
      <div class="tx-card-list mobile-only">
        <div class="tx-card" v-for="tx in transactions" :key="tx.id">
          <div class="tx-icon" :style="{ background: tx.color + '18', color: tx.color }">{{ tx.initial }}</div>
          <div class="tx-details">
            <strong>{{ tx.title }}</strong>
            <span>{{ tx.txnId }} · {{ tx.date }}</span>
          </div>
          <div class="tx-right">
            <span class="amount">₱{{ tx.amount }}</span>
            <span :class="['status-pill', tx.status.toLowerCase()]">{{ tx.status }}</span>
          </div>
        </div>
      </div>

      <!-- Desktop: Table -->
      <div class="table-container desktop-only">
        <table class="history-table">
          <thead>
            <tr><th>DESCRIPTION</th><th>DATE</th><th>STATUS</th><th>AMOUNT</th></tr>
          </thead>
          <tbody>
            <tr v-for="tx in transactions" :key="tx.id">
              <td>
                <div class="tx-desc">
                  <div class="tx-icon" :style="{ background: tx.color + '18', color: tx.color }">{{ tx.initial }}</div>
                  <div class="tx-info"><strong>{{ tx.title }}</strong><span>{{ tx.txnId }}</span></div>
                </div>
              </td>
              <td class="text-bold">{{ tx.date }}</td>
              <td><span :class="['status-pill', tx.status.toLowerCase()]">{{ tx.status }}</span></td>
              <td class="amount-cell">₱{{ tx.amount }}</td>
            </tr>
          </tbody>
        </table>
      </div>

      <div class="table-footer">
        <button class="btn-view-all">View all history →</button>
      </div>
    </div>

  </div>
</template>

<script setup>
import { ref, computed, watch } from 'vue';
import { paymentService } from '../../services/api';

const props = defineProps({ profile: Object });

const payments = ref([]);
const loading = ref(false);

watch(() => props.profile, async (p) => {
  if (p?.user) {
    loading.value = true;
    try {
      const { data } = await paymentService.getStudentPayments(p.user);
      payments.value = Array.isArray(data) ? data : (data.results || []);
    } catch (e) {
      console.error('Failed to fetch payments', e);
    } finally {
      loading.value = false;
    }
  }
}, { immediate: true });

const totalSpent = computed(() =>
  payments.value.reduce((s, p) => s + parseFloat(p.amount || 0), 0).toFixed(2)
);

const sessionCount = computed(() => payments.value.length);

const transactions = computed(() =>
  payments.value.map(p => ({
    id: p.id,
    title: `${p.post_subject || p.post_title || 'Session'} - ${p.tutor_name || 'Tutor'}`,
    txnId: p.transaction_id || `TXN-${p.id}`,
    date: p.booking_date
      ? new Date(p.booking_date + 'T00:00:00').toLocaleDateString('en-US', { month: 'short', day: 'numeric' })
      : '—',
    status: p.status === 'completed' ? 'PAID' : p.status?.toUpperCase() || 'PAID',
    amount: parseFloat(p.amount).toFixed(2),
    initial: (p.post_subject || 'S').charAt(0),
    color: '#1e3a8a',
  }))
);
</script>

<style scoped>
.student-payments { width: 100%; display: flex; flex-direction: column; gap: 1.5rem; }

/* Helpers */
.desktop-only { display: block; }
.mobile-only { display: none; }

/* Desktop Header */
.page-header h1 { font-family: var(--font-display); font-size: 2rem; font-weight: 800; color: #0f172a; }
.page-header p { color: #64748b; font-size: 0.95rem; margin-top: 0.25rem; }

/* Stats Grid */
.stats-grid { display: grid; grid-template-columns: repeat(4, 1fr); gap: 1.25rem; }
.stat-card { padding: 1.25rem 1.25rem 2rem; border-radius: 1.25rem; display: flex; flex-direction: column; position: relative; border: 1px solid #f1f5f9; transition: transform 0.2s; }
.stat-card:hover { transform: translateY(-3px); }
.bg-cream { background: #fffdf5; }
.bg-blue { background: #f5f9ff; }
.bg-mint { background: #f6fdf9; }
.bg-lavender { background: #f9f8ff; }
.stat-icon-wrap { width: 42px; height: 42px; background: #fff; border-radius: 12px; display: flex; align-items: center; justify-content: center; box-shadow: 0 2px 8px rgba(0,0,0,0.05); margin-bottom: 0.75rem; }
.stat-icon-wrap svg { width: 20px; height: 20px; }
.stat-label { font-size: 0.72rem; font-weight: 800; color: #94a3b8; text-transform: uppercase; margin-bottom: 0.3rem; }
.stat-value { font-family: var(--font-display); font-size: 1.75rem; font-weight: 800; color: #0f172a; margin: 0; }
.stat-trend { font-size: 0.75rem; font-weight: 700; margin-top: 0.25rem; }
.trend-up { color: #10b981; }
.trend-neutral { color: #94a3b8; }

/* Cards */
.card { background: #fff; border: 1px solid #f1f5f9; border-radius: 1.25rem; padding: 1.5rem; box-shadow: 0 2px 8px rgba(0,0,0,0.02); }
.card-header { display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 1.5rem; }
.card-header h3 { font-size: 1rem; font-weight: 800; color: #0f172a; }
.card-header p { font-size: 0.8rem; color: #94a3b8; margin-top: 0.2rem; }
.btn-action { background: #f8fafc; border: 1.5px solid #f1f5f9; padding: 0.45rem 0.85rem; border-radius: 0.65rem; font-weight: 800; font-size: 0.78rem; color: #0f172a; cursor: pointer; }

/* Payment Grid */
.payment-grid { display: grid; grid-template-columns: 1.5fr 1fr; gap: 1.25rem; }
.methods-list { display: flex; flex-direction: column; gap: 0.85rem; }
.method-item { display: flex; align-items: center; padding: 1rem; background: #fbfcfd; border: 1px solid #f1f5f9; border-radius: 1rem; gap: 1rem; }
.card-brand { width: 52px; height: 32px; border-radius: 5px; display: flex; align-items: center; justify-content: center; font-weight: 900; font-size: 0.72rem; color: #fff; flex-shrink: 0; }
.card-brand.visa { background: #1a1f71; }
.card-brand.gcash { background: #3b82f6; }
.method-info { flex: 1; }
.method-info strong { font-size: 0.9rem; color: #0f172a; font-weight: 800; display: block; }
.method-info span { font-size: 0.72rem; color: #94a3b8; font-weight: 600; }
.badge-default { background: #f0fdf4; color: #16a34a; font-size: 0.65rem; font-weight: 800; padding: 0.25rem 0.6rem; border-radius: 0.4rem; white-space: nowrap; }
.btn-text { background: none; border: none; color: #3b82f6; font-weight: 800; font-size: 0.78rem; cursor: pointer; }

.billing-details { display: flex; flex-direction: column; gap: 1rem; }
.detail-row { display: flex; justify-content: space-between; align-items: center; padding-bottom: 0.85rem; border-bottom: 1px solid #f8fafc; }
.detail-row span { font-size: 0.72rem; font-weight: 800; color: #94a3b8; text-transform: uppercase; }
.detail-row strong { font-size: 0.88rem; font-weight: 800; color: #0f172a; }

/* History Table (Desktop) */
.table-container { overflow-x: auto; }
.history-table { width: 100%; border-collapse: collapse; }
.history-table th { text-align: left; padding: 1rem; font-size: 0.72rem; font-weight: 800; color: #94a3b8; border-bottom: 1px solid #f1f5f9; }
.history-table td { padding: 1.25rem 1rem; border-bottom: 1px solid #f8fafc; }
.tx-desc { display: flex; align-items: center; gap: 0.85rem; }
.tx-icon { width: 40px; height: 40px; border-radius: 10px; display: flex; align-items: center; justify-content: center; font-weight: 800; font-size: 1rem; flex-shrink: 0; }
.tx-info { display: flex; flex-direction: column; }
.tx-info strong { font-size: 0.88rem; color: #0f172a; }
.tx-info span { font-size: 0.72rem; color: #94a3b8; font-weight: 600; }
.text-bold { font-weight: 700; color: #475569; font-size: 0.85rem; }
.status-pill { padding: 0.25rem 0.7rem; border-radius: 0.5rem; font-size: 0.65rem; font-weight: 800; }
.status-pill.paid { background: #f0fdf4; color: #16a34a; }
.amount-cell { font-size: 1.05rem; font-weight: 800; color: #0f172a; }
.table-footer { margin-top: 1.5rem; display: flex; justify-content: center; }
.btn-view-all { background: #f8fafc; border: 1.5px solid #f1f5f9; color: #3b82f6; padding: 0.65rem 1.75rem; border-radius: 0.85rem; font-weight: 800; font-size: 0.82rem; cursor: pointer; }

/* ── MOBILE ── */
@media (max-width: 768px) {
  .desktop-only { display: none !important; }
  .mobile-only { display: flex !important; }

  .stats-grid { grid-template-columns: 1fr 1fr; gap: 0.75rem; }
  .stat-card { padding: 1rem; border-radius: 1rem; }
  .stat-icon-wrap { width: 34px; height: 34px; border-radius: 10px; margin-bottom: 0.5rem; }
  .stat-icon-wrap svg { width: 16px; height: 16px; }
  .stat-label { font-size: 0.65rem; }
  .stat-value { font-size: 1.4rem; }
  .stat-trend { font-size: 0.68rem; }

  .payment-grid { grid-template-columns: 1fr; gap: 1rem; }
  .card { border-radius: 1rem; padding: 1.1rem; }
  .card-header { margin-bottom: 1rem; }
  .method-item { padding: 0.75rem; border-radius: 0.75rem; gap: 0.75rem; }

  /* Mobile transaction list */
  .tx-card-list { display: flex; flex-direction: column; gap: 0.75rem; }
  .tx-card { display: flex; align-items: center; gap: 0.85rem; padding: 0.85rem; background: #f8fafc; border-radius: 0.85rem; }
  .tx-card .tx-icon { width: 38px; height: 38px; border-radius: 10px; display: flex; align-items: center; justify-content: center; font-weight: 800; font-size: 0.9rem; flex-shrink: 0; }
  .tx-details { flex: 1; min-width: 0; }
  .tx-details strong { font-size: 0.82rem; color: #0f172a; font-weight: 800; display: block; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
  .tx-details span { font-size: 0.68rem; color: #94a3b8; font-weight: 600; }
  .tx-right { display: flex; flex-direction: column; align-items: flex-end; gap: 0.3rem; flex-shrink: 0; }
  .tx-right .amount { font-size: 0.95rem; font-weight: 800; color: #0f172a; }
}
</style>
