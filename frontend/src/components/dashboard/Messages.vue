<template>
  <div class="messages-container">

    <!-- ── Desktop Header ── -->
    <div class="page-header desktop-only">
      <h1>Messages</h1>
      <p>Chat with your {{ profileRole === 'tutor' ? 'students' : 'tutors' }} in real time.</p>
    </div>

    <!-- ── Loading state ── -->
    <div v-if="loadingInbox" class="inbox-loading">
      <div class="spinner"></div>
      <span>Loading conversations…</span>
    </div>

    <!-- ── Chat Wrapper ── -->
    <div class="chat-wrapper" v-else>

      <!-- Conversation List / Sidebar -->
      <div class="chat-sidebar" :class="{ 'mobile-hidden': mobileViewChat }">
        <div class="search-box">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><circle cx="11" cy="11" r="8"/><path d="m21 21-4.3-4.3"/></svg>
          <input type="text" placeholder="Search conversations…" v-model="searchQuery" />
        </div>

        <!-- Empty inbox -->
        <div class="empty-inbox" v-if="filteredConversations.length === 0">
          <div class="empty-icon">💬</div>
          <p>No conversations yet.</p>
          <span v-if="searchQuery">Try a different search.</span>
          <span v-else>Your bookings will appear here once both parties start chatting.</span>
        </div>

        <div class="conversation-list" v-else>
          <div
            v-for="conv in filteredConversations" :key="conv.other_user_id"
            :class="['chat-item', { active: activeOtherUserId === conv.other_user_id }]"
            @click="selectConversation(conv)"
          >
            <div class="avatar-wrap" :style="{ backgroundColor: getColor(conv.other_user_id) }">
              {{ initials(conv.other_user_name) }}
              <span v-if="conv.unread_count > 0" class="unread-dot"></span>
            </div>
            <div class="chat-info">
              <div class="chat-top">
                <strong>{{ conv.other_user_name }}</strong>
                <span class="chat-time">{{ formatRelativeTime(conv.last_message_timestamp) }}</span>
              </div>
              <p class="chat-preview">{{ conv.last_message }}</p>
            </div>
            <span v-if="conv.unread_count > 0" class="unread-badge">{{ conv.unread_count }}</span>
            <svg class="chevron-right desktop-hidden" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><path d="m9 18 6-6-6-6"/></svg>
          </div>
        </div>
      </div>

      <!-- Main Chat Panel -->
      <div class="chat-main" :class="{ 'mobile-hidden': !mobileViewChat }" v-if="activeConv">
        <div class="chat-header">
          <button class="btn-back mobile-only" @click="mobileViewChat = false">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><path d="m15 18-6-6 6-6"/></svg>
          </button>
          <div class="header-info">
            <div class="avatar-wrap" :style="{ backgroundColor: getColor(activeConv.other_user_id) }">
              {{ initials(activeConv.other_user_name) }}
            </div>
            <div>
              <h2>{{ activeConv.other_user_name }}</h2>
            </div>
          </div>
        </div>

        <!-- Thread -->
        <div class="message-history" ref="historyRef">
          <div v-if="loadingThread" class="thread-loading">
            <div class="spinner sm"></div>
          </div>
          <div v-else-if="thread.length === 0" class="empty-chat">
            <div class="empty-icon">💬</div>
            <p>No messages yet. Say hello!</p>
          </div>
          <div
            v-for="msg in thread" :key="msg.id"
            :class="['message-row', msg.sender_user_id === myUserId ? 'me' : 'them']"
          >
            <div
              class="msg-avatar"
              v-if="msg.sender_user_id !== myUserId"
              :style="{ backgroundColor: getColor(msg.sender_user_id) }"
            >
              {{ initials(msg.sender_name) }}
            </div>
            <div class="msg-bubble-wrap">
              <div class="msg-bubble">{{ msg.content }}</div>
              <span class="msg-time">{{ formatTime(msg.timestamp) }}</span>
            </div>
          </div>
        </div>

        <!-- Input -->
        <div class="chat-input-row">
          <input
            type="text"
            v-model="newMessage"
            placeholder="Type a message…"
            @keyup.enter="sendMessage"
            :disabled="sending"
          />
          <button class="btn-send" @click="sendMessage" :disabled="sending || !newMessage.trim()">
            <svg viewBox="0 0 24 24" fill="currentColor"><path d="m22 2-7 20-4-9-9-4 20-7z"/></svg>
          </button>
        </div>
      </div>

      <!-- Empty state when no chat selected on desktop -->
      <div class="chat-empty-state" v-if="!activeConv && !mobileViewChat">
        <div class="empty-icon-lg">💬</div>
        <h3>Select a conversation</h3>
        <p>Choose a contact from the left to start chatting.</p>
      </div>
    </div>

  </div>
</template>

<script setup>
import { ref, computed, watch, nextTick, onMounted, onUnmounted } from 'vue';
import { messageService, bookingService } from '../../services/api';

// ── Props ──────────────────────────────────────────────────────────────
const props = defineProps({ profile: Object });

// ── State ──────────────────────────────────────────────────────────────
const myUserId        = computed(() => props.profile?.user ?? null);
const profileRole     = computed(() => props.profile?.role ?? 'student');

const conversations   = ref([]);   // inbox list from /conversations/
const thread          = ref([]);   // current chat messages

const activeConv      = ref(null); // active conversation object
const activeOtherUserId = computed(() => activeConv.value?.other_user_id ?? null);

const newMessage      = ref('');
const historyRef      = ref(null);
const mobileViewChat  = ref(false);
const searchQuery     = ref('');
const loadingInbox    = ref(true);
const loadingThread   = ref(false);
const sending         = ref(false);

let pollInterval = null;

// ── Colour palette for avatars ─────────────────────────────────────────
const PALETTE = [
  '#3b82f6','#f59e0b','#10b981','#8b5cf6','#ef4444',
  '#06b6d4','#f97316','#84cc16','#ec4899','#6366f1',
];
function getColor(userId) {
  return PALETTE[(userId || 0) % PALETTE.length];
}
function initials(name = '') {
  const parts = name.trim().split(/\s+/).filter(Boolean);
  if (parts.length === 0) return '?';
  if (parts.length === 1) return parts[0].charAt(0).toUpperCase();
  return (parts[0].charAt(0) + parts[parts.length - 1].charAt(0)).toUpperCase();
}

// ── Computed ───────────────────────────────────────────────────────────
const filteredConversations = computed(() => {
  const q = searchQuery.value.trim().toLowerCase();
  if (!q) return conversations.value;
  return conversations.value.filter(c =>
    c.other_user_name.toLowerCase().includes(q) ||
    c.last_message.toLowerCase().includes(q)
  );
});

// ── Time helpers ───────────────────────────────────────────────────────
function formatTime(ts) {
  if (!ts) return '';
  const d = new Date(ts);
  return d.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
}
function formatRelativeTime(ts) {
  if (!ts) return '';
  const d = new Date(ts);
  const now = new Date();
  const diffMs = now - d;
  const diffMin = Math.floor(diffMs / 60000);
  if (diffMin < 1) return 'just now';
  if (diffMin < 60) return `${diffMin}m ago`;
  const diffH = Math.floor(diffMin / 60);
  if (diffH < 24) return `${diffH}h ago`;
  const diffD = Math.floor(diffH / 24);
  if (diffD === 1) return 'Yesterday';
  if (diffD < 7) return `${diffD}d ago`;
  return d.toLocaleDateString([], { month: 'short', day: 'numeric' });
}

// ── Inbox ──────────────────────────────────────────────────────────────
async function loadInbox() {
  if (!myUserId.value) return;
  try {
    const { data } = await messageService.getConversations(myUserId.value);
    const fromMsgs = Array.isArray(data) ? data : (data.results || []);

    // Also pull booking contacts so we can start new conversations
    // even before the first message is sent.
    const bookingContacts = await fetchBookingContacts();

    // Merge: conversations already from messages take priority
    const map = new Map();
    bookingContacts.forEach(c => map.set(c.other_user_id, c));
    fromMsgs.forEach(c => map.set(c.other_user_id, c));

    conversations.value = [...map.values()].sort((a, b) => {
      const ta = a.last_message_timestamp ? new Date(a.last_message_timestamp) : new Date(0);
      const tb = b.last_message_timestamp ? new Date(b.last_message_timestamp) : new Date(0);
      return tb - ta;
    });
  } catch (e) {
    console.error('[Messages] Failed to load inbox', e);
  } finally {
    loadingInbox.value = false;
  }
}

/** Fetch the other-side users from bookings to pre-populate the contact list. */
async function fetchBookingContacts() {
  const uid = myUserId.value;
  if (!uid) return [];
  try {
    let res;
    if (profileRole.value === 'student') {
      res = await bookingService.getStudentBookings(uid);
    } else {
      res = await bookingService.getTutorBookings(uid);
    }
    const bookings = Array.isArray(res.data) ? res.data : (res.data?.results || []);
    const seen = new Set();
    const contacts = [];
    for (const b of bookings) {
      const otherId   = profileRole.value === 'student' ? b.tutor   : b.student;
      const otherName = profileRole.value === 'student' ? b.tutor_name : b.student_name;
      const avatarUrl = profileRole.value === 'student' ? b.tutor_avatar_url : b.student_avatar_url;
      if (!otherId || seen.has(otherId)) continue;
      seen.add(otherId);
      contacts.push({
        other_user_id: otherId,
        other_user_name: otherName || 'Unknown',
        other_user_avatar_url: avatarUrl || null,
        last_message: 'No messages yet.',
        last_message_timestamp: null,
        unread_count: 0,
      });
    }
    return contacts;
  } catch (e) {
    console.warn('[Messages] Could not load booking contacts', e);
    return [];
  }
}

// ── Thread ─────────────────────────────────────────────────────────────
async function loadThread(otherUserId, silent = false) {
  if (!myUserId.value || !otherUserId) return;
  if (!silent) loadingThread.value = true;
  try {
    const { data } = await messageService.getThread(myUserId.value, otherUserId);
    const msgs = Array.isArray(data) ? data : (data.results || []);
    thread.value = msgs;
    // Update unread badge in sidebar
    const conv = conversations.value.find(c => c.other_user_id === otherUserId);
    if (conv) conv.unread_count = 0;
    await nextTick();
    scrollToBottom();
  } catch (e) {
    console.error('[Messages] Failed to load thread', e);
  } finally {
    loadingThread.value = false;
  }
}

function scrollToBottom() {
  if (historyRef.value) {
    historyRef.value.scrollTop = historyRef.value.scrollHeight;
  }
}

// ── Send ───────────────────────────────────────────────────────────────
async function sendMessage() {
  const text = newMessage.value.trim();
  if (!text || !myUserId.value || !activeOtherUserId.value || sending.value) return;
  sending.value = true;
  newMessage.value = '';
  try {
    await messageService.sendMessage({
      sender: myUserId.value,
      receiver: activeOtherUserId.value,
      content: text,
    });
    // Refresh thread to show sent message
    await loadThread(activeOtherUserId.value, true);
    // Update inbox preview
    const conv = conversations.value.find(c => c.other_user_id === activeOtherUserId.value);
    if (conv) {
      conv.last_message = text;
      conv.last_message_timestamp = new Date().toISOString();
    }
  } catch (e) {
    console.error('[Messages] Send failed', e);
    newMessage.value = text; // restore on error
  } finally {
    sending.value = false;
    await nextTick();
    scrollToBottom();
  }
}

// ── Select conversation ────────────────────────────────────────────────
async function selectConversation(conv) {
  activeConv.value = conv;
  mobileViewChat.value = true;
  thread.value = [];
  await loadThread(conv.other_user_id);
  startPolling(conv.other_user_id);
}

// ── Polling ────────────────────────────────────────────────────────────
function startPolling(otherUserId) {
  stopPolling();
  pollInterval = setInterval(() => loadThread(otherUserId, true), 5000);
}
function stopPolling() {
  if (pollInterval) { clearInterval(pollInterval); pollInterval = null; }
}

// ── Lifecycle ──────────────────────────────────────────────────────────
watch(() => props.profile?.user, async (uid) => {
  if (uid) {
    loadingInbox.value = true;
    conversations.value = [];
    thread.value = [];
    activeConv.value = null;
    await loadInbox();
  }
}, { immediate: true });

onUnmounted(() => stopPolling());
</script>

<style scoped>
/* Helpers */
.desktop-only { display: block; }
.mobile-only  { display: none; }
.desktop-hidden { display: flex; }

.messages-container { display: flex; flex-direction: column; gap: 2rem; height: 100%; }

/* Desktop Header */
.page-header h1 { font-family: var(--font-display); font-size: 2rem; font-weight: 800; color: #0f172a; }
.page-header p  { color: #64748b; font-size: 0.95rem; margin-top: 0.25rem; }

/* Loading */
.inbox-loading {
  flex: 1; display: flex; flex-direction: column; align-items: center;
  justify-content: center; gap: 0.85rem; color: #94a3b8;
}
.thread-loading { display: flex; justify-content: center; align-items: center; padding: 2rem; }
.spinner {
  width: 32px; height: 32px;
  border: 3px solid #e2e8f0; border-top-color: #0f172a;
  border-radius: 50%; animation: spin 0.7s linear infinite;
}
.spinner.sm { width: 22px; height: 22px; border-width: 2px; }
@keyframes spin { to { transform: rotate(360deg); } }

/* Chat Wrapper */
.chat-wrapper {
  display: grid;
  grid-template-columns: 300px 1fr;
  background: #fff;
  border: 1px solid #f1f5f9;
  border-radius: 1.5rem;
  min-height: 540px;
  overflow: hidden;
  box-shadow: 0 4px 12px rgba(0,0,0,0.03);
  flex: 1;
}

/* Sidebar */
.chat-sidebar { border-right: 1px solid #f1f5f9; display: flex; flex-direction: column; background: #fff; }
.search-box { padding: 1.25rem; position: relative; border-bottom: 1px solid #f1f5f9; }
.search-box svg { position: absolute; left: 2.25rem; top: 50%; transform: translateY(-50%); color: #94a3b8; width: 15px; }
.search-box input { width: 100%; padding: 0.65rem 1rem 0.65rem 2.25rem; border: none; background: #f8fafc; border-radius: 0.65rem; outline: none; font-size: 0.85rem; font-weight: 600; }
.conversation-list { flex: 1; overflow-y: auto; }

/* Empty inbox */
.empty-inbox { flex: 1; display: flex; flex-direction: column; align-items: center; justify-content: center; gap: 0.5rem; padding: 2rem 1.5rem; text-align: center; color: #94a3b8; }
.empty-inbox .empty-icon { font-size: 2.5rem; }
.empty-inbox p { font-size: 0.9rem; font-weight: 700; color: #475569; }
.empty-inbox span { font-size: 0.78rem; font-weight: 500; line-height: 1.4; }

.chat-item { display: flex; align-items: center; gap: 0.85rem; padding: 1rem 1.25rem; cursor: pointer; transition: background 0.15s; border-bottom: 1px solid #f8fafc; }
.chat-item:hover { background: #f8fafc; }
.chat-item.active { background: #f0f7ff; }
.avatar-wrap { width: 44px; height: 44px; border-radius: 50%; display: flex; align-items: center; justify-content: center; color: #fff; font-weight: 800; font-size: 0.85rem; flex-shrink: 0; position: relative; }
.unread-dot { position: absolute; bottom: 1px; right: 1px; width: 11px; height: 11px; background: #ef4444; border: 2px solid #fff; border-radius: 50%; }
.unread-badge { background: #ef4444; color: #fff; font-size: 0.65rem; font-weight: 800; min-width: 18px; height: 18px; padding: 0 4px; border-radius: 999px; display: flex; align-items: center; justify-content: center; flex-shrink: 0; }
.chat-info { flex: 1; overflow: hidden; }
.chat-top { display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.2rem; }
.chat-top strong { font-size: 0.88rem; color: #0f172a; font-weight: 800; }
.chat-time { font-size: 0.68rem; color: #94a3b8; font-weight: 700; }
.chat-preview { font-size: 0.78rem; color: #64748b; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; font-weight: 500; }
.chevron-right { width: 16px; height: 16px; color: #cbd5e1; flex-shrink: 0; }

/* Main Chat */
.chat-main { display: flex; flex-direction: column; background: #f8fafc; }
.chat-header { padding: 1rem 1.5rem; border-bottom: 1px solid #f1f5f9; display: flex; align-items: center; gap: 1rem; background: #fff; }
.btn-back { background: none; border: none; padding: 0.35rem; border-radius: 50%; display: flex; align-items: center; justify-content: center; color: #0f172a; cursor: pointer; }
.btn-back svg { width: 22px; height: 22px; }
.header-info { display: flex; align-items: center; gap: 0.85rem; flex: 1; }
.header-info h2 { font-size: 0.95rem; font-weight: 800; color: #0f172a; }

.message-history { flex: 1; overflow-y: auto; padding: 1.5rem; display: flex; flex-direction: column; gap: 1rem; }
.empty-chat { flex: 1; display: flex; flex-direction: column; align-items: center; justify-content: center; text-align: center; gap: 0.5rem; color: #94a3b8; }
.empty-icon { font-size: 3rem; }
.empty-chat p { font-size: 0.9rem; font-weight: 600; }
.chat-empty-state { display: flex; flex-direction: column; align-items: center; justify-content: center; text-align: center; gap: 0.5rem; color: #94a3b8; background: #fbfcfd; }
.empty-icon-lg { font-size: 3.5rem; }
.chat-empty-state h3 { font-size: 1rem; font-weight: 800; color: #334155; }
.chat-empty-state p { font-size: 0.85rem; }

.message-row { display: flex; gap: 0.75rem; max-width: 80%; }
.message-row.me { align-self: flex-end; flex-direction: row-reverse; }
.message-row.them { align-self: flex-start; }
.msg-avatar { width: 30px; height: 30px; border-radius: 50%; display: flex; align-items: center; justify-content: center; color: #fff; font-size: 0.65rem; font-weight: 800; flex-shrink: 0; }
.msg-bubble-wrap { display: flex; flex-direction: column; gap: 0.2rem; }
.message-row.me .msg-bubble-wrap { align-items: flex-end; }
.msg-bubble { padding: 0.75rem 1rem; border-radius: 1rem; font-size: 0.88rem; line-height: 1.5; font-weight: 500; }
.message-row.them .msg-bubble { background: #fff; color: #0f172a; border-bottom-left-radius: 0.2rem; border: 1px solid #f1f5f9; box-shadow: 0 2px 4px rgba(0,0,0,0.02); }
.message-row.me .msg-bubble { background: #0f172a; color: #fff; border-bottom-right-radius: 0.2rem; }
.msg-time { font-size: 0.65rem; color: #94a3b8; font-weight: 700; }

.chat-input-row { padding: 1rem 1.25rem; border-top: 1px solid #f1f5f9; display: flex; gap: 0.75rem; align-items: center; background: #fff; }
.chat-input-row input { flex: 1; padding: 0.8rem 1.1rem; border: 1.5px solid #f1f5f9; background: #f8fafc; border-radius: 0.85rem; outline: none; font-size: 0.9rem; font-weight: 500; min-width: 0; }
.chat-input-row input:focus { border-color: #0f172a; background: #fff; }
.chat-input-row input:disabled { opacity: 0.6; cursor: not-allowed; }
.btn-send { background: #0f172a; color: #fff; border: none; width: 42px; height: 42px; border-radius: 50%; display: flex; align-items: center; justify-content: center; cursor: pointer; flex-shrink: 0; transition: transform 0.15s; }
.btn-send:hover:not(:disabled) { transform: scale(1.05); }
.btn-send:disabled { opacity: 0.4; cursor: not-allowed; }
.btn-send svg { width: 16px; height: 16px; }

/* ── MOBILE ── */
@media (max-width: 768px) {
  .desktop-only  { display: none !important; }
  .mobile-only   { display: flex !important; }
  .desktop-hidden { display: none; }

  .messages-container { gap: 0; height: auto; }

  .chat-wrapper {
    display: flex; flex-direction: column;
    border-radius: 0; border: none; box-shadow: none;
    background: transparent; min-height: auto;
  }

  .chat-sidebar { border-right: none; background: transparent; }
  .chat-sidebar.mobile-hidden { display: none; }
  .chat-main.mobile-hidden { display: none; }

  .chat-main {
    position: fixed; inset: 0; z-index: 400;
    background: #f8fafc; display: flex; flex-direction: column;
  }

  .chat-header { padding: 1rem; padding-top: env(safe-area-inset-top, 1rem); }
  .message-history { padding: 1rem; flex: 1; overflow-y: auto; }
  .chat-input-row { padding: 0.75rem 1rem; padding-bottom: calc(env(safe-area-inset-bottom, 0px) + 90px); }

  .search-box { padding: 0.75rem 0 1rem; background: transparent; border-bottom: none; }
  .search-box input { background: #fff; border-radius: 0.85rem; padding: 0.7rem 1rem 0.7rem 2.25rem; }

  .chat-item { background: #fff; border-radius: 1rem; margin-bottom: 0.5rem; border: 1px solid #f1f5f9; }
  .chat-item.active { background: #eff6ff; }

  .message-row { max-width: 88%; }
  .msg-bubble { font-size: 0.92rem; }
}
</style>
