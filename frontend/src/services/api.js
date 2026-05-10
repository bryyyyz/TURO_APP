import axios from 'axios';

const API_URL = (import.meta.env.VITE_API_URL || 'http://127.0.0.1:8000/api/').replace(/\/?$/, '/');

const api = axios.create({
    baseURL: API_URL,
    headers: {
        'Content-Type': 'application/json',
    },
});

// Add interceptors if you have auth tokens
// api.interceptors.request.use(config => { ... });

export const profileService = {
    getProfile: (id) => api.get(`profiles/${id}/`),
    getProfileByEmail: (email, role) =>
        api.get(`profiles/`, { params: { ...(email && { email }), ...(role && { role }) } }),
    updateProfile: (id, data) => {
        const isFormData = data instanceof FormData;
        return api.patch(`profiles/${id}/`, data, isFormData ? {
            headers: { 'Content-Type': undefined },
        } : {});
    },
    createProfile: (data) => api.post(`profiles/`, data),
};

export const postService = {
    getAllPosts: (params = {}) => api.get('posts/', { params }),
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
    getAvailability: (tutorId) => api.get(`availability/`, { params: { tutor_id: tutorId } }),
    updateAvailability: (data) => api.post(`availability/`, data),
};

export const sessionSlotService = {
    getSlots: (params) => api.get('session-slots/', { params }),
    createSlot: (data) => api.post('session-slots/', data),
    deleteSlot: (id) => api.delete(`session-slots/${id}/`),
    bulkCreate: (slots) => Promise.all(slots.map(s => api.post('session-slots/', s))),
};

export const bookingService = {
    getBookings: () => api.get('bookings/'),
    getStudentBookings: (studentId) => api.get('bookings/', { params: { student_id: studentId } }),
    getTutorBookings: (tutorId) => api.get('bookings/', { params: { tutor_id: tutorId } }),
    createBooking: (data) => api.post('bookings/', data),
    updateBooking: (id, data) => api.patch(`bookings/${id}/`, data),
};

export const paymentService = {
    getPayments: () => api.get('payments/'),
    getStudentPayments: (studentId) => api.get('payments/', { params: { student_id: studentId } }),
    getTutorPayments: (tutorId) => api.get('payments/', { params: { tutor_id: tutorId } }),
    createPayment: (data) => api.post('payments/', data),
};

export const messageService = {
    getMessages: () => api.get('messages/'),
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
};

export default api;
