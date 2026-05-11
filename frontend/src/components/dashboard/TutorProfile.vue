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
          <div class="role-badge tutor">Tutor</div>
        </div>
        <div class="hero-text">
          <div class="hero-name-row">
            <h1>{{ displayFullName || 'Your Name' }}</h1>
            <span class="hero-tier-badge">{{ tierLabel }}</span>
          </div>
          <div class="hero-elig">
            <span class="hero-elig-text">Sessions: {{ completedSessionsCount }}/{{ UPGRADE_ELIGIBILITY_SESSIONS }}</span>
            <div class="hero-elig-bar" aria-hidden="true">
              <div class="hero-elig-fill" :style="{ width: eligibilityPercent + '%' }"></div>
            </div>
          </div>
          <p class="hero-sub">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0z"/><circle cx="12" cy="10" r="3"/></svg>
            {{ fullLocation || 'Location not set — students cannot find you yet' }}
          </p>
        </div>
      </div>
    </div>

    <!-- ── Alert Banner ── -->
    <div class="location-alert" v-if="!form.municipality || !form.province">
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"/><line x1="12" y1="8" x2="12" y2="12"/><line x1="12" y1="16" x2="12.01" y2="16"/></svg>
      <span><strong>Complete your location</strong> — your listings will only be visible to students in your area</span>
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
              <p>Your public tutor identity</p>
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
            <p>{{ displayFullName || '—' }}</p>
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
            <label for="t-first-name">First Name</label>
            <input id="t-first-name" v-model="editForm.first_name" type="text" placeholder="Maria" />
          </div>
          <div class="form-group">
            <label for="t-last-name">Last Name</label>
            <input id="t-last-name" v-model="editForm.last_name" type="text" placeholder="Santos" />
          </div>
          <div class="form-group">
            <label for="t-middle-name">Middle Name</label>
            <input id="t-middle-name" v-model="editForm.middle_name" type="text" placeholder="Optional" />
          </div>
          <div class="form-group">
            <label for="t-name-ext">Name Extension</label>
            <input id="t-name-ext" v-model="editForm.name_extension" type="text" placeholder="Jr., III" />
          </div>
          <div class="form-group full-width">
            <label for="t-email">Email Address (Login Email)</label>
            <input id="t-email" :value="form.email" type="email" disabled class="disabled-input" />
            <span class="field-hint">This is the email address you used to login. It cannot be changed.</span>
          </div>
          <div class="form-group">
            <label for="t-phone">Phone Number</label>
            <input id="t-phone" v-model="editForm.phone" type="tel" placeholder="+63 900 000 0000" />
          </div>
          <div class="form-group full-width">
            <label for="t-avatar">Profile photo</label>
            <input
              id="t-avatar"
              type="file"
              accept="image/jpeg,image/png,image/webp,image/gif"
              class="file-input"
              @change="onAvatarFileChange"
            />
            <span class="field-hint">Shown on your profile and in Discover. JPG, PNG, or WebP.</span>
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
              <h2>Teaching Location <span class="required-badge">Required</span></h2>
              <p>Students in this area will see your listings</p>
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
            <label for="t-barangay">Barangay</label>
            <input id="t-barangay" v-model="editForm.barangay" type="text" placeholder="e.g. Brgy. 456" />
          </div>
          <div class="form-group">
            <label for="t-municipality">City / Municipality</label>
            <input id="t-municipality" v-model="editForm.municipality" type="text" placeholder="e.g. Makati City" />
          </div>
          <div class="form-group full-width">
            <label for="t-province">Province</label>
            <input id="t-province" v-model="editForm.province" type="text" placeholder="e.g. Metro Manila" />
          </div>
          <span class="field-hint loc-hint">📍 Accurate location helps students find you easily.</span>
        </div>
      </section>

      <!-- ── Teaching Bio ── -->
      <section class="profile-section">
        <div class="section-header">
          <div class="header-left">
            <div class="section-icon">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M22 10v6M2 10l10-5 10 5-10 5z"/><path d="M6 12v5c3 3 9 3 12 0v-5"/></svg>
            </div>
            <div>
              <h2>Teaching Profile</h2>
              <p>Your professional background</p>
            </div>
          </div>
        </div>

        <div v-if="!isEditing" class="info-display-full">
           <label>About You</label>
           <p class="bio-text">{{ form.bio || 'You haven\'t written a bio yet. Tell students about your teaching experience!' }}</p>
        </div>

        <div v-else class="form-group full-width">
          <label for="t-bio">About You as a Tutor</label>
          <textarea id="t-bio" v-model="editForm.bio" rows="5"
            placeholder="e.g. I'm a licensed Math teacher with 5 years of experience...">
          </textarea>
          <span class="char-count">{{ editForm.bio?.length || 0 }} / 500</span>
        </div>

        <div v-if="!isEditing" class="info-display-full" style="margin-top: 1rem;">
           <label>Achievements / Accomplishments</label>
           <p class="bio-text">{{ form.achievements || 'No achievements added yet.' }}</p>
        </div>

        <div v-else class="form-group full-width" style="margin-top: 1rem;">
          <label for="t-achievements">Achievements / Accomplishments</label>
          <textarea
            id="t-achievements"
            v-model="editForm.achievements"
            rows="4"
            placeholder="e.g. • PRC Licensed Teacher (2021)\n• Top 10 Math Olympiad Coach (2023)\n• AB English, University of ..."
          ></textarea>
          <span class="field-hint">Displayed to students in Discover when they open your profile.</span>
        </div>

        <div class="expertise-display" v-if="subjectTags.length">
          <label class="form-label-sm">Your Subject Areas (from listings)</label>
          <div class="tag-cloud">
            <span class="exp-tag" v-for="tag in subjectTags" :key="tag">{{ tag }}</span>
          </div>
        </div>
      </section>

      <!-- ── Actions ── -->
      <div class="save-row" v-if="isEditing">
        <button class="btn-cancel" @click="cancelEditing" :disabled="saving">Cancel</button>
        <button class="btn-save" @click="saveProfile" :disabled="saving">
          <span v-if="saving" class="spinner"></span>
          <svg v-else viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><path d="M19 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h11l5 5v11a2 2 0 0 1-2 2z"/><polyline points="17 21 17 13 7 13 7 21"/><polyline points="7 3 7 8 15 8"/></svg>
          {{ saving ? 'Saving...' : 'Save Changes' }}
        </button>
      </div>

      <section class="profile-section">
        <div class="section-header">
          <div class="header-left">
            <div class="section-icon">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 2l2.7 5.47L21 8.4l-4.5 4.39 1.06 6.21L12 16.2 6.44 19l1.06-6.21L3 8.4l6.3-.93L12 2z"/></svg>
            </div>
            <div>
              <h2>Tutor Tier</h2>
              <p>Upgrade workflow</p>
            </div>
          </div>
        </div>
        <div class="tier-box simple-tier-box">
          <div class="tier-status-row">
            <span class="tier-badge">{{ tierLabel }}</span>
            <span class="review-badge" :class="tierReviewBadgeClass">{{ tierReviewLabel }}</span>
          </div>
          <p class="tier-stage">{{ tierStageMessage }}</p>
          <p v-if="tierReviewSubmittedLabel" class="review-time">• {{ tierReviewSubmittedLabel }}</p>

          <div class="elig-progress">
            <div class="elig-row">
              <span class="elig-label">Completed sessions</span>
              <span class="elig-value">{{ completedSessionsCount }} / {{ UPGRADE_ELIGIBILITY_SESSIONS }}</span>
            </div>
            <div
              class="elig-bar"
              role="progressbar"
              :aria-valuenow="eligibilityPercent"
              aria-valuemin="0"
              aria-valuemax="100"
            >
              <div class="elig-fill" :style="{ width: eligibilityPercent + '%' }"></div>
            </div>
          </div>

          <div v-if="showCredentialStep" class="credential-card">
            <div class="tier-field">
              <label class="credential-label" for="tier-achievements">Achievements</label>
              <textarea
                id="tier-achievements"
                v-model="tierAchievements"
                rows="3"
                class="tier-textarea"
                placeholder="Add key achievements for your upgrade request"
              />
            </div>
            <div class="credential-card-top">
              <label for="tier-credential" class="credential-label">Credentials proof</label>
              <span class="credential-hint">You can upload multiple files</span>
            </div>
            <input
              id="tier-credential"
              type="file"
              accept=".pdf,image/*,.doc,.docx"
              class="file-input tier-file-input"
              multiple
              @change="onCredentialFileChange"
            />
            <div class="credential-list" v-if="existingCredentialDocs.length || credentialFiles.length">
              <a
                v-for="doc in existingCredentialDocs"
                :key="'existing-'+doc.id"
                :href="doc.url"
                target="_blank"
                rel="noopener noreferrer"
                class="credential-link"
              >
                {{ doc.name }}
              </a>
              <span
                v-for="(file, idx) in credentialFiles"
                :key="'new-'+idx+'-'+file.name"
                class="selected-file"
              >
                {{ file.name }}
                <button type="button" class="file-remove-btn" @click="removeCredentialFile(idx)">×</button>
              </span>
            </div>
          </div>

          <div class="tier-actions">
            <button
              v-if="showSubmitForReviewAction"
              class="btn-upgrade-tier"
              type="button"
              :disabled="tierSubmitDisabled"
              @click="submitTierReview"
            >
              {{ tierSubmitting ? 'Submitting...' : 'Submit Review' }}
            </button>

            <template v-if="canUpgradeAfterApproval">
              <button
                class="btn-simulate-payment"
                type="button"
                :disabled="tierSubmitting || paymentSimulated"
                @click="openPaymentModal"
              >
                {{ paymentSimulated ? 'Paid' : 'Pay PHP 199' }}
              </button>
              <button
                class="btn-upgrade-after-pay"
                type="button"
                :disabled="tierSubmitting || !paymentSimulated"
                @click="activateTierUpgrade"
              >
                {{ tierSubmitting ? 'Activating...' : 'Upgrade Now' }}
              </button>
            </template>
          </div>
        </div>
      </section>

    </div>
  </div>
  <Teleport to="body">
    <div v-if="showPaymentModal" class="pay-modal-backdrop" @click.self="closePaymentModal">
      <div class="pay-modal-card">
        <h3>Payment</h3>
        <div class="pay-amount">Amount: <strong>PHP 199</strong></div>
        <label class="pay-field">
          Payment Method
          <select v-model="paymentMethod">
            <option value="gcash">GCash</option>
            <option value="card">Card</option>
            <option value="bank">Bank Transfer</option>
          </select>
        </label>
        <label class="pay-field">
          Reference Number
          <input v-model.trim="paymentReference" type="text" placeholder="e.g. TXN-123456" />
        </label>
        <div class="pay-actions">
          <button class="btn-cancel-pay" type="button" @click="closePaymentModal">Cancel</button>
          <button class="btn-confirm-pay" type="button" @click="confirmPaymentSimulation">Confirm</button>
        </div>
      </div>
    </div>
  </Teleport>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted, watch } from 'vue';
import { supabase } from '../../supabase';
import { bookingService, profileService, postService, formatApiErrorMessage } from '../../services/api';
import { useToast } from '../../composables/useToast';

const props = defineProps({ profile: Object });
const emit = defineEmits(['profile-updated']);
const { showToast } = useToast();

const isEditing = ref(false);
const saving = ref(false);
const djangoProfileId = ref(null);
const subjectTags = ref([]);

const form = ref({
  first_name: '', last_name: '', middle_name: '', name_extension: '', email: '', phone: '', bio: '', achievements: '',
  barangay: '', municipality: '', province: '',
  avatar_url: '', tutor_tier: 'basic',
  tier_review_status: 'not_submitted',
  tier_review_submitted_at: null,
  credentials_document_url: '',
  credentials_documents: [],
});

const avatarFile = ref(null);
const avatarPreviewUrl = ref('');
const credentialFiles = ref([]);
const tierSubmitting = ref(false);
const showPaymentModal = ref(false);
const paymentMethod = ref('gcash');
const paymentReference = ref('');
const paymentSimulated = ref(false);
const tierAchievements = ref('');

const UPGRADE_ELIGIBILITY_SESSIONS = 10;
const completedSessionsCount = ref(0);

// Separate form for editing to allow cancellation
const editForm = ref({});

const initials = computed(() => {
  const f = form.value.first_name?.charAt(0) || '?';
  const l = form.value.last_name?.charAt(0) || '';
  return (f + l).toUpperCase();
});

const displayFullName = computed(() => {
  const f = form.value.first_name?.trim() || '';
  const m = form.value.middle_name?.trim() || '';
  const l = form.value.last_name?.trim() || '';
  const ext = form.value.name_extension?.trim() || '';
  const core = [f, m, l].filter(Boolean).join(' ');
  if (!core && !ext) return '';
  return ext ? `${core} ${ext}`.trim() : core;
});

const avatarDisplayUrl = computed(() => {
  if (isEditing.value && avatarPreviewUrl.value) return avatarPreviewUrl.value;
  return form.value.avatar_url || '';
});

const tierLabel = computed(() => {
  const tier = form.value.tutor_tier || 'basic';
  if (tier === 'pro') return 'Tier 3 - Pro Tutor';
  if (tier === 'plus') return 'Tier 2 - Plus Tutor';
  return 'Tier 1 - Basic Tutor';
});

const tierReviewLabel = computed(() => {
  const s = form.value.tier_review_status || 'not_submitted';
  if (s === 'approved') return 'Approved';
  if (s === 'rejected') return 'Rejected';
  if (s === 'pending') return 'Pending';
  return 'Draft';
});

const tierReviewBadgeClass = computed(() => {
  const s = form.value.tier_review_status || 'not_submitted';
  if (s === 'approved') return 'approved';
  if (s === 'rejected') return 'rejected';
  if (s === 'pending') return 'pending';
  return 'not-submitted';
});

const tierReviewSubmittedLabel = computed(() => {
  if (!form.value.tier_review_submitted_at) return '';
  return new Date(form.value.tier_review_submitted_at).toLocaleString('en-US', {
    month: 'short',
    day: 'numeric',
    hour: 'numeric',
    minute: '2-digit',
  });
});

const isUpgradeLocked = computed(() => form.value.tutor_tier !== 'basic');
const canUpgradeAfterApproval = computed(() => form.value.tutor_tier === 'basic' && form.value.tier_review_status === 'approved');
// Credentials upload should be visible for all non-upgraded tutors,
// including "pending" and "rejected" states (so they can re-submit).
const showCredentialStep = computed(() => !isUpgradeLocked.value);
// Submit button should only appear when not pending and not approved.
const showSubmitForReviewAction = computed(() =>
  !isUpgradeLocked.value && form.value.tier_review_status !== 'pending' && form.value.tier_review_status !== 'approved'
);
const tierSubmitDisabled = computed(() =>
  tierSubmitting.value || isUpgradeLocked.value || form.value.tier_review_status === 'pending' || canUpgradeAfterApproval.value
);
const tierStageMessage = computed(() => {
  if (isUpgradeLocked.value) return 'Upgrade complete';
  if (canUpgradeAfterApproval.value) return 'Eligible for upgrade';
  if (form.value.tier_review_status === 'pending') return 'Waiting for review';
  if (form.value.tier_review_status === 'rejected') return 'Rejected';
  return 'Ready to submit';
});

const eligibilityPercent = computed(() => {
  const pct = (completedSessionsCount.value / UPGRADE_ELIGIBILITY_SESSIONS) * 100;
  return Math.max(0, Math.min(100, Math.round(pct)));
});

async function loadCompletedSessionsCount(tutorUserId) {
  if (!tutorUserId) return;
  try {
    const { data } = await bookingService.getTutorBookings(tutorUserId);
    const bookings = Array.isArray(data) ? data : (data?.results || []);
    completedSessionsCount.value = bookings.filter((b) => b.status === 'completed').length;
  } catch (_e) {
    completedSessionsCount.value = 0;
  }
}

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

function onCredentialFileChange(ev) {
  const input = ev.target;
  const files = Array.from(input.files || []);
  if (files.length) {
    credentialFiles.value = [...credentialFiles.value, ...files];
  }
  input.value = '';
}

function removeCredentialFile(idx) {
  credentialFiles.value.splice(idx, 1);
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
  form.value.middle_name  = p.middle_name  || '';
  form.value.name_extension = p.name_extension || '';
  form.value.email        = p.email        || '';
  form.value.phone        = p.phone        || '';
  form.value.bio          = p.bio          || '';
  form.value.achievements = p.achievements || '';
  form.value.barangay     = p.barangay     || '';
  form.value.municipality = p.municipality || '';
  form.value.province     = p.province     || '';
  form.value.avatar_url   = p.avatar_url   || '';
  form.value.tutor_tier   = p.tutor_tier   || 'basic';
  form.value.tier_review_status = p.tier_review_status || 'not_submitted';
  form.value.tier_review_submitted_at = p.tier_review_submitted_at || null;
  form.value.credentials_document_url = p.credentials_document_url || '';
  form.value.credentials_documents = Array.isArray(p.credentials_documents) ? p.credentials_documents : [];
  tierAchievements.value = form.value.achievements || '';
};

const existingCredentialDocs = computed(() => {
  const docs = Array.isArray(form.value.credentials_documents) ? form.value.credentials_documents : [];
  if (docs.length) return docs;
  return form.value.credentials_document_url
    ? [{ id: 'legacy', name: 'Current file', url: form.value.credentials_document_url }]
    : [];
});

watch(() => props.profile, (newProfile) => {
  populateFromProp(newProfile);
}, { immediate: true });

watch(
  () => props.profile?.user,
  (tutorUserId) => {
    if (tutorUserId) loadCompletedSessionsCount(tutorUserId);
  },
  { immediate: true }
);

// Get Django profile ID for save operations
const loadDjangoProfileId = async () => {
  const { data: { session } } = await supabase.auth.getSession();
  if (!session?.user) return;
  try {
    const { data } = await profileService.getProfileByEmail(session.user.email, 'tutor');
    const profiles = Array.isArray(data) ? data : (data.results || []);
    if (profiles[0]) {
      djangoProfileId.value = profiles[0].id;
      const row = profiles[0];
      if (row.email) form.value.email = row.email;
      if (row.avatar_url) form.value.avatar_url = row.avatar_url;
      if (row.middle_name != null && row.middle_name !== '') form.value.middle_name = row.middle_name;
      if (row.name_extension != null && row.name_extension !== '') form.value.name_extension = row.name_extension;
      if (row.barangay) form.value.barangay = row.barangay;
      if (row.municipality) form.value.municipality = row.municipality;
      if (row.province) form.value.province = row.province;
      paymentSimulated.value = sessionStorage.getItem(`turo_upgrade_paid_${profiles[0].id}`) === '1';
    }
  } catch (e) {
    console.warn('Could not get Django profile ID:', e);
  }
};

onUnmounted(() => {
  clearAvatarSelection();
});

onMounted(async () => {
  loadDjangoProfileId();

  // Load subjects from tutor's posts
  try {
    const { data: { session } } = await supabase.auth.getSession();
    const { data: posts } = await postService.getAllPosts();
    const myPosts = (Array.isArray(posts) ? posts : posts.results || [])
      .filter(post => post.tutor_profile?.email === session?.user?.email);
    const subjects = [...new Set(myPosts.map(p => p.subject).filter(Boolean))];
    subjectTags.value = subjects;
  } catch (e) { /* non-critical */ }
});

function openPaymentModal() {
  if (form.value.tutor_tier !== 'basic') {
    showToast('This account already has a completed upgrade.', 'info');
    return;
  }
  if (form.value.tier_review_status !== 'approved') {
    showToast('Wait for admin approval first before payment.', 'info');
    return;
  }
  showPaymentModal.value = true;
}

function closePaymentModal() {
  showPaymentModal.value = false;
  paymentMethod.value = 'gcash';
  paymentReference.value = '';
}

function confirmPaymentSimulation() {
  if (!paymentReference.value) {
    showToast('Please enter a payment reference number.', 'error');
    return;
  }
  paymentSimulated.value = true;
  if (djangoProfileId.value) {
    sessionStorage.setItem(`turo_upgrade_paid_${djangoProfileId.value}`, '1');
  }
  closePaymentModal();
  showToast('Payment simulated successfully. You can now submit for review.', 'success');
}

const saveProfile = async () => {
  saving.value = true;
  try {
    const { data: { user }, error: userErr } = await supabase.auth.getUser();
    if (userErr) throw userErr;
    const email = user?.email;
    if (!email) throw new Error('You must be signed in to save your profile.');

    if (!djangoProfileId.value) {
      const { data } = await profileService.getProfileByEmail(email, 'tutor');
      const profiles = Array.isArray(data) ? data : (data.results || []);
      if (profiles[0]) djangoProfileId.value = profiles[0].id;
    }
    if (!djangoProfileId.value) {
      throw new Error('Could not load your profile from the server. Try refreshing the page.');
    }

    const payload = {
      first_name: editForm.value.first_name ?? '',
      last_name: editForm.value.last_name ?? '',
      middle_name: editForm.value.middle_name ?? '',
      name_extension: editForm.value.name_extension ?? '',
      phone: editForm.value.phone ?? '',
      bio: editForm.value.bio ?? '',
      achievements: editForm.value.achievements ?? '',
      barangay: editForm.value.barangay ?? '',
      municipality: editForm.value.municipality ?? '',
      province: editForm.value.province ?? '',
    };

    let newAvatarUrl = null;
    if (avatarFile.value) {
      const fd = new FormData();
      Object.entries(payload).forEach(([k, v]) => fd.append(k, v ?? ''));
      fd.append('avatar', avatarFile.value);
      const { data } = await profileService.updateProfile(djangoProfileId.value, fd);
      newAvatarUrl = data?.avatar_url ?? null;
    } else {
      await profileService.updateProfile(djangoProfileId.value, payload);
    }

    const { error: metaErr } = await supabase.auth.updateUser({
      data: { first_name: payload.first_name, last_name: payload.last_name },
    });
    if (metaErr) console.warn('Supabase auth metadata update:', metaErr.message);

    const { error: sbErr } = await supabase.from('profiles').upsert(
      {
        id: user.id,
        first_name: payload.first_name,
        last_name: payload.last_name,
      },
      { onConflict: 'id' },
    );
    if (sbErr) console.warn('Supabase profiles upsert:', sbErr.message);

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
    showToast(formatApiErrorMessage(err), 'error');
  } finally {
    saving.value = false;
  }
};

const submitTierReview = async () => {
  if (tierSubmitting.value) return;
  if (form.value.tutor_tier !== 'basic') {
    showToast('Your account already received the one-time tier upgrade.', 'info');
    return;
  }
  if (form.value.tier_review_status === 'approved') {
    showToast('You are already approved for eligibility. Complete payment to activate upgrade.', 'info');
    return;
  }
  if (form.value.tier_review_status === 'pending') {
    showToast('Your previous request is still pending admin review.', 'info');
    return;
  }
  if (!tierAchievements.value?.trim()) {
    showToast('Please add achievements/accomplishments first before submitting.', 'error');
    return;
  }
  if (!credentialFiles.value.length && !existingCredentialDocs.value.length) {
    showToast('Please upload at least one credentials document.', 'error');
    return;
  }
  if (!djangoProfileId.value) {
    showToast('Profile not loaded yet. Please try again in a moment.', 'error');
    return;
  }

  tierSubmitting.value = true;
  try {
    const fd = new FormData();
    fd.append('achievements', tierAchievements.value || '');
    fd.append('tier_review_status', 'pending');
    credentialFiles.value.forEach((file) => fd.append('credentials_documents', file));
    const { data } = await profileService.updateProfile(djangoProfileId.value, fd);
    form.value.achievements = data?.achievements ?? tierAchievements.value ?? form.value.achievements;
    tierAchievements.value = form.value.achievements || '';
    form.value.tier_review_status = data?.tier_review_status ?? 'pending';
    form.value.tier_review_submitted_at = data?.tier_review_submitted_at ?? form.value.tier_review_submitted_at;
    form.value.credentials_document_url = data?.credentials_document_url ?? form.value.credentials_document_url;
    form.value.credentials_documents = Array.isArray(data?.credentials_documents)
      ? data.credentials_documents
      : form.value.credentials_documents;
    if (isEditing.value) {
      editForm.value.achievements = form.value.achievements;
    }
    credentialFiles.value = [];
    emit('profile-updated', { ...form.value });
    showToast('Tier eligibility submitted. Waiting for admin validation.', 'success');
  } catch (err) {
    console.error('Tier review submit error:', err);
    showToast(formatApiErrorMessage(err), 'error');
  } finally {
    tierSubmitting.value = false;
  }
};

const activateTierUpgrade = async () => {
  if (tierSubmitting.value) return;
  if (!canUpgradeAfterApproval.value) {
    showToast('You are not eligible for activation yet.', 'error');
    return;
  }
  if (!paymentSimulated.value) {
    showToast('Please complete payment simulation first.', 'error');
    return;
  }
  if (!djangoProfileId.value) {
    showToast('Profile not loaded yet. Please try again in a moment.', 'error');
    return;
  }

  tierSubmitting.value = true;
  try {
    const { data } = await profileService.updateProfile(djangoProfileId.value, {
      tutor_tier: 'plus',
    });
    form.value.tutor_tier = data?.tutor_tier || 'plus';
    paymentSimulated.value = false;
    if (djangoProfileId.value) {
      sessionStorage.removeItem(`turo_upgrade_paid_${djangoProfileId.value}`);
    }
    emit('profile-updated', { ...form.value });
    showToast('Tier upgrade activated successfully!', 'success');
  } catch (err) {
    console.error('Tier activation error:', err);
    showToast(formatApiErrorMessage(err), 'error');
  } finally {
    tierSubmitting.value = false;
  }
};
</script>

<style scoped>
/* Styles remain identical to the previous version */
.profile-page { display: flex; flex-direction: column; gap: 0; max-width: 820px; margin: 0 auto; }
.profile-hero { position: relative; border-radius: 1.5rem; overflow: hidden; margin-bottom: 1.25rem; }
.hero-bg { position: absolute; inset: 0; background: linear-gradient(135deg, #07193f 0%, #0d2859 50%, #1a3a6e 100%); }
.hero-content { position: relative; display: flex; align-items: center; gap: 1.5rem; padding: 2rem 2.5rem; }
.avatar-ring { position: relative; flex-shrink: 0; }
.avatar-circle { width: 80px; height: 80px; border-radius: 50%; background: linear-gradient(135deg, #4ecdc4, #26a69a); display: flex; align-items: center; justify-content: center; font-size: 1.8rem; font-weight: 900; color: #ffffff; border: 3px solid rgba(255,255,255,0.25); box-shadow: 0 8px 24px rgba(0,0,0,0.25); }
.avatar-circle.has-photo { padding: 0; background: #0f172a; overflow: hidden; }
.avatar-img { width: 100%; height: 100%; object-fit: cover; display: block; }
.file-input { padding: 0.5rem 0; font-size: 0.88rem; }
.role-badge { position: absolute; bottom: -4px; right: -4px; font-size: 0.6rem; font-weight: 900; padding: 0.2rem 0.5rem; border-radius: 2rem; text-transform: uppercase; letter-spacing: 0.05em; border: 2px solid white; }
.role-badge.tutor { background: #4ecdc4; color: #0f172a; }
.hero-name-row { display: flex; align-items: center; gap: 0.6rem; flex-wrap: wrap; }
.hero-tier-badge { display: inline-flex; align-items: center; padding: 0.25rem 0.6rem; border-radius: 999px; background: rgba(59, 130, 246, 0.18); border: 1px solid rgba(147, 197, 253, 0.55); color: #dbeafe; font-size: 0.68rem; font-weight: 900; text-transform: uppercase; letter-spacing: 0.03em; }
.hero-elig { display: flex; align-items: center; gap: 0.6rem; margin-top: 0.4rem; flex-wrap: wrap; }
.hero-elig-text { font-size: 0.78rem; font-weight: 800; color: rgba(255,255,255,0.78); }
.hero-elig-bar { width: 160px; height: 8px; background: rgba(255,255,255,0.18); border-radius: 999px; overflow: hidden; }
.hero-elig-fill { height: 100%; background: linear-gradient(90deg, #f59e0b, #22c55e); border-radius: 999px; transition: width 0.35s ease; }
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
.form-label-sm { font-size: 0.82rem; font-weight: 700; color: #475569; text-transform: uppercase; letter-spacing: 0.05em; display: block; margin-bottom: 0.5rem; }
.form-group input, .form-group textarea { padding: 0.75rem 1rem; border: 1.5px solid #e8ecf4; border-radius: 0.75rem; font-size: 0.92rem; color: #0f172a; background: #f8fafc; outline: none; transition: border-color 0.2s, box-shadow 0.2s; font-family: inherit; }
.form-group input:focus, .form-group textarea:focus { border-color: #0f172a; box-shadow: 0 0 0 3px rgba(15,23,42,0.06); background: #ffffff; }
.disabled-input { opacity: 0.55; cursor: not-allowed; }
.form-group textarea { resize: vertical; min-height: 120px; }
.field-hint { font-size: 0.75rem; color: #94a3b8; }
.loc-hint { color: #d97706; font-weight: 600; margin-top: 0.5rem; display: block; }
.char-count { font-size: 0.72rem; color: #94a3b8; text-align: right; }
.expertise-display { margin-top: 1rem; }
.tag-cloud { display: flex; flex-wrap: wrap; gap: 0.5rem; }
.exp-tag {
  display: inline-flex;
  align-items: center;
  padding: 0.28rem 0.62rem;
  border-radius: 999px;
  background: #f1f5f9;
  color: #475569;
  font-size: 0.74rem;
  font-weight: 800;
}
.save-row { display: flex; align-items: center; justify-content: flex-end; gap: 1rem; padding: 0.5rem 0 1rem; }
.btn-cancel { padding: 0.85rem 1.5rem; background: transparent; border: 1.5px solid #e2e8f0; border-radius: 0.85rem; color: #64748b; font-weight: 800; cursor: pointer; transition: all 0.2s; }
.btn-cancel:hover:not(:disabled) { background: #f1f5f9; color: #0f172a; }
.btn-save { display: flex; align-items: center; gap: 0.6rem; padding: 0.85rem 2rem; background: linear-gradient(135deg, #07193f, #0d2859); color: #ffffff; border: none; border-radius: 0.85rem; font-size: 0.92rem; font-weight: 800; cursor: pointer; transition: all 0.2s; box-shadow: 0 4px 16px rgba(7,25,63,0.3); }
.btn-save:hover:not(:disabled) { transform: translateY(-2px); box-shadow: 0 8px 24px rgba(7,25,63,0.35); }
.btn-save:disabled { opacity: 0.6; cursor: not-allowed; }
.btn-save svg { width: 18px; height: 18px; }
.tier-box {
  position: relative;
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  gap: 1rem;
  padding: 1.1rem 1.2rem;
  border: 1.5px solid #dbe4f4;
  border-radius: 1rem;
  background: linear-gradient(145deg, #f8fbff 0%, #ffffff 45%, #f5f9ff 100%);
  box-shadow: 0 12px 30px rgba(15, 23, 42, 0.06);
}
.tier-box::after {
  content: '';
  position: absolute;
  right: -30px;
  top: -30px;
  width: 120px;
  height: 120px;
  border-radius: 50%;
  background: radial-gradient(circle, rgba(147, 197, 253, 0.22) 0%, rgba(147, 197, 253, 0) 70%);
  pointer-events: none;
}
.tier-left { display: flex; flex-direction: column; gap: 0.55rem; flex: 1; }
.tier-head-row { display: flex; align-items: center; gap: 0.5rem; flex-wrap: wrap; }
.tier-badge {
  display: inline-flex;
  align-items: center;
  width: fit-content;
  padding: 0.4rem 0.85rem;
  border-radius: 999px;
  background: linear-gradient(135deg, #dbeafe, #bfdbfe);
  color: #1e3a8a;
  border: 1px solid #93c5fd;
  font-size: 0.74rem;
  font-weight: 900;
  text-transform: uppercase;
  letter-spacing: 0.04em;
}
.tier-note { margin: 0; font-size: 0.82rem; color: #475569; line-height: 1.45; }
.review-badge {
  display: inline-flex;
  align-items: center;
  padding: 0.24rem 0.58rem;
  border-radius: 999px;
  font-size: 0.68rem;
  font-weight: 900;
  border: 1px solid transparent;
}
.review-badge.not-submitted { background: #f1f5f9; color: #475569; }
.review-badge.pending { background: #fef3c7; color: #92400e; border-color: #fcd34d; }
.review-badge.approved { background: #dcfce7; color: #166534; border-color: #86efac; }
.review-badge.rejected { background: #fee2e2; color: #b91c1c; border-color: #fca5a5; }
.review-time { font-size: 0.72rem; color: #64748b; font-weight: 600; margin: 0; }
.credential-card {
  border: 1px solid #dfe8f7;
  border-radius: 0.9rem;
  padding: 0.8rem 0.95rem;
  background: #ffffff;
  display: flex;
  flex-direction: column;
  gap: 0.45rem;
  box-shadow: inset 0 1px 0 rgba(255, 255, 255, 0.8);
}
.credential-card-top { display: flex; align-items: flex-start; justify-content: space-between; gap: 0.8rem; flex-wrap: wrap; }
.credential-label { font-size: 0.72rem; font-weight: 900; color: #334155; text-transform: uppercase; letter-spacing: 0.05em; }
.credential-hint { margin: 0.15rem 0 0; font-size: 0.72rem; color: #94a3b8; }
.credential-link { font-size: 0.76rem; color: #1d4ed8; font-weight: 800; text-decoration: underline; text-underline-offset: 3px; white-space: nowrap; }
.tier-file-input { padding: 0.2rem 0; font-size: 0.85rem; }
.selected-file { font-size: 0.75rem; color: #64748b; font-weight: 600; }
.credential-list {
  display: flex;
  flex-wrap: wrap;
  gap: 0.45rem;
  align-items: center;
}
.tier-field { display: flex; flex-direction: column; gap: 0.35rem; margin-bottom: 0.6rem; }
.tier-textarea {
  border: 1px solid #dbe4f4;
  border-radius: 0.75rem;
  padding: 0.65rem 0.75rem;
  font-size: 0.88rem;
  resize: vertical;
  min-height: 78px;
  background: #ffffff;
  color: #0f172a;
  outline: none;
}
.tier-textarea:focus { border-color: #0f172a; box-shadow: 0 0 0 3px rgba(15,23,42,0.06); }
.selected-file {
  display: inline-flex;
  align-items: center;
  gap: 0.35rem;
  background: #f8fafc;
  border: 1px solid #dbe4f4;
  border-radius: 999px;
  padding: 0.18rem 0.45rem;
}
.file-remove-btn {
  border: none;
  background: transparent;
  color: #64748b;
  cursor: pointer;
  font-weight: 900;
  line-height: 1;
  padding: 0;
}
.btn-upgrade-tier {
  border: 1px solid #0f172a;
  background: linear-gradient(135deg, #0f172a, #1e293b);
  color: #ffffff;
  padding: 0.72rem 1.05rem;
  border-radius: 0.8rem;
  font-weight: 800;
  font-size: 0.8rem;
  cursor: pointer;
  white-space: nowrap;
  box-shadow: 0 10px 22px rgba(15, 23, 42, 0.28);
}
.btn-upgrade-tier:hover:not(:disabled) { transform: translateY(-1px); }
.btn-upgrade-tier:disabled { opacity: 0.65; cursor: not-allowed; }
.tier-locked-note { margin: 0; font-size: 0.78rem; color: #475569; font-weight: 700; }
.simple-tier-box {
  gap: 0.8rem;
  padding: 1rem;
  box-shadow: none;
  background: #ffffff;
}
.simple-tier-box::after { display: none; }
.tier-status-row { display: flex; align-items: center; gap: 0.45rem; flex-wrap: wrap; }
.tier-stage {
  margin: 0;
  font-size: 0.86rem;
  color: #334155;
  font-weight: 600;
}
.tier-actions {
  display: flex;
  flex-wrap: wrap;
  gap: 0.55rem;
}
.elig-progress {
  border: 1px solid #dbe4f4;
  border-radius: 0.85rem;
  padding: 0.75rem 0.85rem;
  background: #f8fafc;
}
.elig-row { display: flex; align-items: center; justify-content: space-between; margin-bottom: 0.45rem; }
.elig-label { font-size: 0.75rem; font-weight: 900; color: #334155; text-transform: uppercase; letter-spacing: 0.04em; }
.elig-value { font-size: 0.85rem; font-weight: 900; color: #0f172a; }
.elig-bar { height: 10px; background: #e2e8f0; border-radius: 999px; overflow: hidden; }
.elig-fill { height: 100%; background: linear-gradient(90deg, #0f172a, #3b82f6); border-radius: 999px; transition: width 0.35s ease; }
.payment-sim-card {
  border: 1px solid #dbe4f4;
  border-radius: 0.85rem;
  padding: 0.75rem 0.85rem;
  background: #f8fbff;
  display: flex;
  flex-direction: column;
  gap: 0.35rem;
}
.payment-row { display: flex; align-items: center; justify-content: space-between; font-size: 0.82rem; font-weight: 800; color: #0f172a; }
.payment-note { margin: 0; font-size: 0.74rem; color: #64748b; }
.btn-simulate-payment {
  border: 1px solid #1d4ed8;
  background: #ffffff;
  color: #1d4ed8;
  border-radius: 0.65rem;
  font-size: 0.78rem;
  font-weight: 800;
  padding: 0.55rem 0.7rem;
  cursor: pointer;
}
.btn-simulate-payment:disabled { opacity: 0.65; cursor: not-allowed; }
.btn-upgrade-after-pay {
  border: 1px solid #0f172a;
  background: #0f172a;
  color: #fff;
  border-radius: 0.65rem;
  font-size: 0.78rem;
  font-weight: 800;
  padding: 0.55rem 0.7rem;
  cursor: pointer;
}
.btn-upgrade-after-pay:disabled { opacity: 0.65; cursor: not-allowed; }
.btn-upgrade-tier,
.btn-simulate-payment,
.btn-upgrade-after-pay {
  box-shadow: none;
}
.pay-modal-backdrop {
  position: fixed;
  inset: 0;
  background: rgba(2, 6, 23, 0.45);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1200;
}
.pay-modal-card {
  width: min(460px, 92vw);
  background: #fff;
  border-radius: 1rem;
  padding: 1rem;
  border: 1px solid #dbe4f4;
}
.pay-modal-card h3 { margin: 0; font-size: 1rem; font-weight: 900; color: #0f172a; }
.pay-sub { margin: 0.35rem 0 0.7rem; font-size: 0.83rem; color: #64748b; }
.pay-amount { font-size: 0.9rem; color: #0f172a; margin-bottom: 0.65rem; }
.pay-field { display: flex; flex-direction: column; gap: 0.35rem; font-size: 0.8rem; font-weight: 700; color: #334155; margin-bottom: 0.65rem; }
.pay-field select, .pay-field input {
  border: 1px solid #dbe4f4;
  border-radius: 0.65rem;
  padding: 0.55rem 0.65rem;
  font-size: 0.85rem;
}
.pay-actions { display: flex; justify-content: flex-end; gap: 0.5rem; margin-top: 0.7rem; }
.btn-cancel-pay, .btn-confirm-pay {
  border-radius: 0.65rem;
  padding: 0.55rem 0.85rem;
  font-size: 0.8rem;
  font-weight: 800;
  cursor: pointer;
}
.btn-cancel-pay { border: 1px solid #cbd5e1; background: #fff; color: #334155; }
.btn-confirm-pay { border: 1px solid #0f172a; background: #0f172a; color: #fff; }
.spinner { width: 16px; height: 16px; border: 2px solid rgba(255,255,255,0.3); border-top-color: white; border-radius: 50%; animation: spin 0.7s linear infinite; flex-shrink: 0; }
@keyframes spin { to { transform: rotate(360deg); } }
@media (max-width: 768px) {
  .hero-content { padding: 1.5rem; gap: 1rem; }
  .avatar-circle { width: 64px; height: 64px; font-size: 1.4rem; }
  .hero-text h1 { font-size: 1.25rem; }
  .profile-section { padding: 1.25rem; }
  .form-grid { grid-template-columns: 1fr; }
  .save-row { flex-direction: column; align-items: stretch; }
  .btn-save, .btn-cancel { justify-content: center; width: 100%; }
  .tier-box,
  .simple-tier-box { flex-direction: column; align-items: stretch !important; gap: 1rem; }
  .tier-status-row { width: 100%; flex-wrap: wrap; }
  .tier-field { width: 100%; box-sizing: border-box; }
  .tier-textarea { max-width: 100%; box-sizing: border-box; width: 100%; }
  .elig-progress { width: 100%; box-sizing: border-box; }
  .elig-row { flex-wrap: wrap; gap: 0.25rem; }
  .credential-card { width: 100%; box-sizing: border-box; padding: 0.75rem; }
  .credential-card-top { flex-direction: column; align-items: flex-start; gap: 0.5rem; }
  .tier-actions { width: 100%; flex-direction: column; }
  .tier-actions button,
  .btn-upgrade-tier,
  .btn-simulate-payment,
  .btn-upgrade-after-pay { width: 100%; justify-content: center; }
  .credential-list { flex-direction: column; align-items: flex-start; }
  .credential-link { white-space: normal; word-break: break-word; }
  .selected-file { max-width: 100%; word-break: break-all; }
  .info-display-grid { grid-template-columns: 1fr; }
  .tier-file-input { width: 100%; }
}
</style>
