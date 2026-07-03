import urllib.request
import json
import re
import os
import datetime
import time

def parse_existing_events(path):
    if not os.path.exists(path): return {}
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()
    pattern = re.compile(r"\{\s*name:\s*'([^']*)',\s*date:\s*'([^']*)',\s*place:\s*(\d+),\s*points:\s*([\d.]+),\s*rating:\s*([\d.]+)\s*\}")
    return {m[0]: {'name': m[0], 'date': m[1], 'place': int(m[2]), 'points': float(m[3]), 'rating': float(m[4])} for m in pattern.findall(content)}

def fetch_json(url):
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    with urllib.request.urlopen(req) as res:
        return json.loads(res.read().decode('utf-8'))

def main():
    d = os.path.dirname(os.path.abspath(__file__))
    path = os.path.join(os.path.dirname(d) if os.path.basename(d) == 'updates' else d, 'src', 'data', 'events.ts')
    existing = parse_existing_events(path)
    print(f"Loaded {len(existing)} existing events from {path}")
    
    recent_names = [e['name'] for e in sorted(existing.values(), key=lambda x: x['date'])[-2:]]
    year = datetime.datetime.now().year
    years = [year] + ([year - 1] if datetime.datetime.now().month <= 2 else [])
    
    updated = dict(existing)
    for y in years:
        print(f"Fetching results for year {y}...")
        for eid, ed in fetch_json(f"https://ctftime.org/api/v1/results/{y}/").items():
            title = ed['title']
            score = next((s for s in ed['scores'] if s['team_id'] == 419270), None)
            if not score or (title in existing and title not in recent_names):
                continue
                
            print(f"Fetching details for: {title} (ID: {eid})")
            details = fetch_json(f"https://ctftime.org/api/v1/events/{eid}/")
            best = float(ed['scores'][0]['points']) if ed['scores'] else 0.0
            place = int(score['place'])
            rating = (float(score['points']) / best + 1.0 / place) * float(details.get('weight', 0.0)) if best > 0 else 0.0
            
            updated[title] = {
                'name': title,
                'date': details.get('start', '').split('T')[0] or f"{y}-01-01",
                'place': place,
                'points': float(score['points']),
                'rating': round(rating, 3)
            }
            time.sleep(0.5)

    final = sorted(updated.values(), key=lambda x: x['date'])
    lines = [
        "export interface CtfEvent {",
        "  name: string;",
        "  date: string;",
        "  place: number;",
        "  points: number;",
        "  rating: number;",
        "}",
        "",
        "export const events: CtfEvent[] = ["
    ]
    for e in final:
        pts = int(e['points']) if e['points'].is_integer() else e['points']
        rtg = int(e['rating']) if e['rating'].is_integer() else e['rating']
        lines.append(f"  {{ name: '{e['name']}', date: '{e['date']}', place: {e['place']}, points: {pts}, rating: {rtg} }},")
    lines.append("];")
    
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines))
    print(f"Successfully wrote {len(final)} events to {path}")

if __name__ == '__main__':
    main()
