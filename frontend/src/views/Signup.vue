<template>
  <div class="page">
    <!-- LEFT: Branding -->
    <div class="panel panel--brand desktop-only">
      <div class="brand-bg"></div>
      <div class="brand-orb orb--1"></div>
      <div class="brand-orb orb--2"></div>
      <div class="brand-logo">
        <img src="/images/TURO_LOGO_WITH_MEANING.png" alt="TURO Logo" class="main-logo" />
      </div>
      <div class="brand-body">
        <h2>Start your learning<br />journey today.</h2>
        <p>Join thousands of students and tutors in TURO — the Philippines' modern tutoring platform.</p>
        <div class="feature-list">
          <div class="feature-item" v-for="f in features" :key="f.icon">
            <span class="feature-icon">{{ f.icon }}</span>
            <div><strong>{{ f.title }}</strong><span>{{ f.sub }}</span></div>
          </div>
        </div>
      </div>
      <p class="brand-footer">Already have an account? <router-link to="/login/student" class="brand-link">Sign in ➔</router-link></p>
    </div>

    <!-- RIGHT: Form -->
    <div class="panel panel--form">
      <div class="mobile-only mobile-header">
        <img src="/images/TURO_LOGO_WITH_MEANING.png" alt="TURO" class="mobile-logo-img" />
      </div>

      <div class="form-wrap animate-scale-in">
        <div class="form-header">
          <h1>Create your account</h1>
          <p>Fill in your details below to get started</p>
          <!-- Step indicator -->
          <div class="step-indicator">
            <div :class="['step-dot', currentStep >= 1 ? 'active' : '']">1</div>
            <div class="step-line"></div>
            <div :class="['step-dot', currentStep >= 2 ? 'active' : '']">2</div>
            <template v-if="isMinor">
              <div class="step-line"></div>
              <div :class="['step-dot', currentStep >= 3 ? 'active' : '']">3</div>
            </template>
          </div>
        </div>

        <form @submit.prevent="handleSubmit" class="signup-form">

          <!-- ── STEP 1: Personal Info + Birthday ── -->
          <div v-show="currentStep === 1" class="step-block">
            <div class="role-group">
              <button class="role-btn" :class="{ 'role-btn--active': selectedRole === 'student' }" @click="selectedRole = 'student'" type="button">
                <span class="role-icon">🎓</span>
                <div><strong>Student</strong><small>Learn</small></div>
              </button>
              <button class="role-btn" :class="{ 'role-btn--active': selectedRole === 'tutor' }" @click="selectedRole = 'tutor'" type="button">
                <span class="role-icon">📖</span>
                <div><strong>Tutor</strong><small>Teach</small></div>
              </button>
            </div>
            <p class="role-note">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"/><path d="M12 8v4M12 16h.01"/></svg>
              Your role <strong>cannot be changed</strong> after sign up.
            </p>

            <div class="grid-row">
              <div class="field"><label>First Name *</label><input type="text" v-model="form.firstName" required /></div>
              <div class="field"><label>Last Name *</label><input type="text" v-model="form.lastName" required /></div>
            </div>
            <div class="grid-row">
              <div class="field"><label>Middle Name</label><input type="text" v-model="form.middleName" /></div>
              <div class="field"><label>Name Extension</label><input type="text" v-model="form.nameExtension" placeholder="Jr., Sr., III" /></div>
            </div>

            <!-- Birthday -->
            <div class="field">
              <label>Date of Birth *</label>
              <input type="date" v-model="form.birthday" :max="maxBirthdayDate" required />
              <span v-if="form.birthday && isMinor" class="minor-badge">
                🔒 Minor detected — guardian consent required
              </span>
            </div>

            <button type="button" class="btn-submit" @click="goToStep2">Proceed →</button>
            <p class="signin-link">Already have an account? <router-link to="/login/student" class="lnk">Sign in</router-link></p>
          </div>

          <!-- ── STEP 2: Account Credentials ── -->
          <div v-show="currentStep === 2" class="step-block">
            <div class="field"><label>Email Address *</label><input type="email" v-model="form.email" required /></div>
            <div class="field">
              <label>Password *</label>
              <div class="pw-wrap">
                <input :type="showPw ? 'text' : 'password'" v-model="form.password" required />
                <button type="button" class="pw-toggle" @click="showPw = !showPw">{{ showPw ? '🙈' : '👁️' }}</button>
              </div>
            </div>
            <div class="field">
              <label>Confirm Password *</label>
              <input :type="showPw ? 'text' : 'password'" v-model="form.confirmPassword" required />
            </div>

            <label class="terms-row">
              <input type="checkbox" v-model="agreedToTerms" />
              <span>I agree to the <a href="#" class="lnk">Terms</a> and <a href="#" class="lnk">Privacy Policy</a></span>
            </label>

            <div class="btn-row">
              <button type="button" class="btn-back" @click="currentStep = 1">← Back</button>
              <button v-if="isMinor" type="button" class="btn-submit flex-1" @click="goToStep3">Next: Guardian Info →</button>
              <button v-else type="submit" class="btn-submit flex-1" :disabled="loading || !agreedToTerms">
                <span v-if="loading">Creating...</span>
                <span v-else>Create Account ➔</span>
              </button>
            </div>
            <p class="signin-link">Already have an account? <router-link to="/login/student" class="lnk">Sign in</router-link></p>
          </div>

          <!-- ── STEP 3 (Minor only): Guardian Info ── -->
          <div v-show="currentStep === 3" class="step-block">
            <div class="guardian-banner">
              <span class="guardian-icon">👨‍👩‍👧</span>
              <div>
                <strong>Guardian Consent Required</strong>
                <p>Since you are a minor, a parent or guardian must provide their identification.</p>
              </div>
            </div>

            <div class="field">
              <label>Guardian Full Name *</label>
              <input type="text" v-model="form.guardianName" placeholder="Parent or legal guardian's full name" required />
            </div>

            <div class="field">
              <label>Guardian ID Type *</label>
              <select v-model="form.guardianIdType" required>
                <option value="" disabled>Select ID type</option>
                <option value="Philippine National ID">Philippine National ID (PhilSys)</option>
                <option value="Passport">Passport</option>
                <option value="Driver's License">Driver's License</option>
                <option value="SSS ID">SSS ID</option>
                <option value="GSIS ID">GSIS ID</option>
                <option value="PRC ID">PRC ID</option>
                <option value="Voter's ID">Voter's ID</option>
                <option value="Postal ID">Postal ID</option>
                <option value="PhilHealth ID">PhilHealth ID</option>
                <option value="Senior Citizen ID">Senior Citizen ID</option>
                <option value="OFW ID">OFW ID</option>
                <option value="Barangay ID">Barangay ID</option>
              </select>
            </div>

            <div class="field">
              <label>Upload Guardian ID Photo *</label>
              <div class="upload-zone" @click="$refs.guardianIdInput.click()" :class="{ 'has-file': guardianIdPreview }">
                <img v-if="guardianIdPreview" :src="guardianIdPreview" alt="Guardian ID Preview" class="id-preview" />
                <div v-else class="upload-placeholder">
                  <span class="upload-icon">📷</span>
                  <strong>Click to upload</strong>
                  <small>JPG, PNG, or PDF — clear photo of the ID</small>
                </div>
              </div>
              <input ref="guardianIdInput" type="file" accept="image/*,.pdf" @change="onGuardianIdChange" class="hidden-input" />
              <p v-if="guardianIdFile" class="file-name">✅ {{ guardianIdFile.name }}</p>
            </div>

            <div class="btn-row">
              <button type="button" class="btn-back" @click="currentStep = 2">← Back</button>
              <button type="submit" class="btn-submit flex-1" :disabled="loading || !agreedToTerms || !form.guardianName || !form.guardianIdType || !guardianIdFile">
                <span v-if="loading">Creating Account...</span>
                <span v-else>Create Account ➔</span>
              </button>
            </div>
          </div>

        </form>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, computed } from 'vue';
import { useRouter } from 'vue-router';
import { supabase } from '../supabase';
import { useToast } from '../composables/useToast';
import { profileService } from '../services/api';

const router = useRouter();
const { showToast } = useToast();

const selectedRole = ref('student');
const agreedToTerms = ref(false);
const loading = ref(false);
const currentStep = ref(1);
const showPw = ref(false);
const guardianIdFile = ref(null);
const guardianIdPreview = ref('');
const guardianIdInput = ref(null);

const form = reactive({
  firstName: '',
  lastName: '',
  middleName: '',
  nameExtension: '',
  birthday: '',
  email: '',
  password: '',
  confirmPassword: '',
  guardianName: '',
  guardianIdType: '',
});

const features = [
  { title: 'Expert Tutors', sub: 'Verified and passionate', icon: '🎓' },
  { title: 'Flexible Schedule', sub: 'Book on your terms', icon: '📅' },
  { title: 'Live Sessions', sub: 'Real-time interaction', icon: '💬' },
];

// Max date = today (can't be born in the future)
const maxBirthdayDate = computed(() => new Date().toISOString().split('T')[0]);

const isMinor = computed(() => {
  if (!form.birthday) return false;
  const birth = new Date(form.birthday);
  const today = new Date();
  let age = today.getFullYear() - birth.getFullYear();
  const m = today.getMonth() - birth.getMonth();
  if (m < 0 || (m === 0 && today.getDate() < birth.getDate())) age--;
  return age < 18;
});

function goToStep2() {
  if (!form.firstName || !form.lastName) {
    showToast('Please fill in your first and last name.', 'error');
    return;
  }
  if (!form.birthday) {
    showToast('Please enter your date of birth.', 'error');
    return;
  }
  currentStep.value = 2;
}

function goToStep3() {
  if (form.password !== form.confirmPassword) {
    showToast('Passwords do not match.', 'error');
    return;
  }
  if (!agreedToTerms.value) {
    showToast('You must agree to the Terms and Privacy Policy.', 'error');
    return;
  }
  currentStep.value = 3;
}

function onGuardianIdChange(e) {
  const file = e.target.files[0];
  if (!file) return;
  guardianIdFile.value = file;
  if (file.type.startsWith('image/')) {
    const reader = new FileReader();
    reader.onload = (ev) => { guardianIdPreview.value = ev.target.result; };
    reader.readAsDataURL(file);
  } else {
    guardianIdPreview.value = '';
  }
}

async function handleSubmit() {
  if (form.password !== form.confirmPassword) {
    showToast('Passwords do not match.', 'error');
    return;
  }
  if (!agreedToTerms.value) {
    showToast('You must agree to the Terms and Privacy Policy.', 'error');
    return;
  }
  if (isMinor.value && (!form.guardianName || !form.guardianIdType || !guardianIdFile.value)) {
    showToast('Please complete all guardian information.', 'error');
    return;
  }
  if (loading.value) return;
  loading.value = true;

  try {
    const derivedUsername = String(form.email || '').split('@')[0] || 'user';

    const { data: authData, error: authError } = await supabase.auth.signUp({
      email: form.email,
      password: form.password,
      options: {
        data: {
          first_name: form.firstName,
          last_name: form.lastName,
          middle_name: form.middleName || '',
          name_extension: form.nameExtension || '',
        },
      },
    });
    if (authError) throw authError;

    if (authData.user) {
      const { error: profileError } = await supabase.from('profiles').insert({
        id: authData.user.id,
        first_name: form.firstName,
        last_name: form.lastName,
        username: derivedUsername,
        role: selectedRole.value,
      });
      if (profileError) throw profileError;

      // Sync to Django profile
      try {
        const { data } = await profileService.getProfileByEmail(form.email, selectedRole.value);
        const profiles = Array.isArray(data) ? data : (data.results || []);
        if (profiles.length > 0) {
          const pid = profiles[0].id;
          const patch = new FormData();
          patch.append('first_name', form.firstName);
          patch.append('last_name', form.lastName);
          patch.append('middle_name', form.middleName || '');
          patch.append('name_extension', form.nameExtension || '');
          patch.append('role', selectedRole.value);
          patch.append('birthday', form.birthday);
          if (isMinor.value) {
            patch.append('guardian_name', form.guardianName);
            patch.append('guardian_id_type', form.guardianIdType);
            if (guardianIdFile.value) {
              patch.append('guardian_id_photo', guardianIdFile.value);
            }
          }
          await profileService.updateProfile(pid, patch);
        }
      } catch (err) {
        console.error('Django profile sync failed:', err);
        showToast('Account created but profile sync failed. Please update from My Profile.', 'warning');
      }

      if (authData.session) {
        showToast('Account created successfully! Welcome to TURO.', 'success');
        router.push(selectedRole.value === 'tutor' ? '/dashboard/tutor' : '/dashboard/student');
      } else {
        showToast('Success! Please verify your email before logging in.', 'info');
        router.push(selectedRole.value === 'tutor' ? '/login/tutor' : '/login/student');
      }
    }
  } catch (error) {
    showToast(error.message || 'Something went wrong.', 'error');
  } finally {
    loading.value = false;
  }
}
</script>

<style scoped>
.page { display: flex; width: 100%; min-height: 100vh; background: #f0f4f8; }
.desktop-only { display: block; }
.mobile-only { display: none; }

/* LEFT PANEL */
.panel--brand { flex: 0 0 40%; position: sticky; top: 0; height: 100vh; display: flex; flex-direction: column; justify-content: space-between; padding: 2.5rem 2.8rem; overflow: hidden; background: #1a2c42; }
.brand-bg { position: absolute; inset: 0; z-index: 0; background: radial-gradient(ellipse at 20% 15%, rgba(60,100,200,0.5) 0%, transparent 55%), radial-gradient(ellipse at 80% 85%, rgba(245,192,60,0.2) 0%, transparent 50%); }
.brand-logo .main-logo { height: 110px; width: auto; object-fit: contain; filter: brightness(0) invert(1); position: relative; z-index: 5; margin-left: -15px; }
.brand-body { position: relative; z-index: 5; flex: 1; display: flex; flex-direction: column; justify-content: center; gap: 2rem; }
.brand-body h2 { font-family: var(--font-display); font-size: 2.2rem; color: #fff; line-height: 1.25; }
.brand-body p { font-size: 0.95rem; color: rgba(255,255,255,0.55); line-height: 1.6; }
.feature-list { display: flex; flex-direction: column; gap: 1.1rem; }
.feature-item { display: flex; align-items: center; gap: 1rem; padding: 1rem; background: rgba(255,255,255,0.06); border: 1px solid rgba(255,255,255,0.1); border-radius: 0.75rem; backdrop-filter: blur(8px); }
.feature-icon { font-size: 1.4rem; }
.feature-item strong { font-size: 0.85rem; color: #fff; display: block; }
.feature-item span { font-size: 0.75rem; color: rgba(255,255,255,0.5); }
.brand-footer { position: relative; z-index: 5; font-size: 0.85rem; color: rgba(255,255,255,0.45); }
.brand-link { color: #fff; font-weight: 700; text-decoration: none; }

/* RIGHT PANEL */
.panel--form { flex: 1; display: flex; flex-direction: column; align-items: center; justify-content: center; padding: 2rem; overflow-y: auto; }
.form-wrap { width: 100%; max-width: 480px; }
.form-header { margin-bottom: 1.5rem; }
.form-header h1 { font-family: var(--font-display); font-size: 2rem; color: #1a202c; margin-bottom: 0.3rem; font-weight: 800; }
.form-header p { font-size: 1rem; color: #718096; margin-bottom: 1rem; }

/* Step Indicator */
.step-indicator { display: flex; align-items: center; gap: 0; margin-top: 0.75rem; }
.step-dot { width: 28px; height: 28px; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-size: 0.75rem; font-weight: 800; background: #e2e8f0; color: #94a3b8; transition: all 0.3s; }
.step-dot.active { background: #1e3a8a; color: #fff; }
.step-line { flex: 1; height: 2px; background: #e2e8f0; min-width: 20px; }

/* Role Toggle */
.role-group { display: grid; grid-template-columns: 1fr 1fr; gap: 0.75rem; margin-bottom: 0.75rem; }
.role-btn { display: flex; align-items: center; gap: 0.75rem; padding: 0.85rem 1rem; background: #fff; border: 2px solid #e2e8f0; border-radius: 0.75rem; cursor: pointer; transition: all 0.2s; text-align: left; }
.role-btn--active { border-color: #4299e1; background: #ebf8ff; }
.role-icon { font-size: 1.5rem; }
.role-btn strong { font-size: 0.95rem; color: #2d3748; display: block; font-weight: 700; }
.role-btn small { font-size: 0.75rem; color: #718096; }
.role-btn--active strong { color: #2b6cb0; }
.role-note { display: flex; align-items: center; gap: 0.4rem; font-size: 0.8rem; color: #718096; margin-bottom: 1rem; }
.role-note svg { width: 16px; height: 16px; flex-shrink: 0; }

/* Fields */
.signup-form { display: flex; flex-direction: column; gap: 0; }
.step-block { display: flex; flex-direction: column; gap: 1rem; }
.grid-row { display: grid; grid-template-columns: 1fr 1fr; gap: 1rem; }
.field { display: flex; flex-direction: column; gap: 0.4rem; }
.field label { font-size: 0.85rem; font-weight: 800; color: #2d3748; }
.field input, .field select { width: 100%; padding: 0.85rem 1rem; background: #fff; border: 1.5px solid #cbd5e0; border-radius: 0.6rem; outline: none; font-size: 0.95rem; color: #2d3748; transition: border-color 0.2s; }
.field input:focus, .field select:focus { border-color: #4299e1; box-shadow: 0 0 0 3px rgba(66,153,225,0.15); }
.field select { appearance: none; background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='12' height='12' viewBox='0 0 24 24'%3E%3Cpath fill='%2394a3b8' d='M7 10l5 5 5-5z'/%3E%3C/svg%3E"); background-repeat: no-repeat; background-position: right 1rem center; padding-right: 2.5rem; }

/* Minor badge */
.minor-badge { display: inline-flex; align-items: center; gap: 0.4rem; background: #fef3c7; color: #92400e; font-size: 0.78rem; font-weight: 700; padding: 0.4rem 0.75rem; border-radius: 0.5rem; border: 1px solid #fde68a; margin-top: 0.25rem; }

/* Password */
.pw-wrap { position: relative; display: flex; align-items: center; }
.pw-wrap input { width: 100%; padding: 0.85rem 3rem 0.85rem 1rem; background: #fff; border: 1.5px solid #cbd5e0; border-radius: 0.6rem; outline: none; font-size: 0.95rem; color: #2d3748; }
.pw-wrap input:focus { border-color: #4299e1; box-shadow: 0 0 0 3px rgba(66,153,225,0.15); }
.pw-toggle { position: absolute; right: 0.75rem; background: none; border: none; cursor: pointer; font-size: 1rem; line-height: 1; }

/* Guardian section */
.guardian-banner { display: flex; align-items: flex-start; gap: 1rem; background: #fffbeb; border: 1px solid #fde68a; border-radius: 0.85rem; padding: 1rem; }
.guardian-icon { font-size: 1.8rem; flex-shrink: 0; }
.guardian-banner strong { font-size: 0.95rem; color: #92400e; display: block; font-weight: 800; }
.guardian-banner p { font-size: 0.8rem; color: #78350f; margin: 0.2rem 0 0; line-height: 1.4; }

/* Upload zone */
.upload-zone { border: 2px dashed #cbd5e0; border-radius: 0.85rem; padding: 1.5rem; text-align: center; cursor: pointer; transition: all 0.2s; background: #f8fafc; min-height: 120px; display: flex; align-items: center; justify-content: center; }
.upload-zone:hover { border-color: #4299e1; background: #ebf8ff; }
.upload-zone.has-file { border-color: #10b981; background: #f0fdf4; padding: 0.5rem; }
.upload-placeholder { display: flex; flex-direction: column; align-items: center; gap: 0.5rem; }
.upload-icon { font-size: 2rem; }
.upload-placeholder strong { font-size: 0.9rem; color: #4a5568; font-weight: 700; }
.upload-placeholder small { font-size: 0.75rem; color: #94a3b8; }
.id-preview { max-width: 100%; max-height: 180px; border-radius: 0.5rem; object-fit: contain; }
.hidden-input { display: none; }
.file-name { font-size: 0.78rem; color: #10b981; font-weight: 700; margin-top: 0.25rem; }

/* Buttons */
.btn-row { display: flex; gap: 0.75rem; align-items: center; margin-top: 0.5rem; }
.btn-back { background: #f8fafc; border: 1.5px solid #e2e8f0; color: #64748b; padding: 0.85rem 1.25rem; border-radius: 0.65rem; font-weight: 800; font-size: 0.9rem; cursor: pointer; white-space: nowrap; }
.btn-submit { width: 100%; padding: 1rem; background: #1a202c; color: #fff; border: none; border-radius: 0.65rem; font-weight: 800; font-size: 1rem; display: flex; align-items: center; justify-content: center; gap: 0.6rem; cursor: pointer; transition: all 0.2s; margin-top: 0.5rem; }
.btn-submit.flex-1 { width: auto; flex: 1; margin-top: 0; }
.btn-submit:hover:not(:disabled) { background: #2d3748; }
.btn-submit:disabled { opacity: 0.6; cursor: not-allowed; }
.terms-row { display: flex; gap: 0.6rem; font-size: 0.85rem; color: #4a5568; align-items: center; cursor: pointer; }
.terms-row input[type="checkbox"] { width: 18px; height: 18px; cursor: pointer; flex-shrink: 0; }
.signin-link { text-align: center; margin-top: 1.5rem; font-size: 0.85rem; color: #718096; }
.lnk { color: #3182ce; font-weight: 700; text-decoration: none; }

/* MOBILE */
@media (max-width: 768px) {
  .desktop-only { display: none !important; }
  .mobile-only { display: block !important; }
  .page { flex-direction: column; background: #fff; }
  .panel--form { padding: 1.5rem; justify-content: flex-start; }
  .mobile-header { text-align: center; margin-bottom: 1.5rem; padding-top: 1rem; display: flex; justify-content: center; }
  .mobile-logo-img { height: 100px; width: auto; }
  .form-wrap { max-width: 100%; }
  .grid-row { grid-template-columns: 1fr; gap: 0.85rem; }
  .role-btn { padding: 0.85rem; }
  .form-header h1 { font-size: 1.6rem; }
}
</style>
