<template>
  <div class="dashboard-container">
    <!-- ══ MOBILE TOPBAR (Only visible on mobile) ══ -->
    <div class="mobile-topbar">
      <div class="topbar-logo">
        <img src="/images/TURO_LOGO_WITH_MEANING.png" alt="TURO" class="mobile-logo-img" />
      </div>
      <div class="topbar-center">
        <div class="topbar-title">{{ mobileHeaderTitle }}</div>
      </div>
      <div class="topbar-actions">
        <button type="button" class="icon-btn" @click.stop="toggleNotifications">
          <TuroIcon name="bell" :size="18" class="mob-topbar-ic" />
          <span v-if="notificationBadgeCount > 0" class="badge badge-count">{{ notificationBadgeLabel }}</span>
        </button>
        <div class="avatar-mobile" @click="menuOpen = true">
          {{ mobileProfileInitials }}
        </div>
      </div>
    </div>

    <!-- ══ SIDEBAR (Desktop Primary Navigation) ══ -->
    <aside class="sidebar">
      <div class="sidebar-header">
        <img src="/images/TURO_LOGO_WITH_MEANING.png" alt="TURO" class="sidebar-logo" />
      </div>

      <nav class="sidebar-nav">
        <button 
          v-for="tab in tabs" 
          :key="tab.id"
          :class="['nav-link', { active: currentTab === tab.id }]"
          @click="currentTab = tab.id"
        >
          <span class="nav-icon"><TuroIcon :name="tab.icon" :size="20" /></span>
          <span class="nav-label">{{ tab.label }}</span>
        </button>
      </nav>



      <!-- Sidebar Footer (User Profile) -->
      <div class="sidebar-footer">
        <div class="user-profile-wrap">
          <div class="user-profile-widget" @click.stop="toggleLogoutMenu">
            <img :src="dashboardAvatarSrc" alt="Avatar" class="mini-avatar" @error="onAvatarError" />
            <div class="user-meta">
              <span class="name">{{ dashboardDisplayName }}</span>
              <span class="role">Tutor</span>
            </div>
            <TuroIcon name="chevronDown" :size="14" class="sidebar-chevron-ic" />
          </div>
          <div v-if="showLogoutMenu" class="logout-menu">
            <button type="button" class="logout-menu-btn" @click="openLogoutModal">
              <TuroIcon name="logOut" :size="14" class="logout-menu-icon" />
              Logout
            </button>
          </div>
        </div>
      </div>
    </aside>

    <!-- ══ MAIN CONTENT AREA ══ -->
    <main class="main-viewport">
      <!-- Top Header (Desktop Only) -->
      <header class="content-header desktop-only">
        <div class="header-left">
          <div class="header-placeholder"></div>
        </div>

        <div class="header-right">
          <!-- Search Bar -->
          <div class="search-box-desktop">
            <input type="text" placeholder="Search tutors, students, subjects..." />
            <TuroIcon name="search" :size="18" class="search-icon" />
          </div>

          <!-- Notification Bell -->
          <div
            class="notification-trigger"
            role="button"
            tabindex="0"
            aria-label="Recent activity"
            @click.stop="toggleNotifications"
            @keydown.enter.prevent="toggleNotifications"
            @keydown.space.prevent="toggleNotifications"
          >
            <TuroIcon name="bell" :size="22" />
            <span v-if="notificationBadgeCount > 0" class="count-badge">{{ notificationBadgeLabel }}</span>
          </div>

          <!-- User Quick Profile -->
          <div class="quick-profile">
            <img :src="dashboardAvatarSrc" alt="Profile" class="header-avatar" @error="onAvatarError" />
            <div class="header-user-meta">
              <span class="h-name">{{ dashboardDisplayName }}</span>
              <span class="h-role">Tutor</span>
            </div>
            <TuroIcon name="chevronDown" :size="16" class="h-chevron-ic" />
          </div>
        </div>
      </header>

      <!-- Active View Content -->
      <div class="view-viewport">
        <keep-alive>
          <component
            :is="activeComponent"
            :profile="profile"
            @profile-updated="onProfileUpdated"
            @navigate-post="currentTab = 'post'"
          />
        </keep-alive>
      </div>
      
      <!-- Footer (Desktop Only) -->
      <footer class="dashboard-footer desktop-only">
        <span class="copyright">© 2026 TURO. All rights reserved.</span>
        <div class="footer-nav-desktop">
          <a href="#">Terms of Service</a>
          <a href="#">Privacy Policy</a>
          <a href="#">Help Center</a>
        </div>
      </footer>
    </main>

    <!-- Removed ID VERIFICATION MODAL (Now optional via Profile settings) -->

    <!-- ══ MOBILE BOTTOM NAV (Only visible on mobile) ══ -->
    <nav class="bottom-nav">
      <div class="nav-item" :class="{ active: currentTab === 'overview' }" @click="currentTab = 'overview'">
        <span class="mob-nav-ic-wrap"><TuroIcon name="layoutGrid" :size="22" class="mob-nav-ic" /></span>
        <div class="nav-label">Home</div>
      </div>
      <div class="nav-item" :class="{ active: currentTab === 'schedule' }" @click="currentTab = 'schedule'">
        <span class="mob-nav-ic-wrap"><TuroIcon name="calendar" :size="22" class="mob-nav-ic" /></span>
        <div class="nav-label">Schedule</div>
      </div>
      <div class="nav-center-btn" @click="currentTab = 'post'">
        <div class="nav-fab"><TuroIcon name="penSquare" :size="24" class="mob-fab-ic" /></div>
        <div class="nav-fab-label">Post</div>
      </div>
      <div class="nav-item" :class="{ active: currentTab === 'messages' }" @click="currentTab = 'messages'">
        <span class="mob-nav-ic-wrap"><TuroIcon name="messageSquare" :size="22" class="mob-nav-ic" /></span>
        <div class="nav-label">Messages</div>
      </div>
      <div class="nav-item" :class="{ active: menuOpen }" @click="menuOpen = true">
        <span class="mob-nav-ic-wrap"><TuroIcon name="user" :size="22" class="mob-nav-ic" /></span>
        <div class="nav-label">Profile</div>
      </div>
    </nav>

    <!-- ══ MOBILE DRAWER MENU ══ -->
    <transition name="fade">
      <div class="drawer-overlay" v-if="menuOpen" @click="menuOpen = false"></div>
    </transition>
    <transition name="slide-up">
      <div class="drawer" v-if="menuOpen">
        <div class="drawer-handle"></div>
        <div class="drawer-title">Navigation</div>
        <div class="menu-list">
          <div class="menu-item" :class="{ 'active-menu': currentTab === tab.id }"
               v-for="tab in tabs" :key="tab.id"
               @click="currentTab = tab.id; menuOpen = false">
            <span class="menu-icon"><TuroIcon :name="tab.icon" :size="22" class="menu-ic-svg" /></span>
            <span class="menu-label">{{ tab.label }}</span>
          </div>
          <div class="menu-item logout-item" @click="menuOpen = false; openLogoutModal()">
            <span class="menu-icon"><TuroIcon name="logOut" :size="22" class="menu-ic-svg menu-ic-logout" /></span>
            <span class="menu-label">Logout</span>
          </div>
        </div>
      </div>
    </transition>

    <Teleport to="body">
      <div v-if="notificationsOpen" class="notif-shell">
        <div class="notif-backdrop" aria-hidden="true" @click="notificationsOpen = false"></div>
        <DashboardActivityPanel
          floating
          :loading="notificationsLoading"
          :items="notificationItems"
          @close="notificationsOpen = false"
        />
      </div>
    </Teleport>

    <Teleport to="body">
      <div v-if="showLogoutModal" class="logout-modal-shell">
        <div class="logout-modal-backdrop" @click="closeLogoutModal"></div>
        <div class="logout-modal" role="dialog" aria-modal="true" aria-label="Log out confirmation">
          <div class="logout-modal-icon">
            <TuroIcon name="logOut" :size="24" />
          </div>
          <h3>Log out of your account?</h3>
          <p>You can always sign back in anytime to continue tutoring.</p>
          <div class="logout-modal-actions">
            <button type="button" class="btn-logout-cancel" @click="closeLogoutModal" :disabled="loggingOut">Cancel</button>
            <button type="button" class="btn-logout-confirm" @click="handleLogout" :disabled="loggingOut">
              {{ loggingOut ? 'Logging out...' : 'Log out' }}
            </button>
          </div>
        </div>
      </div>
    </Teleport>

  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted, onErrorCaptured, watch, provide, nextTick } from 'vue';
import { useRouter } from 'vue-router';
import { supabase } from '../supabase';
import { useToast } from '../composables/useToast';
import { profileService, bookingService, paymentService } from '../services/api';
import { REFRESH_TRIGGER } from '../symbols/injectionKeys';

// Tab Components
import Overview from '../components/dashboard/Overview.vue';
import PostExpertise from '../components/dashboard/PostExpertise.vue';
import MyListings from '../components/dashboard/MyListings.vue';
import Schedule from '../components/dashboard/Schedule.vue';
import Students from '../components/dashboard/Students.vue';
import Earnings from '../components/dashboard/Earnings.vue';
import Messages from '../components/dashboard/Messages.vue';
import TutorProfile from '../components/dashboard/TutorProfile.vue';
import { TuroIcon } from '../components/icons';
import DashboardActivityPanel from '../components/DashboardActivityPanel.vue';
import { buildTutorActivities } from '../utils/buildDashboardActivity';
import { OPEN_NOTIFICATIONS } from '../symbols/injectionKeys';

const router = useRouter();
const { showToast, toasts } = useToast();
const user = ref(null);
const profile = ref(null);
const currentTab = ref('overview');
const menuOpen = ref(false);
const notificationsOpen = ref(false);
const notificationsLoading = ref(false);
const notificationItems = ref([]);
const notificationBadgeCount = ref(0);
const showLogoutMenu = ref(false);
const showLogoutModal = ref(false);
const loggingOut = ref(false);
const avatarLoadFailed = ref(false);
const refreshTrigger = ref(0);
const realtimeChannel = ref(null);

const notificationBadgeLabel = computed(() =>
  notificationBadgeCount.value > 9 ? '9+' : String(notificationBadgeCount.value),
);

const DEFAULT_AVATAR_PLACEHOLDER =
  "data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' width='80' height='80'><rect width='100%25' height='100%25' fill='%23e2e8f0'/><circle cx='40' cy='30' r='14' fill='%2394a3b8'/><rect x='18' y='50' width='44' height='20' rx='10' fill='%2394a3b8'/></svg>";

const dashboardDisplayName = computed(() => {
  const first = String(profile.value?.first_name || '').trim();
  const last = String(profile.value?.last_name || '').trim();
  const full = `${first} ${last}`.trim();
  return full || 'No profile yet';
});

const mobileProfileInitials = computed(() => {
  const first = String(profile.value?.first_name || '').trim();
  const last = String(profile.value?.last_name || '').trim();
  if (!first && !last) return 'NP';
  return `${first.charAt(0) || ''}${last.charAt(0) || ''}`.toUpperCase() || 'NP';
});

const dashboardAvatarSrc = computed(() => {
  if (avatarLoadFailed.value) return DEFAULT_AVATAR_PLACEHOLDER;
  return profile.value?.avatar_url || DEFAULT_AVATAR_PLACEHOLDER;
});

function onAvatarError() {
  avatarLoadFailed.value = true;
}

function toggleLogoutMenu() {
  showLogoutMenu.value = !showLogoutMenu.value;
}

function closeLogoutMenu() {
  showLogoutMenu.value = false;
}

function openLogoutModal() {
  showLogoutMenu.value = false;
  showLogoutModal.value = true;
}

const onIdSubmitted = (updatedProfile) => {
  if (profile.value && updatedProfile) {
    profile.value.requires_id_verification = updatedProfile.requires_id_verification;
    profile.value.id_verification_status = updatedProfile.id_verification_status;
    profile.value.id_photo_url = updatedProfile.id_photo_url;
  }
};

function closeLogoutModal() {
  if (loggingOut.value) return;
  showLogoutModal.value = false;
}

function onGlobalClick() {
  closeLogoutMenu();
}

async function loadTutorActivityFeed(forPanel = false) {
  const tid = profile.value?.user;
  if (!tid) return;
  if (forPanel) notificationsLoading.value = true;
  try {
    const [bRes, pRes] = await Promise.all([
      bookingService.getTutorBookings(tid),
      paymentService.getTutorPayments(tid),
    ]);
    const bookings = Array.isArray(bRes.data) ? bRes.data : (bRes.data?.results || []);
    const payments = Array.isArray(pRes.data) ? pRes.data : (pRes.data?.results || []);
    notificationItems.value = buildTutorActivities(bookings, payments);
    notificationBadgeCount.value = Math.min(notificationItems.value.length, 99);
  } catch (e) {
    console.error('[TutorDashboard] activity feed', e);
  } finally {
    notificationsLoading.value = false;
  }
}

function toggleNotifications() {
  notificationsOpen.value = !notificationsOpen.value;
  if (notificationsOpen.value) loadTutorActivityFeed(true);
}

function openNotificationsPanel() {
  notificationsOpen.value = true;
  loadTutorActivityFeed(true);
}

provide(OPEN_NOTIFICATIONS, openNotificationsPanel);
provide(REFRESH_TRIGGER, refreshTrigger);

function setupRealtime() {
  const tid = profile.value?.user;
  if (!tid || realtimeChannel.value) return;

  console.log('[TutorDashboard] Setting up realtime for user:', tid);

  realtimeChannel.value = supabase
    .channel(`tutor-realtime-${tid}`)
    .on(
      'postgres_changes',
      {
        event: '*',
        schema: 'public',
        table: 'bookings',
        filter: `tutor_id=eq.${tid}`
      },
      (payload) => {
        console.log('[Realtime] Booking change:', payload);
        refreshTrigger.value++;
        loadTutorActivityFeed(false);
        showToast('Booking updated!', 'info');
      }
    )
    .on(
      'postgres_changes',
      {
        event: '*',
        schema: 'public',
        table: 'payments',
        // Note: filter might need adjustment if payment table doesn't have a direct tutor_id column
        // filter: `tutor_id=eq.${tid}` 
      },
      (payload) => {
        console.log('[Realtime] Payment change:', payload);
        refreshTrigger.value++;
        loadTutorActivityFeed(false);
      }
    )
    .subscribe();
}

watch(
  () => profile.value?.user,
  (uid) => {
    if (uid) {
      loadTutorActivityFeed(false);
      setupRealtime();
    }
  },
);

watch(
  () => profile.value?.avatar_url,
  () => {
    avatarLoadFailed.value = false;
  },
);

const tabs = [
  { id: 'overview', label: 'Overview', icon: 'layoutGrid', component: Overview },
  { id: 'post', label: 'New Post', icon: 'penSquare', component: PostExpertise },
  { id: 'listings', label: 'My Listings', icon: 'list', component: MyListings },
  { id: 'schedule', label: 'Schedule', icon: 'calendar', component: Schedule },
  { id: 'students', label: 'Students', icon: 'usersGroup', component: Students },
  { id: 'earnings', label: 'Earnings', icon: 'dollarCircle', component: Earnings },
  { id: 'messages', label: 'Messages', icon: 'messageSquare', component: Messages },
  { id: 'settings', label: 'My Profile', icon: 'settings', component: TutorProfile },
];

const activeComponent = computed(() => {
  const tab = tabs.find(t => t.id === currentTab.value);
  return tab?.component || Overview;
});

const mobileHeaderTitle = computed(() => {
  const tab = tabs.find(t => t.id === currentTab.value);
  return tab?.label || 'Dashboard';
});

// Catch any child component error — prevent it from killing the whole dashboard
onErrorCaptured((err, instance, info) => {
  console.error('[Dashboard] Child component error:', err, info);
  return false; // suppress propagation
});

const onProfileUpdated = (updated) => {
  if (profile.value) {
    profile.value = { ...profile.value, ...updated };
  }
};

function fallbackNameFromSession(sessionUser, roleLabel = 'Tutor') {
  const meta = sessionUser?.user_metadata || {};
  const first = String(meta.first_name || '').trim();
  const last = String(meta.last_name || '').trim();
  if (first || last) return { first_name: first, last_name: last };

  const full = String(meta.full_name || meta.name || '').trim();
  if (full) {
    const parts = full.split(/\s+/).filter(Boolean);
    return {
      first_name: parts[0] || roleLabel,
      last_name: parts.slice(1).join(' '),
    };
  }
  return { first_name: roleLabel, last_name: '' };
}

/** If Django profile row is missing signup fields, copy from Supabase auth metadata and PATCH once. */
async function mergeSignupMetadataIntoDjangoProfile(sessionUser, role, row) {
  if (!row?.id || !sessionUser?.user_metadata) return row;
  const meta = sessionUser.user_metadata;
  const patch = {};
  const empty = (s) => !String(s ?? '').trim();
  if (empty(row.first_name) && meta.first_name) patch.first_name = String(meta.first_name).trim();
  if (empty(row.last_name) && meta.last_name) patch.last_name = String(meta.last_name).trim();
  if (empty(row.middle_name) && meta.middle_name) patch.middle_name = String(meta.middle_name).trim();
  if (empty(row.name_extension) && meta.name_extension) patch.name_extension = String(meta.name_extension).trim();
  if (empty(row.barangay) && meta.barangay) patch.barangay = String(meta.barangay).trim();
  if (empty(row.municipality) && meta.municipality) patch.municipality = String(meta.municipality).trim();
  if (empty(row.province) && meta.province) patch.province = String(meta.province).trim();
  if (Object.keys(patch).length === 0) return row;
  try {
    await profileService.updateProfile(row.id, patch);
    const { data } = await profileService.getProfileByEmail(sessionUser.email, role);
    const profiles = Array.isArray(data) ? data : (data.results || []);
    const next = profiles?.[0];
    if (next) return { ...next, email: next.email || sessionUser.email };
  } catch (e) {
    console.warn('Could not persist signup metadata to Django profile:', e);
  }
  return { ...row, ...patch };
}

/** Load the Django profile for a given Supabase session user. */
async function loadProfileForSession(sessionUser) {
  user.value = sessionUser;
  try {
    const { data } = await profileService.getProfileByEmail(sessionUser.email, 'tutor');
    const profiles = Array.isArray(data) ? data : (data.results || []);
    if (profiles && profiles.length > 0) {
      let row = {
        ...profiles[0],
        email: profiles[0].email || sessionUser.email,
      };
      row = await mergeSignupMetadataIntoDjangoProfile(sessionUser, 'tutor', row);
      profile.value = row;
    } else {
      const fallback = fallbackNameFromSession(sessionUser, 'Tutor');
      profile.value = {
        first_name: fallback.first_name,
        last_name: fallback.last_name,
        email: sessionUser.email,
        role: 'tutor',
      };
    }
  } catch (error) {
    console.error('[TutorDashboard] Error fetching tutor profile:', error);
    const fallback = fallbackNameFromSession(sessionUser, 'Tutor');
    profile.value = {
      first_name: fallback.first_name,
      last_name: fallback.last_name,
      email: sessionUser.email,
      role: 'tutor',
    };
  }
}

onMounted(async () => {
  document.addEventListener('click', onGlobalClick);

  // Listen for auth events. This covers both the normal login flow AND the
  // hard-refresh case where Supabase fires INITIAL_SESSION once it has
  // restored the token from localStorage (getSession alone can return null
  // during that brief initialization window).
  supabase.auth.onAuthStateChange(async (event, newSession) => {
    if (event === 'SIGNED_OUT') {
      user.value = null;
      profile.value = null;
      router.replace('/login/tutor');
      return;
    }

    if (event === 'INITIAL_SESSION' || event === 'SIGNED_IN' || event === 'TOKEN_REFRESHED') {
      if (!newSession?.user) {
        // No active session — send to login
        router.replace('/login/tutor');
        return;
      }
      // Cross-tab guard: a different user signed in on another tab
      if (event === 'SIGNED_IN' && user.value && newSession.user.id !== user.value.id) {
        console.warn('[TutorDashboard] Cross-tab session change — redirecting to login');
        user.value = null;
        profile.value = null;
        router.replace('/login/tutor');
        return;
      }
      // Only fetch profile if we don't already have it for this user
      if (!profile.value || profile.value.email !== newSession.user.email) {
        await loadProfileForSession(newSession.user);
      }
    }
  });

  // Also attempt an immediate getSession() call so data loads without waiting
  // for the auth event on fast connections / already-initialized sessions.
  const { data: { session } } = await supabase.auth.getSession();
  if (session?.user && !profile.value) {
    await loadProfileForSession(session.user);
  } else if (!session?.user && !profile.value) {
    // Give the INITIAL_SESSION event a moment before hard-redirecting
    await nextTick();
  }
});

onUnmounted(() => {
  document.removeEventListener('click', onGlobalClick);
  if (realtimeChannel.value) {
    supabase.removeChannel(realtimeChannel.value);
  }
});

const handleLogout = async () => {
  if (loggingOut.value) return;
  loggingOut.value = true;
  toasts.value = [];
  try {
    await supabase.auth.signOut();
  } catch (e) {
    console.warn('Supabase signout issue:', e);
  }

  showLogoutMenu.value = false;
  showLogoutModal.value = false;
  menuOpen.value = false;
  notificationsOpen.value = false;
  user.value = null;
  profile.value = null;

  try {
    await router.replace('/login/tutor');
    showToast('Logged out successfully', 'success');
  } catch (err) {
    // Vue router might throw NavigationDuplicated, fallback to window.location
    window.location.href = '/login/tutor';
  } finally {
    loggingOut.value = false;
  }
};

</script>

<style scoped>
.dashboard-container {
  display: flex;
  height: 100vh;
  width: 100%;
  background-color: #f8fafc;
  overflow: hidden;
  position: relative;
}

/* ══ SIDEBAR ══ */
.sidebar {
  width: 280px;
  background-color: #ffffff;
  border-right: 1px solid #eef2f6;
  display: flex; flex-direction: column;
  padding: 0 1rem 1rem 1rem;
  flex-shrink: 0;
  z-index: 50;
  overflow-y: auto;
  scrollbar-width: none;
}
.sidebar::-webkit-scrollbar { display: none; }

.sidebar-header { padding: 0.25rem 1rem 1rem; display: flex; justify-content: flex-start; }
.sidebar-logo { width: 100%; max-width: 150px; height: auto; object-fit: contain; }

.sidebar-nav { display: flex; flex-direction: column; gap: 0.5rem; }
.nav-link {
  display: flex; align-items: center; gap: 1rem; padding: 0.75rem 1rem;
  border-radius: 0.6rem; border: none; background: transparent;
  color: #334155; font-weight: 600; font-size: 0.95rem; cursor: pointer;
  transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1); text-align: left;
}
.nav-link:hover { background-color: #f1f5f9; color: #0f172a; }
.nav-link.active { background-color: #0f172a; color: #ffffff; }
.nav-icon {
  width: 20px;
  height: 20px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: inherit;
}
.nav-icon :deep(svg) {
  width: 20px;
  height: 20px;
  flex-shrink: 0;
}

/* Sidebar Promo */
.sidebar-promo { margin-top: auto; padding: 1.5rem 0 1rem; }
.promo-card {
  background: linear-gradient(135deg, #07193f 0%, #0d2859 100%);
  border-radius: 1rem; padding: 1.25rem; color: #ffffff;
  position: relative; overflow: hidden;
  box-shadow: 0 8px 20px -5px rgba(7, 25, 63, 0.4);
}
.promo-card h3 { font-size: 0.95rem; font-weight: 800; line-height: 1.2; margin-bottom: 0.35rem; }
.promo-card p { font-size: 0.7rem; opacity: 0.8; line-height: 1.3; margin-bottom: 1rem; max-width: 90%; }
.btn-promo { background-color: #ffc107; color: #0f172a; border: none; padding: 0.5rem 0.75rem; border-radius: 0.4rem; font-size: 0.7rem; font-weight: 800; cursor: pointer; width: 100%; position: relative; z-index: 2; }
.promo-decoration { position: absolute; right: -10px; bottom: -20px; width: 110px; height: 110px; opacity: 0.9; z-index: 1; color: #1e3a8a; transform: rotate(-10deg); }
.star-dec { position: absolute; z-index: 1; }
.s1 { width: 28px; height: 28px; right: 10px; bottom: 45px; transform: rotate(-15deg); }
.s2 { width: 12px; height: 12px; right: 25px; bottom: 95px; opacity: 0.9; }
.s3 { width: 18px; height: 18px; right: 65px; bottom: 5px; transform: rotate(15deg); }
.promo-boost { background: #0f172a; }
.profile-strength { display: flex; align-items: center; gap: 1rem; margin-bottom: 1.25rem; }
.strength-circle { width: 40px; height: 40px; border: 3px solid #f59e0b; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-size: 0.75rem; font-weight: 800; }
.btn-yellow { background-color: #f59e0b; color: #fff; }

/* Sidebar Footer */
.sidebar-footer { margin-top: auto; padding-top: 1rem; border-top: 1px solid #f1f5f9; }
.user-profile-wrap { position: relative; }
.user-profile-widget { display: flex; align-items: center; gap: 0.75rem; padding: 0.75rem; background-color: #f8fafc; border-radius: 1rem; cursor: pointer; }
.mini-avatar { width: 40px; height: 40px; border-radius: 50%; object-fit: cover; }
.user-meta { display: flex; flex-direction: column; flex: 1; }
.user-meta .name { font-size: 0.85rem; font-weight: 800; color: #0f172a; }
.user-meta .role { font-size: 0.7rem; color: #94a3b8; font-weight: 700; }
.sidebar-chevron-ic {
  width: 14px !important;
  height: 14px !important;
  color: #94a3b8;
  flex-shrink: 0;
}

.logout-menu {
  position: absolute;
  left: 0;
  right: 0;
  bottom: calc(100% + 0.4rem);
  background: #ffffff;
  border: 1px solid #e2e8f0;
  border-radius: 0.85rem;
  box-shadow: 0 14px 28px rgba(15, 23, 42, 0.12);
  padding: 0.35rem;
  z-index: 60;
}
.logout-menu-btn {
  width: 100%;
  display: flex;
  align-items: center;
  gap: 0.5rem;
  border: none;
  border-radius: 0.6rem;
  padding: 0.55rem 0.7rem;
  background: #fff1f2;
  color: #be123c;
  font-size: 0.82rem;
  font-weight: 800;
  cursor: pointer;
}
.logout-menu-btn:hover { background: #ffe4e6; }
.logout-menu-icon { color: currentColor; }
.logout-modal-shell { position: fixed; inset: 0; z-index: 1200; display: flex; align-items: center; justify-content: center; }
.logout-modal-backdrop { position: absolute; inset: 0; background: rgba(15, 23, 42, 0.45); backdrop-filter: blur(2px); }
.logout-modal {
  position: relative;
  width: min(92vw, 420px);
  background: #ffffff;
  border-radius: 1.2rem;
  border: 1px solid #e2e8f0;
  box-shadow: 0 24px 50px rgba(2, 6, 23, 0.28);
  padding: 1.25rem 1.25rem 1.1rem;
}
.logout-modal-icon {
  width: 42px;
  height: 42px;
  border-radius: 0.9rem;
  background: #fff1f2;
  color: #e11d48;
  display: inline-flex;
  align-items: center;
  justify-content: center;
}
.logout-modal h3 { margin: 0.8rem 0 0.35rem; color: #0f172a; font-size: 1.02rem; font-weight: 900; }
.logout-modal p { margin: 0; color: #64748b; font-size: 0.86rem; line-height: 1.45; }
.logout-modal-actions { margin-top: 1rem; display: flex; justify-content: flex-end; gap: 0.6rem; }
.btn-logout-cancel, .btn-logout-confirm {
  border-radius: 0.7rem;
  padding: 0.58rem 0.95rem;
  font-size: 0.82rem;
  font-weight: 800;
  cursor: pointer;
}
.btn-logout-cancel { border: 1.5px solid #e2e8f0; background: #ffffff; color: #475569; }
.btn-logout-cancel:hover:not(:disabled) { background: #f8fafc; }
.btn-logout-confirm { border: none; background: #e11d48; color: #ffffff; }
.btn-logout-confirm:hover:not(:disabled) { opacity: 0.92; }
.btn-logout-cancel:disabled, .btn-logout-confirm:disabled { opacity: 0.6; cursor: not-allowed; }

/* ══ MAIN VIEWPORT ══ */
.main-viewport { flex: 1; display: flex; flex-direction: column; overflow: hidden; }
.content-header {
  height: 80px; background-color: #ffffff;
  border-bottom: 1px solid #f1f5f9;
  display: flex; align-items: center; justify-content: space-between;
  padding: 0 3rem; flex-shrink: 0;
}
.header-right { display: flex; align-items: center; gap: 2rem; margin-left: auto; }
.search-box-desktop {
  display: flex; align-items: center; background-color: #ffffff;
  border: 1px solid #e2e8f0; border-radius: 0.75rem;
  padding: 0.65rem 1.25rem; width: 380px;
}
.search-box-desktop input { flex: 1; background: transparent; border: none; font-size: 0.9rem; font-weight: 600; outline: none; color: #334155; }
.search-icon { width: 18px; height: 18px; color: #94a3b8; margin-left: 0.75rem; }

.notification-trigger {
  position: relative;
  color: #64748b;
  cursor: pointer;
  width: 44px;
  height: 44px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: #f8fafc;
  border-radius: 12px;
  outline: none;
}
.notification-trigger:focus-visible {
  box-shadow: 0 0 0 2px #fff, 0 0 0 4px #0f172a;
}
.notification-trigger :deep(.turo-icon) {
  width: 22px;
  height: 22px;
}
.count-badge {
  position: absolute;
  top: 4px;
  right: 4px;
  min-width: 18px;
  height: 18px;
  padding: 0 4px;
  background-color: #ef4444;
  color: #ffffff;
  font-size: 0.62rem;
  font-weight: 800;
  border-radius: 999px;
  display: flex;
  align-items: center;
  justify-content: center;
  border: 2px solid #ffffff;
}

.quick-profile { display: flex; align-items: center; gap: 0.85rem; cursor: pointer; }
.header-avatar { width: 44px; height: 44px; border-radius: 50%; object-fit: cover; border: 2px solid #f1f5f9; }
.header-user-meta { display: flex; flex-direction: column; }
.h-name { font-size: 0.9rem; font-weight: 800; color: #0f172a; }
.h-role { font-size: 0.75rem; color: #94a3b8; font-weight: 700; }
.h-chevron-ic {
  width: 16px !important;
  height: 16px !important;
  color: #94a3b8;
  flex-shrink: 0;
}

.view-viewport { flex: 1; overflow-y: auto; padding: 3rem; background-color: #fbfcfd; }
.dashboard-footer { height: 60px; background-color: #ffffff; border-top: 1px solid #f1f5f9; display: flex; align-items: center; justify-content: space-between; padding: 0 3rem; flex-shrink: 0; }
.copyright { font-size: 0.8rem; font-weight: 600; color: #94a3b8; }
.footer-nav-desktop { display: flex; gap: 2rem; }
.footer-nav-desktop a { font-size: 0.8rem; font-weight: 700; color: #94a3b8; text-decoration: none; }
.footer-nav-desktop a:hover { color: #0f172a; }

/* ── MOBILE SPECIFIC STYLES ── */
.mobile-topbar, .bottom-nav, .drawer-overlay, .drawer { display: none; }

@media (max-width: 768px) {
  .sidebar, .desktop-only { display: none !important; }
  .dashboard-container { flex-direction: column; height: auto; min-height: 100vh; overflow-x: hidden; overflow-y: auto; }
  .main-viewport { overflow: visible; height: auto; }
  .view-viewport { padding: 1rem; padding-bottom: 100px; background-color: #f4f6fb; }

  /* Top Bar Mobile */
  .mobile-topbar {
    display: flex;
    background: linear-gradient(135deg, #07193f, #0f172a 55%, #0b2a4f);
    padding: 0.75rem 1rem;
    align-items: center; justify-content: space-between;
    position: sticky; top: 0; z-index: 100;
    padding-top: max(1rem, env(safe-area-inset-top));
    box-shadow: 0 10px 24px rgba(2, 6, 23, 0.25);
    border-bottom: 1px solid rgba(255,255,255,0.08);
  }
  .topbar-logo { display: flex; align-items: center; }
  .mobile-logo-img { height: 44px; width: auto; filter: brightness(0) invert(1); margin-left: -6px; }
  .topbar-center { flex: 1; display: flex; justify-content: center; min-width: 0; padding: 0 0.5rem; }
  .topbar-title {
    font-size: 0.92rem;
    font-weight: 900;
    color: rgba(255,255,255,0.92);
    letter-spacing: 0.01em;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
  }
  .topbar-actions { display: flex; gap: 12px; align-items: center; }
  .icon-btn {
    width: 40px; height: 40px; background: rgba(255,255,255,0.1); border: 1px solid rgba(255,255,255,0.12); border-radius: 14px;
    display: flex; align-items: center; justify-content: center; position: relative;
  }
  .icon-btn:active { transform: scale(0.98); }
  .mob-topbar-ic { color: #ffffff; }
  .badge {
    position: absolute;
    top: 2px;
    right: 2px;
    min-width: 16px;
    height: 16px;
    padding: 0 4px;
    background: #ffc107;
    border-radius: 999px;
    border: 2px solid #0f172a;
    font-size: 10px;
    font-weight: 800;
    color: #0f172a;
    display: flex;
    align-items: center;
    justify-content: center;
    line-height: 1;
  }
  .avatar-mobile {
    width: 40px; height: 40px; border-radius: 14px;
    background: linear-gradient(135deg, #ffc107, #4ecdc4);
    display: flex; align-items: center; justify-content: center;
    font-family: var(--font-display); font-size: 14px; font-weight: 700; color: #0f172a;
    border: 1px solid rgba(255,255,255,0.35);
  }

  /* Bottom Nav Mobile */
  .bottom-nav {
    display: flex; position: fixed; bottom: 0; left: 0; width: 100%;
    background: #ffffff; border-top: 1px solid #e8edf5;
    padding: 8px 0 20px; z-index: 200; box-shadow: 0 -4px 20px rgba(15,22,41,0.08);
  }
  .nav-item { flex: 1; display: flex; flex-direction: column; align-items: center; gap: 4px; }
  .mob-nav-ic-wrap {
    display: flex;
    align-items: center;
    justify-content: center;
    width: 26px;
    height: 26px;
    transition: transform 0.2s;
  }
  .mob-nav-ic { color: #94a3b8; }
  .nav-item.active .mob-nav-ic-wrap { transform: scale(1.08); }
  .nav-item.active .mob-nav-ic { color: #0f172a; }
  .nav-label { font-size: 10px; font-weight: 700; color: #94a3b8; }
  .nav-item.active .nav-label { color: #0f172a; }
  .nav-center-btn { flex: 1; display: flex; flex-direction: column; align-items: center; position: relative; top: -20px; }
  .nav-fab {
    width: 52px;
    height: 52px;
    background: linear-gradient(135deg, #ffc107, #e8951d);
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    box-shadow: 0 4px 16px rgba(245,166,35,0.45);
  }
  .mob-fab-ic { color: #0f172a; }
  .nav-fab-label { font-size: 10px; font-weight: 800; color: #ffc107; margin-top: 4px; }

  /* Drawer Mobile */
  .drawer-overlay { display: block; position: fixed; inset: 0; background: rgba(0,0,0,0.4); backdrop-filter: blur(4px); z-index: 300; }
  .drawer {
    display: block; position: fixed; bottom: 0; left: 0; width: 100%;
    background: #ffffff; border-radius: 24px 24px 0 0; padding: 12px 20px 40px;
    z-index: 301; box-shadow: 0 -10px 30px rgba(0,0,0,0.1);
  }
  .drawer-handle { width: 36px; height: 4px; background: #dde2ed; border-radius: 2px; margin: 0 auto 20px; }
  .drawer-title { font-family: var(--font-display); font-size: 18px; font-weight: 800; color: #0f172a; margin-bottom: 16px; }
  .menu-list { display: flex; flex-direction: column; gap: 4px; }
  .menu-item { display: flex; align-items: center; gap: 14px; padding: 12px; border-radius: 12px; transition: background 0.2s; }
  .menu-item.active-menu { background: #0f172a; color: #ffffff; }
  .menu-item.active-menu .menu-label { color: #ffffff; }
  .menu-icon {
    width: 24px;
    height: 24px;
    display: flex;
    align-items: center;
    justify-content: center;
    flex-shrink: 0;
  }
  .menu-ic-svg { color: #64748b; }
  .menu-item.active-menu .menu-ic-svg { color: #ffffff; }
  .menu-ic-logout.menu-ic-svg,
  .logout-item .menu-ic-svg { color: #ef4444; }
  .menu-item.active-menu .menu-ic-logout { color: #fecaca; }
  .menu-label { font-size: 15px; font-weight: 600; color: #0f172a; }
  .logout-item .menu-label { color: #ef4444; }
}

/* Animations Mobile Drawer */
.notif-backdrop {
  position: fixed;
  inset: 0;
  z-index: 500;
  background: rgba(15, 22, 41, 0.22);
  backdrop-filter: blur(2px);
}

.fade-enter-active, .fade-leave-active { transition: opacity 0.25s; }
.fade-enter-from, .fade-leave-to { opacity: 0; }
.slide-up-enter-active, .slide-up-leave-active { transition: transform 0.3s cubic-bezier(0.4, 0, 0.2, 1); }
.slide-up-enter-from, .slide-up-leave-to { transform: translateY(100%); }

</style>
