import statsData from './stats.json';

export interface TeamStats {
  globalRank: number;
  countryRank: number;
  ratingPoints: number;
  eventsPlayed: number;
}

export const teamStats: TeamStats = statsData;
