<script setup>
defineProps({
  loading: { type: Boolean, default: false },
  /** When true: fixed positioning for teleport overlay (dashboard shell). */
  floating: { type: Boolean, default: false },
  /** @type {{ id: string|number; title: string; subtitle: string; value: string; kind: string }[]} */
  items: { type: Array, default: () => [] },
});
defineEmits(['close']);
</script>

<template>
  <div class="dap" :class="{ 'dap--floating': floating }" role="dialog" aria-labelledby="dap-title">
    <div class="dap-header">
      <h3 id="dap-title">Recent activity</h3>
      <button type="button" class="dap-close" aria-label="Close" @click="$emit('close')">×</button>
    </div>
    <div class="dap-body">
      <div v-if="loading" class="dap-loading">Loading…</div>
      <p v-else-if="!items.length" class="dap-empty">No activity yet.</p>
      <ul v-else class="dap-list">
        <li v-for="row in items" :key="row.id" class="dap-item" :data-kind="row.kind">
          <div class="dap-text">
            <span class="dap-title-row">{{ row.title }}</span>
            <span class="dap-sub">{{ row.subtitle }}</span>
          </div>
          <span class="dap-value">{{ row.value }}</span>
        </li>
      </ul>
    </div>
  </div>
</template>

<style scoped>
.dap {
  position: absolute;
  right: 0;
  top: calc(100% + 10px);
  width: min(380px, calc(100vw - 24px));
  max-height: min(440px, 70vh);
  background: #fff;
  border: 1px solid #e2e8f0;
  border-radius: 14px;
  box-shadow: 0 16px 40px rgba(15, 22, 41, 0.12);
  z-index: 400;
  display: flex;
  flex-direction: column;
  overflow: hidden;
}

.dap.dap--floating {
  position: fixed;
  top: 92px;
  right: clamp(16px, 3vw, 40px);
  width: min(380px, calc(100vw - 24px));
  z-index: 502;
}

@media (max-width: 768px) {
  .dap.dap--floating {
    left: 12px;
    right: 12px;
    top: auto;
    bottom: calc(76px + env(safe-area-inset-bottom));
    width: auto;
    max-height: min(480px, 58vh);
  }
}

.dap-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0.85rem 1rem;
  border-bottom: 1px solid #f1f5f9;
  background: #fafbfc;
}

.dap-header h3 {
  margin: 0;
  font-size: 0.9rem;
  font-weight: 800;
  color: #0f172a;
}

.dap-close {
  border: none;
  background: transparent;
  font-size: 1.35rem;
  line-height: 1;
  color: #94a3b8;
  cursor: pointer;
  padding: 0 0.25rem;
  border-radius: 6px;
}
.dap-close:hover {
  color: #0f172a;
  background: #f1f5f9;
}

.dap-body {
  overflow-y: auto;
  flex: 1;
  min-height: 0;
}

.dap-loading,
.dap-empty {
  padding: 1.5rem;
  margin: 0;
  font-size: 0.82rem;
  font-weight: 600;
  color: #64748b;
  text-align: center;
}

.dap-list {
  list-style: none;
  margin: 0;
  padding: 0.5rem;
}

.dap-item {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  gap: 0.75rem;
  padding: 0.65rem 0.65rem;
  border-radius: 10px;
  margin-bottom: 2px;
}
.dap-item:hover {
  background: #f8fafc;
}

.dap-text {
  display: flex;
  flex-direction: column;
  gap: 2px;
  min-width: 0;
}

.dap-title-row {
  font-size: 0.8rem;
  font-weight: 800;
  color: #0f172a;
}

.dap-sub {
  font-size: 0.72rem;
  font-weight: 600;
  color: #64748b;
  line-height: 1.35;
}

.dap-value {
  flex-shrink: 0;
  font-size: 0.72rem;
  font-weight: 800;
  color: #0f172a;
}

.dap-item[data-kind='success'] .dap-value {
  color: #047857;
}
.dap-item[data-kind='pending'] .dap-value {
  color: #b45309;
}
.dap-item[data-kind='payment'] .dap-value {
  color: #1e40af;
}
.dap-item[data-kind='muted'] .dap-sub,
.dap-item[data-kind='muted'] .dap-value {
  color: #94a3b8;
}

</style>
