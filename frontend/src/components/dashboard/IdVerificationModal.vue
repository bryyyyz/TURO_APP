<template>
  <div class="id-modal-overlay">
    <div class="id-modal-content">
      <div class="modal-header">
        <div class="shield-icon">🛡️</div>
        <h2>Verify Your Identity</h2>
      </div>
      <div class="modal-body">
        <p>
          Welcome to TURO! To keep our community safe and secure, we require all new users to upload a valid Government ID or Student ID before browsing or posting.
        </p>

        <div class="upload-zone" @click="triggerFileInput" :class="{ 'has-file': previewUrl }">
          <template v-if="previewUrl">
            <img :src="previewUrl" alt="ID Preview" class="preview-img" />
            <div class="change-overlay">Click to change photo</div>
          </template>
          <template v-else>
            <span class="upload-icon">📸</span>
            <strong>Upload ID Photo</strong>
            <span>PNG, JPG up to 5MB</span>
          </template>
          <input type="file" ref="fileInput" @change="onFileSelected" accept="image/*" class="hidden-input" />
        </div>

        <button class="btn-submit" :disabled="!selectedFile || uploading" @click="submitId">
          <span v-if="uploading" class="spinner"></span>
          <span v-else>Submit ID</span>
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import { profileService } from '../../services/api';
import { useToast } from '../../composables/useToast';

const props = defineProps({
  profile: Object
});

const emit = defineEmits(['submitted']);

const { showToast } = useToast();
const fileInput = ref(null);
const selectedFile = ref(null);
const previewUrl = ref(null);
const uploading = ref(false);

function triggerFileInput() {
  fileInput.value.click();
}

function onFileSelected(event) {
  const file = event.target.files[0];
  if (!file) return;
  if (!file.type.startsWith('image/')) {
    showToast('Please select a valid image file.', 'error');
    return;
  }
  selectedFile.value = file;
  previewUrl.value = URL.createObjectURL(file);
}

async function submitId() {
  if (!selectedFile.value || !props.profile?.id) return;
  uploading.value = true;
  try {
    const formData = new FormData();
    formData.append('id_photo', selectedFile.value);
    formData.append('requires_id_verification', 'false');
    formData.append('id_verification_status', 'pending');

    const { data } = await profileService.updateProfile(props.profile.id, formData);
    showToast('ID uploaded! Waiting for admin approval.', 'success');
    emit('submitted', data);
  } catch (error) {
    console.error('Failed to upload ID:', error);
    showToast('Failed to upload ID. Please try again.', 'error');
  } finally {
    uploading.value = false;
  }
}
</script>

<style scoped>
.id-modal-overlay {
  position: fixed; inset: 0; z-index: 9999;
  background: rgba(15, 23, 42, 0.85); backdrop-filter: blur(8px);
  display: flex; align-items: center; justify-content: center;
  padding: 1.5rem;
}
.id-modal-content {
  background: #ffffff; border-radius: 1.5rem; width: 100%; max-width: 480px;
  overflow: hidden; box-shadow: 0 25px 50px -12px rgba(0,0,0,0.25);
  animation: slideUp 0.3s ease-out;
}
@keyframes slideUp { from { opacity: 0; transform: translateY(20px); } to { opacity: 1; transform: translateY(0); } }

.modal-header {
  background: linear-gradient(135deg, #0f172a, #1e3a8a); color: #fff;
  padding: 2.5rem 2rem 1.5rem; text-align: center;
}
.shield-icon { font-size: 3rem; margin-bottom: 0.5rem; line-height: 1; }
.modal-header h2 { font-family: var(--font-display); font-size: 1.6rem; font-weight: 800; margin: 0; }

.modal-body { padding: 2rem; display: flex; flex-direction: column; gap: 1.5rem; }
.modal-body p { color: #475569; font-size: 0.95rem; line-height: 1.5; text-align: center; margin: 0; }

.upload-zone {
  border: 2px dashed #cbd5e1; border-radius: 1rem; padding: 2.5rem 1.5rem;
  display: flex; flex-direction: column; align-items: center; justify-content: center;
  gap: 0.5rem; cursor: pointer; transition: all 0.2s; position: relative; overflow: hidden;
  background: #f8fafc;
}
.upload-zone:hover { border-color: #3b82f6; background: #eff6ff; }
.upload-zone.has-file { padding: 0; border: none; background: #000; height: 220px; }

.upload-icon { font-size: 2.5rem; }
.upload-zone strong { color: #0f172a; font-size: 1rem; font-weight: 700; }
.upload-zone span { color: #64748b; font-size: 0.85rem; font-weight: 500; }

.preview-img { width: 100%; height: 100%; object-fit: contain; }
.change-overlay {
  position: absolute; inset: 0; background: rgba(0,0,0,0.5); color: #fff;
  display: flex; align-items: center; justify-content: center; font-weight: 700;
  opacity: 0; transition: opacity 0.2s;
}
.upload-zone:hover .change-overlay { opacity: 1; }
.hidden-input { display: none; }

.btn-submit {
  background: #10b981; color: #fff; border: none; padding: 1rem; border-radius: 0.85rem;
  font-size: 1rem; font-weight: 800; cursor: pointer; transition: all 0.2s;
  display: flex; justify-content: center; align-items: center; min-height: 52px;
}
.btn-submit:hover:not(:disabled) { background: #059669; transform: translateY(-1px); }
.btn-submit:disabled { opacity: 0.5; cursor: not-allowed; }

.spinner {
  width: 20px; height: 20px; border: 3px solid rgba(255,255,255,0.3); border-top-color: #fff;
  border-radius: 50%; animation: spin 0.8s linear infinite;
}
@keyframes spin { to { transform: rotate(360deg); } }
</style>
