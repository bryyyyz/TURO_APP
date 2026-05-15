import axios from 'axios';

/** Human-readable message from axios / API validation errors */
export function formatApiErrorMessage(err) {
    if (!err) return 'Something went wrong.';
    const d = err.response?.data;
    if (typeof d === 'string') return d;
    if (d && typeof d === 'object') {
        if (typeof d.detail === 'string') return d.detail;
        if (Array.isArray(d.detail)) {
            return d.detail
                .map((x) => (typeof x === 'string' ? x : x?.msg || JSON.stringify(x)))
                .join(' ');
        }
        const msgs = [];
        for (const [k, v] of Object.entries(d)) {
            if (Array.isArray(v)) msgs.push(`${k}: ${v.join('; ')}`);
            else if (v != null && typeof v === 'object') msgs.push(`${k}: ${JSON.stringify(v)}`);
            else msgs.push(`${k}: ${v}`);
        }
        if (msgs.length) return msgs.join(' ');
    }
    return err.message || 'Something went wrong.';
}

const API_URL = (import.meta.env.VITE_API_URL || 'http://127.0.0.1:8000/api/').replace(/\/?$/, '/');

const api = axios.create({
    baseURL: API_URL,
    headers: {
        'Content-Type': 'application/json',
    },
});

// Add interceptors if you have auth tokens
// api.interceptors.request.use(config => { ... });

// ── Deduplicate concurrent GET requests ──
const requestCache = new Map();
function deduplicatedGet(url, config = {}) {
    const key = `${url}?${new URLSearchParams(config.params || {}).toString()}`;
    if (requestCache.has(key)) {
        return requestCache.get(key);
    }
    const promise = api.get(url, config).finally(() => {
        setTimeout(() => requestCache.delete(key), 500); // cache for 500ms
    });
    requestCache.set(key, promise);
    return promise;
}

export const profileService = {
    getProfile: (id) => deduplicatedGet(`profiles/${id}/`),
    getProfileByEmail: (email, role) =>
        deduplicatedGet(`profiles/`, { params: { ...(email && { email }), ...(role && { role }) } }),
    updateProfile: (id, data) => {
        const isFormData = data instanceof FormData;
        return api.patch(`profiles/${id}/`, data, isFormData ? {
            headers: { 'Content-Type': undefined },
        } : {});
    },
    createProfile: (data) => api.post(`profiles/`, data),
};

export const postService = {
    getAllPosts: (params = {}) => deduplicatedGet('posts/', { params }),
    createPost: (data) => {
        const isFormData = data instanceof FormData;
        // For FormData, remove Content-Type so browser sets it with the required boundary
        return api.post('posts/', data, isFormData ? {
            headers: { 'Content-Type': undefined }
        } : {});
    },
    updatePost: (id, data) => {
        const isFormData = data instanceof FormData;
        return api.put(`posts/${id}/`, data, isFormData ? {
            headers: { 'Content-Type': undefined }
        } : {});
    },
    deletePost: (id) => api.delete(`posts/${id}/`),
};

export const availabilityService = {
    getAvailability: (tutorId) => deduplicatedGet(`availability/`, { params: { tutor_id: tutorId } }),
    updateAvailability: (data) => api.post(`availability/`, data),
};

export const sessionSlotService = {
    getSlots: (params) => deduplicatedGet('session-slots/', { params }),
    createSlot: (data) => api.post('session-slots/', data),
    deleteSlot: (id) => api.delete(`session-slots/${id}/`),
    bulkCreate: (slots) => Promise.all(slots.map(s => api.post('session-slots/', s))),
};

export const bookingService = {
    getBookings: () => deduplicatedGet('bookings/'),
    getStudentBookings: (studentId, params = {}) => deduplicatedGet('bookings/', { params: { student_id: studentId, ...params } }),
    getTutorBookings: (tutorId, params = {}) => deduplicatedGet('bookings/', { params: { tutor_id: tutorId, ...params } }),
    createBooking: (data) => api.post('bookings/', data),
    updateBooking: (id, data) => api.patch(`bookings/${id}/`, data),
};

export const paymentService = {
    getPayments: () => deduplicatedGet('payments/'),
    getStudentPayments: (studentId, params = {}) => deduplicatedGet('payments/', { params: { student_id: studentId, ...params } }),
    getTutorPayments: (tutorId, params = {}) => deduplicatedGet('payments/', { params: { tutor_id: tutorId, ...params } }),
    createPayment: (data) => api.post('payments/', data),
};

export const messageService = {
    /** Inbox: one entry per unique conversation partner for the given user */
    getConversations: (userId) =>
        api.get('conversations/', { params: { user_id: userId } }),
    /** Thread: all messages between user_id and other_user_id (also marks incoming as read) */
    getThread: (userId, otherUserId) =>
        api.get('messages/', { params: { user_id: userId, other_user_id: otherUserId } }),
    /** Send a new message */
    sendMessage: (data) => api.post('messages/', data),
};

function getAdminAuthHeaders() {
    const authToken = sessionStorage.getItem('turo_admin_auth') || '';
    if (!authToken) return {};
    try {
        const decoded = atob(authToken);
        const [username, password] = decoded.split(':');
        if (!username || !password) return {};
        return {
            'X-Admin-Username': username,
            'X-Admin-Password': password,
        };
    } catch (_err) {
        return {};
    }
}

export const adminService = {
    getPendingTierRequests: () => api.get('admin/tier-requests/', { headers: getAdminAuthHeaders() }),
    reviewTierRequest: (profileId, payload) =>
        api.patch(`admin/tier-requests/${profileId}/`, payload, { headers: getAdminAuthHeaders() }),
    getPendingIdVerifications: () => api.get('admin/id-verifications/', { headers: getAdminAuthHeaders() }),
    reviewIdVerification: (profileId, payload) =>
        api.patch(`admin/id-verifications/${profileId}/`, payload, { headers: getAdminAuthHeaders() }),
};

export default api;
