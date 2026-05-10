<template>
  <AdminLayout
    title="Tutor Tier Upgrade Reviews"
    subtitle="Review pending tutor submissions and approve or reject requests."
    @logout="logout"
  >
    <template #actions>
      <label class="toolbar-field">
        <span class="toolbar-label">Search</span>
        <input v-model.trim="query" class="toolbar-input" type="search" placeholder="Name or email…" />
      </label>

      <label class="toolbar-field">
        <span class="toolbar-label">Tier</span>
        <select v-model="tierFilter" class="toolbar-select">
          <option value="all">All</option>
          <option value="basic">Tier 1</option>
          <option value="plus">Tier 2</option>
          <option value="pro">Tier 3</option>
        </select>
      </label>

      <button class="btn-refresh" type="button" :disabled="loading" @click="loadRequests">
        {{ loading ? 'Refreshing…' : 'Refresh' }}
      </button>
    </template>

    <section class="stats">
      <div class="stat">
        <div class="stat-k">Pending</div>
        <div class="stat-v">{{ requests.length }}</div>
      </div>
      <div class="stat">
        <div class="stat-k">Showing</div>
        <div class="stat-v">{{ filteredRequests.length }}</div>
      </div>
      <div class="stat">
        <div class="stat-k">Last updated</div>
        <div class="stat-v small">{{ lastUpdatedLabel }}</div>
      </div>
    </section>

    <section class="admin-body">
      <div v-if="loading" class="empty">Loading pending requests…</div>
      <div v-else-if="filteredRequests.length === 0" class="empty">No matching tier review requests.</div>

      <article v-for="req in filteredRequests" :key="req.id" class="request-card" v-else>
        <div class="tutor-head">
          <img :src="req.avatar_url || '/images/tutor_avatar.png'" alt="Tutor avatar" />
          <div class="tutor-meta">
            <h2>{{ fullName(req) }}</h2>
            <p class="muted">{{ req.email }}</p>
            <div class="badges">
              <span class="badge">Current: {{ tierLabel(req.current_tier) }}</span>
            </div>
          </div>
        </div>

        <div class="content">
          <div class="field">
            <div class="field-k">Achievements</div>
            <div class="field-v">{{ req.achievements || 'No achievements provided.' }}</div>
          </div>
          <div class="field">
            <div class="field-k">Bio</div>
            <div class="field-v">{{ req.bio || 'No bio provided.' }}</div>
          </div>

          <div v-if="req.credentials_documents?.length || req.credentials_document_url" class="field">
            <div class="field-k">Credentials</div>
            <div class="cred-links">
              <a
                v-for="doc in (req.credentials_documents || [])"
                :key="doc.id"
                :href="doc.url"
                target="_blank"
                rel="noopener"
              >
                {{ doc.name || 'Document' }}
              </a>
              <a
                v-if="!req.credentials_documents?.length && req.credentials_document_url"
                :href="req.credentials_document_url"
                target="_blank"
                rel="noopener"
              >
                View document
              </a>
            </div>
          </div>
        </div>

        <div class="actions">
          <button class="btn-approve" type="button" @click="review(req.id, 'approve')">Approve</button>
          <button class="btn-reject" type="button" @click="review(req.id, 'reject')">Reject</button>
        </div>
      </article>
    </section>
  </AdminLayout>
</template>

<script setup>
import { computed, onMounted, ref } from 'vue';
import { useRouter } from 'vue-router';
import { adminService } from '../services/api';
import { useToast } from '../composables/useToast';
import AdminLayout from '../components/admin/AdminLayout.vue';

const router = useRouter();
const { showToast } = useToast();
const loading = ref(true);
const requests = ref([]);
const query = ref('');
const tierFilter = ref('all');
const lastUpdatedAt = ref(null);

const filteredRequests = computed(() => {
  const q = query.value.toLowerCase();
  const tier = tierFilter.value;
  return (requests.value || []).filter((r) => {
    const name = `${r.first_name || ''} ${r.last_name || ''}`.trim().toLowerCase();
    const email = (r.email || '').toLowerCase();
    const matchesQuery = !q || name.includes(q) || email.includes(q);
    const currentTier = (r.current_tier || 'basic').toLowerCase();
    const matchesTier = tier === 'all' ? true : currentTier === tier;
    return matchesQuery && matchesTier;
  });
});

const lastUpdatedLabel = computed(() => {
  if (!lastUpdatedAt.value) return '—';
  try {
    return new Date(lastUpdatedAt.value).toLocaleString();
  } catch (_e) {
    return '—';
  }
});

function fullName(req) {
  const full = `${req.first_name || ''} ${req.last_name || ''}`.trim();
  return full || 'Tutor';
}

function tierLabel(tier) {
  if (tier === 'pro') return 'Tier 3 - Pro Tutor';
  if (tier === 'plus') return 'Tier 2 - Plus Tutor';
  return 'Tier 1 - Basic Tutor';
}

async function loadRequests() {
  loading.value = true;
  try {
    const { data } = await adminService.getPendingTierRequests();
    requests.value = Array.isArray(data) ? data : [];
    lastUpdatedAt.value = Date.now();
  } catch (err) {
    showToast('Failed to load tier requests.', 'error');
    if (err?.response?.status === 401) {
      sessionStorage.removeItem('turo_admin_auth');
      router.push('/admin/login');
    }
  } finally {
    loading.value = false;
  }
}

async function review(profileId, action) {
  try {
    await adminService.reviewTierRequest(profileId, { action });
    showToast(`Request ${action}d successfully.`, 'success');
    await loadRequests();
  } catch (_err) {
    showToast(`Failed to ${action} request.`, 'error');
  }
}

function logout() {
  sessionStorage.removeItem('turo_admin_auth');
  router.push('/admin/login');
}

onMounted(async () => {
  if (!sessionStorage.getItem('turo_admin_auth')) {
    router.push('/admin/login');
    return;
  }
  await loadRequests();
});
</script>

<style scoped>
.toolbar-field {
  display: grid;
  gap: 0.2rem;
}
.toolbar-label {
  font-size: 0.72rem;
  color: #475569;
  font-weight: 850;
  letter-spacing: 0.02em;
}
.toolbar-input,
.toolbar-select {
  border: 1px solid rgba(148, 163, 184, 0.7);
  background: rgba(255, 255, 255, 0.75);
  border-radius: 0.85rem;
  padding: 0.55rem 0.75rem;
  font-weight: 800;
  color: #0f172a;
  min-width: 190px;
}
.toolbar-select {
  min-width: 120px;
}
.btn-refresh {
  border: 1px solid rgba(37, 99, 235, 0.35);
  background: rgba(37, 99, 235, 0.10);
  color: #1d4ed8;
  border-radius: 0.85rem;
  padding: 0.62rem 0.85rem;
  font-weight: 950;
  cursor: pointer;
}
.btn-refresh:disabled {
  opacity: 0.7;
  cursor: not-allowed;
}

.stats {
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: 0.75rem;
}
.stat {
  background: rgba(255, 255, 255, 0.75);
  border: 1px solid rgba(148, 163, 184, 0.35);
  border-radius: 1rem;
  padding: 0.9rem;
}
.stat-k {
  color: #64748b;
  font-weight: 900;
  font-size: 0.8rem;
  letter-spacing: 0.02em;
}
.stat-v {
  margin-top: 0.25rem;
  font-weight: 950;
  font-size: 1.35rem;
  color: #0f172a;
}
.stat-v.small {
  font-size: 0.95rem;
  font-weight: 900;
  color: #334155;
}

.admin-body {
  display: grid;
  gap: 0.9rem;
}
.empty {
  background: rgba(255, 255, 255, 0.75);
  border: 1px solid rgba(148, 163, 184, 0.35);
  border-radius: 1rem;
  padding: 1rem;
  color: #64748b;
  font-weight: 750;
}
.request-card {
  background: rgba(255, 255, 255, 0.82);
  border: 1px solid rgba(148, 163, 184, 0.35);
  border-radius: 1.1rem;
  padding: 1rem;
  display: grid;
  gap: 0.85rem;
  box-shadow: 0 18px 40px rgba(15, 23, 42, 0.06);
}
.tutor-head {
  display: flex;
  align-items: center;
  gap: 0.85rem;
}
.tutor-head img {
  width: 52px;
  height: 52px;
  border-radius: 16px;
  object-fit: cover;
  border: 1px solid rgba(148, 163, 184, 0.35);
}
.tutor-meta h2 {
  font-size: 1.05rem;
  font-weight: 950;
  color: #0f172a;
  letter-spacing: -0.01em;
}
.muted {
  color: #64748b;
  font-size: 0.86rem;
  font-weight: 750;
}
.badges {
  display: flex;
  flex-wrap: wrap;
  gap: 0.4rem;
  margin-top: 0.35rem;
}
.badge {
  display: inline-flex;
  align-items: center;
  border: 1px solid rgba(148, 163, 184, 0.35);
  background: rgba(248, 250, 252, 0.85);
  color: #0f172a;
  border-radius: 999px;
  padding: 0.25rem 0.55rem;
  font-size: 0.78rem;
  font-weight: 900;
}

.content {
  display: grid;
  gap: 0.65rem;
}
.field {
  display: grid;
  gap: 0.25rem;
}
.field-k {
  font-size: 0.78rem;
  font-weight: 950;
  color: #475569;
  letter-spacing: 0.02em;
}
.field-v {
  color: #0f172a;
  font-weight: 700;
  line-height: 1.45;
  font-size: 0.92rem;
}
.cred-links {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
}
.cred-links a {
  font-size: 0.82rem;
  font-weight: 950;
  color: #1d4ed8;
  text-decoration: none;
  border-bottom: 2px solid rgba(29, 78, 216, 0.25);
}
.cred-links a:hover {
  border-bottom-color: rgba(29, 78, 216, 0.65);
}

.actions {
  display: flex;
  align-items: center;
  gap: 0.6rem;
  flex-wrap: wrap;
}
.btn-approve,
.btn-reject {
  border: none;
  border-radius: 0.9rem;
  padding: 0.6rem 0.95rem;
  font-weight: 950;
  cursor: pointer;
}
.btn-approve {
  background: linear-gradient(135deg, #16a34a, #22c55e);
  color: #fff;
  box-shadow: 0 10px 22px rgba(34, 197, 94, 0.25);
}
.btn-reject {
  background: linear-gradient(135deg, #ef4444, #f97316);
  color: #fff;
  box-shadow: 0 10px 22px rgba(239, 68, 68, 0.22);
}

@media (max-width: 860px) {
  .stats {
    grid-template-columns: 1fr;
  }
  .toolbar-input {
    min-width: 220px;
  }
}
</style>
