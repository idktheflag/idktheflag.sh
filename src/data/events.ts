import eventsData from './events.json';

export interface CtfEvent {
  name: string;
  date: string;
  place: number;
  points: number;
  rating: number;
  ctftimeUrl?: string;
}

export const events: CtfEvent[] = eventsData as CtfEvent[];
