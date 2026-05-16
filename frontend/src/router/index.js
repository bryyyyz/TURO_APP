import { createRouter, createWebHistory } from 'vue-router';

const routes = [
  {
    path: '/',
    name: 'Landing',
    component: () => import('../views/LandingPage.vue')
  },
  {
    path: '/login/student',
    name: 'LoginStudent',
    component: () => import('../views/LoginStudent.vue')
  },
  {
    path: '/login/tutor',
    name: 'LoginTutor',
    component: () => import('../views/LoginTutor.vue')
  },
  {
    path: '/signup',
    name: 'Signup',
    component: () => import('../views/Signup.vue')
  },
  {
    path: '/admin/login',
    name: 'AdminLogin',
    component: () => import('../views/AdminLogin.vue')
  },
  {
    path: '/admin/reviews',
    name: 'AdminTierReviews',
    component: () => import('../views/AdminTierReviews.vue'),
    meta: { requiresAdmin: true }
  },
  {
    path: '/admin/id-verifications',
    name: 'AdminIdReviews',
    component: () => import('../views/AdminIdReviews.vue'),
    meta: { requiresAdmin: true }
  },
  {
    path: '/dashboard/tutor',
    name: 'TutorDashboard',
    component: () => import('../views/TutorDashboard.vue')
  },
  {
    path: '/dashboard/student',
    name: 'StudentDashboard',
    component: () => import('../views/StudentDashboard.vue')
  }
];

const router = createRouter({
  history: createWebHistory(),
  routes
});

router.beforeEach((to, _from, next) => {
  if (!to.meta.requiresAdmin) return next();
  if (sessionStorage.getItem('turo_admin_auth')) return next();
  return next('/admin/login');
});

export default router;
