<template>
  <div class="landing">

    <!-- ══ NAVBAR ══ -->
    <nav class="navbar" :class="{ scrolled: isScrolled }">
      <div class="nav-inner">
        <img src="/images/TURO_LOGO_WITH_MEANING.png" alt="TURO" class="nav-logo" />
        <div class="nav-links desktop-only">
          <a href="#features">Features</a>
          <a href="#how-it-works">How It Works</a>
          <a href="#for-tutors">For Tutors</a>
          <a href="#testimonials">Testimonials</a>
        </div>
        <div class="nav-actions">
          <router-link to="/login/student" class="btn-nav-ghost">Log In</router-link>
          <router-link to="/signup" class="btn-nav-primary">Get Started</router-link>
        </div>
      </div>
    </nav>

    <!-- ══ HERO ══ -->
    <section class="hero">
      <div class="hero-bg-shapes">
        <div class="hero-shape shape-1"></div>
        <div class="hero-shape shape-2"></div>
        <div class="hero-dots dots-tl"></div>
        <div class="hero-dots dots-br"></div>
      </div>
      <div class="hero-content">
        <div class="hero-badge">
          <span class="badge-star">★</span>
          Philippines' Modern Tutoring Platform
        </div>
        <h1 class="hero-title">
          Empowering Minds.<br />
          <span class="hero-title-accent">Shaping Futures.</span>
        </h1>
        <p class="hero-sub">
          Connect with verified expert tutors, book flexible sessions, and unlock your full potential — all in one place.
        </p>
        <div class="hero-cta">
          <router-link to="/signup" class="btn-primary-lg">
            Start Learning Free
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" class="btn-arrow"><path d="M5 12h14M12 5l7 7-7 7"/></svg>
          </router-link>
          <router-link to="/login/tutor" class="btn-ghost-lg">
            Become a Tutor
          </router-link>
        </div>
        <div class="hero-stats">
          <div class="hero-stat" v-for="s in heroStats" :key="s.label">
            <span class="stat-num">{{ s.num }}</span>
            <span class="stat-lbl">{{ s.label }}</span>
          </div>
        </div>
      </div>
      <div class="hero-visual desktop-only">
        <div class="hero-card-stack">
          <div class="floating-card card-tutor animate-float">
            <div class="fc-avatar">JD</div>
            <div class="fc-info">
              <strong>Juan dela Cruz</strong>
              <span>Mathematics · ★ 4.9</span>
            </div>
            <div class="fc-badge verified">Verified</div>
          </div>
          <div class="diamond-hero">
            <img src="/images/student.png" alt="Student" class="diamond-img" />
          </div>
          <div class="floating-card card-session animate-float" style="animation-delay:1.5s">
            <div class="fc-icon">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="3" y="4" width="18" height="18" rx="2"/><path d="M16 2v4M8 2v4M3 10h18"/></svg>
            </div>
            <div class="fc-info">
              <strong>Session Booked!</strong>
              <span>Today, 3:00 PM</span>
            </div>
          </div>
          <div class="floating-card card-rating animate-float" style="animation-delay:3s">
            <div class="fc-stars">★★★★★</div>
            <span>"Best tutor I've had!"</span>
          </div>
        </div>
      </div>
    </section>

    <!-- ══ TRUST BAR ══ -->
    <section class="trust-bar">
      <div class="trust-inner">
        <div class="trust-item" v-for="t in trustItems" :key="t.label">
          <div class="trust-icon" v-html="t.svg"></div>
          <div class="trust-text">
            <strong>{{ t.label }}</strong>
            <span>{{ t.sub }}</span>
          </div>
        </div>
      </div>
    </section>

    <!-- ══ FEATURES ══ -->
    <section class="features-section" id="features">
      <div class="section-header">
        <div class="section-tag">Why TURO</div>
        <h2>Everything you need to learn better</h2>
        <p>A complete platform built for students and tutors in the Philippines.</p>
      </div>
      <div class="features-grid">
        <div class="feature-card" v-for="f in features" :key="f.title" :class="f.accent">
          <div class="feature-icon-wrap">
            <div class="feature-icon" v-html="f.svg"></div>
          </div>
          <h3>{{ f.title }}</h3>
          <p>{{ f.desc }}</p>
        </div>
      </div>
    </section>

    <!-- ══ HOW IT WORKS ══ -->
    <section class="how-section" id="how-it-works">
      <div class="how-bg"></div>
      <div class="section-header light">
        <div class="section-tag light">Simple Process</div>
        <h2>Get started in minutes</h2>
        <p>Three easy steps to your first tutoring session.</p>
      </div>
      <div class="steps-row">
        <div class="step-card" v-for="(step, i) in steps" :key="step.title">
          <div class="step-num">{{ String(i + 1).padStart(2, '0') }}</div>
          <div class="step-icon" v-html="step.svg"></div>
          <h3>{{ step.title }}</h3>
          <p>{{ step.desc }}</p>
        </div>
        <div class="step-connector desktop-only" v-for="n in 2" :key="'c'+n"></div>
      </div>
      <div class="how-cta">
        <router-link to="/signup" class="btn-primary-lg">
          Create Your Free Account
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" class="btn-arrow"><path d="M5 12h14M12 5l7 7-7 7"/></svg>
        </router-link>
      </div>
    </section>

    <!-- ══ FOR TUTORS ══ -->
    <section class="tutor-section" id="for-tutors">
      <div class="tutor-visual desktop-only">
        <div class="tutor-card-wrap">
          <div class="tutor-earnings-card">
            <div class="tec-label">This Month's Earnings</div>
            <div class="tec-amount">₱12,500</div>
            <div class="tec-bar">
              <div class="tec-fill"></div>
            </div>
            <div class="tec-meta">
              <span>32 sessions completed</span>
              <span class="tec-up">↑ 18%</span>
            </div>
          </div>
          <div class="tutor-tier-badge">
            <span class="tier-star">★</span>
            <div>
              <strong>Gold Tier Tutor</strong>
              <span>Top 10% on TURO</span>
            </div>
          </div>
        </div>
      </div>
      <div class="tutor-content">
        <div class="section-tag">For Tutors</div>
        <h2>Turn your expertise into income</h2>
        <p class="tutor-sub">
          Join hundreds of verified tutors earning on their own schedule. Post your expertise, set your rates, and grow your student base.
        </p>
        <ul class="tutor-perks">
          <li v-for="p in tutorPerks" :key="p">
            <span class="perk-check">✓</span>
            {{ p }}
          </li>
        </ul>
        <router-link to="/login/tutor" class="btn-primary-lg tutor-btn">
          Apply as a Tutor
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" class="btn-arrow"><path d="M5 12h14M12 5l7 7-7 7"/></svg>
        </router-link>
      </div>
    </section>

    <!-- ══ TESTIMONIALS ══ -->
    <section class="testimonials-section" id="testimonials">
      <div class="section-header">
        <div class="section-tag">Success Stories</div>
        <h2>Hear it from our community</h2>
        <p>Real experiences from students and tutors across the Philippines.</p>
      </div>
      <div class="testimonials-grid">
        <div class="testimonial-card" v-for="t in testimonials" :key="t.name">
          <div class="t-stars">★★★★★</div>
          <p class="t-quote">"{{ t.quote }}"</p>
          <div class="t-author">
            <div class="t-avatar">{{ t.initials }}</div>
            <div class="t-meta">
              <strong>{{ t.name }}</strong>
              <span>{{ t.role }}</span>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- ══ CTA BANNER ══ -->
    <section class="cta-banner">
      <div class="cta-shapes">
        <div class="cta-shape s1"></div>
        <div class="cta-shape s2"></div>
      </div>
      <div class="cta-content">
        <h2>Ready to start your journey?</h2>
        <p>Join thousands of students and tutors already on TURO.</p>
        <div class="cta-btns">
          <router-link to="/signup" class="btn-cta-white">
            Sign Up as Student
          </router-link>
          <router-link to="/login/tutor" class="btn-cta-outline">
            Join as Tutor
          </router-link>
        </div>
      </div>
    </section>

    <!-- ══ FOOTER ══ -->
    <footer class="landing-footer">
      <div class="footer-inner">
        <div class="footer-brand">
          <img src="/images/TURO_LOGO_WITH_MEANING.png" alt="TURO" class="footer-logo" />
          <p>Empowering Minds. Shaping Futures.<br />The Philippines' modern tutoring platform.</p>
        </div>
        <div class="footer-links">
          <div class="footer-col">
            <strong>Platform</strong>
            <router-link to="/login/student">Student Login</router-link>
            <router-link to="/login/tutor">Tutor Login</router-link>
            <router-link to="/signup">Sign Up</router-link>
          </div>
          <div class="footer-col">
            <strong>Company</strong>
            <a href="#">About Us</a>
            <a href="#">Help Center</a>
            <a href="#">Contact</a>
          </div>
          <div class="footer-col">
            <strong>Legal</strong>
            <a href="#">Terms of Service</a>
            <a href="#">Privacy Policy</a>
          </div>
        </div>
      </div>
      <div class="footer-bottom">
        <span>© 2026 TURO. All rights reserved.</span>
      </div>
    </footer>

  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue';

const isScrolled = ref(false);

function onScroll() {
  isScrolled.value = window.scrollY > 40;
}
onMounted(() => window.addEventListener('scroll', onScroll));
onUnmounted(() => window.removeEventListener('scroll', onScroll));

const heroStats = [
  { num: '500+', label: 'Verified Tutors' },
  { num: '2,000+', label: 'Students' },
  { num: '10,000+', label: 'Sessions Done' },
  { num: '4.9★', label: 'Avg. Rating' },
];

const trustItems = [
  {
    label: 'Verified Tutors Only',
    sub: 'Every tutor is ID-verified',
    svg: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/><polyline points="9 12 11 14 15 10"/></svg>',
  },
  {
    label: 'Flexible Scheduling',
    sub: 'Book sessions anytime',
    svg: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="3" y="4" width="18" height="18" rx="2"/><path d="M16 2v4M8 2v4M3 10h18"/></svg>',
  },
  {
    label: 'Secure Payments',
    sub: 'GCash & online payments',
    svg: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="2" y="5" width="20" height="14" rx="2"/><path d="M2 10h20"/></svg>',
  },
  {
    label: 'Real-time Messaging',
    sub: 'Chat with your tutor',
    svg: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/></svg>',
  },
];

const features = [
  {
    title: 'Expert Verified Tutors',
    desc: 'Every tutor goes through ID verification and credential review before they can teach on TURO.',
    accent: 'accent-navy',
    svg: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M22 10v6M2 10l10-5 10 5-10 5z"/><path d="M6 12v5c3 3 9 3 12 0v-5"/></svg>',
  },
  {
    title: 'Smart Session Booking',
    desc: 'Browse tutor availability, pick a time slot, and confirm your session in just a few taps.',
    accent: 'accent-amber',
    svg: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="3" y="4" width="18" height="18" rx="2"/><path d="M16 2v4M8 2v4M3 10h18"/><path d="m9 16 2 2 4-4"/></svg>',
  },
  {
    title: 'Tutor Tier System',
    desc: 'Tutors earn tiers based on performance — so you always know who the top educators are.',
    accent: 'accent-navy',
    svg: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="8" r="6"/><path d="M15.477 12.89 17 22l-5-3-5 3 1.523-9.11"/></svg>',
  },
  {
    title: 'Discover by Subject',
    desc: 'Search tutors by subject, location, hourly rate, and availability to find your perfect match.',
    accent: 'accent-amber',
    svg: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="11" cy="11" r="8"/><path d="m21 21-4.3-4.3"/></svg>',
  },
  {
    title: 'Earnings Dashboard',
    desc: 'Tutors get a full earnings overview, session history, and payment tracking in one place.',
    accent: 'accent-navy',
    svg: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 1v22M17 5H9.5a3.5 3.5 0 0 0 0 7h5a3.5 3.5 0 0 1 0 7H6"/></svg>',
  },
  {
    title: 'Safe for Minors',
    desc: 'Students under 18 require guardian consent during signup — keeping the platform safe for everyone.',
    accent: 'accent-amber',
    svg: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/></svg>',
  },
];

const steps = [
  {
    title: 'Create Your Account',
    desc: 'Sign up as a student or tutor in minutes. Minors get a safe guardian-consent flow.',
    svg: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"/><circle cx="12" cy="7" r="4"/></svg>',
  },
  {
    title: 'Find the Right Tutor',
    desc: 'Browse verified tutors by subject, rate, and location. Read reviews and check their tier.',
    svg: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="11" cy="11" r="8"/><path d="m21 21-4.3-4.3"/></svg>',
  },
  {
    title: 'Book & Start Learning',
    desc: 'Pick a session slot, confirm your booking, and start your learning journey right away.',
    svg: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="3" y="4" width="18" height="18" rx="2"/><path d="M16 2v4M8 2v4M3 10h18"/><path d="m9 16 2 2 4-4"/></svg>',
  },
];

const tutorPerks = [
  'Set your own hourly rate and schedule',
  'Get verified and earn a tutor tier badge',
  'Receive payments via GCash',
  'Manage all your students in one dashboard',
  'Track earnings and session history',
  'Build your reputation with student reviews',
];

const testimonials = [
  {
    quote: 'TURO helped me find a Math tutor in just 10 minutes. My grades improved so much in one semester!',
    name: 'Maria Santos',
    role: 'Grade 11 Student',
    initials: 'MS',
  },
  {
    quote: 'As a tutor, TURO gave me a professional platform to grow my student base and track my earnings easily.',
    name: 'Carlo Reyes',
    role: 'College Tutor · Gold Tier',
    initials: 'CR',
  },
  {
    quote: 'The booking system is so smooth. I love that I can see my tutor\'s availability and book instantly.',
    name: 'Ana Lim',
    role: 'College Student',
    initials: 'AL',
  },
  {
    quote: 'The ID verification gave me confidence that my child is learning from a trusted, qualified tutor.',
    name: 'Rosario Dela Cruz',
    role: 'Parent',
    initials: 'RD',
  },
  {
    quote: 'I went from zero students to 15 regular students in 3 months. TURO\'s platform just works.',
    name: 'Paolo Mendoza',
    role: 'Science Tutor · Silver Tier',
    initials: 'PM',
  },
  {
    quote: 'Finally a tutoring app that feels modern and actually works well on mobile. Love the design!',
    name: 'Jasmine Torres',
    role: 'Grade 12 Student',
    initials: 'JT',
  },
];
</script>

<style scoped>
/* ── BASE ── */
.landing {
  font-family: var(--font-sans);
  color: var(--color-text-dark);
  background: #f8fafc;
  overflow-x: hidden;
}
.desktop-only { display: block; }
@media (max-width: 768px) { .desktop-only { display: none !important; } }

/* ── NAVBAR ── */
.navbar {
  position: fixed;
  top: 0; left: 0; right: 0;
  z-index: 100;
  padding: 1rem 0;
  transition: all 0.3s ease;
}
.navbar.scrolled {
  background: rgba(255,255,255,0.95);
  backdrop-filter: blur(12px);
  box-shadow: 0 1px 20px rgba(0,0,0,0.08);
  padding: 0.75rem 0;
}
.nav-inner {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 2rem;
  display: flex;
  align-items: center;
  gap: 2rem;
}
.nav-logo { height: 120px; width: auto; }
.nav-links {
  display: flex;
  gap: 2rem;
  margin-left: auto;
}
.nav-links a {
  font-size: 0.9rem;
  font-weight: 600;
  color: #1f2937;
  text-decoration: none;
  transition: color 0.2s;
}
.nav-links a:hover { color: #f59e0b; }
.nav-actions {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  margin-left: auto;
}
.nav-links + .nav-actions { margin-left: 0; }
.btn-nav-ghost {
  padding: 0.5rem 1.2rem;
  border: 1.5px solid #e2e8f0;
  border-radius: 0.75rem;
  font-size: 0.85rem;
  font-weight: 700;
  color: #0f172a;
  background: #fff;
  text-decoration: none;
  transition: all 0.2s;
}
.btn-nav-ghost:hover { border-color: #0f172a; }
.btn-nav-primary {
  padding: 0.5rem 1.2rem;
  background: linear-gradient(135deg, #0f172a, #1e293b);
  color: #fff;
  border-radius: 0.75rem;
  font-size: 0.85rem;
  font-weight: 700;
  text-decoration: none;
  transition: all 0.2s;
  box-shadow: 0 4px 12px rgba(15,23,42,0.2);
}
.btn-nav-primary:hover { transform: translateY(-1px); box-shadow: 0 6px 18px rgba(15,23,42,0.3); }

/* ── HERO ── */
.hero {
  min-height: 100vh;
  display: flex;
  align-items: center;
  padding: 7rem 2rem 4rem;
  max-width: 1200px;
  margin: 0 auto;
  gap: 4rem;
  position: relative;
  overflow: hidden;
}
.hero-bg-shapes {
  position: absolute;
  inset: 0;
  pointer-events: none;
  z-index: 0;
  overflow: hidden;
}
.hero-shape {
  position: absolute;
  transform: rotate(45deg);
  border-radius: 3rem;
}
.shape-1 {
  width: 500px; height: 500px;
  background: linear-gradient(135deg, #0f172a 0%, #1e3a8a 100%);
  opacity: 0.04;
  top: -100px; right: -100px;
}
.shape-2 {
  width: 350px; height: 350px;
  background: #f59e0b;
  opacity: 0.05;
  bottom: 100px; left: -80px;
}
.hero-dots {
  position: absolute;
  width: 200px; height: 200px;
  background-image: radial-gradient(#cbd5e1 2px, transparent 2px);
  background-size: 16px 16px;
}
.dots-tl { top: 80px; left: 40px; }
.dots-br { bottom: 80px; right: 40px; }

.hero-content {
  flex: 1;
  position: relative;
  z-index: 1;
}
.hero-badge {
  display: inline-flex;
  align-items: center;
  gap: 0.4rem;
  background: #fff;
  border: 1.5px solid #e2e8f0;
  border-radius: 9999px;
  padding: 0.35rem 1rem;
  font-size: 0.8rem;
  font-weight: 700;
  color: #64748b;
  margin-bottom: 1.5rem;
  box-shadow: 0 2px 8px rgba(0,0,0,0.06);
}
.badge-star { color: #f59e0b; font-size: 1rem; }
.hero-title {
  font-family: var(--font-display);
  font-size: clamp(2.4rem, 5vw, 3.8rem);
  font-weight: 800;
  color: #0f172a;
  line-height: 1.1;
  margin-bottom: 1.25rem;
}
.hero-title-accent { color: #f59e0b; }
.hero-sub {
  font-size: 1.1rem;
  color: #64748b;
  font-weight: 500;
  line-height: 1.7;
  max-width: 520px;
  margin-bottom: 2rem;
}
.hero-cta {
  display: flex;
  gap: 1rem;
  flex-wrap: wrap;
  margin-bottom: 3rem;
}
.btn-primary-lg {
  display: inline-flex;
  align-items: center;
  gap: 0.6rem;
  padding: 0.9rem 1.8rem;
  background: linear-gradient(135deg, #0f172a, #1e293b);
  color: #fff;
  border-radius: 0.875rem;
  font-size: 0.95rem;
  font-weight: 800;
  text-decoration: none;
  transition: all 0.3s cubic-bezier(0.4,0,0.2,1);
  box-shadow: 0 4px 15px rgba(15,23,42,0.25);
}
.btn-primary-lg:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 25px rgba(15,23,42,0.35);
}
.btn-primary-lg:hover .btn-arrow { transform: translateX(4px); }
.btn-arrow { width: 18px; height: 18px; transition: transform 0.3s ease; }
.btn-ghost-lg {
  display: inline-flex;
  align-items: center;
  padding: 0.9rem 1.8rem;
  border: 2px solid #e2e8f0;
  color: #0f172a;
  border-radius: 0.875rem;
  font-size: 0.95rem;
  font-weight: 800;
  text-decoration: none;
  background: #fff;
  transition: all 0.2s;
}
.btn-ghost-lg:hover { border-color: #0f172a; background: #f8fafc; }
.hero-stats {
  display: flex;
  gap: 2.5rem;
  flex-wrap: wrap;
}
.hero-stat { display: flex; flex-direction: column; }
.stat-num {
  font-family: var(--font-display);
  font-size: 1.6rem;
  font-weight: 800;
  color: #0f172a;
}
.stat-lbl { font-size: 0.78rem; font-weight: 600; color: #94a3b8; }

/* ── HERO VISUAL ── */
.hero-visual {
  flex: 0 0 420px;
  position: relative;
  z-index: 1;
  height: 480px;
  display: flex;
  align-items: center;
  justify-content: center;
}
.hero-card-stack { position: relative; width: 100%; height: 100%; }
.diamond-hero {
  position: absolute;
  top: 50%; left: 50%;
  transform: translate(-50%, -50%) rotate(45deg);
  width: 260px; height: 260px;
  background: #fff;
  border-radius: 2.5rem;
  overflow: hidden;
  border: 10px solid #fff;
  box-shadow: 0 20px 40px -10px rgba(0,0,0,0.15);
  display: flex; align-items: center; justify-content: center;
}
.diamond-img {
  width: 145%; height: 145%;
  object-fit: cover;
  transform: rotate(-45deg);
}
.floating-card {
  position: absolute;
  background: #fff;
  border-radius: 1rem;
  padding: 0.75rem 1rem;
  box-shadow: 0 8px 24px rgba(0,0,0,0.1);
  display: flex;
  align-items: center;
  gap: 0.75rem;
  border: 1px solid #f1f5f9;
  min-width: 180px;
}
.card-tutor { top: 30px; left: -20px; }
.card-session { bottom: 60px; right: -20px; }
.card-rating { bottom: 10px; left: 10px; flex-direction: column; align-items: flex-start; gap: 0.2rem; }
.fc-avatar {
  width: 36px; height: 36px;
  background: linear-gradient(135deg, #0f172a, #1e293b);
  color: #fff;
  border-radius: 50%;
  display: flex; align-items: center; justify-content: center;
  font-size: 0.75rem; font-weight: 800;
  flex-shrink: 0;
}
.fc-icon {
  width: 36px; height: 36px;
  background: #f0fdf4;
  border-radius: 10px;
  display: flex; align-items: center; justify-content: center;
  color: #16a34a;
  flex-shrink: 0;
}
.fc-icon svg { width: 18px; height: 18px; }
.fc-info { display: flex; flex-direction: column; }
.fc-info strong { font-size: 0.8rem; font-weight: 800; color: #0f172a; }
.fc-info span { font-size: 0.7rem; color: #64748b; font-weight: 600; }
.fc-badge { font-size: 0.65rem; font-weight: 800; padding: 0.2rem 0.5rem; border-radius: 9999px; }
.fc-badge.verified { background: #dcfce7; color: #16a34a; }
.fc-stars { color: #f59e0b; font-size: 0.85rem; letter-spacing: 1px; }
.card-rating span { font-size: 0.75rem; color: #64748b; font-weight: 600; font-style: italic; }

/* ── TRUST BAR ── */
.trust-bar {
  background: #fff;
  border-top: 1px solid #f1f5f9;
  border-bottom: 1px solid #f1f5f9;
  padding: 2rem 2rem;
}
.trust-inner {
  max-width: 1100px;
  margin: 0 auto;
  display: flex;
  justify-content: space-around;
  flex-wrap: wrap;
  gap: 1.5rem;
}
.trust-item { display: flex; align-items: center; gap: 0.75rem; }
.trust-icon {
  width: 40px; height: 40px;
  background: #f8fafc;
  border-radius: 10px;
  display: flex; align-items: center; justify-content: center;
  color: #0f172a;
  flex-shrink: 0;
}
.trust-icon svg { width: 20px; height: 20px; }
.trust-text { display: flex; flex-direction: column; }
.trust-text strong { font-size: 0.85rem; font-weight: 800; color: #0f172a; }
.trust-text span { font-size: 0.72rem; color: #94a3b8; font-weight: 600; }

/* ── SECTION HEADER ── */
.section-header {
  text-align: center;
  margin-bottom: 3.5rem;
}
.section-header h2 {
  font-family: var(--font-display);
  font-size: clamp(1.8rem, 3.5vw, 2.6rem);
  font-weight: 800;
  color: #0f172a;
  margin: 0.5rem 0;
}
.section-header p { font-size: 1rem; color: #64748b; font-weight: 500; }
.section-header.light h2 { color: #fff; }
.section-header.light p { color: #94a3b8; }
.section-tag {
  display: inline-block;
  background: #fef3c7;
  color: #92400e;
  font-size: 0.75rem;
  font-weight: 800;
  padding: 0.3rem 0.9rem;
  border-radius: 9999px;
  letter-spacing: 0.05em;
  text-transform: uppercase;
  margin-bottom: 0.5rem;
}
.section-tag.light { background: rgba(245,158,11,0.15); color: #fbbf24; }

/* ── FEATURES ── */
.features-section {
  padding: 5rem 2rem;
  max-width: 1200px;
  margin: 0 auto;
}
.features-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 1.5rem;
}
.feature-card {
  background: #fff;
  border-radius: 1.25rem;
  padding: 2rem;
  border: 1px solid #f1f5f9;
  transition: all 0.3s ease;
}
.feature-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 12px 30px rgba(0,0,0,0.08);
}
.feature-icon-wrap { margin-bottom: 1.25rem; }
.feature-icon {
  width: 48px; height: 48px;
  border-radius: 14px;
  display: flex; align-items: center; justify-content: center;
}
.feature-icon svg { width: 24px; height: 24px; }
.accent-navy .feature-icon { background: #0f172a; color: #fff; }
.accent-amber .feature-icon { background: #fef3c7; color: #92400e; }
.feature-card h3 {
  font-family: var(--font-display);
  font-size: 1.05rem;
  font-weight: 800;
  color: #0f172a;
  margin-bottom: 0.5rem;
}
.feature-card p { font-size: 0.88rem; color: #64748b; line-height: 1.65; font-weight: 500; }

/* ── HOW IT WORKS ── */
.how-section {
  position: relative;
  padding: 5rem 2rem;
  overflow: hidden;
}
.how-bg {
  position: absolute;
  inset: 0;
  background: linear-gradient(135deg, #0f172a 0%, #1e3a8a 100%);
  z-index: 0;
}
.how-section .section-header,
.steps-row,
.how-cta { position: relative; z-index: 1; }
.steps-row {
  max-width: 1000px;
  margin: 0 auto 3rem;
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 2rem;
  position: relative;
}
.step-card {
  background: rgba(255,255,255,0.06);
  border: 1px solid rgba(255,255,255,0.1);
  border-radius: 1.25rem;
  padding: 2rem 1.5rem;
  text-align: center;
  backdrop-filter: blur(8px);
  transition: all 0.3s ease;
}
.step-card:hover { background: rgba(255,255,255,0.1); transform: translateY(-4px); }
.step-num {
  font-family: var(--font-display);
  font-size: 2.5rem;
  font-weight: 800;
  color: rgba(245,158,11,0.3);
  line-height: 1;
  margin-bottom: 1rem;
}
.step-icon {
  width: 52px; height: 52px;
  background: rgba(245,158,11,0.15);
  border-radius: 14px;
  display: flex; align-items: center; justify-content: center;
  margin: 0 auto 1rem;
  color: #f59e0b;
}
.step-icon svg { width: 26px; height: 26px; }
.step-card h3 {
  font-family: var(--font-display);
  font-size: 1rem;
  font-weight: 800;
  color: #fff;
  margin-bottom: 0.5rem;
}
.step-card p { font-size: 0.85rem; color: #94a3b8; line-height: 1.6; font-weight: 500; }
.how-cta { text-align: center; }

/* ── FOR TUTORS ── */
.tutor-section {
  padding: 5rem 2rem;
  max-width: 1200px;
  margin: 0 auto;
  display: flex;
  align-items: center;
  gap: 5rem;
}
.tutor-visual { flex: 0 0 380px; }
.tutor-card-wrap { display: flex; flex-direction: column; gap: 1.25rem; }
.tutor-earnings-card {
  background: linear-gradient(135deg, #0f172a, #1e3a8a);
  border-radius: 1.25rem;
  padding: 1.75rem;
  color: #fff;
}
.tec-label { font-size: 0.8rem; font-weight: 600; color: #94a3b8; margin-bottom: 0.4rem; }
.tec-amount {
  font-family: var(--font-display);
  font-size: 2.2rem;
  font-weight: 800;
  color: #fff;
  margin-bottom: 1rem;
}
.tec-bar {
  height: 6px;
  background: rgba(255,255,255,0.1);
  border-radius: 9999px;
  margin-bottom: 0.75rem;
  overflow: hidden;
}
.tec-fill {
  height: 100%;
  width: 72%;
  background: linear-gradient(90deg, #f59e0b, #fbbf24);
  border-radius: 9999px;
}
.tec-meta { display: flex; justify-content: space-between; font-size: 0.78rem; color: #94a3b8; font-weight: 600; }
.tec-up { color: #4ade80; }
.tutor-tier-badge {
  background: #fff;
  border: 1px solid #f1f5f9;
  border-radius: 1rem;
  padding: 1rem 1.25rem;
  display: flex;
  align-items: center;
  gap: 0.75rem;
  box-shadow: 0 4px 12px rgba(0,0,0,0.06);
}
.tier-star { font-size: 1.5rem; color: #f59e0b; }
.tutor-tier-badge strong { display: block; font-size: 0.9rem; font-weight: 800; color: #0f172a; }
.tutor-tier-badge span { font-size: 0.75rem; color: #64748b; font-weight: 600; }
.tutor-content { flex: 1; }
.tutor-content h2 {
  font-family: var(--font-display);
  font-size: clamp(1.8rem, 3vw, 2.4rem);
  font-weight: 800;
  color: #0f172a;
  margin: 0.5rem 0 1rem;
}
.tutor-sub { font-size: 1rem; color: #64748b; line-height: 1.7; font-weight: 500; margin-bottom: 1.75rem; }
.tutor-perks { list-style: none; display: flex; flex-direction: column; gap: 0.65rem; margin-bottom: 2rem; }
.tutor-perks li { display: flex; align-items: center; gap: 0.6rem; font-size: 0.9rem; font-weight: 600; color: #1f2937; }
.perk-check {
  width: 22px; height: 22px;
  background: #dcfce7;
  color: #16a34a;
  border-radius: 50%;
  display: flex; align-items: center; justify-content: center;
  font-size: 0.7rem;
  font-weight: 800;
  flex-shrink: 0;
}
.tutor-btn { display: inline-flex; }

/* ── TESTIMONIALS ── */
.testimonials-section {
  padding: 5rem 2rem;
  background: #fff;
}
.testimonials-section .section-header { max-width: 1200px; margin: 0 auto 3.5rem; }
.testimonials-grid {
  max-width: 1200px;
  margin: 0 auto;
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 1.5rem;
}
.testimonial-card {
  background: #f8fafc;
  border: 1px solid #f1f5f9;
  border-radius: 1.25rem;
  padding: 1.75rem;
  transition: all 0.3s ease;
}
.testimonial-card:hover { transform: translateY(-3px); box-shadow: 0 8px 24px rgba(0,0,0,0.07); }
.t-stars { color: #f59e0b; font-size: 0.9rem; letter-spacing: 2px; margin-bottom: 0.75rem; }
.t-quote { font-size: 0.9rem; color: #374151; line-height: 1.7; font-weight: 500; margin-bottom: 1.25rem; font-style: italic; }
.t-author { display: flex; align-items: center; gap: 0.75rem; }
.t-avatar {
  width: 38px; height: 38px;
  background: linear-gradient(135deg, #0f172a, #1e293b);
  color: #fff;
  border-radius: 50%;
  display: flex; align-items: center; justify-content: center;
  font-size: 0.75rem; font-weight: 800;
  flex-shrink: 0;
}
.t-meta { display: flex; flex-direction: column; }
.t-meta strong { font-size: 0.85rem; font-weight: 800; color: #0f172a; }
.t-meta span { font-size: 0.75rem; color: #94a3b8; font-weight: 600; }

/* ── CTA BANNER ── */
.cta-banner {
  position: relative;
  padding: 5rem 2rem;
  overflow: hidden;
  text-align: center;
}
.cta-banner::before {
  content: '';
  position: absolute;
  inset: 0;
  background: linear-gradient(135deg, #0f172a 0%, #1e3a8a 100%);
  z-index: 0;
}
.cta-shapes { position: absolute; inset: 0; z-index: 0; pointer-events: none; }
.cta-shape {
  position: absolute;
  transform: rotate(45deg);
  border-radius: 3rem;
}
.cta-shape.s1 { width: 300px; height: 300px; background: rgba(245,158,11,0.08); top: -80px; right: 10%; }
.cta-shape.s2 { width: 200px; height: 200px; background: rgba(255,255,255,0.04); bottom: -60px; left: 15%; }
.cta-content { position: relative; z-index: 1; }
.cta-content h2 {
  font-family: var(--font-display);
  font-size: clamp(1.8rem, 3.5vw, 2.8rem);
  font-weight: 800;
  color: #fff;
  margin-bottom: 0.75rem;
}
.cta-content p { font-size: 1rem; color: #94a3b8; font-weight: 500; margin-bottom: 2rem; }
.cta-btns { display: flex; gap: 1rem; justify-content: center; flex-wrap: wrap; }
.btn-cta-white {
  padding: 0.9rem 2rem;
  background: #fff;
  color: #0f172a;
  border-radius: 0.875rem;
  font-size: 0.95rem;
  font-weight: 800;
  text-decoration: none;
  transition: all 0.2s;
  box-shadow: 0 4px 15px rgba(0,0,0,0.15);
}
.btn-cta-white:hover { transform: translateY(-2px); box-shadow: 0 8px 25px rgba(0,0,0,0.2); }
.btn-cta-outline {
  padding: 0.9rem 2rem;
  border: 2px solid rgba(255,255,255,0.3);
  color: #fff;
  border-radius: 0.875rem;
  font-size: 0.95rem;
  font-weight: 800;
  text-decoration: none;
  transition: all 0.2s;
}
.btn-cta-outline:hover { border-color: #fff; background: rgba(255,255,255,0.05); }

/* ── FOOTER ── */
.landing-footer {
  background: #0f172a;
  padding: 3.5rem 2rem 1.5rem;
}
.footer-inner {
  max-width: 1200px;
  margin: 0 auto;
  display: flex;
  gap: 4rem;
  flex-wrap: wrap;
  margin-bottom: 2.5rem;
}
.footer-brand { flex: 1; min-width: 220px; }
.footer-logo { height: 52px; width: auto; filter: brightness(0) invert(1); opacity: 0.9; margin-bottom: 1rem; }
.footer-brand p { font-size: 0.85rem; color: #64748b; line-height: 1.7; font-weight: 500; }
.footer-links { display: flex; gap: 3rem; flex-wrap: wrap; }
.footer-col { display: flex; flex-direction: column; gap: 0.6rem; }
.footer-col strong { font-size: 0.8rem; font-weight: 800; color: #fff; text-transform: uppercase; letter-spacing: 0.05em; margin-bottom: 0.25rem; }
.footer-col a { font-size: 0.85rem; color: #64748b; text-decoration: none; font-weight: 500; transition: color 0.2s; }
.footer-col a:hover { color: #f59e0b; }
.footer-bottom {
  max-width: 1200px;
  margin: 0 auto;
  padding-top: 1.5rem;
  border-top: 1px solid rgba(255,255,255,0.06);
  text-align: center;
}
.footer-bottom span { font-size: 0.8rem; color: #475569; font-weight: 500; }

/* ── ANIMATIONS ── */
@keyframes float {
  0% { transform: translateY(0px); }
  50% { transform: translateY(-10px); }
  100% { transform: translateY(0px); }
}
.animate-float { animation: float 6s ease-in-out infinite; }

/* ── MOBILE ── */
@media (max-width: 768px) {
  .hero {
    flex-direction: column;
    padding: 6rem 1.25rem 3rem;
    min-height: auto;
    gap: 2rem;
  }
  .hero-stats { gap: 1.5rem; }
  .nav-inner { padding: 0 1.25rem; }
  .nav-links { display: none; }
  .features-section, .tutor-section, .testimonials-section { padding: 3.5rem 1.25rem; }
  .tutor-section { flex-direction: column; gap: 2.5rem; }
  .steps-row { grid-template-columns: 1fr; }
  .how-section { padding: 3.5rem 1.25rem; }
  .footer-inner { gap: 2rem; }
  .footer-links { gap: 2rem; }
}
</style>
