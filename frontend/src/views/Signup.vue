<template>
  <div class="page">

    <!-- ══ LEFT: Branding Panel (Desktop Only) ══ -->
    <div class="panel panel--brand desktop-only">
      <div class="brand-bg"></div>
      <div class="brand-orb orb--1"></div>
      <div class="brand-orb orb--2"></div>

      <div class="brand-logo">
        <img src="/images/TURO_LOGO_WITH_MEANING.png" alt="TURO Logo" class="main-logo" />
      </div>

      <div class="brand-body">
        <h2>Start your learning<br />journey today.</h2>
        <p>Join thousand of students and tutors in TURO - the Philippines' modern tutoring platform</p>

        <div class="feature-list">
          <div class="feature-item" v-for="f in features" :key="f.icon">
            <span class="feature-icon">{{ f.icon }}</span>
            <div>
              <strong>{{ f.title }}</strong>
              <span>{{ f.sub }}</span>
            </div>
          </div>
        </div>
      </div>

      <p class="brand-footer">Already have an account? <router-link to="/login/student" class="brand-link">Sign in ➔</router-link></p>
    </div>

    <!-- ══ RIGHT: Signup Form (Primary on Mobile) ══ -->
    <div class="panel panel--form">
      <!-- Mobile Logo -->
      <div class="mobile-only mobile-header">
        <img src="/images/TURO_LOGO_WITH_MEANING.png" alt="TURO" class="mobile-logo-img" />
      </div>

      <div class="form-wrap animate-scale-in">
        <div class="form-header">
          <h1>Create your account</h1>
          <p>Fill in your details below to get started</p>
        </div>

        <form @submit.prevent="currentStep === 1 ? nextStep() : handleSignup()" class="signup-form">
          <!-- STEP 1 -->
          <div v-show="currentStep === 1" class="step-1">
            <!-- Role Toggle -->
            <div class="role-group" :class="{ 'disabled-ui': loading }">
              <button
                class="role-btn"
                :class="{ 'role-btn--active': selectedRole === 'student' }"
                @click="selectedRole = 'student'"
                type="button"
              >
                <span class="role-icon">🎓</span>
                <div>
                  <strong>Student</strong>
                  <small>Learn</small>
                </div>
              </button>
              <button
                class="role-btn"
                :class="{ 'role-btn--active': selectedRole === 'tutor' }"
                @click="selectedRole = 'tutor'"
                type="button"
              >
                <span class="role-icon">📖</span>
                <div>
                  <strong>Tutor</strong>
                  <small>Teach</small>
                </div>
              </button>
            </div>

            <p class="role-note">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"/><path d="M12 8v4M12 16h.01"/></svg>
              Your role <strong>cannot be changed</strong> after sign up.
            </p>

            <div class="grid-row">
              <div class="field">
                <label>First Name</label>
                <input type="text" v-model="form.firstName" required />
              </div>
              <div class="field">
                <label>Last Name</label>
                <input type="text" v-model="form.lastName" required />
              </div>
            </div>

            <div class="grid-row">
              <div class="field">
                <label>Middle Name</label>
                <input type="text" v-model="form.middleName" />
              </div>
              <div class="field">
                <label>Name Extension</label>
                <input type="text" v-model="form.nameExtension" />
              </div>
            </div>

            <div class="grid-row">
              <div class="field">
                <label>Barangay</label>
                <input type="text" v-model="form.barangay" required />
              </div>
              <div class="field">
                <label>Municipality / City</label>
                <input type="text" v-model="form.municipality" required />
              </div>
            </div>

            <div class="field">
              <label>Province</label>
              <input type="text" v-model="form.province" required />
            </div>

            <button type="button" class="btn-submit" @click="nextStep">
              Proceed
            </button>
            
            <p class="signin-link">Already have an account? <router-link to="/login/student" class="lnk">Sign in</router-link></p>
          </div>

          <!-- STEP 2 -->
          <div v-show="currentStep === 2" class="step-2">
            <div class="field">
              <label>Email Address</label>
              <input type="email" v-model="form.email" required />
            </div>

            <div class="field">
              <label>Username</label>
              <input type="text" v-model="form.username" required />
            </div>

            <div class="field">
              <label>Password</label>
              <input type="password" v-model="form.password" required />
            </div>

            <div class="field">
              <label>Confirm Password</label>
              <input type="password" v-model="form.confirmPassword" required />
            </div>

            <label class="terms-row">
              <input type="checkbox" v-model="agreedToTerms" required />
              <span>I agree to the <a href="#" class="lnk">Terms</a> and <a href="#" class="lnk">Privacy Policy</a></span>
            </label>

            <button type="submit" class="btn-submit" :disabled="loading || !agreedToTerms">
              <span v-if="loading">Creating...</span>
              <span v-else>Create Account ➔</span>
            </button>

            <p class="signin-link">Already have an account? <router-link to="/login/student" class="lnk">Sign in</router-link></p>
          </div>
        </form>

      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue';
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

const form = reactive({ 
  firstName: '', 
  lastName: '', 
  middleName: '', 
  nameExtension: '', 
  barangay: '',
  municipality: '',
  province: '',
  email: '', 
  username: '', 
  password: '',
  confirmPassword: ''
});

const features = [
  { title: 'Expert Tutors', sub: 'Verified and passionate', icon: '🎓' },
  { title: 'Flexible Schedule', sub: 'Book on your terms', icon: '📅' },
  { title: 'Live Sessions', sub: 'Real-time interaction', icon: '💬' }
];

const nextStep = () => {
  if (!form.firstName || !form.lastName || !form.barangay || !form.municipality || !form.province) {
    showToast('Please fill in all required fields.', 'error');
    return;
  }
  currentStep.value = 2;
};

const handleSignup = async () => {
  if (form.password !== form.confirmPassword) {
    showToast('Passwords do not match.', 'error');
    return;
  }
  if (!agreedToTerms.value) {
    showToast('You must agree to the Terms and Privacy Policy.', 'error');
    return;
  }
  if (loading.value) return;
  loading.value = true;
  try {
    const { data: authData, error: authError } = await supabase.auth.signUp({
      email: form.email,
      password: form.password,
      options: {
        data: {
          first_name: form.firstName,
          last_name: form.lastName,
          middle_name: form.middleName || '',
          name_extension: form.nameExtension || '',
          barangay: form.barangay || '',
          municipality: form.municipality || '',
          province: form.province || '',
        },
      },
    });
    if (authError) throw authError;
    
    if (authData.user) {
      // Keep Supabase profile payload minimal for schema compatibility.
      // Full location/profile fields are persisted in Django profile below.
      const { error: profileError } = await supabase.from('profiles').insert({
        id: authData.user.id,
        first_name: form.firstName,
        last_name: form.lastName,
        username: form.username,
        role: selectedRole.value,
      });
      if (profileError) throw profileError;

      // Sync full name + location to Django (used by dashboards and My Profile)
      try {
        const { data } = await profileService.getProfileByEmail(form.email, selectedRole.value);
        const profiles = Array.isArray(data) ? data : (data.results || []);
        if (profiles.length > 0) {
          await profileService.updateProfile(profiles[0].id, {
            first_name: form.firstName,
            last_name: form.lastName,
            middle_name: form.middleName,
            name_extension: form.nameExtension,
            barangay: form.barangay,
            municipality: form.municipality,
            province: form.province,
            role: selectedRole.value,
          });
        }
      } catch (err) {
        console.error('Django profile sync failed:', err);
        showToast(
          'Account created, but we could not save your name and address to the server yet. They will fill in when you open My Profile, or try signing up again.',
          'warning',
        );
      }
      if (authData.session) {
        showToast('Account created successfully!', 'success');
        router.push(selectedRole.value === 'tutor' ? '/dashboard/tutor' : '/dashboard/student');
      } else {
        showToast('Success! Please verify your email.', 'info');
      }
    }
  } catch (error) {
    showToast(error.message, 'error');
  } finally {
    loading.value = false;
  }
};
</script>

<style scoped>
.page { display: flex; width: 100%; min-height: 100vh; background: #f0f4f8; }

/* Helpers */
.desktop-only { display: block; }
.mobile-only { display: none; }

/* LEFT PANEL (Desktop) */
.panel--brand {
  flex: 0 0 40%; position: sticky; top: 0; height: 100vh;
  display: flex; flex-direction: column; justify-content: space-between;
  padding: 2.5rem 2.8rem; overflow: hidden; background: #1a2c42;
}
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

/* RIGHT PANEL (Form) */
.panel--form { flex: 1; display: flex; flex-direction: column; align-items: center; justify-content: center; padding: 2rem; }
.form-wrap { width: 100%; max-width: 480px; }
.form-header { margin-bottom: 1.5rem; }
.form-header h1 { font-family: var(--font-display); font-size: 2.2rem; color: #1a202c; margin-bottom: 0.4rem; font-weight: 800; }
.form-header p { font-size: 1.05rem; color: #718096; }

/* Role Toggle */
.role-group { display: grid; grid-template-columns: 1fr 1fr; gap: 0.75rem; margin-bottom: 0.75rem; }
.role-btn { display: flex; align-items: center; gap: 0.75rem; padding: 0.85rem 1rem; background: #fff; border: 2px solid #e2e8f0; border-radius: 0.75rem; cursor: pointer; transition: all 0.2s; text-align: left; }
.role-btn--active { border-color: #4299e1; background: #ebf8ff; }
.role-icon { font-size: 1.5rem; }
.role-btn strong { font-size: 0.95rem; color: #2d3748; display: block; font-weight: 700; }
.role-btn small { font-size: 0.75rem; color: #718096; }
.role-btn--active strong { color: #2b6cb0; }
.role-note { display: flex; align-items: center; gap: 0.4rem; font-size: 0.8rem; color: #718096; margin-bottom: 1.5rem; }
.role-note svg { width: 16px; height: 16px; }

/* Form Fields */
.signup-form { display: flex; flex-direction: column; gap: 1rem; }
.grid-row { display: grid; grid-template-columns: 1fr 1fr; gap: 1rem; }
.field { display: flex; flex-direction: column; gap: 0.5rem; }
.field label { font-size: 0.85rem; font-weight: 800; color: #2d3748; }
.field input { width: 100%; padding: 0.85rem 1rem; background: #fff; border: 1.5px solid #cbd5e0; border-radius: 0.6rem; outline: none; font-size: 0.95rem; color: #2d3748; transition: border-color 0.2s; }
.field input:focus { border-color: #4299e1; box-shadow: 0 0 0 3px rgba(66,153,225,0.15); }
.terms-row { display: flex; gap: 0.6rem; font-size: 0.85rem; color: #4a5568; margin-top: 0.5rem; align-items: center; cursor: pointer; }
.terms-row input[type="checkbox"] { width: 18px; height: 18px; cursor: pointer; border-radius: 4px; border: 1.5px solid #cbd5e0; }
.lnk { color: #3182ce; font-weight: 700; text-decoration: none; }
.btn-submit { width: 100%; padding: 1rem; background: #1a202c; color: #fff; border: none; border-radius: 0.65rem; font-weight: 800; font-size: 1rem; display: flex; align-items: center; justify-content: center; gap: 0.6rem; cursor: pointer; transition: all 0.2s; margin-top: 0.5rem; }
.btn-submit:hover:not(:disabled) { background: #2d3748; }
.btn-submit:disabled { opacity: 0.7; cursor: not-allowed; }
.signin-link { text-align: center; margin-top: 1.5rem; font-size: 0.85rem; color: #718096; }

/* ── MOBILE ADAPTATION ── */
@media (max-width: 768px) {
  .desktop-only { display: none !important; }
  .mobile-only { display: block !important; }
  .page { flex-direction: column; background: #ffffff; }
  .panel--form { padding: 1.5rem; justify-content: flex-start; }
  .mobile-header { text-align: center; margin-bottom: 2rem; padding-top: 1rem; display: flex; justify-content: center; }
  .mobile-logo-img { height: 120px; width: auto; }
  .form-wrap { max-width: 100%; }
  .grid-row { grid-template-columns: 1fr; gap: 1rem; }
  .role-btn { padding: 1rem; }
}
</style>

