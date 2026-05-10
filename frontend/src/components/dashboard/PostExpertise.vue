<template>
  <div class="post-expertise-container">
    <div class="page-header desktop-only">
      <h1>Post Expertise</h1>
      <p>Create a tutoring listing and define available dates for each session.</p>
    </div>

    <!-- Location Warning -->
    <div v-if="!profileProvince" class="location-warning-banner">
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"/><line x1="12" y1="8" x2="12" y2="12"/><line x1="12" y1="16" x2="12.01" y2="16"/></svg>
      <div class="warn-content">
        <p><strong>Province Required</strong> — Please set your teaching province in your profile before publishing a listing.</p>
        <p class="warn-sub">This ensures students in your area can find your services.</p>
      </div>
    </div>

    <div class="split-layout">
      <!-- FORM -->
      <div class="form-side">
        <div class="form-card">
          <h3 class="section-title">📋 Listing Details</h3>

          <div class="form-group">
            <label>Subject Title <span class="req">*</span></label>
            <input v-model="form.title" placeholder="e.g. Advanced Algebra" />
          </div>
          <div class="form-row">
            <div class="form-group">
              <label>Category <span class="req">*</span></label>
              <select v-model="form.category">
                <option>Mathematics</option><option>Science</option><option>Music</option>
                <option>Languages</option><option>Sports</option><option>Arts</option>
              </select>
            </div>
            <div class="form-group">
              <label>Rate (₱/hr) <span class="req">*</span></label>
              <input type="number" v-model="form.rate" placeholder="700" />
            </div>
          </div>
          <div class="form-row">
            <div class="form-group">
              <label>Level</label>
              <select v-model="form.level">
                <option>Beginner</option><option>Intermediate</option>
                <option>Advanced</option><option>All Levels</option>
              </select>
            </div>
            <div class="form-group">
              <label>Total Sessions <span class="req">*</span></label>
              <input type="number" v-model.number="form.totalSessions" min="1" max="30" placeholder="e.g. 3" @change="initSessions" />
              <span class="hint">Number of sessions to complete this service</span>
            </div>
          </div>
          <div class="form-group">
            <label>Description <span class="req">*</span></label>
            <textarea v-model="form.description" rows="3" placeholder="Describe what students will learn..."></textarea>
          </div>
          
          <div class="form-group listing-location-info">
            <label>Listing Location</label>
            <div class="loc-static-field">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0z"/><circle cx="12" cy="10" r="3"/></svg>
              <span>{{ profileProvince ? profileProvince : 'Not set in profile' }}</span>
              <span class="loc-badge">Province</span>
            </div>
            <p class="field-hint">Listing location is automatically pulled from your profile's province.</p>
          </div>

          <div class="form-group">
            <label>Display Photo</label>
            <div class="photo-row">
              <div class="photo-box" @click="photoInput.click()">
                <img v-if="form.photoPreview" :src="form.photoPreview" class="photo-img" />
                <div v-else class="photo-placeholder">
                  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" width="28" height="28"><rect x="3" y="3" width="18" height="18" rx="2"/><circle cx="8.5" cy="8.5" r="1.5"/><polyline points="21 15 16 10 5 21"/></svg>
                  <span>Upload Photo</span>
                </div>
              </div>
              <div class="photo-guide"><strong>Guidelines</strong><ul><li>800×600 px recommended</li><li>JPG/PNG · max 5MB</li></ul></div>
            </div>
            <input type="file" ref="photoInput" hidden accept="image/*" @change="onPhoto" />
          </div>
        </div>

        <!-- SESSION SCHEDULE SECTION -->
        <div class="sessions-card" v-if="form.totalSessions > 0">
          <h3 class="section-title">📅 Session Availability</h3>
          <p class="section-desc">For each session, add one or more date/time options so students can choose when to attend.</p>

          <!-- Session Tabs -->
          <div class="session-tabs">
            <button
              v-for="n in form.totalSessions"
              :key="n"
              :class="['stab', { active: activeSession === n, done: sessionSlots[n]?.length > 0 }]"
              @click="activeSession = n"
            >
              Session {{ n }}
              <span class="stab-check" v-if="sessionSlots[n]?.length > 0">✓</span>
            </button>
          </div>

          <!-- Calendar for active session -->
          <div class="session-panel" v-if="activeSession">
            <p class="session-label">Setting availability for <strong>Session {{ activeSession }}</strong></p>

            <!-- Month nav -->
            <div class="cal-nav">
              <button type="button" @click="prevMonth">‹</button>
              <span>{{ monthLabel }}</span>
              <button type="button" @click="nextMonth">›</button>
            </div>

            <!-- Calendar grid -->
            <div class="cal-grid">
              <div class="cal-dow" v-for="d in ['Su','Mo','Tu','We','Th','Fr','Sa']" :key="d">{{ d }}</div>
              <div v-for="b in calendarBlanks" :key="'b'+b" class="cal-blank"></div>
              <button
                type="button"
                v-for="day in calendarDays"
                :key="day.date"
                :class="['cal-day', { past: day.past, 'has-slot': hasSlot(day.date), picking: pickingDate === day.date }]"
                :disabled="day.past"
                @click="openTimePicker(day.date)"
              >
                {{ day.n }}
                <span class="tick" v-if="hasSlot(day.date)">✓</span>
              </button>
            </div>

            <!-- Time picker -->
            <div class="time-picker" v-if="pickingDate">
              <div class="tp-header">
                <span>⏰ <strong>{{ pickingDate }}</strong></span>
                <button type="button" @click="pickingDate = null">✕</button>
              </div>
              <div class="tp-body">
                <div class="tfield"><label>Start</label><input type="time" v-model="slotForm.start" /></div>
                <div class="tfield"><label>End</label><input type="time" v-model="slotForm.end" /></div>
                <button type="button" class="btn-add" @click="addSlot">Add Slot</button>
              </div>
            </div>

            <!-- Slots for this session -->
            <div class="chips-area" v-if="sessionSlots[activeSession]?.length">
              <p class="chips-label">Available options for Session {{ activeSession }}:</p>
              <div class="chips">
                <div class="chip" v-for="(s, i) in sessionSlots[activeSession]" :key="i">
                  <span>📅 {{ s.date }} · {{ s.start_time }}–{{ s.end_time }}</span>
                  <button type="button" @click="removeSlot(activeSession, i)">✕</button>
                </div>
              </div>
            </div>
            <p class="empty-session" v-else>No slots added yet. Click a date above to add availability.</p>
          </div>
        </div>

        <div class="form-card" style="padding: 1.25rem;">
          <button class="btn-publish" @click="handlePublish" :disabled="loading || !profileProvince">
            {{ loading ? 'Publishing...' : 'Publish Listing →' }}
          </button>
        </div>
      </div>

      <!-- PREVIEW -->
      <div class="info-side desktop-only">
        <div class="preview-card">
          <h3>Preview</h3>
          <div class="listing-mock">
            <div class="mock-img">
              <img v-if="form.photoPreview" :src="form.photoPreview" />
              <div v-else class="mock-ph">📷</div>
            </div>
            <div class="mock-body">
              <p class="mock-title">{{ form.title || 'Your listing title' }}</p>
              <div class="mock-loc-badge" v-if="profileProvince">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0z"/><circle cx="12" cy="10" r="3"/></svg>
                {{ profileProvince }}
              </div>
              <p class="mock-sub">{{ form.category }} · {{ form.level }}</p>
              <p class="mock-sessions-badge">{{ form.totalSessions || 1 }} sessions · ₱{{ form.rate || '—' }}/hr</p>
              <p class="mock-desc">{{ form.description || 'Your description will appear here.' }}</p>
            </div>
          </div>
          <!-- Session slot summary -->
          <div class="slot-summary" v-if="form.totalSessions > 0">
            <p class="summary-title">📅 Session Slots</p>
            <div v-for="n in form.totalSessions" :key="n" class="summary-row">
              <span class="sn-badge">S{{ n }}</span>
              <span v-if="sessionSlots[n]?.length" class="sn-ok">{{ sessionSlots[n].length }} slot{{ sessionSlots[n].length > 1 ? 's' : '' }} set</span>
              <span v-else class="sn-missing">No slots yet</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, computed, onMounted, watch } from 'vue';
import { postService, sessionSlotService, profileService } from '../../services/api';
import { useToast } from '../../composables/useToast';
import { supabase } from '../../supabase';

const props = defineProps({ profile: Object });

const { showToast } = useToast();
const photoInput = ref(null);
const loading = ref(false);
const currentTutorId = ref(null);
const profileProvince = ref('');

const today = new Date();
const todayStr = today.toISOString().split('T')[0];
const viewYear = ref(today.getFullYear());
const viewMonth = ref(today.getMonth());
const pickingDate = ref(null);
const activeSession = ref(null);
// sessionSlots[sessionNumber] = [{date, start_time, end_time}, ...]
const sessionSlots = ref({});

const slotForm = reactive({ start: '09:00', end: '10:00' });

const form = reactive({
  title: '', category: 'Mathematics', rate: '', level: 'All Levels',
  totalSessions: '', description: '', photo: null, photoPreview: null
});

// Instantly populate from the profile prop passed by TutorDashboard
watch(() => props.profile, (p) => {
  if (p) {
    currentTutorId.value = p.user || p.id;
    profileProvince.value = p.province || '';
  }
}, { immediate: true });

onMounted(async () => {
  // Only fetch if prop wasn't available (fallback)
  if (!profileProvince.value) {
    try {
      const { data: { session } } = await supabase.auth.getSession();
      if (session?.user) {
        const { data } = await profileService.getProfileByEmail(session.user.email, 'tutor');
        const profiles = Array.isArray(data) ? data : (data.results || []);
        const profile = profiles[0];
        if (profile) {
          currentTutorId.value = profile.user;
          profileProvince.value = profile.province || '';
        }
      }
    } catch (e) {
      console.error('Failed to load tutor profile:', e);
    }
  }
});

function initSessions() {
  const n = parseInt(form.totalSessions) || 0;
  // Clear sessions that are now out of range
  Object.keys(sessionSlots.value).forEach(k => {
    if (parseInt(k) > n) delete sessionSlots.value[k];
  });
  activeSession.value = n > 0 ? 1 : null;
  pickingDate.value = null;
}

const monthLabel = computed(() =>
  new Date(viewYear.value, viewMonth.value, 1)
    .toLocaleDateString('en-US', { month: 'long', year: 'numeric' })
);
const calendarBlanks = computed(() =>
  new Date(viewYear.value, viewMonth.value, 1).getDay()
);
const calendarDays = computed(() => {
  const days = new Date(viewYear.value, viewMonth.value + 1, 0).getDate();
  return Array.from({ length: days }, (_, i) => {
    const n = i + 1;
    const date = `${viewYear.value}-${String(viewMonth.value+1).padStart(2,'0')}-${String(n).padStart(2,'0')}`;
    return { n, date, past: date < todayStr };
  });
});
function prevMonth() {
  if (viewMonth.value === 0) { viewMonth.value = 11; viewYear.value--; }
  else viewMonth.value--;
}
function nextMonth() {
  if (viewMonth.value === 11) { viewMonth.value = 0; viewYear.value++; }
  else viewMonth.value++;
}

function hasSlot(date) {
  return sessionSlots.value[activeSession.value]?.some(s => s.date === date);
}

function openTimePicker(date) {
  if (pickingDate.value === date) { pickingDate.value = null; return; }
  pickingDate.value = date;
  slotForm.start = '09:00';
  slotForm.end = '10:00';
}

function addSlot() {
  if (!slotForm.start || !slotForm.end || slotForm.end <= slotForm.start) {
    showToast('End time must be after start time', 'error'); return;
  }
  if (!sessionSlots.value[activeSession.value]) sessionSlots.value[activeSession.value] = [];
  const exists = sessionSlots.value[activeSession.value].some(
    s => s.date === pickingDate.value && s.start_time === slotForm.start
  );
  if (exists) { showToast('Slot already added', 'error'); return; }
  sessionSlots.value[activeSession.value].push({
    date: pickingDate.value,
    start_time: slotForm.start,
    end_time: slotForm.end
  });
  pickingDate.value = null;
}

function removeSlot(sessionNum, idx) {
  sessionSlots.value[sessionNum].splice(idx, 1);
}

function onPhoto(e) {
  const file = e.target.files[0];
  if (!file) return;
  form.photo = file;
  const reader = new FileReader();
  reader.onload = ev => { form.photoPreview = ev.target.result; };
  reader.readAsDataURL(file);
}

async function handlePublish() {
  if (!form.title || !form.rate || !form.description || !form.totalSessions) {
    showToast('Please fill all required fields', 'error'); return;
  }
  if (!profileProvince.value) {
    showToast('Please set your teaching province in your profile first', 'error'); return;
  }
  const n = parseInt(form.totalSessions);
  for (let i = 1; i <= n; i++) {
    if (!sessionSlots.value[i]?.length) {
      showToast(`Please add at least one slot for Session ${i}`, 'error');
      activeSession.value = i;
      return;
    }
  }
  loading.value = true;
  try {
    const fd = new FormData();
    fd.append('tutor_id', currentTutorId.value);
    fd.append('title', form.title);
    fd.append('subject', form.category);
    fd.append('hourly_rate', parseFloat(form.rate));
    fd.append('level', form.level);
    fd.append('total_sessions', n);
    fd.append('description', form.description);
    fd.append('is_published', 'true');
    if (form.photo) fd.append('photo', form.photo);

    const { data: post } = await postService.createPost(fd);

    // Save all session slots with their session_number
    const allSlots = [];
    for (let i = 1; i <= n; i++) {
      for (const s of (sessionSlots.value[i] || [])) {
        allSlots.push({ post: post.id, session_number: i, ...s });
      }
    }
    await sessionSlotService.bulkCreate(allSlots);

    showToast('Listing published!', 'success');
    Object.assign(form, { title:'', rate:'', description:'', totalSessions:'', photo:null, photoPreview:null });
    sessionSlots.value = {};
    activeSession.value = null;
  } catch (err) {
    console.error(err);
    showToast('Failed to publish listing', 'error');
  } finally {
    loading.value = false;
  }
}
</script>

<style scoped>
.post-expertise-container { display: flex; flex-direction: column; gap: 1.5rem; }
.page-header h1 { font-size: 2rem; font-weight: 800; color: #0f172a; }
.page-header p { color: #64748b; margin-top: 0.25rem; }

/* Location Warning */
.location-warning-banner {
  display: flex; gap: 1.25rem; align-items: center;
  background: #fff1f2; border: 1.5px solid #fecaca;
  padding: 1.25rem 1.75rem; border-radius: 1.25rem;
  color: #9f1239;
}
.location-warning-banner svg { width: 24px; height: 24px; flex-shrink: 0; color: #e11d48; }
.warn-content p { margin: 0; font-size: 0.95rem; }
.warn-sub { font-size: 0.8rem !important; opacity: 0.8; margin-top: 0.2rem !important; }

.split-layout { display: grid; grid-template-columns: 1fr 360px; gap: 2rem; align-items: start; }
.form-side { display: flex; flex-direction: column; gap: 1.25rem; }
.info-side { display: flex; flex-direction: column; gap: 1.25rem; }

.form-card, .sessions-card, .preview-card {
  background: #fff; border-radius: 1.25rem; padding: 1.75rem;
  border: 1px solid #f1f5f9; box-shadow: 0 4px 16px rgba(0,0,0,0.04);
  display: flex; flex-direction: column; gap: 1.25rem;
}
.section-title { font-size: 1rem; font-weight: 800; color: #0f172a; margin: 0; }
.section-desc { font-size: 0.82rem; color: #64748b; margin: -0.5rem 0 0; }

.form-group { display: flex; flex-direction: column; gap: 0.4rem; }
.form-row { display: grid; grid-template-columns: 1fr 1fr; gap: 1rem; }
label { font-size: 0.82rem; font-weight: 700; color: #374151; }
.req { color: #ef4444; }
.hint { font-size: 0.72rem; color: #94a3b8; }
input, select, textarea { padding: 0.7rem 1rem; border: 1.5px solid #e2e8f0; border-radius: 0.75rem; font-size: 0.9rem; color: #0f172a; outline: none; background: #fafafa; }
input:focus, select:focus, textarea:focus { border-color: #0f172a; background: #fff; }
textarea { resize: vertical; }

/* Location field */
.loc-static-field {
  display: flex; align-items: center; gap: 0.75rem;
  padding: 0.75rem 1rem; background: #f0f9ff;
  border: 1.5px solid #bae6fd; border-radius: 0.75rem;
  font-size: 0.95rem; font-weight: 700; color: #0369a1;
}
.loc-static-field svg { width: 18px; height: 18px; color: #0ea5e9; }
.loc-badge { font-size: 0.65rem; background: #0ea5e9; color: #fff; padding: 0.15rem 0.5rem; border-radius: 2rem; margin-left: auto; text-transform: uppercase; }

.photo-row { display: flex; gap: 1rem; align-items: flex-start; }
.photo-box { width: 100px; height: 80px; border: 2px dashed #cbd5e1; border-radius: 0.75rem; display: flex; align-items: center; justify-content: center; cursor: pointer; overflow: hidden; flex-shrink: 0; background: #f8fafc; }
.photo-img { width: 100%; height: 100%; object-fit: cover; }
.photo-placeholder { display: flex; flex-direction: column; align-items: center; gap: 0.3rem; color: #94a3b8; font-size: 0.68rem; }
.photo-guide ul { list-style: none; padding: 0; margin: 0.4rem 0 0; }
.photo-guide li { font-size: 0.7rem; color: #64748b; }

/* Session tabs */
.session-tabs { display: flex; flex-wrap: wrap; gap: 0.5rem; }
.stab {
  display: flex; align-items: center; gap: 0.35rem;
  padding: 0.45rem 1rem; border-radius: 2rem; border: 1.5px solid #e2e8f0;
  font-size: 0.8rem; font-weight: 700; cursor: pointer; background: #f8fafc; color: #64748b;
  transition: all 0.15s;
}
.stab.active { background: #0f172a; color: #fff; border-color: #0f172a; }
.stab.done { border-color: #10b981; color: #10b981; }
.stab.done.active { background: #0f172a; color: #fff; }
.stab-check { font-size: 0.75rem; }

/* Session panel */
.session-panel { display: flex; flex-direction: column; gap: 0.75rem; border-top: 1px solid #f1f5f9; padding-top: 1rem; }
.session-label { font-size: 0.82rem; color: #64748b; margin: 0; }

/* Calendar nav */
.cal-nav { display: flex; align-items: center; justify-content: space-between; background: #0f172a; border-radius: 0.65rem; padding: 0.55rem 1rem; }
.cal-nav span { color: #fff; font-weight: 700; font-size: 0.85rem; }
.cal-nav button { background: rgba(255,255,255,0.15); border: none; color: #fff; width: 26px; height: 26px; border-radius: 50%; cursor: pointer; font-size: 1.1rem; }

/* Calendar grid */
.cal-grid { display: grid; grid-template-columns: repeat(7,1fr); gap: 3px; }
.cal-dow { text-align: center; font-size: 0.62rem; font-weight: 700; color: #94a3b8; padding: 0.25rem 0; }
.cal-day {
  position: relative; aspect-ratio: 1; border: none; border-radius: 0.5rem;
  font-size: 0.75rem; font-weight: 600; cursor: pointer; background: #f8fafc; color: #0f172a;
  transition: all 0.15s; display: flex; align-items: center; justify-content: center;
}
.cal-day:hover:not(:disabled) { background: #e2e8f0; }
.cal-day:disabled { color: #cbd5e1; cursor: not-allowed; background: transparent; }
.cal-day.has-slot { background: #dcfce7; color: #16a34a; font-weight: 800; }
.cal-day.picking { background: #0f172a; color: #fff; }
.tick { position: absolute; top: 1px; right: 3px; font-size: 0.5rem; }

/* Time picker */
.time-picker { background: #eff6ff; border: 1.5px solid #bfdbfe; border-radius: 0.75rem; padding: 0.85rem; }
.tp-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.65rem; font-size: 0.82rem; color: #1e3a8a; }
.tp-header button { background: none; border: none; cursor: pointer; color: #94a3b8; }
.tp-body { display: flex; gap: 0.65rem; align-items: flex-end; }
.tfield { display: flex; flex-direction: column; gap: 0.25rem; flex: 1; }
.tfield label { font-size: 0.7rem; font-weight: 700; color: #374151; }
.tfield input { padding: 0.5rem 0.65rem; font-size: 0.82rem; }
.btn-add { background: #0f172a; color: #fff; border: none; border-radius: 0.6rem; padding: 0.55rem 1rem; font-weight: 700; font-size: 0.82rem; cursor: pointer; white-space: nowrap; }

/* Chips */
.chips-area { display: flex; flex-direction: column; gap: 0.4rem; }
.chips-label { font-size: 0.75rem; font-weight: 700; color: #374151; margin: 0; }
.chips { display: flex; flex-wrap: wrap; gap: 0.4rem; }
.chip { display: flex; align-items: center; gap: 0.4rem; background: #eff6ff; border: 1px solid #bfdbfe; border-radius: 2rem; padding: 0.3rem 0.65rem; font-size: 0.75rem; font-weight: 600; color: #1e3a8a; }
.chip button { background: none; border: none; cursor: pointer; color: #94a3b8; font-size: 0.75rem; }
.empty-session { font-size: 0.78rem; color: #94a3b8; text-align: center; padding: 1rem; }

/* Publish */
.btn-publish { width: 100%; background: #0f172a; color: #fff; border: none; padding: 0.9rem; border-radius: 0.75rem; font-weight: 800; font-size: 1rem; cursor: pointer; }
.btn-publish:disabled { opacity: 0.6; cursor: not-allowed; }

/* Preview */
.preview-card h3 { font-size: 1rem; font-weight: 800; color: #0f172a; }
.listing-mock { border-radius: 0.75rem; overflow: hidden; border: 1px solid #f1f5f9; }
.mock-img { height: 120px; background: #f1f5f9; display: flex; align-items: center; justify-content: center; }
.mock-img img { width: 100%; height: 100%; object-fit: cover; }
.mock-ph { font-size: 2.5rem; }
.mock-body { padding: 0.85rem; display: flex; flex-direction: column; gap: 0.25rem; }
.mock-title { font-weight: 800; color: #0f172a; font-size: 0.9rem; }
.mock-loc-badge { display: flex; align-items: center; gap: 0.3rem; font-size: 0.68rem; font-weight: 800; color: #0ea5e9; background: #f0f9ff; padding: 0.2rem 0.5rem; border-radius: 0.4rem; width: fit-content; margin-top: -2px; }
.mock-loc-badge svg { width: 12px; height: 12px; }
.mock-sub { font-size: 0.72rem; color: #64748b; }
.mock-sessions-badge { font-size: 0.72rem; font-weight: 700; color: #0f172a; background: #f1f5f9; display: inline-block; padding: 0.2rem 0.5rem; border-radius: 0.4rem; }
.mock-desc { font-size: 0.75rem; color: #64748b; line-height: 1.4; }

.slot-summary { border-top: 1px solid #f1f5f9; padding-top: 1rem; display: flex; flex-direction: column; gap: 0.5rem; }
.summary-title { font-size: 0.82rem; font-weight: 700; color: #374151; margin: 0; }
.summary-row { display: flex; align-items: center; gap: 0.6rem; }
.sn-badge { background: #0f172a; color: #fff; font-size: 0.65rem; font-weight: 800; padding: 0.2rem 0.5rem; border-radius: 0.35rem; }
.sn-ok { font-size: 0.78rem; font-weight: 700; color: #16a34a; }
.sn-missing { font-size: 0.78rem; color: #94a3b8; }

@media (max-width: 768px) {
  .split-layout { grid-template-columns: 1fr; }
  .desktop-only { display: none !important; }
  .form-row { grid-template-columns: 1fr; }
}
</style>
