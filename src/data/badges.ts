import { teamStats } from './stats.ts';
export interface Badge {
  title: string;
  sub: string;
  tone: 'gold' | 'crimson' | 'muted';
}
export const badges: Badge[] = [
  { title: '1st Place', sub: 'THEM?!CTF 2026', tone: 'gold' },
  { title: `Top ${Math.ceil(teamStats.globalRank / 50) * 50} Worldwide`, sub: `#${teamStats.globalRank} global team on CTFtime`, tone: 'crimson' },
  { title: `Top ${Math.ceil(teamStats.countryRank / 5) * 5} National`, sub: `#${teamStats.countryRank} US team on CTFtime`, tone: 'crimson' },
  { title: 'To be unlocked', sub: '', tone: 'muted' },
  { title: 'To be unlocked', sub: '', tone: 'muted' },
  { title: 'To be unlocked', sub: '', tone: 'muted' },
];
