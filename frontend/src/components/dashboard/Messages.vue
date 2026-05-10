<template>
  <div class="messages-container">

    <!-- ── Desktop Header ── -->
    <div class="page-header desktop-only">
      <h1>Messages</h1>
      <p>Chat with your tutors and manage your sessions.</p>
    </div>

    <!-- ── Mobile: Show list OR chat depending on state ── -->
    <div class="chat-wrapper">

      <!-- Conversation List -->
      <div class="chat-sidebar" :class="{ 'mobile-hidden': mobileViewChat }">
        <div class="search-box">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><circle cx="11" cy="11" r="8"/><path d="m21 21-4.3-4.3"/></svg>
          <input type="text" placeholder="Search conversations..." />
        </div>
        <div class="conversation-list">
          <div
            v-for="chat in conversations" :key="chat.id"
            :class="['chat-item', { active: activeChatId === chat.id }]"
            @click="selectChat(chat.id)"
          >
            <div class="avatar-wrap" :style="{ backgroundColor: chat.color }">
              {{ chat.initials }}
              <span v-if="chat.online" class="online-dot"></span>
            </div>
            <div class="chat-info">
              <div class="chat-top">
                <strong>{{ chat.name }}</strong>
                <span class="chat-time">{{ chat.time }}</span>
              </div>
              <p class="chat-preview">{{ chat.lastMessage }}</p>
            </div>
            <svg class="chevron-right desktop-hidden" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><path d="m9 18 6-6-6-6"/></svg>
          </div>
        </div>
      </div>

      <!-- Main Chat Panel -->
      <div class="chat-main" :class="{ 'mobile-hidden': !mobileViewChat }" v-if="activeChat">
        <div class="chat-header">
          <button class="btn-back mobile-only" @click="mobileViewChat = false">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><path d="m15 18-6-6 6-6"/></svg>
          </button>
          <div class="header-info">
            <div class="avatar-wrap" :style="{ backgroundColor: activeChat.color }">
              {{ activeChat.initials }}
              <span v-if="activeChat.online" class="online-dot"></span>
            </div>
            <div>
              <h2>{{ activeChat.name }}</h2>
              <span class="status" v-if="activeChat.online">● Online</span>
              <span class="status offline" v-else>● Offline</span>
            </div>
          </div>
          <button class="btn-call">
            <svg viewBox="0 0 24 24" fill="currentColor" width="16" height="16"><path d="M6.62 10.79a15.15 15.15 0 0 0 6.59 6.59l2.2-2.2a1 1 0 0 1 1.11-.27c1.12.45 2.33.69 3.58.69a1 1 0 0 1 1 1V20a1 1 0 0 1-1 1A17 17 0 0 1 3 4a1 1 0 0 1 1-1h3.5a1 1 0 0 1 1 1c0 1.25.24 2.46.69 3.58a1 1 0 0 1-.27 1.11l-2.2 2.2z"/></svg>
          </button>
        </div>

        <div class="message-history" ref="historyRef">
          <div v-if="activeChat.messages.length === 0" class="empty-chat">
            <div class="empty-icon">💬</div>
            <p>No messages yet. Say hello!</p>
          </div>
          <div
            v-for="msg in activeChat.messages" :key="msg.id"
            :class="['message-row', msg.sender === 'me' ? 'me' : 'them']"
          >
            <div class="msg-avatar" v-if="msg.sender !== 'me'" :style="{ backgroundColor: activeChat.color }">
              {{ activeChat.initials }}
            </div>
            <div class="msg-bubble-wrap">
              <div class="msg-bubble">{{ msg.text }}</div>
              <span class="msg-time">{{ msg.time }}</span>
            </div>
          </div>
        </div>

        <div class="chat-input-row">
          <button class="btn-attach">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="m21.44 11.05-9.19 9.19a6 6 0 0 1-8.49-8.49l9.19-9.19a4 4 0 0 1 5.66 5.66l-9.2 9.19a2 2 0 0 1-2.83-2.83l8.49-8.48"/></svg>
          </button>
          <input type="text" v-model="newMessage" placeholder="Type a message..." @keyup.enter="sendMessage" />
          <button class="btn-send" @click="sendMessage">
            <svg viewBox="0 0 24 24" fill="currentColor"><path d="m22 2-7 20-4-9-9-4 20-7z"/></svg>
          </button>
        </div>
      </div>

      <!-- Empty state when no chat selected on desktop -->
      <div class="chat-empty-state" v-if="!activeChat">
        <div class="empty-icon-lg">💬</div>
        <h3>Select a conversation</h3>
        <p>Choose a contact from the left to start chatting.</p>
      </div>
    </div>

  </div>
</template>

<script setup>
import { ref, computed, onMounted, nextTick } from 'vue';

const activeChatId = ref(1);
const newMessage = ref('');
const historyRef = ref(null);
const mobileViewChat = ref(false);

const conversations = ref([
  {
    id: 1, name: 'Jamie Dela Cruz', initials: 'JD', color: '#3b82f6', online: true,
    time: '2:33 PM', lastMessage: 'Perfect. We\'ll also cover quadratic equations today.',
    messages: [
      { id: 1, sender: 'them', text: 'Hello! Ready for today\'s session at 3 PM?', time: '2:30 PM' },
      { id: 2, sender: 'me', text: 'Yes! I\'ve been reviewing the functions chapter.', time: '2:31 PM' },
      { id: 3, sender: 'them', text: 'Perfect. We\'ll also cover quadratic equations today.', time: '2:33 PM' },
    ]
  },
  { id: 2, name: 'Maria Santos', initials: 'MS', color: '#f59e0b', online: false, time: '11:00 AM', lastMessage: 'Sure! Will do tonight.', messages: [] },
  { id: 3, name: 'Carlos Reyes', initials: 'CR', color: '#10b981', online: false, time: 'Yesterday', lastMessage: 'You\'re welcome! Great progress...', messages: [] }
]);

const activeChat = computed(() => conversations.value.find(c => c.id === activeChatId.value));

const selectChat = (id) => {
  activeChatId.value = id;
  mobileViewChat.value = true;
};

const sendMessage = async () => {
  if (!newMessage.value.trim()) return;
  activeChat.value.messages.push({
    id: Date.now(), sender: 'me', text: newMessage.value,
    time: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
  });
  newMessage.value = '';
  await nextTick();
  if (historyRef.value) historyRef.value.scrollTop = historyRef.value.scrollHeight;
};

onMounted(() => {
  if (historyRef.value) historyRef.value.scrollTop = historyRef.value.scrollHeight;
});
</script>

<style scoped>
/* Helpers */
.desktop-only { display: block; }
.mobile-only { display: none; }
.desktop-hidden { display: flex; }

.messages-container { display: flex; flex-direction: column; gap: 2rem; height: 100%; }

/* Desktop Header */
.page-header h1 { font-family: var(--font-display); font-size: 2rem; font-weight: 800; color: #0f172a; }
.page-header p { color: #64748b; font-size: 0.95rem; margin-top: 0.25rem; }

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
.chat-item { display: flex; align-items: center; gap: 0.85rem; padding: 1rem 1.25rem; cursor: pointer; transition: background 0.15s; border-bottom: 1px solid #f8fafc; }
.chat-item:hover { background: #f8fafc; }
.chat-item.active { background: #f0f7ff; }
.chat-item.active::before { display: none; }
.avatar-wrap { width: 44px; height: 44px; border-radius: 50%; display: flex; align-items: center; justify-content: center; color: #fff; font-weight: 800; font-size: 0.85rem; flex-shrink: 0; position: relative; }
.online-dot { position: absolute; bottom: 1px; right: 1px; width: 11px; height: 11px; background: #10b981; border: 2px solid #fff; border-radius: 50%; }
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
.status { font-size: 0.72rem; color: #10b981; font-weight: 700; }
.status.offline { color: #94a3b8; }
.btn-call { background: #f1f5f9; border: none; width: 38px; height: 38px; border-radius: 50%; display: flex; align-items: center; justify-content: center; color: #0f172a; cursor: pointer; margin-left: auto; flex-shrink: 0; }

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
.btn-attach { background: none; border: none; color: #94a3b8; display: flex; align-items: center; cursor: pointer; flex-shrink: 0; }
.btn-attach svg { width: 20px; height: 20px; }
.chat-input-row input { flex: 1; padding: 0.8rem 1.1rem; border: 1.5px solid #f1f5f9; background: #f8fafc; border-radius: 0.85rem; outline: none; font-size: 0.9rem; font-weight: 500; min-width: 0; }
.chat-input-row input:focus { border-color: #0f172a; background: #fff; }
.btn-send { background: #0f172a; color: #fff; border: none; width: 42px; height: 42px; border-radius: 50%; display: flex; align-items: center; justify-content: center; cursor: pointer; flex-shrink: 0; transition: transform 0.15s; }
.btn-send:hover { transform: scale(1.05); }
.btn-send svg { width: 16px; height: 16px; }

/* ── MOBILE ── */
@media (max-width: 768px) {
  .desktop-only { display: none !important; }
  .mobile-only { display: flex !important; }
  .desktop-hidden { display: none; }

  .messages-container { gap: 0; height: auto; }

  .chat-wrapper {
    display: flex;
    flex-direction: column;
    border-radius: 0;
    border: none;
    box-shadow: none;
    background: transparent;
    min-height: auto;
  }

  /* Mobile: Show/hide panels */
  .chat-sidebar { border-right: none; background: transparent; }
  .chat-sidebar.mobile-hidden { display: none; }
  .chat-main.mobile-hidden { display: none; }

  .chat-main {
    position: fixed;
    inset: 0;
    z-index: 400;
    background: #f8fafc;
    display: flex;
    flex-direction: column;
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
