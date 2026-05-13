<template>
  <div class="discover-tab">
    
    <!-- ── Desktop Header ── -->
    <div class="page-header desktop-only">
      <div class="header-text">
        <h1>Discover Tutors</h1>
        <p>Find the best tutors for your needs</p>
      </div>
    </div>

    <!-- ── Location Scope Banner ── -->
    <div class="location-banner" v-if="profile?.province">
      <div class="loc-left">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0z"/><circle cx="12" cy="10" r="3"/></svg>
        <span>Your location: <strong>{{ [profile.barangay, profile.municipality, profile.province].filter(Boolean).join(', ') }}</strong></span>
      </div>
      <div class="loc-scope-group">
        <button type="button"
          :class="['scope-pill', { active: locationScope === 'municipality' }]"
          @click="locationScope = 'municipality'"
          :disabled="!profile.municipality"
          :title="profile.municipality ? 'Same city/municipality' : 'Set your municipality in My Profile'"
        >📍 Same City</button>
        <button type="button"
          :class="['scope-pill', { active: locationScope === 'province' }]"
          @click="locationScope = 'province'"
        >🏙️ Same Province</button>
        <button type="button"
          :class="['scope-pill', { active: locationScope === 'all' }]"
          @click="locationScope = 'all'"
        >🌐 All</button>
      </div>
    </div>
    <div class="location-banner warn" v-else>
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"/><line x1="12" y1="8" x2="12" y2="12"/><line x1="12" y1="16" x2="12.01" y2="16"/></svg>
      <span>Set your <strong>location</strong> in <strong>My Profile</strong> to filter tutors near you</span>
    </div>

    <!-- ── Browse mode: tutors (grouped) vs every listing ── -->
    <div class="browse-mode-row">
      <span class="browse-label">View</span>
      <div class="browse-toggle" role="group" aria-label="Browse mode">
        <button
          type="button"
          :class="['browse-pill', { active: browseMode === 'tutors' }]"
          @click="setBrowseMode('tutors')"
        >
          {{ tutorsBrowseLabel }}
        </button>
        <button
          type="button"
          :class="['browse-pill', { active: browseMode === 'listings' }]"
          @click="setBrowseMode('listings')"
        >
          All listings
        </button>
      </div>
    </div>

    <!-- ── Drill-down: one tutor's listings ── -->
    <div v-if="browseMode === 'tutors' && selectedTutorId !== null" class="tutor-listings-bar">
      <button type="button" class="btn-back-tutor" @click="clearSelectedTutor">
        <span aria-hidden="true">←</span> Back to {{ tutorsBrowseLabel }}
      </button>
      <p class="tutor-listings-intro">
        <strong>{{ selectedTutorDisplayName }}</strong>
        — {{ tutorDetailPostsFiltered.length }}
        listing{{ tutorDetailPostsFiltered.length === 1 ? '' : 's' }}
      </p>
    </div>

    <!-- ── Search & Filter ── -->
    <div class="filter-bar">
      <div class="search-field">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><circle cx="11" cy="11" r="8"/><path d="m21 21-4.3-4.3"/></svg>
        <input type="text" v-model="searchQuery" placeholder="Search by subject, name, or expertise..." />
      </div>
      
      <div class="category-scroll">
        <button 
          type="button"
          v-for="cat in categories" 
          :key="cat"
          @click="activeCategory = cat"
          :class="['cat-pill', { active: activeCategory === cat }]"
        >
          {{ cat }}
        </button>
      </div>

      <select class="sort-select">
        <option>Best Match</option>
        <option>Top Rated</option>
        <option>Lowest Price</option>
      </select>
    </div>

    <!-- ── Results Meta ── -->
    <div class="results-bar">
      <p v-if="browseMode === 'tutors' && selectedTutorId === null" class="results-count">
        Found <strong>{{ tutorGroupsFiltered.length }}</strong>
        tutor{{ tutorGroupsFiltered.length === 1 ? '' : 's' }}
        <span class="results-hint">{{ tutorsBrowseHint }}</span>
      </p>
      <p v-else-if="browseMode === 'tutors' && selectedTutorId !== null" class="results-count">
        Showing <strong>{{ tutorDetailPostsFiltered.length }}</strong> listing{{ tutorDetailPostsFiltered.length === 1 ? '' : 's' }} from this tutor
      </p>
      <p v-else class="results-count">
        Found <strong>{{ listingCardsFiltered.length }}</strong> listing{{ listingCardsFiltered.length === 1 ? '' : 's' }}
      </p>
    </div>

    <!-- ── Tutors Grid ── -->
    <div v-if="loading" class="loading-state">
      <div class="spinner"></div>
      <p>Finding the best tutors for you...</p>
    </div>

    <p v-else-if="browseMode === 'tutors' && selectedTutorId === null && !tutorGroupsFiltered.length" class="empty-discover">
      No tutors match your filters. Try turning off the location filter or search “All listings”.
    </p>

    <div v-else-if="browseMode === 'tutors' && selectedTutorId === null" class="tutors-grid tutors-grid--summary">
      <div
        v-for="group in tutorGroupsFiltered"
        :key="'tutor-' + group.tutor_id"
        class="tutor-card tutor-summary-card"
        @click="selectTutor(group.tutor_id)"
        @keydown.enter.prevent="selectTutor(group.tutor_id)"
        @keydown.space.prevent="selectTutor(group.tutor_id)"
        tabindex="0"
        role="button"
        :aria-label="'View all listings from ' + group.displayName"
      >
        <div class="tutor-row">
          <div class="tutor-row-left">
            <div class="avatar-lg" aria-hidden="true">
              <img :src="group.thumbnail" :alt="group.displayName" @error="onImageError" />
            </div>
            <div class="tutor-row-main">
              <div class="row-top">
                <h3 class="tutor-name">{{ group.displayName }}</h3>
                <div class="meta-pills">
                  <span class="pill pill-muted">{{ group.posts.length }} listing{{ group.posts.length === 1 ? '' : 's' }}</span>
                  <span class="pill pill-rating">
                    <svg viewBox="0 0 24 24" fill="currentColor"><path d="M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z"/></svg>
                    4.9
                  </span>
                </div>
              </div>
              <div class="row-subjects">{{ group.subjectsLine }}</div>
              <div v-if="group.location" class="row-loc">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0z"/><circle cx="12" cy="10" r="3"/></svg>
                {{ group.location }}
              </div>
              <div class="row-tags">
                <span v-for="tag in group.previewTags" :key="tag" class="tag">{{ tag }}</span>
              </div>
            </div>
          </div>

          <div class="tutor-row-right">
            <div class="row-price">
              <div class="price-big">₱{{ group.minRate }}</div>
              <div class="price-sub">/hr from</div>
            </div>
            <div class="row-actions">
              <button type="button" class="btn-secondary" @click.stop="openTutorProfile(group)">View profile</button>
              <button type="button" class="btn-primary" @click.stop="selectTutor(group.tutor_id)">View listings</button>
            </div>
          </div>
        </div>
      </div>
    </div>

    <div
      v-else-if="browseMode === 'tutors' && selectedTutorId !== null && tutorDetailLoading"
      class="loading-state"
    >
      <div class="spinner"></div>
      <p>Loading listings…</p>
    </div>

    <p v-else-if="browseMode === 'listings' && !gridListingCards.length" class="empty-discover">
      No listings match your search. Adjust filters or browse <button type="button" class="inline-link" @click="setBrowseMode('tutors')">all tutors</button>.
    </p>

    <!-- Listing cards: all-listings mode OR tutor drill-down -->
    <div v-else-if="gridListingCards.length" class="tutors-grid tutors-grid--listings">
      <div
        v-for="tutor in gridListingCards"
        :key="tutor.id"
        :class="['tutor-card', { 'is-booked': isBooked(tutor.id) }]"
      >
        <div class="preview-area">
          <img :src="tutor.thumbnail" :alt="tutor.name" @error="onImageError" />
          <div class="preview-overlay">
            <button type="button" class="btn-preview">Quick View</button>
          </div>
          <div v-if="isBooked(tutor.id)" class="time-badge booked-badge">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3" style="width:11px;height:11px"><polyline points="20 6 9 17 4 12"/></svg>
            Booked
          </div>
          <div v-else class="time-badge">Available Now</div>
        </div>
        <div class="card-body">
          <div class="tutor-top">
            <div class="name-row">
              <h3>{{ tutor.name }}</h3>
              <div class="rating-badge">
                <svg viewBox="0 0 24 24" fill="currentColor"><path d="M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z"/></svg>
                <span>{{ tutor.rating }}</span>
              </div>
            </div>
            <p class="expertise">{{ tutor.expertise }}</p>
            <p v-if="tutor.location" class="location-text">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0z"/><circle cx="12" cy="10" r="3"/></svg>
              {{ tutor.location }}
            </p>
          </div>

          <div class="tag-row">
            <span v-for="tag in tutor.tags" :key="tag" class="tag">{{ tag }}</span>
          </div>

          <div class="card-footer">
            <div class="price">
              <strong>₱{{ tutor.rate }}</strong>
              <span>/hr</span>
            </div>
            <div class="footer-actions">
              <span class="reviews">{{ tutor.reviews }} reviews</span>
              <button
                v-if="isBooked(tutor.id)"
                type="button"
                class="btn-book btn-booked"
                disabled
              >
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3" style="width:13px;height:13px"><polyline points="20 6 9 17 4 12"/></svg>
                Booked
              </button>
              <button
                type="button"
                v-else
                class="btn-book"
                @click.stop="openBookingModal(tutor)"
              >
                Book
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>

    <p
      v-else-if="browseMode === 'tutors' && selectedTutorId !== null && !tutorDetailLoading"
      class="empty-discover"
    >
      No published listings for this tutor.
    </p>

    <!-- Booking Modal -->
    <div v-if="showModal && !showPaymentModal" class="modal-backdrop" @click="closeModal">
      <div class="modal-content" @click.stop>
        <button class="close-btn" @click="closeModal">×</button>
        
        <div class="modal-header">
          <div class="tutor-avatar-lg">
             <img :src="selectedTutor?.thumbnail" @error="onImageError" />
          </div>
          <div class="header-info">
            <h2>Book {{ selectedTutor?.name }}</h2>
            <p class="modal-sub">{{ selectedTutor?.expertise }} • {{ selectedTutor?.total_sessions }} sessions total</p>
          </div>
        </div>

        <div class="modal-body">
          <p class="sessions-info">Select available slots for your {{ selectedTutor?.total_sessions }} sessions:</p>
          
          <div v-if="slotsLoading" class="slots-loading">
            <div class="mini-spinner"></div>
            <span>Loading availability...</span>
          </div>

          <div v-else class="slots-container">
            <div v-for="n in selectedTutor?.total_sessions" :key="n" class="session-block">
              <div class="session-block-header">
                <span class="snum">Session {{ n }}</span>
                <span v-if="selectedSlots[n]" class="spick">Selected</span>
              </div>
              
              <div class="slot-options">
                <button 
                  v-for="slot in getSlotsForSession(n)" 
                  :key="slot.id"
                  @click="selectSlot(n, slot)"
                  :class="['slot-option', { active: selectedSlots[n]?.id === slot.id }]"
                >
                  <div class="slot-date">
                    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="3" y="4" width="18" height="18" rx="2" ry="2"/><line x1="16" y1="2" x2="16" y2="6"/><line x1="8" y1="2" x2="8" y2="6"/><line x1="3" y1="10" x2="21" y2="10"/></svg>
                    {{ formatDate(slot.date) }}
                  </div>
                  <div class="slot-time">
                    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/></svg>
                    {{ slot.start_time }} - {{ slot.end_time }}
                  </div>
                </button>
              </div>
            </div>
          </div>
        </div>

        <div class="modal-footer">
          <button class="btn-cancel" @click="closeModal">Cancel</button>
          <button 
            class="btn-confirm-booking" 
            :disabled="!canBook || bookingLoading"
            @click="goToPayment"
          >
            Proceed to Payment →
          </button>
        </div>
      </div>
    </div>

    <!-- ── PAYMENT SIMULATION MODAL ── -->
    <div v-if="showPaymentModal" class="modal-backdrop" @click.self="closeAllModals">
      <div class="modal-content payment-modal" @click.stop>

        <!-- Header -->
        <div class="pay-header">
          <div class="pay-header-icon">💳</div>
          <div>
            <h2>Complete Payment</h2>
            <p class="modal-sub">{{ selectedTutor?.name }} · {{ selectedTutor?.expertise }}</p>
          </div>
        </div>

        <!-- Success Screen -->
        <div v-if="paymentSuccess" class="pay-success">
          <div class="success-icon">✅</div>
          <h3>Payment Successful!</h3>
          <p>Your session has been booked and payment recorded.</p>
          <p class="tx-ref">Ref: <strong>{{ completedTxId }}</strong></p>
          <button class="btn-confirm-booking" style="margin-top:1.5rem" @click="closeAllModals">Done</button>
        </div>

        <!-- Payment Form -->
        <template v-else>
          <!-- Amount Summary -->
          <div class="pay-summary">
            <div class="pay-row">
              <span>Sessions</span>
              <span>{{ selectedTutor?.total_sessions }}</span>
            </div>
            <div class="pay-row">
              <span>Rate</span>
              <span>₱{{ selectedTutor?.rate }}/hr</span>
            </div>
            <div class="pay-row total-row">
              <span>Total Due</span>
              <strong>₱{{ totalPayable }}</strong>
            </div>
          </div>

          <!-- Payment Methods -->
          <div class="pay-methods-label">Choose Payment Method</div>
          <div class="pay-methods-list">
            <label 
              v-for="pm in paymentMethods" 
              :key="pm.key"
              :class="['pay-method-item', { active: selectedPaymentMethod === pm.key }]"
            >
              <input type="radio" v-model="selectedPaymentMethod" :value="pm.key" style="display:none" />
              <div class="pm-icon" :style="{ background: pm.color }">
                <span>{{ pm.label.charAt(0) }}</span>
              </div>
              <div class="pm-info">
                <strong>{{ pm.label }}</strong>
                <span>{{ pm.detail }}</span>
              </div>
              <div class="pm-check" v-if="selectedPaymentMethod === pm.key">
                <svg viewBox="0 0 24 24" fill="none" stroke="#16a34a" stroke-width="3"><polyline points="20 6 9 17 4 12"/></svg>
              </div>
            </label>
          </div>

          <!-- Processing bar -->
          <div v-if="paymentProcessing" class="pay-processing">
            <div class="processing-bar"><div class="processing-fill"></div></div>
            <span>Processing payment securely…</span>
          </div>

          <div class="modal-footer" style="border-top: none; padding-top: 0;">
            <button class="btn-cancel" @click="backToBooking">Back</button>
            <button 
              class="btn-confirm-booking pay-now-btn"
              :disabled="!selectedPaymentMethod || paymentProcessing || bookingLoading"
              @click="processPayment"
            >
              <svg v-if="!paymentProcessing" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="2" y="5" width="20" height="14" rx="2"/><line x1="2" y1="10" x2="22" y2="10"/></svg>
              {{ paymentProcessing ? 'Processing…' : 'Pay Now' }}
            </button>
          </div>
        </template>
      </div>
    </div>

    <!-- Tutor Profile Modal (Achievements / Accomplishments) -->
    <div v-if="showTutorProfileModal" class="modal-backdrop" @click.self="closeTutorProfile">
      <div class="modal-content tutor-profile-modal" @click.stop>
        <button class="close-btn" @click="closeTutorProfile">×</button>

        <div class="modal-header">
          <div class="tutor-avatar-lg">
            <img :src="tutorProfileSelected?.thumbnail" :alt="tutorProfileSelected?.displayName" @error="onImageError" />
          </div>
          <div class="header-info">
            <h2>{{ tutorProfileSelected?.displayName }}</h2>
            <p class="modal-sub" v-if="tutorProfileSelected?.location">{{ tutorProfileSelected.location }}</p>
          </div>
        </div>

        <div class="modal-body">
          <div class="profile-section-mini">
            <div class="mini-label">About</div>
            <p class="mini-text">
              {{ tutorProfileSelected?.bio || 'No bio provided yet.' }}
            </p>
          </div>

          <div class="profile-section-mini" style="margin-top: 1rem;">
            <div class="mini-label">Achievements / Accomplishments</div>
            <p class="mini-text prewrap">
              {{ tutorProfileSelected?.achievements || 'No achievements added yet.' }}
            </p>
          </div>
        </div>

        <div class="modal-footer">
          <button class="btn-cancel" @click="closeTutorProfile">Close</button>
          <button class="btn-confirm-booking" @click="selectTutor(tutorProfileSelected?.tutor_id); closeTutorProfile()">
            View listings →
          </button>
        </div>
      </div>
    </div>

  </div>
</template>

<script setup>
import { ref, computed, watch } from 'vue';
import { postService, bookingService, sessionSlotService, profileService, paymentService } from '../../services/api';
import { useToast } from '../../composables/useToast';
import { supabase } from '../../supabase';

const props = defineProps({ profile: Object });
const { showToast } = useToast();
const searchQuery = ref('');
const activeCategory = ref('All');
/** Raw API posts (published only), ordered newest first */
const rawPosts = ref([]);
const loading = ref(true);

/**
 * Location scope:
 *  'municipality' — strict same city/municipality match
 *  'province'     — strict same province match
 *  'all'          — no location filter
 */
const locationScope = ref('province');
// keep filterByLocation in sync so existing code that reads it still works
const filterByLocation = computed(() => locationScope.value !== 'all');

/** tutors = grouped nearby/all tutors; listings = flat feed */
const browseMode = ref('tutors');
const selectedTutorId = ref(null);
const tutorDetailPosts = ref([]);
const tutorDetailLoading = ref(false);

const showModal = ref(false);
const selectedTutor = ref(null);
const bookingLoading = ref(false);
const slotsLoading = ref(false);
const allSlots = ref([]);
const selectedSlots = ref({});

function onImageError(ev) {
  const img = ev?.target;
  if (!img) return;
  const fallback = '/images/tutor_piano.png';
  if (img.src && img.src.endsWith(fallback)) return;
  img.src = fallback;
}

// ── Student's existing bookings (for booked-state detection) ──
const studentBookedPostIds = ref(new Set());

const isBooked = (postId) => studentBookedPostIds.value.has(postId);

async function fetchStudentBookings() {
  if (!props.profile?.user) return;
  try {
    const { data } = await bookingService.getStudentBookings(props.profile.user);
    const list = Array.isArray(data) ? data : (data.results || []);
    studentBookedPostIds.value = new Set(list.map(b => b.expertise_post));
  } catch (e) {
    console.error('Could not load student bookings', e);
  }
}

watch(() => props.profile, (p) => { if (p?.user) fetchStudentBookings(); }, { immediate: true });

// ── Payment state ──
const showPaymentModal  = ref(false);
const selectedPaymentMethod = ref('');
const paymentProcessing = ref(false);
const paymentSuccess    = ref(false);
const completedTxId     = ref('');

const paymentMethods = [
  { key: 'gcash', label: 'GCash',          detail: '+63 991 ••89  · Linked',         color: '#3b82f6' },
  { key: 'visa',  label: 'Visa •••• 4242', detail: 'Expires 06/27 · Jayson Dela Cruz', color: '#1a1f71' },
];

const categories = ['All', 'Math', 'Science', 'Music', 'Sports', 'Language', 'Arts'];

function tutorIdFromPost(post) {
  let tid = post.tutor_id ?? post.tutor;
  if (tid != null && typeof tid === 'object') tid = tid.id;
  const n = tid != null ? Number(tid) : NaN;
  return Number.isFinite(n) ? n : null;
}

function tutorDisplayName(post) {
  const fromProfile = `${post.tutor_first_name || ''} ${post.tutor_last_name || ''}`.trim();
  if (fromProfile) return fromProfile;
  const tp = post.tutor_profile;
  const fromAuthUser = `${tp?.first_name || ''} ${tp?.last_name || ''}`.trim();
  return fromAuthUser || 'Tutor';
}

function postLocationLine(post) {
  return [post.tutor_barangay, post.tutor_municipality, post.tutor_province].filter(Boolean).join(', ');
}

function normLoc(s) {
  return String(s || '')
    .toLowerCase()
    .replace(/[-,]/g, ' ')
    .replace(/\s+/g, ' ')
    .replace(/\bcity\b/g, '')
    .replace(/\bprovince\b/g, '')
    .replace(/\bmunicipality\b/g, '')
    .trim();
}

/**
 * Strict location match: checks whether the tutor's address field
 * contains or is contained by the student's field (handles cases like
 * "Cebu" vs "Cebu Province" or "Cebu City" vs "Cebu").
 */
function strictMatch(a, b) {
  if (!a || !b) return false;
  const na = normLoc(a);
  const nb = normLoc(b);
  return na === nb || na.includes(nb) || nb.includes(na);
}

function postMatchesNearby(post) {
  if (locationScope.value === 'all') return true;

  if (locationScope.value === 'municipality') {
    const sm = props.profile?.municipality;
    if (!sm) return false; // no student municipality — don't show anyone
    return strictMatch(post.tutor_municipality, sm);
  }

  // 'province'
  const sp = props.profile?.province;
  if (!sp) return false;
  return strictMatch(post.tutor_province, sp);
}

function postMatchesCategory(post) {
  if (activeCategory.value === 'All') return true;
  const cat = activeCategory.value;
  return (
    (post.subject && post.subject.includes(cat)) ||
    (post.title && post.title.includes(cat))
  );
}

function postMatchesSearch(post) {
  const q = searchQuery.value?.trim().toLowerCase();
  if (!q) return true;
  const name = tutorDisplayName(post).toLowerCase();
  return (
    name.includes(q) ||
    String(post.title || '').toLowerCase().includes(q) ||
    String(post.subject || '').toLowerCase().includes(q)
  );
}

const postsAfterNearby = computed(() => rawPosts.value.filter((p) => postMatchesNearby(p)));

const postsPassingFilters = computed(() =>
  postsAfterNearby.value.filter((p) => postMatchesCategory(p) && postMatchesSearch(p)),
);

const tutorGroupsFiltered = computed(() => {
  const map = new Map();
  for (const post of postsPassingFilters.value) {
    const tid = tutorIdFromPost(post);
    if (tid == null) continue;
    if (!map.has(tid)) map.set(tid, []);
    map.get(tid).push(post);
  }
  const groups = [];
  for (const [tutor_id, posts] of map.entries()) {
    const sortedPosts = [...posts].sort(
      (a, b) => new Date(b.created_at || 0) - new Date(a.created_at || 0),
    );
    const first = sortedPosts[0];
    const rates = sortedPosts.map((p) => parseFloat(p.hourly_rate || 0)).filter((n) => !Number.isNaN(n));
    const minNum = rates.length ? Math.min(...rates) : NaN;
    const minRateLabel = Number.isFinite(minNum) ? String(Math.round(minNum)) : '—';
    const subjects = [...new Set(sortedPosts.map((p) => p.subject).filter(Boolean))];
    const displayName = tutorDisplayName(first);
    groups.push({
      tutor_id,
      posts: sortedPosts,
      displayName,
      thumbnail: first.tutor_avatar_url || first.photo_url || '/images/tutor_piano.png',
      bio: first.tutor_bio || '',
      achievements: first.tutor_achievements || '',
      location: postLocationLine(first),
      minRate: minRateLabel,
      subjectsLine:
        subjects.length <= 2
          ? subjects.join(' · ') || first.title || 'Tutoring'
          : `${subjects.slice(0, 2).join(' · ')} +${subjects.length - 2} more`,
      previewTags: ['Tutor', ...subjects.slice(0, 2)],
    });
  }
  groups.sort((a, b) => a.displayName.localeCompare(b.displayName));
  return groups;
});

// Tutor "stalk" / profile modal
const showTutorProfileModal = ref(false);
const tutorProfileSelected = ref(null);

function openTutorProfile(group) {
  tutorProfileSelected.value = group ? {
    tutor_id: group.tutor_id,
    displayName: group.displayName,
    thumbnail: group.thumbnail,
    location: group.location,
    bio: group.bio,
    achievements: group.achievements,
  } : null;
  showTutorProfileModal.value = true;
}

function closeTutorProfile() {
  showTutorProfileModal.value = false;
  tutorProfileSelected.value = null;
}

const tutorsBrowseLabel = computed(() => {
  if (locationScope.value === 'municipality' && props.profile?.municipality)
    return `Tutors in ${props.profile.municipality}`;
  if (locationScope.value === 'province' && props.profile?.province)
    return `Tutors in ${props.profile.province}`;
  return 'All tutors';
});

const tutorsBrowseHint = computed(() => {
  if (locationScope.value === 'municipality') return '(same city/municipality)';
  if (locationScope.value === 'province') return '(same province)';
  return '';
});

function mapPostToListingCard(post, { preferListingPhoto = false } = {}) {
  const thumb = preferListingPhoto
    ? (post.photo_url || '/images/tutor_piano.png')
    : (post.tutor_avatar_url || post.photo_url || '/images/tutor_piano.png');
  return {
    id: post.id,
    tutor_id: tutorIdFromPost(post),
    name: tutorDisplayName(post),
    expertise: post.title,
    total_sessions: post.total_sessions,
    rating: '4.9',
    reviews: 0,
    rate: post.hourly_rate,
    tags: [post.subject, 'Tutor'],
    thumbnail: thumb,
    municipality: post.tutor_municipality || '',
    province: post.tutor_province || '',
    location: postLocationLine(post),
  };
}

const listingCardsFiltered = computed(() =>
  // All listings feed: use each listing's own display photo
  postsPassingFilters.value.map((p) => mapPostToListingCard(p, { preferListingPhoto: true })),
);

const tutorDetailPostsFiltered = computed(() =>
  tutorDetailPosts.value.filter((p) => postMatchesCategory(p) && postMatchesSearch(p)),
);

const gridListingCards = computed(() => {
  if (browseMode.value === 'tutors' && selectedTutorId.value != null) {
    // Tutor drill-down: show each listing's own display photo (not the tutor avatar)
    return tutorDetailPostsFiltered.value.map((p) =>
      mapPostToListingCard(p, { preferListingPhoto: true }),
    );
  }
  return listingCardsFiltered.value;
});

const selectedTutorDisplayName = computed(() => {
  if (selectedTutorId.value == null) return '';
  const p = tutorDetailPosts.value[0];
  return p ? tutorDisplayName(p) : '';
});

function setBrowseMode(mode) {
  browseMode.value = mode;
  clearSelectedTutor();
}

function clearSelectedTutor() {
  selectedTutorId.value = null;
  tutorDetailPosts.value = [];
}

async function selectTutor(tutorId) {
  if (browseMode.value !== 'tutors') return;
  selectedTutorId.value = tutorId;
  tutorDetailLoading.value = true;
  tutorDetailPosts.value = [];
  try {
    const { data } = await postService.getAllPosts({ tutor_id: tutorId });
    const list = Array.isArray(data) ? data : (data.results || []);
    tutorDetailPosts.value = list.filter((p) => p.is_published);
  } catch (e) {
    console.error('Failed to load tutor listings', e);
    showToast('Could not load tutor listings', 'error');
    clearSelectedTutor();
  } finally {
    tutorDetailLoading.value = false;
  }
}

const loadPosts = async () => {
  loading.value = true;
  try {
    const prov = String(props.profile?.province || '').trim();
    const params = {};
    if (filterByLocation.value && prov) {
      params.region_match = prov;
    }
    const { data } = await postService.getAllPosts(params);
    const arr = Array.isArray(data) ? data : (data.results || []);
    rawPosts.value = arr
      .filter((post) => post.is_published)
      .sort((a, b) => new Date(b.created_at || 0) - new Date(a.created_at || 0));
  } catch (error) {
    console.error('Error fetching tutors:', error);
  } finally {
    loading.value = false;
  }
};

watch(
  () => [locationScope.value, props.profile?.province, props.profile?.municipality, props.profile?.user],
  () => { loadPosts(); },
  { immediate: true },
);

const openBookingModal = async (tutor) => {
  selectedTutor.value = tutor;
  showModal.value = true;
  slotsLoading.value = true;
  selectedSlots.value = {};
  
  try {
    const { data } = await sessionSlotService.getSlots({ post_id: tutor.id });
    allSlots.value = Array.isArray(data) ? data : (data.results || []);
  } catch (err) {
    showToast('Could not load availability', 'error');
  } finally {
    slotsLoading.value = false;
  }
};

const closeModal = () => {
  showModal.value = false;
  selectedTutor.value = null;
  allSlots.value = [];
};

const getSlotsForSession = (sessionNum) => {
  return allSlots.value.filter(s => s.session_number === sessionNum && !s.is_booked);
};

const selectSlot = (sessionNum, slot) => {
  selectedSlots.value[sessionNum] = slot;
};

const canBook = computed(() => {
  return Object.keys(selectedSlots.value).length === selectedTutor.value?.total_sessions;
});

const totalPayable = computed(() => {
  if (!selectedTutor.value) return 0;
  // rate * total_sessions (simplified; adjust if hourly diff)
  return (parseFloat(selectedTutor.value.rate) * selectedTutor.value.total_sessions).toFixed(2);
});

const formatDate = (dateStr) => {
  return new Date(dateStr).toLocaleDateString('en-US', {
    weekday: 'short',
    month: 'short',
    day: 'numeric'
  });
};

// Step 1 → open payment modal (keep showModal + selectedTutor alive)
const goToPayment = () => {
  selectedPaymentMethod.value = '';
  paymentProcessing.value = false;
  paymentSuccess.value = false;
  completedTxId.value = '';
  showPaymentModal.value = true; // booking modal hides via v-if condition
};

// Step 2 → process: simulate delay, create bookings + payment record
const processPayment = async () => {
  paymentProcessing.value = true;
  bookingLoading.value = true;
  try {
    const { data: { session } } = await supabase.auth.getSession();
    if (!session) throw new Error('Please login to book');

    const { data } = await profileService.getProfileByEmail(session.user.email, 'student');
    const profiles = Array.isArray(data) ? data : (data.results || []);
    if (!profiles || profiles.length === 0) throw new Error('User profile not found in system.');
    const studentUserId = profiles[0].user;

    // Simulate payment gateway delay
    await new Promise(resolve => setTimeout(resolve, 2000));

    // Create one booking per selected slot
    let lastBookingId = null;
    for (const sessionNum in selectedSlots.value) {
      const slot = selectedSlots.value[sessionNum];
      const bookingRes = await bookingService.createBooking({
        student: studentUserId,
        tutor: selectedTutor.value.tutor_id,
        expertise_post: selectedTutor.value.id,
        session_slot: slot.id,
        session_number: slot.session_number,
        date: slot.date,
        start_time: slot.start_time,
        end_time: slot.end_time,
        status: 'confirmed',
      });
      lastBookingId = bookingRes.data.id;
    }

    // Generate a transaction ID and record the payment on the LAST booking
    const txId = 'TXN-' + Math.random().toString(36).substring(2, 8).toUpperCase();
    await paymentService.createPayment({
      booking: lastBookingId,
      amount: totalPayable.value,
      transaction_id: txId,
      status: 'completed',
      payment_method: selectedPaymentMethod.value,
      notes: `Online payment for ${selectedTutor.value.expertise}`,
    });

    completedTxId.value = txId;
    paymentSuccess.value = true;
    loadPosts();
    fetchStudentBookings(); // refresh booked state after payment
  } catch (err) {
    showToast(err.message || 'Payment failed', 'error');
    paymentProcessing.value = false;
  } finally {
    bookingLoading.value = false;
    paymentProcessing.value = false;
  }
};

const closeAllModals = () => {
  showPaymentModal.value = false;
  showModal.value = false;
  selectedTutor.value = null;
  allSlots.value = [];
  selectedSlots.value = {};
  paymentSuccess.value = false;
};

// back button on payment modal: go back to booking modal
const backToBooking = () => {
  showPaymentModal.value = false;
};

const confirmBooking = async () => {
  goToPayment();
};

watch([filterByLocation, () => props.profile?.municipality, () => props.profile?.province], () => {
  if (selectedTutorId.value != null) clearSelectedTutor();
});
</script>

<style scoped>
.discover-tab { display: flex; flex-direction: column; gap: 1.5rem; }

/* ── Location Banner ── */
.location-banner {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 0.75rem;
  background: linear-gradient(90deg, #f0f9ff, #e0f2fe);
  border: 1.5px solid #bae6fd;
  border-radius: 1rem;
  padding: 0.75rem 1.25rem;
  margin-bottom: 0;
  font-size: 0.88rem;
  color: #0c4a6e;
}
.location-banner.warn {
  background: linear-gradient(90deg, #fffbeb, #fef9e7);
  border-color: #fcd34d;
  color: #78350f;
  justify-content: flex-start;
}
.location-banner svg { width: 16px; height: 16px; flex-shrink: 0; }
.loc-left { display: flex; align-items: center; gap: 0.5rem; }
.loc-right { flex-shrink: 0; }
.loc-scope-group { display: flex; gap: 0.4rem; flex-shrink: 0; flex-wrap: wrap; }
.scope-pill {
  padding: 0.35rem 0.85rem;
  border-radius: 2rem;
  border: 1.5px solid #7dd3fc;
  background: #ffffff;
  color: #0369a1;
  font-size: 0.78rem;
  font-weight: 800;
  cursor: pointer;
  transition: all 0.18s;
  white-space: nowrap;
}
.scope-pill.active {
  background: #0f172a;
  color: #38bdf8;
  border-color: #0f172a;
}
.scope-pill:hover:not(:disabled):not(.active) { transform: scale(1.03); background: #e0f2fe; }
.scope-pill:disabled { opacity: 0.45; cursor: not-allowed; }

/* Browse mode */
.browse-mode-row {
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  gap: 0.65rem 1rem;
  background: #fff;
  border: 1px solid #f1f5f9;
  border-radius: 1rem;
  padding: 0.65rem 1rem;
}
.browse-label {
  font-size: 0.78rem;
  font-weight: 800;
  color: #64748b;
  text-transform: uppercase;
  letter-spacing: 0.04em;
}
.browse-toggle {
  display: flex;
  gap: 0.35rem;
  flex-wrap: wrap;
}
.browse-pill {
  padding: 0.5rem 1rem;
  border-radius: 0.75rem;
  border: 1.5px solid #e2e8f0;
  background: #f8fafc;
  color: #475569;
  font-size: 0.82rem;
  font-weight: 800;
  cursor: pointer;
  transition: all 0.18s;
}
.browse-pill:hover {
  border-color: #cbd5e1;
  color: #0f172a;
}
.browse-pill.active {
  background: #0f172a;
  color: #fff;
  border-color: #0f172a;
}

.tutor-listings-bar {
  display: flex;
  flex-direction: column;
  gap: 0.35rem;
  padding: 0.5rem 0;
}
.btn-back-tutor {
  align-self: flex-start;
  border: none;
  background: transparent;
  color: #2563eb;
  font-size: 0.85rem;
  font-weight: 800;
  cursor: pointer;
  padding: 0.25rem 0;
}
.btn-back-tutor:hover {
  text-decoration: underline;
}
.tutor-listings-intro {
  margin: 0;
  font-size: 0.88rem;
  color: #64748b;
  font-weight: 600;
}
.tutor-listings-intro strong {
  color: #0f172a;
}

.results-hint {
  font-weight: 600;
  color: #94a3b8;
  margin-left: 0.35rem;
  font-size: 0.85rem;
}

.tutor-summary-card {
  cursor: pointer;
  outline: none;
}
.tutor-summary-card:focus-visible {
  box-shadow: 0 0 0 3px rgba(37, 99, 235, 0.35);
}
.listing-count-badge {
  position: absolute;
  top: 1rem;
  right: 1rem;
  background: #0f172a;
  color: #fff;
  font-size: 0.65rem;
  font-weight: 900;
  padding: 0.3rem 0.55rem;
  border-radius: 0.5rem;
  text-transform: uppercase;
  letter-spacing: 0.02em;
}
.btn-view-listings {
  background: #1e3a8a !important;
}
.btn-view-listings:hover {
  opacity: 0.92;
}

.empty-discover {
  margin: 0;
  padding: 2rem 1rem;
  text-align: center;
  font-size: 0.9rem;
  font-weight: 600;
  color: #64748b;
  background: #f8fafc;
  border-radius: 1rem;
  border: 1px dashed #e2e8f0;
}
.inline-link {
  border: none;
  background: none;
  color: #2563eb;
  font-weight: 800;
  cursor: pointer;
  text-decoration: underline;
  padding: 0;
  font: inherit;
}

/* Header */
.page-header h1 { font-size: 1.75rem; font-weight: 900; color: #0f172a; margin: 0 0 0.5rem; }
.page-header p { font-size: 0.95rem; color: #64748b; margin: 0; }

/* Filter Bar */
.filter-bar { display: flex; align-items: center; gap: 1rem; background: #fff; padding: 0.5rem; border-radius: 1rem; }
.search-field { flex: 1; display: flex; align-items: center; gap: 0.75rem; padding: 0.65rem 1rem; background: #f8fafc; border-radius: 0.75rem; border: 1.5px solid #f1f5f9; }
.search-field input { border: none; background: transparent; outline: none; font-size: 0.9rem; width: 100%; color: #0f172a; }
.search-field svg { width: 18px; height: 18px; color: #94a3b8; }

.category-scroll { display: flex; gap: 0.5rem; overflow-x: auto; padding-bottom: 4px; }
.cat-pill { padding: 0.55rem 1.1rem; border-radius: 0.75rem; background: #f1f5f9; color: #475569; font-weight: 700; font-size: 0.82rem; border: none; cursor: pointer; white-space: nowrap; transition: all 0.2s; }
.cat-pill.active { background: #0f172a; color: #fff; }
.sort-select { padding: 0.65rem 1rem; border-radius: 0.75rem; border: 1.5px solid #f1f5f9; background: #f8fafc; color: #475569; font-weight: 700; font-size: 0.82rem; outline: none; }

/* Results */
.results-bar { display: flex; align-items: center; justify-content: space-between; }
.results-count { font-size: 0.9rem; color: #64748b; }
.results-count strong { color: #0f172a; }

/* Tutors Grid */
.tutors-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(340px, 1fr)); gap: 1.5rem; }
.tutors-grid--summary { grid-template-columns: 1fr; gap: 0.85rem; }
.tutor-card { background: #fff; border-radius: 1.25rem; overflow: hidden; border: 1px solid #f1f5f9; transition: all 0.3s; }
.tutor-card:hover { transform: translateY(-4px); box-shadow: 0 12px 30px rgba(15,23,42,0.08); }

.card-body { padding: 1rem; }
.tutors-grid--listings .card-body { padding: 1.25rem; }

/* Listing cards keep the large preview image */
.tutors-grid--listings .preview-area { height: 180px; position: relative; background: #f1f5f9; overflow: hidden; }
.tutors-grid--listings .preview-area img { width: 100%; height: 100%; object-fit: cover; }
.tutors-grid--listings .preview-overlay { position: absolute; inset: 0; background: rgba(15,23,42,0.4); opacity: 0; display: flex; align-items: center; justify-content: center; transition: 0.2s; }
.tutors-grid--listings .tutor-card:hover .preview-overlay { opacity: 1; }
.tutors-grid--listings .btn-preview { background: #fff; color: #0f172a; border: none; padding: 0.6rem 1.25rem; border-radius: 0.75rem; font-weight: 800; font-size: 0.82rem; cursor: pointer; }
.tutors-grid--listings .time-badge { position: absolute; top: 1rem; left: 1rem; background: #16a34a; color: #fff; font-size: 0.65rem; font-weight: 900; padding: 0.25rem 0.6rem; border-radius: 0.5rem; text-transform: uppercase; }

.card-head { display: flex; align-items: flex-start; gap: 0.75rem; margin-bottom: 0.75rem; }
.head-main { flex: 1; min-width: 0; }
.avatar-sm { width: 44px; height: 44px; border-radius: 999px; overflow: hidden; background: #e2e8f0; border: 2px solid #fff; box-shadow: 0 10px 24px rgba(15,23,42,0.08); flex-shrink: 0; }
.avatar-sm img { width: 100%; height: 100%; object-fit: cover; display: block; }
.listing-pill { flex-shrink: 0; font-size: 0.7rem; font-weight: 900; color: #0f172a; background: #f1f5f9; padding: 0.3rem 0.6rem; border-radius: 999px; }
.status-pill { flex-shrink: 0; display: inline-flex; align-items: center; gap: 0.35rem; font-size: 0.7rem; font-weight: 900; color: #0f172a; background: #f1f5f9; padding: 0.3rem 0.6rem; border-radius: 999px; }
.status-pill svg { width: 14px; height: 14px; }
.status-pill.booked { background: #f0fdf4; color: #16a34a; border: 1px solid #bbf7d0; }
.name-row { display: flex; align-items: center; justify-content: space-between; margin-bottom: 0.25rem; }
.name-row h3 { font-size: 1.05rem; font-weight: 800; color: #0f172a; margin: 0; }
.rating-badge { display: flex; align-items: center; gap: 0.25rem; background: #fffbeb; color: #b45309; padding: 0.25rem 0.5rem; border-radius: 0.5rem; font-size: 0.78rem; font-weight: 800; }
.rating-badge svg { width: 14px; height: 14px; }
.expertise { font-size: 0.85rem; color: #64748b; margin-bottom: 0.5rem; }
.location-text { font-size: 0.75rem; color: #94a3b8; display: flex; align-items: center; gap: 0.35rem; margin-top: 0.4rem; }
.location-text svg { width: 14px; height: 14px; }

.tag-row { display: flex; gap: 0.4rem; flex-wrap: wrap; margin-bottom: 0.9rem; }
.tag { font-size: 0.72rem; font-weight: 700; color: #475569; background: #f1f5f9; padding: 0.25rem 0.65rem; border-radius: 0.5rem; }

.card-footer { display: flex; align-items: center; justify-content: space-between; padding-top: 1rem; border-top: 1.5px dashed #f1f5f9; }
.price strong { font-weight: 800; font-size: 1.2rem; color: #0f172a; }
.price span { font-size: 0.75rem; color: #94a3b8; font-weight: 600; }
.footer-actions { display: flex; align-items: center; gap: 0.75rem; }
.reviews { font-size: 0.72rem; color: #94a3b8; font-weight: 600; }
.btn-book { background: #0f172a; color: #fff; border: none; padding: 0.55rem 1.1rem; border-radius: 0.65rem; font-weight: 800; font-size: 0.82rem; cursor: pointer; transition: all 0.2s; }
.btn-book:hover { opacity: 0.85; transform: translateY(-1px); }
.btn-link { background: transparent; border: none; padding: 0.3rem 0.2rem; font-weight: 800; font-size: 0.8rem; color: #0f172a; cursor: pointer; text-decoration: underline; text-underline-offset: 3px; }
.btn-link:hover { opacity: 0.8; }

.profile-section-mini { border: 1.5px solid #f1f5f9; border-radius: 1rem; padding: 1rem 1.1rem; background: #ffffff; }
.mini-label { font-size: 0.72rem; font-weight: 900; letter-spacing: 0.06em; text-transform: uppercase; color: #94a3b8; margin-bottom: 0.5rem; }
.mini-text { margin: 0; font-size: 0.92rem; color: #334155; line-height: 1.55; }
.prewrap { white-space: pre-wrap; }

/* Tutor list (available tutors) redesign */
.tutors-grid--summary .tutor-card { border-radius: 1.25rem; }
.tutor-row { display: flex; align-items: stretch; justify-content: space-between; gap: 1rem; padding: 1rem 1.1rem; }
.tutor-row-left { display: flex; gap: 1rem; align-items: flex-start; min-width: 0; flex: 1; }
.avatar-lg { width: 64px; height: 64px; border-radius: 999px; overflow: hidden; background: #e2e8f0; border: 3px solid #fff; box-shadow: 0 12px 28px rgba(15,23,42,0.10); flex-shrink: 0; }
.avatar-lg img { width: 100%; height: 100%; object-fit: cover; display: block; }
.tutor-row-main { min-width: 0; flex: 1; }
.row-top { display: flex; align-items: center; justify-content: space-between; gap: 0.75rem; }
.tutor-name { margin: 0; font-size: 1.05rem; font-weight: 900; color: #0f172a; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
.meta-pills { display: inline-flex; align-items: center; gap: 0.5rem; flex-shrink: 0; }
.pill { display: inline-flex; align-items: center; gap: 0.35rem; padding: 0.28rem 0.6rem; border-radius: 999px; font-size: 0.72rem; font-weight: 900; }
.pill-muted { background: #f1f5f9; color: #0f172a; }
.pill-rating { background: #fffbeb; color: #b45309; }
.pill-rating svg { width: 14px; height: 14px; }
.row-subjects { margin-top: 0.25rem; font-size: 0.85rem; font-weight: 700; color: #475569; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
.row-loc { margin-top: 0.35rem; font-size: 0.78rem; color: #94a3b8; display: flex; align-items: center; gap: 0.35rem; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
.row-loc svg { width: 14px; height: 14px; flex-shrink: 0; }
.row-tags { margin-top: 0.55rem; display: flex; gap: 0.4rem; flex-wrap: wrap; }

.tutor-row-right { display: flex; flex-direction: column; align-items: flex-end; justify-content: space-between; gap: 0.6rem; flex-shrink: 0; }
.row-price { text-align: right; }
.price-big { font-weight: 950; font-size: 1.15rem; color: #0f172a; line-height: 1; }
.price-sub { font-size: 0.72rem; color: #94a3b8; font-weight: 700; }
.row-actions { display: flex; align-items: center; gap: 0.5rem; }
.btn-secondary { background: #f8fafc; border: 1.5px solid #e2e8f0; color: #0f172a; padding: 0.55rem 0.85rem; border-radius: 0.75rem; font-weight: 900; font-size: 0.78rem; cursor: pointer; transition: 0.2s; }
.btn-secondary:hover { background: #0f172a; color: #fff; border-color: #0f172a; }
.btn-primary { background: #1e3a8a; border: none; color: #fff; padding: 0.55rem 0.95rem; border-radius: 0.75rem; font-weight: 900; font-size: 0.78rem; cursor: pointer; transition: 0.2s; }
.btn-primary:hover { opacity: 0.92; transform: translateY(-1px); }

/* Booked state */
.booked-badge { background: #16a34a !important; display: flex; align-items: center; gap: 0.35rem; }
.btn-booked {
  background: #f0fdf4 !important;
  color: #16a34a !important;
  border: 1.5px solid #bbf7d0 !important;
  cursor: default !important;
  display: flex; align-items: center; gap: 0.4rem;
  opacity: 1 !important;
}
.tutor-card.is-booked { border-color: #bbf7d0; box-shadow: 0 0 0 2px #f0fdf420; }
.tutor-card.is-booked { border-color: #bbf7d0; box-shadow: 0 0 0 2px #f0fdf420; }

/* Modal */
.modal-backdrop { position: fixed; inset: 0; background: rgba(15,23,42,0.6); display: flex; align-items: center; justify-content: center; z-index: 1000; backdrop-filter: blur(4px); }
.modal-content { background: #fff; width: 100%; max-width: 500px; border-radius: 1.5rem; position: relative; max-height: 90vh; display: flex; flex-direction: column; overflow: hidden; }
.close-btn { position: absolute; top: 1.25rem; right: 1.25rem; background: #f1f5f9; border: none; width: 32px; height: 32px; border-radius: 50%; font-size: 1.5rem; cursor: pointer; display: flex; align-items: center; justify-content: center; }

.modal-header { padding: 2rem; background: #f8fafc; display: flex; align-items: center; gap: 1.25rem; border-bottom: 1px solid #f1f5f9; }
.tutor-avatar-lg { width: 64px; height: 64px; border-radius: 1.25rem; overflow: hidden; background: #e2e8f0; }
.tutor-avatar-lg img { width: 100%; height: 100%; object-fit: cover; }
.header-info h2 { font-size: 1.25rem; font-weight: 900; color: #0f172a; margin: 0; }
.modal-sub { font-size: 0.82rem; color: #64748b; margin-top: 0.2rem; }

.modal-body { padding: 2rem; overflow-y: auto; flex: 1; }
.sessions-info { font-size: 0.85rem; color: #475569; margin: 0 0 1.5rem; }

.session-block { margin-bottom: 1.5rem; }
.session-block-header { display: flex; align-items: center; justify-content: space-between; margin-bottom: 0.75rem; }
.snum { font-size: 0.82rem; font-weight: 800; color: #0f172a; background: #f1f5f9; padding: 0.25rem 0.65rem; border-radius: 0.5rem; }
.spick { font-size: 0.75rem; font-weight: 700; color: #16a34a; }

.slot-options { display: flex; flex-direction: column; gap: 0.5rem; }
.slot-option { 
  display: flex; align-items: center; justify-content: space-between; padding: 0.85rem 1.25rem; 
  border: 2px solid #f1f5f9; border-radius: 1rem; background: #fff; cursor: pointer; text-align: left; transition: all 0.2s;
}
.slot-option:hover { border-color: #e2e8f0; background: #f8fafc; }
.slot-option.active { border-color: #0f172a; background: #f8fafc; }
.slot-date { font-size: 0.85rem; font-weight: 700; color: #0f172a; display: flex; align-items: center; gap: 0.5rem; }
.slot-time { font-size: 0.78rem; color: #64748b; display: flex; align-items: center; gap: 0.4rem; }
.slot-date svg, .slot-time svg { width: 16px; height: 16px; }

.modal-footer { padding: 1.5rem 2rem; border-top: 1px solid #f1f5f9; display: flex; gap: 1rem; }
.btn-cancel { flex: 1; padding: 0.75rem; border: 2px solid #f1f5f9; border-radius: 0.75rem; background: transparent; font-weight: 800; cursor: pointer; color: #64748b; }
.btn-confirm-booking { flex: 2; padding: 0.75rem; border: none; border-radius: 0.75rem; background: #0f172a; color: #fff; font-weight: 800; cursor: pointer; }
.btn-confirm-booking:disabled { opacity: 0.5; cursor: not-allowed; }

/* ── Payment Modal ── */
.payment-modal { max-width: 440px; }

.pay-header {
  padding: 1.75rem 2rem 1.25rem;
  display: flex; align-items: center; gap: 1rem;
  border-bottom: 1px solid #f1f5f9;
  background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
  border-radius: 1.5rem 1.5rem 0 0;
}
.pay-header-icon { font-size: 2rem; }
.pay-header h2 { font-size: 1.2rem; font-weight: 900; color: #fff; margin: 0; }
.pay-header .modal-sub { color: #94a3b8; font-size: 0.8rem; margin-top: 0.15rem; }

.pay-summary {
  margin: 1.5rem 2rem 0;
  background: #f8fafc;
  border: 1.5px solid #f1f5f9;
  border-radius: 1rem;
  padding: 1rem 1.25rem;
  display: flex; flex-direction: column; gap: 0.65rem;
}
.pay-row { display: flex; justify-content: space-between; font-size: 0.85rem; color: #475569; font-weight: 600; }
.total-row { padding-top: 0.65rem; border-top: 1.5px dashed #e2e8f0; margin-top: 0.2rem; }
.total-row span { font-weight: 800; color: #0f172a; font-size: 0.95rem; }
.total-row strong { font-size: 1.3rem; font-weight: 900; color: #0f172a; }

.pay-methods-label {
  margin: 1.25rem 2rem 0.75rem;
  font-size: 0.78rem; font-weight: 800; color: #94a3b8; text-transform: uppercase; letter-spacing: 0.05em;
}
.pay-methods-list { padding: 0 2rem; display: flex; flex-direction: column; gap: 0.65rem; }
.pay-method-item {
  display: flex; align-items: center; gap: 1rem;
  padding: 1rem 1.25rem;
  border: 2px solid #f1f5f9;
  border-radius: 1rem;
  cursor: pointer;
  transition: all 0.2s;
  background: #fff;
}
.pay-method-item:hover { border-color: #e2e8f0; background: #f8fafc; }
.pay-method-item.active { border-color: #0f172a; background: #f8fafc; box-shadow: 0 2px 12px rgba(15,23,42,0.08); }
.pm-icon {
  width: 44px; height: 44px; border-radius: 10px;
  display: flex; align-items: center; justify-content: center;
  font-weight: 900; font-size: 1.1rem; color: #fff; flex-shrink: 0;
}
.pm-info { flex: 1; }
.pm-info strong { display: block; font-size: 0.92rem; font-weight: 800; color: #0f172a; }
.pm-info span { font-size: 0.73rem; color: #94a3b8; font-weight: 600; }
.pm-check { width: 22px; height: 22px; }
.pm-check svg { width: 22px; height: 22px; }

.pay-processing {
  margin: 1.25rem 2rem 0;
  display: flex; flex-direction: column; gap: 0.5rem;
}
.pay-processing span { font-size: 0.78rem; color: #64748b; font-weight: 600; text-align: center; }
.processing-bar {
  height: 6px; background: #f1f5f9; border-radius: 99px; overflow: hidden;
}
.processing-fill {
  height: 100%; width: 100%; border-radius: 99px;
  background: linear-gradient(90deg, #3b82f6, #6366f1, #3b82f6);
  background-size: 200% 100%;
  animation: shimmer 1.5s infinite linear;
}
@keyframes shimmer { 0% { background-position: 200% 0; } 100% { background-position: -200% 0; } }

.pay-now-btn {
  display: flex; align-items: center; justify-content: center; gap: 0.5rem;
  background: linear-gradient(135deg, #0f172a, #1e3a8a) !important;
}
.pay-now-btn svg { width: 18px; height: 18px; }
.pay-now-btn:hover:not(:disabled) { opacity: 0.9; transform: translateY(-1px); transition: all 0.2s; }

/* Success screen */
.pay-success {
  padding: 2.5rem 2rem;
  text-align: center;
  display: flex; flex-direction: column; align-items: center; gap: 0.75rem;
}
.success-icon { font-size: 3rem; animation: pop 0.4s ease-out; }
@keyframes pop { 0% { transform: scale(0.5); opacity: 0; } 80% { transform: scale(1.15); } 100% { transform: scale(1); opacity: 1; } }
.pay-success h3 { font-size: 1.3rem; font-weight: 900; color: #0f172a; margin: 0; }
.pay-success p { font-size: 0.85rem; color: #64748b; margin: 0; }
.tx-ref { font-size: 0.8rem; color: #94a3b8; background: #f8fafc; padding: 0.4rem 1rem; border-radius: 0.5rem; border: 1px solid #f1f5f9; }

/* Spinner */
.slots-loading { display: flex; align-items: center; gap: 0.75rem; color: #64748b; font-size: 0.85rem; padding: 1rem; }
.mini-spinner { width: 20px; height: 20px; border: 2px solid #f1f5f9; border-top-color: #0f172a; border-radius: 50%; animation: spin 0.8s linear infinite; }
@keyframes spin { to { transform: rotate(360deg); } }

/* ── MOBILE ── */
@media (max-width: 768px) {
  .desktop-only { display: none !important; }
  .discover-tab { gap: 0; }
  .filter-bar { padding: 1rem 0 0; position: relative; background: transparent; }
  .search-field { border-radius: 0.85rem; padding: 0.7rem 1rem; }
  .category-scroll { padding-bottom: 0; }
  .results-bar { margin-top: 1rem; }
  .tutors-grid { grid-template-columns: 1fr; gap: 1rem; margin-top: 0.5rem; }

  /* Listings: horizontal thumb + body — do NOT fix card height or the Book
     button and footer are clipped by overflow:hidden on .tutor-card */
  .tutors-grid--listings .tutor-card {
    border-radius: 1.25rem;
    display: flex;
    flex-direction: row;
    align-items: flex-start;
    min-height: 120px;
    height: auto;
    overflow: visible;
  }
  .tutors-grid--listings .preview-area {
    width: 120px;
    height: 120px;
    flex-shrink: 0;
    border-radius: 0;
    align-self: flex-start;
  }
  .tutors-grid--listings .preview-overlay,
  .tutors-grid--listings .time-badge,
  .tutors-grid--listings .btn-preview { display: none; }
  .tutors-grid--listings .card-body { flex: 1; padding: 0.85rem; display: flex; flex-direction: column; justify-content: space-between; min-width: 0; }
  .tutors-grid--listings .tutor-top { margin-bottom: 0.3rem; }

  /* Tutor summary cards stay avatar-first */
  .tutors-grid--summary .tutor-card { border-radius: 1.1rem; }
  .tutor-row { flex-direction: column; align-items: stretch; padding: 0.95rem; }
  .tutor-row-right { align-items: flex-start; flex-direction: row; gap: 1rem; }
  .row-price { text-align: left; }
  .avatar-lg { width: 56px; height: 56px; }
  .row-tags { margin-top: 0.4rem; }
  .row-actions { width: 100%; justify-content: flex-end; }
  .name-row h3 { font-size: 0.9rem; }
  .expertise { font-size: 0.72rem; }
  .rating-badge { padding: 0.2rem 0.45rem; }
  .rating-badge span:last-child { font-size: 0.72rem; }
  .tag-row { margin-bottom: 0.5rem; }
  .tag { font-size: 0.62rem; padding: 0.2rem 0.5rem; }
  .card-footer { padding-top: 0.5rem; }
  .price strong { font-size: 1rem; }
  .reviews { display: none; }
  .btn-book { padding: 0.45rem 0.9rem; font-size: 0.75rem; border-radius: 0.5rem; }
}
</style>
