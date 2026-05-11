<template>
  <div class="students-container">
    <div class="page-header">
      <div class="header-text">
        <h1>My Students</h1>
        <p>All your confirmed sessions</p>
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

    <!-- Top Stats -->
    <div class="student-stats">
      <div class="s-card bg-cream">
        <div class="s-info">
          <span class="s-label">Total Students</span>
          <h2 class="s-value">{{ totalStudents }}</h2>
          <span class="s-trend">All time</span>
        </div>
        <div class="s-icon-wrap"><svg viewBox="0 0 24 24" fill="none" stroke="#0f172a" stroke-width="2"><path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M23 21v-2a4 4 0 0 0-3-3.87"/><path d="M16 3.13a4 4 0 0 1 0 7.75"/></svg></div>
        <div class="s-progress-container"><div class="s-progress-bar"><div class="fill" style="width: 100%; background: #f59e0b;"></div></div></div>
      </div>
      <div class="s-card bg-mint">
        <div class="s-info">
          <span class="s-label">Active this week</span>
          <h2 class="s-value">{{ activeThisWeek }}</h2>
          <span class="s-trend trend-up">Last 7 days</span>
        </div>
        <div class="s-icon-wrap"><svg viewBox="0 0 24 24" fill="none" stroke="#0f172a" stroke-width="2"><polyline points="23 6 13.5 15.5 8.5 10.5 1 18"/><polyline points="17 6 23 6 23 12"/></svg></div>
        <div class="s-progress-container"><div class="s-progress-bar"><div class="fill" :style="{ width: (totalStudents ? (activeThisWeek / totalStudents * 100) : 0) + '%', background: '#10b981' }"></div></div></div>
      </div>
      <div class="s-card bg-lavender">
        <div class="s-info">
          <span class="s-label">Average Progress</span>
          <h2 class="s-value">{{ avgProgress }}%</h2>
          <span class="s-trend trend-up">Completion rate</span>
        </div>
        <div class="s-icon-wrap"><svg viewBox="0 0 24 24" fill="none" stroke="#0f172a" stroke-width="2"><line x1="18" y1="20" x2="18" y2="10"/><line x1="12" y1="20" x2="12" y2="4"/><line x1="6" y1="20" x2="6" y2="14"/></svg></div>
        <div class="s-progress-container"><div class="s-progress-bar"><div class="fill" :style="{ width: avgProgress + '%', background: '#1e3a8a' }"></div></div></div>
      </div>
    </div>

    <!-- Student List Card -->
    <div class="list-card">
      <div class="card-header">
        <h3>Student List</h3>
        <div class="header-actions">
          <button class="btn-action">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><polyline points="17 8 12 3 7 8"/><line x1="12" y1="3" x2="12" y2="15"/></svg>
            Export CSV
          </button>
          <div class="sort-dropdown">
            <span>Sort by:</span>
            <select>
              <option>Name (A-Z)</option>
              <option>Recent</option>
              <option>Progress</option>
            </select>
          </div>
        </div>
      </div>

      <div class="table-container">
        <table class="student-table">
          <thead>
            <tr>
              <th>STUDENT</th>
              <th>SUBJECT</th>
              <th>PROGRESS</th>
              <th>SESSIONS</th>
              <th>STATUS</th>
              <th></th>
            </tr>
          </thead>
          <tbody>
            <tr v-if="loading"><td colspan="6" style="text-align:center; padding: 2rem;">Loading students...</td></tr>
            <tr v-else-if="studentList.length === 0"><td colspan="6" style="text-align:center; padding: 2rem; color: #94a3b8;">No students have booked sessions with you yet.</td></tr>
            <tr v-for="s in studentList" :key="s.id" v-else>
              <td data-label="Student">
                <div class="student-cell">
                  <img :src="s.avatar" alt="Avatar" class="mini-avatar" />
                  <div class="cell-info">
                    <strong>{{ s.name }}</strong>
                    <span>{{ s.date }}</span>
                  </div>
                </div>
              </td>
              <td data-label="Subject"><span class="subject-tag">{{ s.subject }}</span></td>
              <td data-label="Progress">
                <div class="progress-cell">
                  <div class="progress-bar"><div class="fill" :style="{ width: s.progress + '%', background: s.pColor }"></div></div>
                  <span class="p-text">{{ s.progress }}%</span>
                </div>
              </td>
              <td data-label="Sessions" class="text-bold">{{ s.sessions }} sessions</td>
              <td data-label="Status"><span :class="['status-pill', s.status.toLowerCase()]">{{ s.status }}</span></td>
              <td data-label="Actions"><button class="btn-more" aria-label="More actions">⋮</button></td>
            </tr>
          </tbody>
        </table>
      </div>

      <!-- Pagination -->
      <div class="table-pagination">
        <span class="page-info">Showing {{ studentList.length }} student{{ studentList.length === 1 ? '' : 's' }}</span>
        <div class="page-controls">
          <button class="page-btn">❮</button>
          <button class="page-btn active">1</button>
          <button class="page-btn">❯</button>
        </div>
        <div class="rows-selector">
          <span>Rows per page</span>
          <select>
            <option>10</option>
            <option>20</option>
            <option>50</option>
          </select>
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

watch(() => props.profile, async (p) => {
  if (p && p.user) {
    await fetchBookings(p.user);
  }
}, { immediate: true });

async function fetchBookings(tutorId) {
  loading.value = true;
  try {
    const { data } = await bookingService.getTutorBookings(tutorId);
    bookings.value = Array.isArray(data) ? data : (data.results || []);
  } catch (e) {
    console.error('Failed to load students', e);
  } finally {
    loading.value = false;
  }
}

// Aggregate bookings by student
const studentList = computed(() => {
  const studentsMap = {};
  
  bookings.value.forEach(b => {
    if (!studentsMap[b.student]) {
      studentsMap[b.student] = {
        id: b.student,
        name: b.student_name || `Student #${b.student}`,
        subject: b.post_subject || 'Subject',
        sessions: 0,
        completed: 0,
        avatar: b.student_avatar_url || '/images/student_avatar.png',
        date: b.date ? new Date(b.date + 'T00:00:00').toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric' }) : 'Recently',
        lastDate: b.date
      };
    }
    studentsMap[b.student].sessions += 1;
    if (b.status === 'completed') {
      studentsMap[b.student].completed += 1;
    }
    // Update subject and date to most recent
    if (b.date && (!studentsMap[b.student].lastDate || b.date > studentsMap[b.student].lastDate)) {
      studentsMap[b.student].lastDate = b.date;
      studentsMap[b.student].date = new Date(b.date + 'T00:00:00').toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric' });
      studentsMap[b.student].subject = b.post_subject || 'Subject';
    }
    if (b.student_avatar_url) {
      studentsMap[b.student].avatar = b.student_avatar_url;
    }
  });

  return Object.values(studentsMap).map(s => {
    const progress = s.sessions > 0 ? Math.round((s.completed / s.sessions) * 100) : 0;
    return {
      ...s,
      progress: progress || 0,
      pColor: progress > 50 ? '#10b981' : '#f59e0b',
      status: 'Active'
    };
  });
});

const totalStudents = computed(() => studentList.value.length);
const activeThisWeek = computed(() => {
  const today = new Date();
  const lastWeek = new Date(today.getTime() - 7 * 24 * 60 * 60 * 1000).toISOString().split('T')[0];
  return studentList.value.filter(s => s.lastDate >= lastWeek).length;
});
const avgProgress = computed(() => {
  if (studentList.value.length === 0) return 0;
  const sum = studentList.value.reduce((acc, s) => acc + s.progress, 0);
  return Math.round(sum / studentList.value.length);
});
</script>

<style scoped>
.students-container {
  display: flex;
  flex-direction: column;
  gap: 2.5rem;
}

.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.page-header h1 {
  font-family: var(--font-display);
  font-size: 2rem;
  font-weight: 800;
  color: #0f172a;
  margin-bottom: 0.25rem;
}

.page-header p { color: #64748b; font-weight: 600; }

.header-actions {
  display: flex;
  gap: 0.75rem;
}

.header-btn {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  padding: 0.6rem 1.5rem;
  background: #ffffff;
  border: 1.5px solid #f1f5f9;
  border-radius: 2rem;
  font-size: 0.85rem;
  font-weight: 700;
  color: #0f172a;
  cursor: pointer;
  transition: all 0.2s;
  box-shadow: 0 2px 8px rgba(0,0,0,0.02);
}

.header-btn svg { width: 16px; height: 16px; }
.header-btn .chevron { width: 14px; height: 14px; margin-left: 0.25rem; }
.notification-btn svg { color: #f59e0b; }

/* Stats Grid */
.student-stats {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 1.5rem;
}

.s-card {
  padding: 1.5rem 1.5rem 2.5rem;
  border-radius: 1.5rem;
  display: flex;
  flex-direction: column;
  position: relative;
  box-shadow: 0 4px 6px -1px rgba(0,0,0,0.02);
  border: 1px solid #f1f5f9;
}

.bg-cream { background: #fffdf5; }
.bg-mint { background: #f6fdf9; }
.bg-lavender { background: #f5f9ff; }

.s-info .s-label { font-size: 0.75rem; font-weight: 800; color: #64748b; text-transform: uppercase; }
.s-info h2 { font-size: 2.2rem; font-weight: 800; color: #0f172a; margin: 0.5rem 0; }
.s-info .s-trend { font-size: 0.8rem; font-weight: 700; color: #10b981; }

.s-icon-wrap {
  position: absolute;
  top: 1.25rem;
  right: 1.25rem;
  width: 48px;
  height: 48px;
  background: #ffffff;
  border-radius: 14px;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 4px 12px rgba(0,0,0,0.06);
}

.s-icon-wrap svg { width: 24px; height: 24px; color: #0f172a; }

.s-progress-container {
  position: absolute;
  bottom: 1.5rem;
  left: 1.5rem;
  right: 1.5rem;
}

.s-progress-bar {
  width: 100%;
  height: 6px;
  background: rgba(0,0,0,0.05);
  border-radius: 10px;
  overflow: hidden;
}

.s-progress-bar .fill {
  height: 100%;
  border-radius: 10px;
}

/* List Card */
.list-card {
  background: #fff;
  border-radius: 1.5rem;
  padding: 2rem;
  border: 1px solid #f1f5f9;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 2rem;
}

.card-header h3 { font-size: 1.1rem; font-weight: 800; color: #0f172a; }

.header-actions { display: flex; gap: 1.5rem; align-items: center; }

.btn-action {
  background: #fff;
  border: 1.5px solid #f1f5f9;
  padding: 0.5rem 1rem;
  border-radius: 0.75rem;
  font-size: 0.8rem;
  font-weight: 700;
  color: #0f172a;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 0.5rem;
}
.btn-action svg { width: 14px; height: 14px; }

.sort-dropdown { display: flex; align-items: center; gap: 0.5rem; font-size: 0.85rem; font-weight: 600; color: #64748b; }
.sort-dropdown select { background: #f8fafc; border: none; padding: 0.4rem; border-radius: 0.5rem; font-weight: 700; outline: none; }

/* Table Section */
.table-container { overflow-x: auto; }
.student-table { width: 100%; border-collapse: collapse; }

.student-table th {
  text-align: left;
  padding: 1rem;
  font-size: 0.75rem;
  font-weight: 800;
  color: #94a3b8;
  border-bottom: 1px solid #f1f5f9;
}

.student-table td { padding: 1.25rem 1rem; border-bottom: 1px solid #f8fafc; }

.student-cell { display: flex; align-items: center; gap: 1rem; }
.mini-avatar { width: 44px; height: 44px; border-radius: 50%; object-fit: cover; }
.cell-info { display: flex; flex-direction: column; }
.cell-info strong { font-size: 0.9rem; color: #0f172a; }
.cell-info span { font-size: 0.75rem; color: #94a3b8; font-weight: 600; }

.subject-tag { font-size: 0.85rem; font-weight: 700; color: #1e3a8a; }

.progress-cell { display: flex; align-items: center; gap: 1rem; min-width: 140px; }
.progress-bar { flex: 1; height: 8px; background: #f1f5f9; border-radius: 4px; overflow: hidden; }
.fill { height: 100%; border-radius: 4px; }
.p-text { font-size: 0.8rem; font-weight: 800; color: #64748b; }

.text-bold { font-weight: 700; color: #475569; font-size: 0.85rem; }

.status-pill {
  padding: 0.25rem 0.75rem;
  border-radius: 0.5rem;
  font-size: 0.7rem;
  font-weight: 800;
  display: inline-block;
  text-align: center;
  min-width: 60px;
}

.status-pill.active { background: #ecfdf5; color: #059669; }
.status-pill.new { background: #eff6ff; color: #1e3a8a; }

.btn-more { background: none; border: none; font-size: 1.2rem; color: #94a3b8; cursor: pointer; }

/* Pagination */
.table-pagination {
  margin-top: 2rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0 1rem;
}

.page-info { font-size: 0.85rem; color: #94a3b8; font-weight: 600; }

.page-controls { display: flex; gap: 0.5rem; }

.page-btn {
  width: 34px;
  height: 34px;
  border: 1.5px solid #f1f5f9;
  background: #fff;
  border-radius: 0.5rem;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 0.85rem;
  font-weight: 800;
  color: #64748b;
  cursor: pointer;
}

.page-btn.active { background: #0f172a; color: #fff; border-color: #0f172a; }

.rows-selector { display: flex; align-items: center; gap: 0.75rem; font-size: 0.85rem; color: #64748b; font-weight: 600; }
.rows-selector select { background: #f8fafc; border: 1px solid #f1f5f9; padding: 0.4rem 0.75rem; border-radius: 0.5rem; font-weight: 700; outline: none; }

/* ── Responsive ── */
@media (max-width: 1024px) {
  .student-stats { grid-template-columns: 1fr; }
}

@media (max-width: 768px) {
  .students-container { gap: 1.25rem; overflow-x: hidden; }

  .page-header {
    flex-direction: column;
    align-items: stretch;
    gap: 1rem;
  }
  .page-header h1 { font-size: 1.35rem; line-height: 1.2; }
  .page-header p { font-size: 0.85rem; }

  .header-actions { flex-direction: column; width: 100%; gap: 0.5rem; }
  .header-btn { width: 100%; justify-content: center; padding: 0.65rem 1rem; border-radius: 1rem; }
  .date-btn span {
    min-width: 0;
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
  }

  .student-stats { grid-template-columns: 1fr; gap: 1rem; }
  .s-card { padding: 1.1rem 1.1rem 2.2rem; border-radius: 1.1rem; }
  .s-info h2 { font-size: 1.8rem; }

  .list-card { padding: 1.25rem 1.1rem; border-radius: 1.1rem; }
  .card-header { flex-direction: column; align-items: flex-start; gap: 0.75rem; }
  .card-header .header-actions { width: 100%; justify-content: space-between; gap: 0.75rem; flex-wrap: wrap; }
  .btn-action { width: 100%; justify-content: center; }
  .sort-dropdown { width: 100%; justify-content: space-between; }

  /* Table → stacked cards */
  .table-container { overflow: visible; }
  .student-table thead { display: none; }
  .student-table,
  .student-table tbody,
  .student-table tr,
  .student-table td { display: block; width: 100%; }

  .student-table tr {
    border: 1px solid #f1f5f9;
    border-radius: 1rem;
    margin-bottom: 0.9rem;
    overflow: hidden;
    background: #fff;
    box-shadow: 0 4px 10px rgba(15, 23, 42, 0.04);
  }
  .student-table td {
    padding: 0.85rem 1rem;
    border-bottom: 1px solid #f1f5f9;
    display: flex;
    align-items: flex-start;
    justify-content: space-between;
    gap: 1rem;
  }
  .student-table td:last-child { border-bottom: none; }
  .student-table td::before {
    content: attr(data-label);
    flex: 0 0 92px;
    font-size: 0.72rem;
    font-weight: 900;
    color: #94a3b8;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    padding-top: 2px;
  }

  .student-cell { gap: 0.75rem; }
  .mini-avatar { width: 40px; height: 40px; }
  .cell-info strong { font-size: 0.9rem; }

  .progress-cell { min-width: 0; width: 100%; justify-content: flex-end; gap: 0.75rem; }
  .progress-bar { max-width: 160px; }

  .btn-more { padding: 0.25rem 0.4rem; }

  .table-pagination {
    flex-direction: column;
    align-items: stretch;
    gap: 0.75rem;
    padding: 0;
  }
  .page-controls { justify-content: center; }
  .rows-selector { justify-content: space-between; }
}
</style>
