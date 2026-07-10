export interface Badge {
  title: string;
  sub: string;
  tone: 'gold' | 'crimson' | 'muted';
}

export const badges: Badge[] = [
  { title: '1st Place', sub: 'THEM?!CTF 2026', tone: 'gold' },
  { title: 'Top 150 Worldwide', sub: '#145 global team on CTFtime', tone: 'crimson' },
  { title: 'Top 15 National', sub: '#13 US team on CTFtime', tone: 'crimson' },
  { title: 'To be unlocked', sub: '', tone: 'muted' },
  { title: 'To be unlocked', sub: '', tone: 'muted' },
  { title: 'To be unlocked', sub: '', tone: 'muted' },
];
