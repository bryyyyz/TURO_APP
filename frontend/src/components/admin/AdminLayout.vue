<template>
  <div class="admin-shell">
    <aside class="sidebar">
      <div class="brand">
        <div class="logo">T</div>
        <div class="brand-text">
          <div class="brand-title">TURO</div>
          <div class="brand-sub">Admin</div>
        </div>
      </div>

      <nav class="nav">
        <RouterLink class="nav-item" :class="{ active: isActive('/admin/reviews') }" to="/admin/reviews">
          <span class="dot" aria-hidden="true" />
          <span>Tier Reviews</span>
        </RouterLink>
      </nav>

      <div class="sidebar-footer">
        <button v-if="showLogout" class="logout" type="button" @click="$emit('logout')">
          Logout
        </button>
      </div>
    </aside>

    <div class="main">
      <header class="topbar">
        <div class="title">
          <h1>{{ title }}</h1>
          <p v-if="subtitle">{{ subtitle }}</p>
        </div>
        <div class="topbar-actions">
          <slot name="actions" />
        </div>
      </header>

      <main class="content">
        <slot />
      </main>
    </div>
  </div>
</template>

<script setup>
import { useRoute } from 'vue-router';

defineProps({
  title: { type: String, required: true },
  subtitle: { type: String, default: '' },
  showLogout: { type: Boolean, default: true }
});

defineEmits(['logout']);

const route = useRoute();
function isActive(prefix) {
  return typeof route.path === 'string' && route.path.startsWith(prefix);
}
</script>

<style scoped>
.admin-shell {
  min-height: 100vh;
  background:
    radial-gradient(900px 500px at 0% 0%, rgba(59, 130, 246, 0.14), transparent 65%),
    radial-gradient(900px 500px at 100% 0%, rgba(16, 185, 129, 0.10), transparent 65%),
    #f8fafc;
  display: grid;
  grid-template-columns: 260px 1fr;
}

.sidebar {
  position: sticky;
  top: 0;
  height: 100vh;
  padding: 1.1rem 0.9rem;
  border-right: 1px solid rgba(148, 163, 184, 0.35);
  background: rgba(255, 255, 255, 0.72);
  backdrop-filter: blur(10px);
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.brand {
  display: flex;
  align-items: center;
  gap: 0.7rem;
  padding: 0.5rem 0.55rem;
}
.logo {
  width: 38px;
  height: 38px;
  border-radius: 12px;
  display: grid;
  place-items: center;
  font-weight: 900;
  color: white;
  background: linear-gradient(135deg, #0f172a, #2563eb);
  box-shadow: 0 10px 25px rgba(15, 23, 42, 0.18);
}
.brand-title {
  font-weight: 900;
  letter-spacing: 0.02em;
  color: #0f172a;
  line-height: 1.1;
}
.brand-sub {
  color: #64748b;
  font-weight: 700;
  font-size: 0.85rem;
}

.nav {
  display: grid;
  gap: 0.35rem;
  padding: 0 0.25rem;
}
.nav-item {
  display: flex;
  align-items: center;
  gap: 0.55rem;
  padding: 0.6rem 0.7rem;
  border-radius: 0.9rem;
  color: #0f172a;
  font-weight: 800;
  text-decoration: none;
  border: 1px solid transparent;
}
.nav-item .dot {
  width: 10px;
  height: 10px;
  border-radius: 999px;
  background: #cbd5e1;
}
.nav-item:hover {
  background: rgba(2, 132, 199, 0.06);
  border-color: rgba(2, 132, 199, 0.25);
}
.nav-item.active {
  background: rgba(37, 99, 235, 0.10);
  border-color: rgba(37, 99, 235, 0.28);
}
.nav-item.active .dot {
  background: #2563eb;
}

.sidebar-footer {
  margin-top: auto;
  padding: 0 0.25rem;
}
.logout {
  width: 100%;
  border: 1px solid rgba(148, 163, 184, 0.6);
  background: rgba(255, 255, 255, 0.7);
  border-radius: 0.9rem;
  padding: 0.65rem 0.9rem;
  font-weight: 900;
  cursor: pointer;
}
.logout:hover {
  background: rgba(248, 250, 252, 0.9);
}

.main {
  padding: 1.25rem;
}

.topbar {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  gap: 1rem;
  margin-bottom: 1rem;
}
.title h1 {
  font-size: 1.35rem;
  font-weight: 950;
  color: #0f172a;
  letter-spacing: -0.02em;
}
.title p {
  margin-top: 0.2rem;
  color: #64748b;
  font-weight: 650;
}
.topbar-actions {
  display: flex;
  align-items: center;
  gap: 0.6rem;
  flex-wrap: wrap;
}

.content {
  display: grid;
  gap: 0.9rem;
}

@media (max-width: 980px) {
  .admin-shell {
    grid-template-columns: 1fr;
  }
  .sidebar {
    position: relative;
    height: auto;
    border-right: none;
    border-bottom: 1px solid rgba(148, 163, 184, 0.35);
    flex-direction: row;
    align-items: center;
  }
  .nav {
    grid-auto-flow: column;
    grid-auto-columns: max-content;
    overflow: auto;
    padding: 0;
  }
  .sidebar-footer {
    margin-top: 0;
    margin-left: auto;
    padding: 0;
  }
}
</style>

