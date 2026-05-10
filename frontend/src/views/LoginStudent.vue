<template>
  <div class="login-page">
    <!-- Left Section: Visuals & Branding (Desktop Only) -->
    <div class="visual-section desktop-only">
      <div class="logo-top">
        <img src="/images/TURO_LOGO_WITH_MEANING.png" alt="TURO Logo" class="main-logo" />
      </div>

      <div class="geometric-wrapper">
        <div class="bg-shape shape-blue"></div>
        <div class="bg-shape shape-light"></div>
        <div class="dots-pattern top-left"></div>
        <div class="dots-pattern bottom-right"></div>
        
        <div class="diamond-frame">
          <img src="/images/student.png" alt="Student" class="feature-image" />
        </div>
      </div>

      <div class="tagline-container">
        <h1>Empowering Minds.<br />Shaping Futures.</h1>
        <p>A better way to learn. Together.</p>
        <div class="accent-dash"></div>
      </div>

      <div class="features-footer">
        <div class="feature" v-for="f in features" :key="f.title">
          <div class="icon-wrap" v-html="f.svg"></div>
          <div class="text">
            <strong>{{ f.title }}</strong>
            <span>{{ f.sub }}</span>
          </div>
        </div>
      </div>
    </div>

    <!-- Right Section: Login Form (Primary on Mobile) -->
    <div class="form-section">
      <!-- Mobile Logo -->
      <div class="mobile-only mobile-header">
        <img src="/images/TURO_LOGO_WITH_MEANING.png" alt="TURO" class="mobile-logo-img" />
      </div>

      <div class="top-nav desktop-only">
        <span>New to TURO?</span>
        <router-link to="/signup" class="btn-signup">Create an account</router-link>
      </div>

      <div class="login-card animate-scale-in">
        <div class="card-header">
          <h2>Welcome back!</h2>
          <p>Sign in to continue your learning journey.</p>
        </div>

        <form @submit.prevent="handleLogin" class="form-body">
          <div class="input-group">
            <label>Email Address</label>
            <div class="input-field">
              <span class="icon">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M4 4h16c1.1 0 2 .9 2 2v12c0 1.1-.9 2-2 2H4c-1.1 0-2-.9-2-2V6c0-1.1.9-2 2-2z"/><polyline points="22,6 12,13 2,6"/></svg>
              </span>
              <input type="email" v-model="username" placeholder="Enter your email address" required />
            </div>
          </div>

          <div class="input-group">
            <label>Password</label>
            <div class="input-field">
              <span class="icon">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="3" y="11" width="18" height="11" rx="2" ry="2"/><path d="M7 11V7a5 5 0 0 1 10 0v4"/></svg>
              </span>
              <input :type="showPassword ? 'text' : 'password'" v-model="password" placeholder="Enter your password" required />
              <button type="button" class="pw-toggle" @click="showPassword = !showPassword">
                <svg v-if="!showPassword" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"/><circle cx="12" cy="12" r="3"/></svg>
                <svg v-else viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M17.94 17.94A10.07 10.07 0 0 1 12 20c-7 0-11-8-11-8a18.45 18.45 0 0 1 5.06-5.94M9.9 4.24A9.12 9.12 0 0 1 12 4c7 0 11 8 11 8a18.5 18.5 0 0 1-2.16 3.19m-6.72-1.07a3 3 0 1 1-4.24-4.24"/><line x1="1" y1="1" x2="23" y2="23"/></svg>
              </button>
            </div>
          </div>

          <div class="form-options">
            <label class="checkbox-label">
              <input type="checkbox" v-model="rememberMe" />
              <span class="custom-check"></span>
              <span>Remember me</span>
            </label>
            <a href="#" class="forgot-pw">Forgot password?</a>
          </div>

          <button type="submit" class="btn-submit" :disabled="loading">
            <span v-if="!loading">Login</span>
            <span v-else>Signing in...</span>
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3" class="btn-arrow-icon"><path d="M5 12h14M12 5l7 7-7 7"/></svg>
          </button>
        </form>

        <p class="switch-link">
          Are you a tutor? <router-link to="/login/tutor">Login here</router-link>
        </p>

        <div class="mobile-only mobile-footer">
          <p>Don't have an account? <router-link to="/signup">Create one</router-link></p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import { supabase } from '../supabase';
import { useToast } from '../composables/useToast';
import { profileService } from '../services/api';

const router = useRouter();
const { showToast } = useToast();

const username = ref('');
const password = ref('');
const rememberMe = ref(false);
const showPassword = ref(false);
const loading = ref(false);

const features = [
  { title: 'Expert Tutors', sub: 'Verified tutors only', svg: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M22 10v6M2 10l10-5 10 5-10 5z"/><path d="M6 12v5c3 3 9 3 12 0v-5"/></svg>' },
  { title: 'Flexible Learning', sub: 'Book sessions anytime', svg: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="3" y="4" width="18" height="18" rx="2" ry="2"/><line x1="16" y1="2" x2="16" y2="6"/><line x1="8" y1="2" x2="8" y2="6"/><line x1="3" y1="10" x2="21" y2="10"/></svg>' },
  { title: 'Secure & Trusted', sub: 'Safe platform', svg: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/></svg>' }
];

async function assertAccountRole(expectedRole) {
  const { data } = await profileService.getProfileByEmail(username.value);
  const profiles = Array.isArray(data) ? data : (data?.results || []);
  const profile = profiles[0];
  const actualRole = profile?.role || '';

  if (!actualRole) {
    throw new Error('No account role found. Please contact support.');
  }
  if (actualRole !== expectedRole) {
    throw new Error(
      expectedRole === 'student'
        ? 'This account is registered as a tutor. Please use Tutor Login.'
        : 'This account is registered as a student. Please use Student Login.'
    );
  }
}

const handleLogin = async () => {
  loading.value = true;
  try {
    if (!username.value.includes('@')) {
      throw new Error('Please enter a valid email address.');
    }
    const { error } = await supabase.auth.signInWithPassword({
      email: username.value,
      password: password.value,
    });
    if (error) throw error;
    await assertAccountRole('student');
    showToast('Login successful! Welcome back.', 'success');
    router.push('/dashboard/student');
  } catch (error) {
    await supabase.auth.signOut();
    showToast(error.message, 'error');
  } finally {
    loading.value = false;
  }
};
</script>

<style scoped>
.login-page {
  display: flex;
  height: 100vh;
  width: 100%;
  overflow: hidden;
  background-color: #f8fafc;
}

/* Helpers */
.desktop-only { display: block; }
.mobile-only { display: none; }

/* LEFT SECTION (Desktop) */
.visual-section {
  flex: 1.1;
  background-color: #ffffff;
  padding: 1.5rem 3rem;
  display: flex;
  flex-direction: column;
  position: relative;
  justify-content: space-between;
}
.logo-top .main-logo { height: 180px; width: auto; object-fit: contain; margin-left: -20px; margin-top: -10px; }
.geometric-wrapper { position: relative; height: 320px; width: 100%; display: flex; align-items: center; justify-content: center; margin: 1rem 0; }
.bg-shape { position: absolute; transform: rotate(45deg); border-radius: 3rem; }
.shape-blue { width: 300px; height: 300px; background: #0f172a; z-index: 1; left: 5%; }
.shape-light { width: 280px; height: 280px; background: #e2e8f0; z-index: 0; left: 20%; top: -15%; }
.dots-pattern { position: absolute; width: 100px; height: 100px; background-image: radial-gradient(#cbd5e1 2px, transparent 2px); background-size: 12px 12px; z-index: 0; }
.dots-pattern.top-left { top: 5%; left: 0; }
.dots-pattern.bottom-right { bottom: 5%; right: 5%; }
.diamond-frame { width: 260px; height: 260px; background: #ffffff; z-index: 2; transform: rotate(45deg); border-radius: 2.5rem; overflow: hidden; border: 10px solid #ffffff; box-shadow: 0 20px 40px -10px rgba(0,0,0,0.15); display: flex; align-items: center; justify-content: center; }
.feature-image { width: 145%; height: 145%; object-fit: cover; transform: rotate(-45deg); }
.tagline-container { text-align: center; margin-top: 0.5rem; }
.tagline-container h1 { font-family: var(--font-display); font-size: 2.2rem; font-weight: 800; color: #0f172a; line-height: 1.1; margin-bottom: 0.5rem; }
.tagline-container p { font-size: 0.95rem; color: #64748b; font-weight: 600; }
.accent-dash { width: 35px; height: 4px; background-color: #f59e0b; margin: 0.75rem auto 0; border-radius: 4px; }
.features-footer { display: flex; justify-content: space-between; gap: 1rem; margin-top: auto; }
.feature { display: flex; align-items: center; gap: 0.6rem; }
.icon-wrap { width: 34px; height: 34px; background-color: #f1f5f9; border-radius: 10px; display: flex; align-items: center; justify-content: center; flex-shrink: 0; color: #0f172a; }
.icon-wrap svg { width: 18px; height: 18px; }
.feature .text strong { display: block; font-size: 0.8rem; font-weight: 800; color: #0f172a; }
.feature .text span { font-size: 0.65rem; color: #64748b; font-weight: 600; line-height: 1.2; }

/* RIGHT SECTION (Form) */
.form-section { flex: 0.9; background-color: #f8fafc; display: flex; flex-direction: column; padding: 1.5rem 3rem; }
.top-nav { display: flex; justify-content: flex-end; align-items: center; gap: 1rem; margin-bottom: 1.5rem; }
.top-nav span { font-size: 0.85rem; color: #64748b; font-weight: 600; }
.btn-signup { padding: 0.5rem 1.2rem; border: 1.5px solid #e2e8f0; border-radius: 0.75rem; color: #0f172a; text-decoration: none; font-weight: 700; font-size: 0.8rem; background: #ffffff; }
.login-card { background: #ffffff; border-radius: 1.5rem; padding: 2.5rem; box-shadow: 0 15px 30px -5px rgba(0,0,0,0.05); width: 100%; max-width: 480px; margin: auto; border: 1px solid #f1f5f9; }
.card-header h2 { font-family: var(--font-display); font-size: 2rem; font-weight: 800; color: #0f172a; margin-bottom: 0.4rem; }
.card-header p { color: #64748b; font-weight: 600; margin-bottom: 1.5rem; font-size: 0.95rem; }
.form-body { display: flex; flex-direction: column; gap: 1.25rem; }
.input-group label { display: block; font-size: 0.85rem; font-weight: 800; color: #0f172a; margin-bottom: 0.4rem; }
.input-field { position: relative; display: flex; align-items: center; }
.icon { position: absolute; left: 1rem; color: #94a3b8; display: flex; align-items: center; }
.icon svg { width: 18px; height: 18px; }
.input-field input { width: 100%; padding: 0.9rem 1rem 0.9rem 2.8rem; border: 1.5px solid #f1f5f9; border-radius: 0.75rem; font-size: 0.95rem; outline: none; background: #fdfdfd; }
.input-field input:focus { border-color: #0f172a; background: #ffffff; box-shadow: 0 0 0 4px rgba(15,23,42,0.05); }
.pw-toggle { position: absolute; right: 1rem; background: none; border: none; cursor: pointer; color: #94a3b8; display: flex; align-items: center; }
.pw-toggle svg { width: 18px; height: 18px; }
.form-options { display: flex; justify-content: space-between; align-items: center; }
.checkbox-label { display: flex; align-items: center; gap: 0.5rem; font-size: 0.8rem; font-weight: 600; color: #64748b; cursor: pointer; }
.forgot-pw { font-size: 0.8rem; font-weight: 700; color: #3b82f6; text-decoration: none; }
.btn-submit {
  width: 100%;
  background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
  color: #ffffff;
  border: none;
  padding: 0.9rem;
  border-radius: 0.75rem;
  font-size: 0.95rem;
  font-weight: 800;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.75rem;
  margin-top: 0.5rem;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  box-shadow: 0 4px 15px rgba(15, 23, 42, 0.25);
}

.btn-submit:hover:not(:disabled) {
  background: linear-gradient(135deg, #1e293b 0%, #334155 100%);
  transform: translateY(-2px);
  box-shadow: 0 8px 25px rgba(15, 23, 42, 0.35);
}

.btn-submit:active {
  transform: translateY(0);
}

.btn-arrow-icon {
  width: 18px;
  height: 18px;
  flex-shrink: 0;
  transition: transform 0.3s ease;
}

.btn-submit:hover .btn-arrow-icon {
  transform: translateX(4px);
}

.switch-link { text-align: center; margin-top: 1.5rem; font-size: 0.9rem; font-weight: 600; color: #64748b; }
.switch-link a { color: #3b82f6; font-weight: 800; text-decoration: none; }

/* ── MOBILE ADAPTATION ── */
@media (max-width: 768px) {
  .desktop-only { display: none !important; }
  .mobile-only { display: block !important; }
  .login-page { flex-direction: column; height: auto; min-height: 100vh; overflow-y: auto; background: #ffffff; }
  .form-section { flex: 1; padding: 1.5rem; background: #ffffff; }
  .mobile-header { text-align: center; margin-bottom: 2rem; padding-top: 1rem; display: flex; justify-content: center; }
  .mobile-logo-img { height: 120px; width: auto; }
  .login-card { border: none; box-shadow: none; padding: 0; max-width: 100%; }
  .card-header h2 { font-size: 24px; }
  .card-header p { font-size: 14px; margin-bottom: 2rem; }
  .form-body { gap: 1rem; }
  .input-field input { padding: 0.8rem 1rem 0.8rem 2.6rem; font-size: 14px; }
  .mobile-footer { margin-top: 2rem; text-align: center; border-top: 1px solid #f1f5f9; padding-top: 1.5rem; }
  .mobile-footer p { font-size: 14px; color: #64748b; font-weight: 600; }
  .mobile-footer a { color: #0f172a; font-weight: 800; text-decoration: none; }
}
</style>
