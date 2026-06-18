export interface CtfEvent {
  /** Event name as listed on CTFtime. */
  name: string;
  /** ISO date (used for sorting + the rating chart). Approximate where unknown. */
  date: string;
  /** Final placement. */
  place: number;
  /** Raw CTF points scored in the event. */
  points: number;
  /** Rating points earned toward the CTFtime season rating. */
  rating: number;
}

// 2026 season event history (source: CTFtime team #419270).
// Stored in chronological order — the rating chart reads them ascending,
// the event table renders them most-recent-first.
export const events: CtfEvent[] = [
  { name: 'LA CTF 2026', date: '2026-01-31', place: 150, points: 2871, rating: 19.276 },
  { name: 'TexSAW 2026', date: '2026-02-07', place: 457, points: 100, rating: 0.859 },
  { name: 'NCTF 2026', date: '2026-02-21', place: 292, points: 600, rating: 2.883 },
  { name: 'UMassCTF 2026', date: '2026-03-07', place: 176, points: 1800, rating: 24.766 },
  { name: 'Pragyan CTF 2026', date: '2026-03-14', place: 335, points: 450, rating: 0.129 },
  { name: 'RITSEC CTF 2026', date: '2026-03-21', place: 75, points: 1511, rating: 12.004 },
  { name: 'UMDCTF 2026', date: '2026-04-04', place: 102, points: 1399, rating: 30.105 },
  { name: 'Midnight Sun CTF 2026 Quals', date: '2026-04-11', place: 115, points: 1970, rating: 25.105 },
  { name: 'Grey Cat The Flag 2026 Qualifiers', date: '2026-04-18', place: 69, points: 6383, rating: 19.847 },
  { name: 'PascalCTF 2026', date: '2026-04-25', place: 134, points: 4705, rating: 15.413 },
  { name: 'From Dusk Till Dawn Quals', date: '2026-05-02', place: 26, points: 1273, rating: 13.245 },
  { name: 'GPN CTF 2026', date: '2026-05-23', place: 52, points: 1791, rating: 28.595 },
  { name: 'TJCTF 2026', date: '2026-05-30', place: 90, points: 8605, rating: 36.887 },
  { name: '0xFUN CTF 2026', date: '2026-06-06', place: 72, points: 7291, rating: 7.088 },
  { name: 'SillyCTF 2', date: '2026-06-13', place: 23, points: 4720, rating: 13.486 },
  { name: 'boroCTF 2026', date: '2026-06-13', place: 16, points: 16800, rating: 0.0 },
  { name: 'THEM?!CTF 2026', date: '2026-06-14', place: 1, points: 17173, rating: 50.0 },
];
