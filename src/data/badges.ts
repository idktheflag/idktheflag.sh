export interface Badge {
  title: string;
  sub: string;
  /** Visual tone: 'gold' for marquee wins, 'crimson' for solid achievements, 'muted' for placeholders. */
  tone: 'gold' | 'crimson' | 'muted';
}

// Awards & milestones. The first three are real (CTFtime); the muted ones are
// placeholders — swap in your own highlights.
export const badges: Badge[] = [
  { title: '1st Place', sub: 'THEM?!CTF 2026', tone: 'gold' },
  { title: 'Top 150 Worldwide', sub: '#145 global team on CTFtime', tone: 'crimson' },
  { title: 'Top 15 National', sub: '#13 US team on CTFtime', tone: 'crimson' },
  { title: 'To be unlocked', sub: '', tone: 'muted' },
  { title: 'To be unlocked', sub: '', tone: 'muted' },
  { title: 'To be unlocked', sub: '', tone: 'muted' },
];
