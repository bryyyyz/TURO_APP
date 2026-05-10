/**
 * Outline icons: 24×24 viewBox, round caps/joins — use with stroke currentColor only.
 * Each entry: array of { d?: string, type?: 'path'|'circle'|'line'|'polyline'|'rect', ...attrs }
 */
export const ICON_PATHS = {
  layoutGrid: [
    { type: 'rect', x: 3, y: 3, width: 7, height: 7, rx: 1 },
    { type: 'rect', x: 14, y: 3, width: 7, height: 7, rx: 1 },
    { type: 'rect', x: 14, y: 14, width: 7, height: 7, rx: 1 },
    { type: 'rect', x: 3, y: 14, width: 7, height: 7, rx: 1 },
  ],
  search: [
    { type: 'circle', cx: 11, cy: 11, r: 8 },
    { type: 'path', d: 'm21 21-4.3-4.3' },
  ],
  calendar: [
    { type: 'rect', x: 3, y: 4, width: 18, height: 18, rx: 2 },
    { type: 'path', d: 'M16 2v4M8 2v4' },
    { type: 'path', d: 'M3 10h18' },
  ],
  calendarCheck: [
    { type: 'rect', x: 3, y: 4, width: 18, height: 18, rx: 2 },
    { type: 'path', d: 'M16 2v4M8 2v4' },
    { type: 'path', d: 'M3 10h18' },
    { type: 'path', d: 'm9 16 2 2 4-4' },
  ],
  messageSquare: [
    { type: 'path', d: 'M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z' },
  ],
  creditCard: [
    { type: 'rect', x: 2, y: 5, width: 20, height: 14, rx: 2 },
    { type: 'path', d: 'M2 10h20' },
  ],
  creditCardThin: [
    { type: 'rect', x: 3, y: 5, width: 18, height: 14, rx: 2 },
    { type: 'path', d: 'M3 10h18' },
  ],
  user: [
    { type: 'path', d: 'M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2' },
    { type: 'circle', cx: 12, cy: 7, r: 4 },
  ],
  users: [
    { type: 'path', d: 'M18 21a6 6 0 0 0-12 0' },
    { type: 'circle', cx: 12, cy: 7, r: 4 },
    { type: 'path', d: 'M22 21a4 4 0 1 0-7.92-.75' },
  ],
  usersGroup: [
    { type: 'path', d: 'M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2' },
    { type: 'circle', cx: 9, cy: 7, r: 4 },
    { type: 'path', d: 'M23 21v-2a4 4 0 0 0-3-3.87' },
    { type: 'path', d: 'M16 3.13a4 4 0 0 1 0 7.75' },
  ],
  bell: [
    { type: 'path', d: 'M18 8A6 6 0 0 0 6 8c0 7-3 9-3 9h18s-3-2-3-9' },
    { type: 'path', d: 'M13.73 21a2 2 0 0 1-3.46 0' },
  ],
  mapPin: [
    { type: 'path', d: 'M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0z' },
    { type: 'circle', cx: 12, cy: 10, r: 3 },
  ],
  alertCircle: [
    { type: 'circle', cx: 12, cy: 12, r: 10 },
    { type: 'line', x1: 12, y1: 8, x2: 12, y2: 12 },
    { type: 'line', x1: 12, y1: 16, x2: 12.01, y2: 16 },
  ],
  pencil: [
    { type: 'path', d: 'M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7' },
    {
      type: 'path',
      d: 'M18.5 2.5a2.121 2.121 0 0 1 3 3L12 15l-4 1 1-4 9.5-9.5z',
    },
  ],
  fileText: [
    { type: 'path', d: 'M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z' },
    { type: 'polyline', points: '14 2 14 8 20 8' },
    { type: 'line', x1: 16, y1: 13, x2: 8, y2: 13 },
    { type: 'line', x1: 16, y1: 17, x2: 8, y2: 17 },
  ],
  editFile: [
    { type: 'path', d: 'M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z' },
    { type: 'polyline', points: '14 2 14 8 20 8' },
    { type: 'line', x1: 16, y1: 13, x2: 8, y2: 13 },
    { type: 'line', x1: 16, y1: 17, x2: 8, y2: 17 },
    { type: 'polyline', points: '10 9 9 9 8 9' },
  ],
  image: [
    { type: 'rect', x: 3, y: 3, width: 18, height: 18, rx: 2 },
    { type: 'circle', cx: 8.5, cy: 8.5, r: 1.5 },
    { type: 'polyline', points: '21 15 16 10 5 21' },
  ],
  graduationCap: [
    { type: 'path', d: 'M22 10v6M2 10l10-5 10 5-10 5z' },
    { type: 'path', d: 'M6 12v5c3 3 9 3 12 0v-5' },
  ],
  fileStack: [
    { type: 'path', d: 'M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z' },
    { type: 'polyline', points: '14 2 14 8 20 8' },
    { type: 'path', d: 'M12 18v-6' },
    { type: 'path', d: 'M9 15h6' },
  ],
  list: [
    { type: 'line', x1: 8, y1: 6, x2: 21, y2: 6 },
    { type: 'line', x1: 8, y1: 12, x2: 21, y2: 12 },
    { type: 'line', x1: 8, y1: 18, x2: 21, y2: 18 },
    { type: 'line', x1: 3, y1: 6, x2: 3.01, y2: 6 },
    { type: 'line', x1: 3, y1: 12, x2: 3.01, y2: 12 },
    { type: 'line', x1: 3, y1: 18, x2: 3.01, y2: 18 },
  ],
  dollarCircle: [{ type: 'path', d: 'M12 1v22M17 5H9.5a3.5 3.5 0 0 0 0 7h5a3.5 3.5 0 0 1 0 7H6' }],
  ledger: [
    { type: 'rect', x: 2, y: 5, width: 20, height: 14, rx: 2 },
    { type: 'circle', cx: 12, cy: 12, r: 2.8 },
    { type: 'path', d: 'M17 11h3M4 13h3' },
  ],
  clock: [
    { type: 'circle', cx: 12, cy: 12, r: 9 },
    { type: 'polyline', points: '12 8 12 12 14.5 14' },
  ],
  chevronDown: [{ type: 'path', d: 'm6 9 6 6 6-6' }],
  chevronRight: [{ type: 'path', d: 'm9 18 6-6-6-6' }],
  plus: [{ type: 'path', d: 'M12 5v14M5 12h14' }],
  check: [{ type: 'polyline', points: '20 6 9 17 4 12' }],
  x: [
    { type: 'line', x1: 18, y1: 6, x2: 6, y2: 18 },
    { type: 'line', x1: 6, y1: 6, x2: 18, y2: 18 },
  ],
  // Classic 5‑point star (stroke or fill via TuroIcon `filled`)
  star: [{ type: 'path', d: 'M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z' }],
  /** “Top rated” / achievement */
  award: [
    { type: 'circle', cx: 12, cy: 8, r: 6 },
    { type: 'path', d: 'M15.477 12.89 17 22l-5-3-5 3 1.523-9.11' },
  ],
  logOut: [
    { type: 'path', d: 'M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4' },
    { type: 'polyline', points: '16 17 21 12 16 7' },
    { type: 'line', x1: 21, y1: 12, x2: 9, y2: 12 },
  ],
  settings: [
    { type: 'circle', cx: 12, cy: 12, r: 3 },
    {
      type: 'path',
      d: 'M19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06a2 2 0 0 1 0 2.83 2 2 0 0 1-2.83 0l-.06-.06a1.65 1.65 0 0 0-1.82-.33 1.65 1.65 0 0 0-1 1.51V21a2 2 0 0 1-2 2 2 2 0 0 1-2-2v-.09A1.65 1.65 0 0 0 9 19.4a1.65 1.65 0 0 0-1.82.33l-.06.06a2 2 0 0 1-2.83 0 2 2 0 0 1 0-2.83l.06-.06a1.65 1.65 0 0 0 .33-1.82 1.65 1.65 0 0 0-1.51-1H3a2 2 0 0 1-2-2 2 2 0 0 1 2-2h.09A1.65 1.65 0 0 0 4.6 9a1.65 1.65 0 0 0-.33-1.82l-.06-.06a2 2 0 0 1 0-2.83 2 2 0 0 1 2.83 0l.06.06a1.65 1.65 0 0 0 1.82.33H9a1.65 1.65 0 0 0 1-1.51V3a2 2 0 0 1 2-2 2 2 0 0 1 2 2v.09a1.65 1.65 0 0 0 1 1.51 1.65 1.65 0 0 0 1.82-.33l.06-.06a2 2 0 0 1 2.83 0 2 2 0 0 1 0 2.83l-.06.06a1.65 1.65 0 0 0-.33 1.82V9a1.65 1.65 0 0 0 1.51 1H21a2 2 0 0 1 2 2 2 2 0 0 1-2 2h-.09a1.65 1.65 0 0 0-1.51 1z',
    },
  ],
  penSquare: [{ type: 'path', d: 'M16 11l3 3-8 8H8v-3l8-8zM22 2l-4 4' }],
};
