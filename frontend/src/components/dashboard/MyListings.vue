<template>
  <div class="listings-tab">

    <!-- Header -->
    <div class="page-header desktop-only">
      <div>
        <h1>My Listings</h1>
        <p>Manage all your published expertise listings</p>
      </div>
      <button class="btn-new" @click="showForm = true">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><line x1="12" y1="5" x2="12" y2="19"/><line x1="5" y1="12" x2="19" y2="12"/></svg>
        New Listing
      </button>
    </div>

    <!-- Stats Row -->
    <div class="stats-row">
      <div class="stat-card" v-for="s in statCards" :key="s.label">
        <span class="stat-icon" aria-hidden="true">
          <TuroIcon :name="s.iconName" :size="18" stroke-width="2.2" />
        </span>
        <div>
          <div class="stat-val">{{ s.value }}</div>
          <div class="stat-label">{{ s.label }}</div>
        </div>
      </div>
    </div>

    <!-- Search -->
    <div class="search-bar">
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="11" cy="11" r="8"/><path d="m21 21-4.3-4.3"/></svg>
      <input v-model="searchQuery" placeholder="Search your listings..." />
    </div>

    <!-- Loading -->
    <div class="loading-state" v-if="loading">
      <div class="spinner"></div>
      <p>Loading your listings...</p>
    </div>

    <!-- Empty state -->
    <div class="empty-state" v-else-if="filtered.length === 0">
      <div class="empty-icon">📋</div>
      <h3>No listings yet</h3>
      <p>Create your first listing to start attracting students.</p>
      <button class="btn-new" @click="showForm = true">Create a Listing</button>
    </div>

    <!-- Listings Grid -->
    <div class="listings-grid" v-else>
      <div class="listing-card" v-for="post in filtered" :key="post.id">
        <div class="card-photo" v-if="post.photo_url">
          <img :src="post.photo_url" :alt="post.title" />
        </div>
        <div class="card-top">
          <div class="subject-badge">{{ post.subject }}</div>
          <div class="card-actions">
            <button class="icon-action" title="Edit" @click="editPost(post)">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7"/><path d="M18.5 2.5a2.121 2.121 0 0 1 3 3L12 15l-4 1 1-4 9.5-9.5z"/></svg>
            </button>
            <button class="icon-action danger" title="Delete" @click="confirmDelete(post)">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="3 6 5 6 21 6"/><path d="M19 6l-1 14H6L5 6"/><path d="M10 11v6"/><path d="M14 11v6"/><path d="M9 6V4h6v2"/></svg>
            </button>
          </div>
        </div>

        <h3 class="card-title">{{ post.title || post.subject }}</h3>
        <p class="card-desc">{{ post.description }}</p>

        <div class="card-meta">
          <span class="level-tag">{{ post.level }}</span>
          <span class="rate">₱{{ post.hourly_rate }}<small>/hr</small></span>
        </div>

        <div class="card-footer">
          <span class="date">{{ formatDate(post.created_at) }}</span>
          <span class="status-badge" :class="post.is_published ? 'published' : 'draft'">
            {{ post.is_published ? 'Published' : 'Draft' }}
          </span>
        </div>
      </div>
    </div>

    <!-- Edit Modal -->
    <transition name="fade">
      <div class="modal-overlay" v-if="showForm" @click.self="closeForm">
        <div class="modal-card">
          <div class="modal-header">
            <h3>{{ editingPost ? 'Edit Listing' : 'New Listing' }}</h3>
            <button class="close-btn" @click="closeForm">✕</button>
          </div>
          <div class="modal-body">
            <div class="field">
              <label>Title *</label>
              <input v-model="form.title" placeholder="e.g. Advanced Math Tutoring" />
            </div>
            <div class="field-row">
              <div class="field">
                <label>Subject *</label>
                <select v-model="form.subject">
                  <option>Mathematics</option><option>Science</option><option>English</option>
                  <option>Physics</option><option>Chemistry</option><option>History</option>
                  <option>Music</option><option>Arts</option><option>Sports</option>
                </select>
              </div>
              <div class="field">
                <label>Level</label>
                <select v-model="form.level">
                  <option>Beginner</option><option>Intermediate</option>
                  <option>Advanced</option><option>All Levels</option>
                </select>
              </div>
            </div>
            <div class="field">
              <label>Hourly Rate (₱) *</label>
              <input type="number" v-model="form.hourly_rate" placeholder="e.g. 300" />
            </div>
            <div class="field">
              <label>Description *</label>
              <textarea v-model="form.description" rows="4" placeholder="Describe what you'll teach..."></textarea>
            </div>
          </div>
          <div class="modal-footer">
            <button class="btn-cancel" @click="closeForm">Cancel</button>
            <button class="btn-save" @click="savePost" :disabled="saving">
              {{ saving ? 'Saving...' : (editingPost ? 'Save Changes' : 'Publish Listing') }}
            </button>
          </div>
        </div>
      </div>
    </transition>

    <!-- Delete Confirm Modal -->
    <transition name="fade">
      <div class="modal-overlay" v-if="deleteTarget" @click.self="deleteTarget = null">
        <div class="modal-card confirm-card">
          <div class="confirm-icon">🗑️</div>
          <h3>Delete Listing?</h3>
          <p>This will permanently remove <strong>{{ deleteTarget?.title || deleteTarget?.subject }}</strong> and all related bookings.</p>
          <div class="modal-footer">
            <button class="btn-cancel" @click="deleteTarget = null">Cancel</button>
            <button class="btn-delete" @click="deletePost" :disabled="saving">
              {{ saving ? 'Deleting...' : 'Yes, Delete' }}
            </button>
          </div>
        </div>
      </div>
    </transition>

  </div>
</template>

<script setup>
import { ref, computed, onMounted, reactive, watch } from 'vue';
import { postService, profileService } from '../../services/api';
import { supabase } from '../../supabase';
import { useToast } from '../../composables/useToast';
import { TuroIcon } from '../icons';

const props = defineProps({ profile: Object });
const { showToast } = useToast();

const posts = ref([]);
const loading = ref(true);
const saving = ref(false);
const searchQuery = ref('');
const showForm = ref(false);
const editingPost = ref(null);
const deleteTarget = ref(null);

const form = reactive({ title: '', subject: 'Mathematics', level: 'All Levels', hourly_rate: '', description: '' });

const TUTOR_EMAIL = ref('');
const djangoProfile = ref(null);

// Use the profile prop from TutorDashboard immediately (no extra API call needed)
watch(() => props.profile, async (p) => {
  if (p && p.user) {
    djangoProfile.value = p;
    TUTOR_EMAIL.value = p.email || '';
    await fetchPosts();
  }
}, { immediate: true });

// No onMounted fallback needed — TutorDashboard guarantees passing the profile prop.

async function fetchPosts() {
  if (!djangoProfile.value?.user) return;
  loading.value = true;
  try {
    const { data } = await postService.getAllPosts({ tutor_id: djangoProfile.value.user });
    posts.value = Array.isArray(data) ? data : (data.results || []);
  } catch (e) {
    showToast('Failed to load listings', 'error');
  } finally {
    loading.value = false;
  }
}

const statCards = computed(() => [
  { label: 'Total Listings', value: loading.value ? '-' : posts.value.length, iconName: 'list' },
  { label: 'Published', value: loading.value ? '-' : posts.value.filter(p => p.is_published).length, iconName: 'check' },
  { label: 'Drafts', value: loading.value ? '-' : posts.value.filter(p => !p.is_published).length, iconName: 'editFile' },
  { label: 'Avg. Rate', value: loading.value ? '-' : '₱' + (posts.value.reduce((acc, p) => acc + Number(p.hourly_rate), 0) / (posts.value.length || 1)).toFixed(0), iconName: 'ledger' }
]);

const filtered = computed(() =>
  posts.value.filter(p =>
    !searchQuery.value ||
    p.title?.toLowerCase().includes(searchQuery.value.toLowerCase()) ||
    p.subject?.toLowerCase().includes(searchQuery.value.toLowerCase())
  )
);

function formatDate(dt) {
  if (!dt) return '';
  return new Date(dt).toLocaleDateString('en-PH', { month: 'short', day: 'numeric', year: 'numeric' });
}

function editPost(post) {
  editingPost.value = post;
  Object.assign(form, {
    title: post.title || '',
    subject: post.subject || 'Mathematics',
    level: post.level || 'All Levels',
    hourly_rate: post.hourly_rate || '',
    description: post.description || ''
  });
  showForm.value = true;
}

function closeForm() {
  showForm.value = false;
  editingPost.value = null;
  Object.assign(form, { title: '', subject: 'Mathematics', level: 'All Levels', hourly_rate: '', description: '' });
}

function confirmDelete(post) {
  deleteTarget.value = post;
}

async function savePost() {
  if (!form.title || !form.hourly_rate || !form.description) {
    showToast('Please fill in all required fields', 'error');
    return;
  }
  if (!djangoProfile.value) {
    showToast('Tutor profile not found. Please try again later.', 'error');
    return;
  }
  saving.value = true;
  try {
    const payload = { 
      tutor_id: djangoProfile.value.user, // Using user ID for the FK
      title: form.title, 
      subject: form.subject, 
      level: form.level, 
      hourly_rate: parseFloat(form.hourly_rate), 
      description: form.description 
    };
    if (editingPost.value) {
      await postService.updatePost(editingPost.value.id, payload);
      showToast('Listing updated!', 'success');
    } else {
      await postService.createPost(payload);
      showToast('Listing published!', 'success');
    }
    closeForm();
    await fetchPosts();
  } catch (e) {
    showToast('Failed to save listing', 'error');
  } finally {
    saving.value = false;
  }
}

async function deletePost() {
  saving.value = true;
  try {
    await postService.deletePost(deleteTarget.value.id);
    showToast('Listing deleted', 'success');
    deleteTarget.value = null;
    await fetchPosts();
  } catch (e) {
    showToast('Failed to delete listing', 'error');
  } finally {
    saving.value = false;
  }
}
</script>

<style scoped>
.listings-tab { display: flex; flex-direction: column; gap: 1.5rem; }

.page-header { display: flex; justify-content: space-between; align-items: center; }
.page-header h1 { font-size: 2rem; font-weight: 800; color: #0f172a; }
.page-header p { color: #64748b; font-size: 0.95rem; margin-top: 0.2rem; }

.btn-new {
  display: flex; align-items: center; gap: 0.5rem;
  background: #0f172a; color: white; border: none;
  padding: 0.75rem 1.5rem; border-radius: 0.75rem;
  font-weight: 700; font-size: 0.9rem; cursor: pointer;
  transition: all 0.2s;
}
.btn-new:hover { background: #1e293b; transform: translateY(-1px); }
.btn-new svg { width: 16px; height: 16px; }

/* Stats */
.stats-row { display: grid; grid-template-columns: repeat(4, 1fr); gap: 1rem; }
.stat-card {
  background: white; border-radius: 1rem; padding: 1.25rem;
  display: flex; align-items: center; gap: 1rem;
  border: 1px solid #f1f5f9; box-shadow: 0 2px 8px rgba(0,0,0,0.03);
}
.stat-icon {
  width: 36px;
  height: 36px;
  border-radius: 10px;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  background: #f8fafc;
  color: #475569;
  flex-shrink: 0;
}
.stat-val { font-size: 1.5rem; font-weight: 800; color: #0f172a; }
.stat-label { font-size: 0.75rem; color: #94a3b8; font-weight: 600; margin-top: 0.1rem; }

/* Search */
.search-bar {
  display: flex; align-items: center; gap: 0.75rem;
  background: white; border: 1.5px solid #f1f5f9;
  padding: 0.8rem 1.25rem; border-radius: 1rem;
  box-shadow: 0 2px 8px rgba(0,0,0,0.03);
}
.search-bar svg { width: 18px; height: 18px; color: #94a3b8; flex-shrink: 0; }
.search-bar input { flex: 1; border: none; outline: none; font-size: 0.95rem; color: #0f172a; background: transparent; }

/* Loading / Empty */
.loading-state { display: flex; flex-direction: column; align-items: center; gap: 1rem; padding: 4rem; color: #94a3b8; }
.spinner { width: 36px; height: 36px; border: 3px solid #f1f5f9; border-top-color: #0f172a; border-radius: 50%; animation: spin 0.7s linear infinite; }
@keyframes spin { to { transform: rotate(360deg); } }
.empty-state { text-align: center; padding: 4rem; background: white; border-radius: 1.5rem; border: 1px solid #f1f5f9; }
.empty-icon { font-size: 3rem; margin-bottom: 1rem; }
.empty-state h3 { font-size: 1.25rem; font-weight: 800; color: #0f172a; margin-bottom: 0.5rem; }
.empty-state p { color: #64748b; margin-bottom: 1.5rem; }

/* Listings Grid */
.listings-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 1.25rem; }
.listing-card {
  background: white; border-radius: 1.25rem; overflow: hidden;
  border: 1px solid #f1f5f9; box-shadow: 0 4px 16px rgba(0,0,0,0.04);
  display: flex; flex-direction: column;
  transition: transform 0.2s, box-shadow 0.2s;
}
.listing-card:hover { transform: translateY(-4px); box-shadow: 0 12px 32px rgba(0,0,0,0.08); }

.card-photo { width: 100%; height: 160px; overflow: hidden; background: #f1f5f9; }
.card-photo img { width: 100%; height: 100%; object-fit: cover; }

.card-top { display: flex; justify-content: space-between; align-items: center; padding: 1.25rem 1.25rem 0; }
.subject-badge { background: #eff6ff; color: #1e3a8a; font-size: 0.7rem; font-weight: 800; padding: 0.3rem 0.75rem; border-radius: 2rem; text-transform: uppercase; letter-spacing: 0.05em; }
.card-actions { display: flex; gap: 0.4rem; }
.icon-action { background: #f8fafc; border: 1px solid #f1f5f9; border-radius: 0.5rem; width: 32px; height: 32px; display: flex; align-items: center; justify-content: center; cursor: pointer; transition: all 0.15s; }
.icon-action svg { width: 14px; height: 14px; color: #64748b; }
.icon-action:hover { background: #e2e8f0; }
.icon-action.danger:hover { background: #fef2f2; border-color: #fecaca; }
.icon-action.danger:hover svg { color: #ef4444; }

.card-title { font-size: 1rem; font-weight: 800; color: #0f172a; line-height: 1.3; padding: 0.75rem 1.25rem 0; }
.card-desc { font-size: 0.82rem; color: #64748b; line-height: 1.5; display: -webkit-box; -webkit-line-clamp: 2; -webkit-box-orient: vertical; overflow: hidden; padding: 0 1.25rem; }
.card-meta { display: flex; justify-content: space-between; align-items: center; padding: 0 1.25rem; }
.level-tag { background: #f1f5f9; color: #475569; font-size: 0.7rem; font-weight: 700; padding: 0.25rem 0.6rem; border-radius: 0.4rem; }
.rate { font-size: 1.1rem; font-weight: 800; color: #0f172a; }
.rate small { font-size: 0.7rem; color: #94a3b8; font-weight: 600; }

.card-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0.75rem 1.25rem;
  border-top: 1px solid #f1f5f9;
  margin-top: auto;
}
.date { font-size: 0.72rem; color: #94a3b8; font-weight: 600; }
.status-badge { font-size: 0.68rem; font-weight: 800; padding: 0.25rem 0.65rem; border-radius: 2rem; }
.status-badge.published { background: #dcfce7; color: #16a34a; }
.status-badge.draft { background: #fef9c3; color: #92400e; }

/* Modal */
.modal-overlay { position: fixed; inset: 0; background: rgba(0,0,0,0.4); backdrop-filter: blur(4px); display: flex; align-items: center; justify-content: center; z-index: 1000; }
.modal-card { background: white; border-radius: 1.5rem; width: 90%; max-width: 560px; overflow: hidden; box-shadow: 0 24px 48px rgba(0,0,0,0.12); }
.modal-header { display: flex; justify-content: space-between; align-items: center; padding: 1.5rem 2rem; border-bottom: 1px solid #f1f5f9; }
.modal-header h3 { font-size: 1.25rem; font-weight: 800; color: #0f172a; }
.close-btn { background: none; border: none; font-size: 1.25rem; cursor: pointer; color: #94a3b8; }
.modal-body { padding: 1.5rem 2rem; display: flex; flex-direction: column; gap: 1.1rem; max-height: 65vh; overflow-y: auto; }
.field { display: flex; flex-direction: column; gap: 0.4rem; }
.field-row { display: grid; grid-template-columns: 1fr 1fr; gap: 1rem; }
.field label { font-size: 0.82rem; font-weight: 700; color: #374151; }
.field input, .field select, .field textarea { padding: 0.75rem 1rem; border: 1.5px solid #e2e8f0; border-radius: 0.75rem; font-size: 0.9rem; outline: none; color: #0f172a; resize: vertical; }
.field input:focus, .field select:focus, .field textarea:focus { border-color: #0f172a; }
.modal-footer { display: flex; gap: 1rem; padding: 1.25rem 2rem; border-top: 1px solid #f1f5f9; }
.btn-cancel { flex: 1; padding: 0.75rem; border: 1.5px solid #e2e8f0; border-radius: 0.75rem; background: white; font-weight: 700; cursor: pointer; }
.btn-save { flex: 2; padding: 0.75rem; border: none; border-radius: 0.75rem; background: #0f172a; color: white; font-weight: 800; cursor: pointer; }
.btn-save:disabled, .btn-delete:disabled { opacity: 0.6; cursor: not-allowed; }

/* Confirm delete */
.confirm-card { max-width: 400px; padding: 2.5rem 2rem; text-align: center; }
.confirm-icon { font-size: 3rem; margin-bottom: 1rem; }
.confirm-card h3 { font-size: 1.2rem; font-weight: 800; color: #0f172a; margin-bottom: 0.5rem; }
.confirm-card p { font-size: 0.9rem; color: #64748b; margin-bottom: 1.5rem; }
.btn-delete { flex: 2; padding: 0.75rem; border: none; border-radius: 0.75rem; background: #ef4444; color: white; font-weight: 800; cursor: pointer; }

/* Animations */
.fade-enter-active, .fade-leave-active { transition: opacity 0.25s; }
.fade-enter-from, .fade-leave-to { opacity: 0; }

/* Mobile */
@media (max-width: 768px) {
  .desktop-only { display: none !important; }
  .stats-row { grid-template-columns: repeat(2, 1fr); }
  .listings-grid { grid-template-columns: 1fr; }
  .field-row { grid-template-columns: 1fr; }
  .modal-card { border-radius: 1.5rem 1.5rem 0 0; position: fixed; bottom: 0; width: 100%; max-width: 100%; margin: 0; }
  .modal-overlay { align-items: flex-end; }
}
</style>
