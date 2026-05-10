<template>
  <div class="toast-container">
    <transition-group name="toast-list" tag="div">
      <div 
        v-for="toast in toasts" 
        :key="toast.id" 
        :class="['toast-item', toast.type]"
        @click="removeToast(toast.id)"
      >
        <div class="toast-icon">
          <svg v-if="toast.type === 'success'" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3"><polyline points="20 6 9 17 4 12"></polyline></svg>
          <svg v-else-if="toast.type === 'error'" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3"><line x1="18" y1="6" x2="6" y2="18"></line><line x1="6" y1="6" x2="18" y2="18"></line></svg>
          <svg v-else viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3"><circle cx="12" cy="12" r="10"></circle><line x1="12" y1="8" x2="12" y2="12"></line><line x1="12" y1="16" x2="12.01" y2="16"></line></svg>
        </div>
        <div class="toast-message">{{ toast.message }}</div>
      </div>
    </transition-group>
  </div>
</template>

<script setup>
import { useToast } from '../composables/useToast';

const { toasts, removeToast } = useToast();
</script>

<style scoped>
.toast-container {
  position: fixed;
  top: 2rem;
  right: 2rem;
  z-index: 9999;
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
  pointer-events: none;
}

.toast-item {
  pointer-events: auto;
  min-width: 300px;
  max-width: 450px;
  padding: 1rem 1.5rem;
  border-radius: 1rem;
  background: #ffffff;
  box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.1), 0 8px 10px -6px rgba(0, 0, 0, 0.1);
  display: flex;
  align-items: center;
  gap: 1rem;
  cursor: pointer;
  border: 1.5px solid #e2e8f0;
  transition: all 0.3s cubic-bezier(0.68, -0.55, 0.265, 1.55);
}

.toast-item.success {
  border-left: 6px solid #10b981;
  background: #f0fdf4;
}

.toast-item.error {
  border-left: 6px solid #ef4444;
  background: #fef2f2;
}

.toast-item.info {
  border-left: 6px solid #3b82f6;
  background: #eff6ff;
}

.toast-icon {
  width: 24px;
  height: 24px;
  flex-shrink: 0;
}

.toast-item.success .toast-icon { color: #10b981; }
.toast-item.error .toast-icon { color: #ef4444; }
.toast-item.info .toast-icon { color: #3b82f6; }

.toast-message {
  font-size: 0.95rem;
  font-weight: 700;
  color: #1e293b;
}

/* Animations */
.toast-list-enter-from {
  opacity: 0;
  transform: translateX(30px) scale(0.9);
}
.toast-list-leave-to {
  opacity: 0;
  transform: translateX(30px) scale(0.9);
}
</style>
