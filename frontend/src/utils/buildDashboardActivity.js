/** Build merged “recent activity” rows for dashboards (sorted newest first). */

function bookingSortTs(b) {
  if (b.created_at) {
    const ms = new Date(b.created_at).getTime();
    if (!Number.isNaN(ms)) return ms;
  }
  if (!b.date) return 0;
  const t = b.start_time ? String(b.start_time).slice(0, 8) : '12:00:00';
  const ms = new Date(`${b.date}T${t}`).getTime();
  return Number.isNaN(ms) ? 0 : ms;
}

function paymentSortTs(p) {
  if (p.paid_at) {
    const ms = new Date(p.paid_at).getTime();
    if (!Number.isNaN(ms)) return ms;
  }
  return 0;
}

function fmtShortDate(dateStr, timeFallback) {
  if (!dateStr) return '';
  const d = new Date(`${dateStr}T${timeFallback || '12:00:00'}`);
  return d.toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric' });
}

/**
 * @param {object[]} bookings
 * @param {object[]} payments
 * @returns {{ id: string|number; title: string; subtitle: string; value: string; kind: string; ts: number }[]}
 */
export function buildStudentActivities(bookings, payments) {
  const rows = [];

  const list = Array.isArray(bookings) ? bookings : [];
  for (const b of list) {
    const subj = b.post_subject || b.post_title || 'Session';
    const ts = bookingSortTs(b);
    if (b.status === 'completed') {
      rows.push({
        id: `bk-done-${b.id}`,
        ts,
        kind: 'success',
        title: 'Session completed',
        subtitle: `${b.tutor_name || 'Tutor'} · ${subj}`,
        value: fmtShortDate(b.date, b.start_time),
      });
    } else if (b.status === 'pending') {
      rows.push({
        id: `bk-pend-${b.id}`,
        ts,
        kind: 'pending',
        title: 'Booking request',
        subtitle: `${b.tutor_name || 'Tutor'} · ${subj}`,
        value: fmtShortDate(b.date, b.start_time),
      });
    } else if (b.status === 'confirmed') {
      rows.push({
        id: `bk-conf-${b.id}`,
        ts,
        kind: 'info',
        title: 'Session confirmed',
        subtitle: `${b.tutor_name || 'Tutor'} · ${subj}`,
        value: fmtShortDate(b.date, b.start_time),
      });
    } else if (b.status === 'cancelled') {
      rows.push({
        id: `bk-cancel-${b.id}`,
        ts,
        kind: 'muted',
        title: 'Booking cancelled',
        subtitle: subj,
        value: fmtShortDate(b.date, b.start_time),
      });
    }
  }

  const pays = Array.isArray(payments) ? payments : [];
  for (const p of pays) {
    const amt = parseFloat(p.amount || 0).toFixed(2);
    const subj = p.post_subject || p.post_title || 'Session';
    rows.push({
      id: `pay-${p.id}`,
      ts: paymentSortTs(p),
      kind: 'payment',
      title: 'Payment processed',
      subtitle: subj,
      value: `₱${amt}`,
    });
  }

  rows.sort((a, b) => b.ts - a.ts);
  return rows.slice(0, 40);
}

/**
 * @param {object[]} bookings
 * @param {object[]} payments
 */
export function buildTutorActivities(bookings, payments) {
  const rows = [];
  const list = Array.isArray(bookings) ? bookings : [];

  for (const b of list) {
    const subj = b.post_subject || b.post_title || 'Session';
    const ts = bookingSortTs(b);
    if (b.status === 'completed') {
      rows.push({
        id: `bk-done-${b.id}`,
        ts,
        kind: 'success',
        title: 'Session marked complete',
        subtitle: `${b.student_name || 'Student'} · ${subj}`,
        value: fmtShortDate(b.date, b.start_time),
      });
    } else if (b.status === 'pending') {
      rows.push({
        id: `bk-pend-${b.id}`,
        ts,
        kind: 'pending',
        title: 'New booking request',
        subtitle: `${b.student_name || 'Student'} · ${subj}`,
        value: fmtShortDate(b.date, b.start_time),
      });
    } else if (b.status === 'confirmed') {
      rows.push({
        id: `bk-conf-${b.id}`,
        ts,
        kind: 'info',
        title: 'Upcoming session',
        subtitle: `${b.student_name || 'Student'} · ${subj}`,
        value: fmtShortDate(b.date, b.start_time),
      });
    } else if (b.status === 'cancelled') {
      rows.push({
        id: `bk-cancel-${b.id}`,
        ts,
        kind: 'muted',
        title: 'Booking cancelled',
        subtitle: `${b.student_name || 'Student'}`,
        value: fmtShortDate(b.date, b.start_time),
      });
    }
  }

  const pays = Array.isArray(payments) ? payments : [];
  for (const p of pays) {
    const amt = parseFloat(p.amount || 0).toFixed(2);
    const subj = p.post_subject || p.post_title || 'Session';
    rows.push({
      id: `earn-${p.id}`,
      ts: paymentSortTs(p),
      kind: 'payment',
      title: 'Earnings recorded',
      subtitle: `${p.student_name || 'Student'} · ${subj}`,
      value: `₱${amt}`,
    });
  }

  rows.sort((a, b) => b.ts - a.ts);
  return rows.slice(0, 40);
}
