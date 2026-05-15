<template>
  <AdminLayout
    title="ID Verifications"
    subtitle="Review pending government or student ID uploads and approve or reject them."
    @logout="logout"
  >
    <template #actions>
      <label class="toolbar-field">
        <span class="toolbar-label">Search</span>
        <input v-model.trim="query" class="toolbar-input" type="search" placeholder="Name or email…" />
      </label>

      <label class="toolbar-field">
        <span class="toolbar-label">Role</span>
        <select v-model="roleFilter" class="toolbar-select">
          <option value="all">All Roles</option>
          <option value="student">Student</option>
          <option value="tutor">Tutor</option>
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
      <div v-if="loading" class="empty">Loading pending ID verifications…</div>
      <div v-else-if="filteredRequests.length === 0" class="empty">No matching ID verification requests.</div>

      <article v-for="req in filteredRequests" :key="req.id" class="request-card" v-else>
        <div class="user-head">
          <img :src="req.avatar_url || '/images/default_avatar.png'" alt="User avatar" class="avatar-img" />
          <div class="user-meta">
            <h2>{{ fullName(req) }}</h2>
            <p class="muted">{{ req.email }}</p>
            <div class="badges">
              <span class="badge role-badge">{{ req.role || 'user' }}</span>
              <span class="badge status-badge pending">Pending ID Review</span>
            </div>
          </div>
        </div>

        <div class="content">
          <div v-if="req.id_photo_url" class="field">
            <div class="field-k">Uploaded ID Photo</div>
            <div class="id-photo-container">
              <a :href="req.id_photo_url" target="_blank" rel="noopener">
                <img :src="req.id_photo_url" alt="ID Photo" class="id-photo-preview" />
              </a>
            </div>
            <p class="muted-hint">Click image to view full size</p>
          </div>
          <div v-else class="field">
            <div class="field-k">Uploaded ID Photo</div>
            <div class="field-v">No photo uploaded.</div>
          </div>
        </div>

        <div class="actions">
          <button class="btn-approve" type="button" @click="review(req.id, 'approve')">Approve ID</button>
          <button class="btn-reject" type="button" @click="review(req.id, 'reject')">Reject ID</button>
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
const roleFilter = ref('all');
const lastUpdatedAt = ref(null);

const filteredRequests = computed(() => {
  const q = query.value.toLowerCase();
  const role = roleFilter.value;
  return (requests.value || []).filter((r) => {
    const name = `${r.first_name || ''} ${r.last_name || ''}`.trim().toLowerCase();
    const email = (r.email || '').toLowerCase();
    const matchesQuery = !q || name.includes(q) || email.includes(q);
    const matchesRole = role === 'all' ? true : (r.role === role);
    return matchesQuery && matchesRole;
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
  return full || 'User';
}

async function loadRequests() {
  loading.value = true;
  try {
    const { data } = await adminService.getPendingIdVerifications();
    requests.value = Array.isArray(data) ? data : (data.results || []);
    lastUpdatedAt.value = Date.now();
  } catch (err) {
    showToast('Failed to load ID requests.', 'error');
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
    await adminService.reviewIdVerification(profileId, { action });
    showToast(`ID ${action}d successfully.`, 'success');
    await loadRequests();
  } catch (_err) {
    showToast(`Failed to ${action} ID.`, 'error');
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
.toolbar-field { display: grid; gap: 0.2rem; }
.toolbar-label { font-size: 0.72rem; color: #475569; font-weight: 850; letter-spacing: 0.02em; }
.toolbar-input, .toolbar-select {
  border: 1px solid rgba(148, 163, 184, 0.7);
  background: rgba(255, 255, 255, 0.75);
  border-radius: 0.85rem; padding: 0.55rem 0.75rem;
  font-weight: 800; color: #0f172a; min-width: 190px;
}
.toolbar-select { min-width: 120px; }
.btn-refresh {
  border: 1px solid rgba(37, 99, 235, 0.35);
  background: rgba(37, 99, 235, 0.10);
  color: #1d4ed8; border-radius: 0.85rem;
  padding: 0.62rem 0.85rem; font-weight: 950; cursor: pointer;
}
.btn-refresh:disabled { opacity: 0.7; cursor: not-allowed; }

.stats { display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); gap: 0.75rem; }
.stat { background: rgba(255, 255, 255, 0.75); border: 1px solid rgba(148, 163, 184, 0.35); border-radius: 1rem; padding: 0.9rem; }
.stat-k { color: #64748b; font-weight: 900; font-size: 0.8rem; letter-spacing: 0.02em; }
.stat-v { margin-top: 0.25rem; font-weight: 950; font-size: 1.35rem; color: #0f172a; }
.stat-v.small { font-size: 0.95rem; font-weight: 900; color: #334155; }

.admin-body { display: grid; gap: 0.9rem; }
.empty { background: rgba(255, 255, 255, 0.75); border: 1px solid rgba(148, 163, 184, 0.35); border-radius: 1rem; padding: 1rem; color: #64748b; font-weight: 750; }

.request-card {
  background: rgba(255, 255, 255, 0.82);
  border: 1px solid rgba(148, 163, 184, 0.35);
  border-radius: 1.1rem; padding: 1.25rem;
  display: grid; gap: 1rem;
  box-shadow: 0 18px 40px rgba(15, 23, 42, 0.06);
}

.user-head { display: flex; align-items: center; gap: 1rem; }
.avatar-img { width: 56px; height: 56px; border-radius: 18px; object-fit: cover; border: 1px solid rgba(148, 163, 184, 0.35); background: #e2e8f0; }
.user-meta h2 { font-size: 1.1rem; font-weight: 950; color: #0f172a; letter-spacing: -0.01em; margin: 0; }
.muted { color: #64748b; font-size: 0.86rem; font-weight: 750; margin: 0.2rem 0 0.4rem; }
.badges { display: flex; flex-wrap: wrap; gap: 0.5rem; }
.badge { display: inline-flex; align-items: center; border-radius: 999px; padding: 0.25rem 0.65rem; font-size: 0.75rem; font-weight: 900; text-transform: uppercase; letter-spacing: 0.03em; }
.role-badge { background: #f1f5f9; color: #475569; border: 1px solid #e2e8f0; }
.status-badge.pending { background: #eff6ff; color: #1d4ed8; border: 1px solid #bfdbfe; }

.content { display: grid; gap: 0.75rem; background: #f8fafc; padding: 1rem; border-radius: 0.85rem; border: 1px solid #e2e8f0; }
.field-k { font-size: 0.78rem; font-weight: 950; color: #475569; letter-spacing: 0.02em; margin-bottom: 0.5rem; text-transform: uppercase; }
.field-v { color: #0f172a; font-weight: 700; font-size: 0.92rem; }

.id-photo-container { border-radius: 0.75rem; overflow: hidden; border: 1px solid #cbd5e1; background: #000; width: fit-content; max-width: 100%; max-height: 250px; display: flex; align-items: center; justify-content: center; }
.id-photo-preview { max-width: 100%; max-height: 250px; object-fit: contain; display: block; transition: opacity 0.2s; }
.id-photo-container:hover .id-photo-preview { opacity: 0.85; }
.muted-hint { font-size: 0.75rem; color: #94a3b8; font-weight: 600; margin-top: 0.35rem; }

.actions { display: flex; align-items: center; gap: 0.6rem; flex-wrap: wrap; margin-top: 0.5rem; }
.btn-approve, .btn-reject { border: none; border-radius: 0.9rem; padding: 0.7rem 1.1rem; font-weight: 950; cursor: pointer; transition: transform 0.2s, box-shadow 0.2s; }
.btn-approve:hover, .btn-reject:hover { transform: translateY(-1px); }
.btn-approve { background: linear-gradient(135deg, #16a34a, #22c55e); color: #fff; box-shadow: 0 10px 22px rgba(34, 197, 94, 0.25); }
.btn-reject { background: linear-gradient(135deg, #ef4444, #f97316); color: #fff; box-shadow: 0 10px 22px rgba(239, 68, 68, 0.22); }

@media (max-width: 860px) {
  .stats { grid-template-columns: 1fr; }
  .toolbar-input { min-width: 220px; }
  .id-photo-container { width: 100%; }
}
</style>
