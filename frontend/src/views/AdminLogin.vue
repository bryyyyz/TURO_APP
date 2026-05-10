<template>
  <div class="admin-login-page">
    <div class="admin-login-card">
      <h1>TURO Admin Panel</h1>
      <p>Sign in to review tutor tier upgrade requests.</p>

      <form class="admin-form" @submit.prevent="handleLogin">
        <label>
          Username
          <input v-model.trim="username" type="text" required />
        </label>
        <label>
          Password
          <input v-model="password" type="password" required />
        </label>
        <button type="submit" :disabled="loading">
          {{ loading ? 'Signing in...' : 'Login' }}
        </button>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import { useToast } from '../composables/useToast';

const router = useRouter();
const { showToast } = useToast();
const username = ref('');
const password = ref('');
const loading = ref(false);

async function handleLogin() {
  loading.value = true;
  try {
    if (username.value !== 'admin' || password.value !== 'admin123') {
      throw new Error('Invalid admin credentials.');
    }
    sessionStorage.setItem('turo_admin_auth', btoa(`${username.value}:${password.value}`));
    showToast('Admin login successful.', 'success');
    router.push('/admin/reviews');
  } catch (err) {
    showToast(err.message || 'Login failed', 'error');
  } finally {
    loading.value = false;
  }
}
</script>

<style scoped>
.admin-login-page {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: #f8fafc;
  padding: 1.25rem;
}
.admin-login-card {
  width: 100%;
  max-width: 420px;
  background: #ffffff;
  border: 1px solid #e2e8f0;
  border-radius: 1rem;
  padding: 1.5rem;
}
.admin-login-card h1 {
  font-size: 1.4rem;
  font-weight: 800;
  color: #0f172a;
}
.admin-login-card p {
  margin-top: 0.25rem;
  color: #64748b;
  font-weight: 600;
}
.admin-form {
  display: flex;
  flex-direction: column;
  gap: 0.85rem;
  margin-top: 1rem;
}
.admin-form label {
  display: flex;
  flex-direction: column;
  gap: 0.35rem;
  color: #0f172a;
  font-size: 0.85rem;
  font-weight: 700;
}
.admin-form input {
  border: 1px solid #cbd5e1;
  border-radius: 0.7rem;
  padding: 0.75rem 0.85rem;
  font-size: 0.9rem;
}
.admin-form button {
  margin-top: 0.25rem;
  border: none;
  border-radius: 0.75rem;
  background: #0f172a;
  color: #fff;
  font-weight: 800;
  padding: 0.75rem 1rem;
  cursor: pointer;
}
</style>
