<template>
  <div class="profile-page">

    <!-- ── Hero Banner ── -->
    <div class="profile-hero">
      <div class="hero-bg"></div>
      <div class="hero-content">
        <div class="avatar-ring">
          <div class="avatar-circle" :class="{ 'has-photo': !!avatarDisplayUrl }">
            <img v-if="avatarDisplayUrl" :src="avatarDisplayUrl" alt="" class="avatar-img" />
            <template v-else>{{ initials }}</template>
          </div>
          <div class="role-badge">Student</div>
        </div>
        <div class="hero-text">
          <h1>{{ form.first_name || 'Your' }} {{ form.last_name || 'Name' }}</h1>
          <p class="hero-sub">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0z"/><circle cx="12" cy="10" r="3"/></svg>
            {{ fullLocation || 'Location not set yet' }}
          </p>
        </div>
      </div>
    </div>

    <!-- ── Alert Banner ── -->
    <div class="location-alert" v-if="!form.municipality || !form.province">
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"/><line x1="12" y1="8" x2="12" y2="12"/><line x1="12" y1="16" x2="12.01" y2="16"/></svg>
      <span><strong>Complete your location</strong> — tutors in your area will appear in Discover</span>
    </div>

    <div class="profile-body">

      <!-- ── Personal Info ── -->
      <section class="profile-section">
        <div class="section-header">
          <div class="header-left">
            <div class="section-icon">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"/><circle cx="12" cy="7" r="4"/></svg>
            </div>
            <div>
              <h2>Personal Information</h2>
              <p>Your basic account details</p>
            </div>
          </div>
          <button v-if="!isEditing" class="btn-edit-toggle" @click="startEditing">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7"/><path d="M18.5 2.5a2.121 2.121 0 0 1 3 3L12 15l-4 1 1-4 9.5-9.5z"/></svg>
            Edit Profile
          </button>
        </div>

        <div v-if="!isEditing" class="info-display-grid">
          <div class="info-item">
            <label>Full Name</label>
            <p>{{ form.first_name }} {{ form.last_name }}</p>
          </div>
          <div class="info-item">
            <label>Email Address</label>
            <p>{{ form.email }}</p>
          </div>
          <div class="info-item">
            <label>Phone Number</label>
            <p>{{ form.phone || 'Not provided' }}</p>
          </div>
        </div>

        <div v-else class="form-grid">
          <div class="form-group">
            <label for="s-first-name">First Name</label>
            <input id="s-first-name" v-model="editForm.first_name" type="text" placeholder="Juan" />
          </div>
          <div class="form-group">
            <label for="s-last-name">Last Name</label>
            <input id="s-last-name" v-model="editForm.last_name" type="text" placeholder="Dela Cruz" />
          </div>
          <div class="form-group full-width">
            <label for="s-email">Email Address (Login Email)</label>
            <input id="s-email" :value="form.email" type="email" disabled class="disabled-input" />
            <span class="field-hint">This is the email address you used to login. It cannot be changed here.</span>
          </div>
          <div class="form-group">
            <label for="s-phone">Phone Number</label>
            <input id="s-phone" v-model="editForm.phone" type="tel" placeholder="+63 900 000 0000" />
          </div>
          <div class="form-group full-width">
            <label for="s-avatar">Profile photo</label>
            <input
              id="s-avatar"
              type="file"
              accept="image/jpeg,image/png,image/webp,image/gif"
              class="file-input"
              @change="onAvatarFileChange"
            />
            <span class="field-hint">Saved to your account. JPG, PNG, or WebP.</span>
          </div>
        </div>
      </section>

      <!-- ── Location (Primary) ── -->
      <section class="profile-section location-section">
        <div class="section-header">
          <div class="header-left">
            <div class="section-icon accent">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0z"/><circle cx="12" cy="10" r="3"/></svg>
            </div>
            <div>
              <h2>Your Location <span class="required-badge">Required</span></h2>
              <p>Tutors near you will appear in your Discover feed</p>
            </div>
          </div>
        </div>

        <div v-if="!isEditing" class="info-display-grid">
          <div class="info-item">
            <label>Barangay</label>
            <p>{{ form.barangay || 'Not set' }}</p>
          </div>
          <div class="info-item">
            <label>Municipality</label>
            <p>{{ form.municipality || 'Not set' }}</p>
          </div>
          <div class="info-item">
            <label>Province</label>
            <p>{{ form.province || 'Not set' }}</p>
          </div>
        </div>

        <div v-else class="form-grid">
          <div class="form-group">
            <label for="s-barangay">Barangay</label>
            <input id="s-barangay" v-model="editForm.barangay" type="text" placeholder="e.g. Brgy. 123" />
          </div>
          <div class="form-group">
            <label for="s-municipality">City / Municipality</label>
            <input id="s-municipality" v-model="editForm.municipality" type="text" placeholder="e.g. Quezon City" />
          </div>
          <div class="form-group full-width">
            <label for="s-province">Province</label>
            <input id="s-province" v-model="editForm.province" type="text" placeholder="e.g. Metro Manila" />
          </div>
          <span class="field-hint loc-hint">📍 Accurate location helps us find tutors closest to you.</span>
        </div>
      </section>

      <!-- ── Bio ── -->
      <section class="profile-section">
        <div class="section-header">
          <div class="header-left">
            <div class="section-icon">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/><line x1="16" y1="13" x2="8" y2="13"/><line x1="16" y1="17" x2="8" y2="17"/></svg>
            </div>
            <div>
              <h2>About You</h2>
              <p>Tell tutors a little about yourself</p>
            </div>
          </div>
        </div>

        <div v-if="!isEditing" class="info-display-full">
           <label>Short Bio</label>
           <p class="bio-text">{{ form.bio || 'Tell tutors a little about yourself and your learning goals!' }}</p>
        </div>

        <div v-else class="form-group full-width">
          <label for="s-bio">Short Bio</label>
          <textarea id="s-bio" v-model="editForm.bio" rows="4" placeholder="e.g. I'm a Grade 11 student looking for help in Math and Sciences..."></textarea>
          <span class="char-count">{{ editForm.bio?.length || 0 }} / 300</span>
        </div>
      </section>

      <!-- ── Actions ── -->
      <div class="save-row" v-if="isEditing">
        <button class="btn-cancel" @click="cancelEditing" :disabled="saving">Cancel</button>
        <button class="btn-save" @click="saveProfile" :disabled="saving">
          <span v-if="saving" class="spinner"></span>
          <svg v-else viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><path d="M19 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h11l5 5v11a2 2 0 0 1-2 2z"/><polyline points="17 21 17 13 7 13 7 21"/><polyline points="7 3 7 8 15 8"/></svg>
          {{ saving ? 'Saving...' : 'Save Profile' }}
        </button>
      </div>

    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted, watch } from 'vue';
import { supabase } from '../../supabase';
import { profileService } from '../../services/api';
import { useToast } from '../../composables/useToast';

const props = defineProps({ profile: Object });
const emit = defineEmits(['profile-updated']);
const { showToast } = useToast();

const isEditing = ref(false);
const saving = ref(false);
const djangoProfileId = ref(null);

const form = ref({
  first_name: '',
  last_name: '',
  email: '',
  phone: '',
  bio: '',
  barangay: '',
  municipality: '',
  province: '',
  avatar_url: '',
});

const avatarFile = ref(null);
const avatarPreviewUrl = ref('');

const editForm = ref({});

const initials = computed(() => {
  const f = form.value.first_name?.charAt(0) || '?';
  const l = form.value.last_name?.charAt(0) || '';
  return (f + l).toUpperCase();
});

const avatarDisplayUrl = computed(() => {
  if (isEditing.value && avatarPreviewUrl.value) return avatarPreviewUrl.value;
  return form.value.avatar_url || '';
});

function clearAvatarSelection() {
  if (avatarPreviewUrl.value && avatarPreviewUrl.value.startsWith('blob:')) {
    URL.revokeObjectURL(avatarPreviewUrl.value);
  }
  avatarPreviewUrl.value = '';
  avatarFile.value = null;
}

function onAvatarFileChange(ev) {
  const input = ev.target;
  const file = input.files?.[0];
  if (avatarPreviewUrl.value && avatarPreviewUrl.value.startsWith('blob:')) {
    URL.revokeObjectURL(avatarPreviewUrl.value);
  }
  avatarPreviewUrl.value = '';
  avatarFile.value = file || null;
  if (file) {
    avatarPreviewUrl.value = URL.createObjectURL(file);
  }
  input.value = '';
}

const fullLocation = computed(() => {
  const parts = [form.value.barangay, form.value.municipality, form.value.province].filter(Boolean);
  return parts.join(', ');
});

const startEditing = () => {
  clearAvatarSelection();
  editForm.value = JSON.parse(JSON.stringify(form.value));
  isEditing.value = true;
};

const cancelEditing = () => {
  clearAvatarSelection();
  isEditing.value = false;
};

// Load immediately from the profile prop (passed from dashboard which fetches from Django)
const populateFromProp = (p) => {
  if (!p) return;
  form.value.first_name   = p.first_name   || '';
  form.value.last_name    = p.last_name    || '';
  form.value.email        = p.email        || '';
  form.value.phone        = p.phone        || '';
  form.value.bio          = p.bio          || '';
  form.value.barangay     = p.barangay     || '';
  form.value.municipality = p.municipality || '';
  form.value.province     = p.province     || '';
  form.value.avatar_url   = p.avatar_url   || '';
};

watch(() => props.profile, (newProfile) => {
  populateFromProp(newProfile);
}, { immediate: true });

// Get Django profile ID for save operations
const loadDjangoProfileId = async () => {
  const { data: { session } } = await supabase.auth.getSession();
  if (!session?.user) return;
  try {
    const { data } = await profileService.getProfileByEmail(session.user.email, 'student');
    const profiles = Array.isArray(data) ? data : (data.results || []);
    if (profiles[0]) {
      djangoProfileId.value = profiles[0].id;
      if (profiles[0].email) {
        form.value.email = profiles[0].email;
      }
      if (profiles[0].avatar_url) {
        form.value.avatar_url = profiles[0].avatar_url;
      }
    }
  } catch (e) {
    console.warn('Could not get Django profile ID:', e);
  }
};

onUnmounted(() => {
  clearAvatarSelection();
});

onMounted(() => {
  loadDjangoProfileId();
});

const saveProfile = async () => {
  saving.value = true;
  try {
    // 1. Update Supabase auth metadata
    await supabase.auth.updateUser({
      data: { first_name: editForm.value.first_name, last_name: editForm.value.last_name }
    });

    // 2. Update Supabase profiles table
    const { data: { session } } = await supabase.auth.getSession();
    if (session?.user) {
      await supabase.from('profiles').upsert({
        id: session.user.id,
        first_name: editForm.value.first_name,
        last_name: editForm.value.last_name,
      }, { onConflict: 'id' });
    }

    // 3. Update Django profile
    if (!djangoProfileId.value) {
      // Fallback: try to re-fetch/create via the backend auto-creation logic
      const { data } = await profileService.getProfileByEmail(session.user.email, 'student');
      const profiles = Array.isArray(data) ? data : (data.results || []);
      if (profiles[0]) djangoProfileId.value = profiles[0].id;
    }

    let newAvatarUrl = null;
    if (djangoProfileId.value) {
      const payload = {
        first_name: editForm.value.first_name,
        last_name: editForm.value.last_name,
        phone: editForm.value.phone,
        bio: editForm.value.bio,
        barangay: editForm.value.barangay,
        municipality: editForm.value.municipality,
        province: editForm.value.province,
      };
      if (avatarFile.value) {
        const fd = new FormData();
        Object.entries(payload).forEach(([k, v]) => fd.append(k, v ?? ''));
        fd.append('avatar', avatarFile.value);
        const { data } = await profileService.updateProfile(djangoProfileId.value, fd);
        newAvatarUrl = data?.avatar_url ?? null;
      } else {
        await profileService.updateProfile(djangoProfileId.value, payload);
      }
    }

    clearAvatarSelection();
    form.value = JSON.parse(JSON.stringify(editForm.value));
    if (newAvatarUrl != null) {
      form.value.avatar_url = newAvatarUrl;
    }
    isEditing.value = false;

    emit('profile-updated', { ...form.value });
    showToast('Profile saved successfully! 🎉', 'success');
  } catch (err) {
    console.error('Save profile error:', err);
    showToast('Failed to save profile. Please try again.', 'error');
  } finally {
    saving.value = false;
  }
};
</script>

<style scoped>
/* Styles remain identical */
.profile-page { display: flex; flex-direction: column; gap: 0; max-width: 820px; margin: 0 auto; }
.profile-hero { position: relative; border-radius: 1.5rem; overflow: hidden; margin-bottom: 1.25rem; }
.hero-bg { position: absolute; inset: 0; background: linear-gradient(135deg, #07193f 0%, #1a3a6e 50%, #0d2859 100%); }
.hero-content { position: relative; display: flex; align-items: center; gap: 1.5rem; padding: 2rem 2.5rem; }
.avatar-ring { position: relative; flex-shrink: 0; }
.avatar-circle { width: 80px; height: 80px; border-radius: 50%; background: linear-gradient(135deg, #ffc107, #f59e0b); display: flex; align-items: center; justify-content: center; font-size: 1.8rem; font-weight: 900; color: #0f172a; border: 3px solid rgba(255,255,255,0.25); box-shadow: 0 8px 24px rgba(0,0,0,0.25); }
.avatar-circle.has-photo { padding: 0; background: #0f172a; overflow: hidden; }
.avatar-img { width: 100%; height: 100%; object-fit: cover; display: block; }
.file-input { padding: 0.5rem 0; font-size: 0.88rem; }
.role-badge { position: absolute; bottom: -4px; right: -4px; background: #ffc107; color: #0f172a; font-size: 0.6rem; font-weight: 900; padding: 0.2rem 0.5rem; border-radius: 2rem; text-transform: uppercase; letter-spacing: 0.05em; border: 2px solid white; }
.hero-text h1 { font-size: 1.6rem; font-weight: 900; color: #ffffff; margin: 0 0 0.4rem; }
.hero-sub { display: flex; align-items: center; gap: 0.4rem; font-size: 0.9rem; color: rgba(255,255,255,0.7); margin: 0; }
.hero-sub svg { width: 14px; height: 14px; }
.location-alert { display: flex; align-items: center; gap: 0.75rem; background: linear-gradient(90deg, #fffbeb, #fef9e7); border: 1.5px solid #fcd34d; border-radius: 1rem; padding: 0.85rem 1.25rem; margin-bottom: 1.25rem; font-size: 0.88rem; color: #78350f; }
.location-alert svg { width: 18px; height: 18px; color: #f59e0b; flex-shrink: 0; }
.profile-body { display: flex; flex-direction: column; gap: 1.25rem; }
.profile-section { background: #ffffff; border-radius: 1.25rem; padding: 1.75rem; border: 1px solid #f1f5f9; box-shadow: 0 2px 12px rgba(0,0,0,0.03); }
.location-section { border: 1.5px solid #fcd34d; background: linear-gradient(135deg, #fffbeb 0%, #ffffff 60%); }
.section-header { display: flex; align-items: center; justify-content: space-between; margin-bottom: 1.5rem; }
.header-left { display: flex; align-items: flex-start; gap: 1rem; }
.section-icon { width: 42px; height: 42px; background: #f1f5f9; border-radius: 0.75rem; display: flex; align-items: center; justify-content: center; flex-shrink: 0; }
.section-icon svg { width: 20px; height: 20px; color: #475569; }
.section-icon.accent { background: linear-gradient(135deg, #fef3c7, #fde68a); }
.section-icon.accent svg { color: #d97706; }
.header-left h2 { font-size: 1rem; font-weight: 800; color: #0f172a; margin: 0 0 0.2rem; display: flex; align-items: center; gap: 0.5rem; }
.header-left p { font-size: 0.82rem; color: #94a3b8; margin: 0; }
.btn-edit-toggle { display: flex; align-items: center; gap: 0.5rem; padding: 0.6rem 1.2rem; background: #f8fafc; border: 1.5px solid #e2e8f0; border-radius: 0.75rem; color: #475569; font-size: 0.85rem; font-weight: 800; cursor: pointer; transition: all 0.2s; }
.btn-edit-toggle:hover { background: #0f172a; color: #fff; border-color: #0f172a; }
.btn-edit-toggle svg { width: 16px; height: 16px; }
.info-display-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(200px, 1fr)); gap: 1.5rem; }
.info-item label { display: block; font-size: 0.75rem; font-weight: 800; color: #94a3b8; text-transform: uppercase; letter-spacing: 0.05em; margin-bottom: 0.4rem; }
.info-item p { font-size: 0.95rem; font-weight: 700; color: #0f172a; margin: 0; }
.info-display-full label { display: block; font-size: 0.75rem; font-weight: 800; color: #94a3b8; text-transform: uppercase; letter-spacing: 0.05em; margin-bottom: 0.5rem; }
.bio-text { font-size: 0.95rem; line-height: 1.6; color: #334155; margin: 0; background: #f8fafc; padding: 1.25rem; border-radius: 1rem; border: 1px solid #f1f5f9; }
.form-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 1rem; }
.form-group { display: flex; flex-direction: column; gap: 0.4rem; }
.form-group.full-width { grid-column: 1 / -1; }
.form-group label { font-size: 0.82rem; font-weight: 700; color: #475569; text-transform: uppercase; letter-spacing: 0.05em; }
.form-group input, .form-group textarea { padding: 0.75rem 1rem; border: 1.5px solid #e8ecf4; border-radius: 0.75rem; font-size: 0.92rem; color: #0f172a; background: #f8fafc; outline: none; transition: border-color 0.2s, box-shadow 0.2s; font-family: inherit; }
.form-group input:focus, .form-group textarea:focus { border-color: #0f172a; box-shadow: 0 0 0 3px rgba(15,23,42,0.06); background: #ffffff; }
.disabled-input { opacity: 0.55; cursor: not-allowed; }
.form-group textarea { resize: vertical; min-height: 100px; }
.field-hint { font-size: 0.75rem; color: #94a3b8; }
.loc-hint { color: #d97706; font-weight: 600; margin-top: 0.5rem; display: block; }
.char-count { font-size: 0.72rem; color: #94a3b8; text-align: right; }
.save-row { display: flex; align-items: center; justify-content: flex-end; gap: 1rem; padding: 0.5rem 0 1rem; }
.btn-cancel { padding: 0.85rem 1.5rem; background: transparent; border: 1.5px solid #e2e8f0; border-radius: 0.85rem; color: #64748b; font-weight: 800; cursor: pointer; transition: all 0.2s; }
.btn-cancel:hover:not(:disabled) { background: #f1f5f9; color: #0f172a; }
.btn-save { display: flex; align-items: center; gap: 0.6rem; padding: 0.85rem 2rem; background: linear-gradient(135deg, #0f172a, #1e293b); color: #ffffff; border: none; border-radius: 0.85rem; font-size: 0.92rem; font-weight: 800; cursor: pointer; transition: all 0.2s; box-shadow: 0 4px 16px rgba(15,23,42,0.25); }
.btn-save:hover:not(:disabled) { transform: translateY(-2px); box-shadow: 0 8px 24px rgba(15,23,42,0.3); }
.btn-save:disabled { opacity: 0.6; cursor: not-allowed; }
.btn-save svg { width: 18px; height: 18px; }
.spinner { width: 16px; height: 16px; border: 2px solid rgba(255,255,255,0.3); border-top-color: white; border-radius: 50%; animation: spin 0.7s linear infinite; flex-shrink: 0; }
@keyframes spin { to { transform: rotate(360deg); } }
@media (max-width: 768px) { .hero-content { padding: 1.5rem; gap: 1rem; } .avatar-circle { width: 64px; height: 64px; font-size: 1.4rem; } .hero-text h1 { font-size: 1.25rem; } .profile-section { padding: 1.25rem; } .form-grid { grid-template-columns: 1fr; } .save-row { flex-direction: column; align-items: stretch; } .btn-save, .btn-cancel { justify-content: center; width: 100%; } }
</style>
