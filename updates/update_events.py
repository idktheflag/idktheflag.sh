import urllib.request
import json
import re
import os
import datetime
import time

def parse_existing_events(path):
    if not os.path.exists(path):
        return {}
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()
    pattern = re.compile(r"\{\s*name:\s*(['\"].*?['\"])\s*,\s*date:\s*['\"]([^'\"]*)['\"]\s*,\s*place:\s*(\d+)\s*,\s*points:\s*([\d.]+)\s*,\s*rating:\s*([\d.]+)\s*,?\s*\}", re.DOTALL)
    res = {}
    for m in pattern.findall(content):
        try:
            name = json.loads(m[0]) if (m[0].startswith('"') and m[0].endswith('"')) else m[0].strip("'")
            res[name] = {
                'name': name,
                'date': m[1],
                'place': int(m[2]),
                'points': float(m[3]),
                'rating': float(m[4])
            }
        except Exception:
            pass
    return res

def fetch_json(url):
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'})
    with urllib.request.urlopen(req, timeout=15) as res:
        return json.loads(res.read().decode('utf-8'))

def main():
    d = os.path.dirname(os.path.abspath(__file__))
    path = os.path.join(os.path.dirname(d) if os.path.basename(d) == 'updates' else d, 'src', 'data', 'events.ts')
    existing = parse_existing_events(path)
    
    recent_names = [e['name'] for e in sorted(existing.values(), key=lambda x: x['date'])[-2:]] if existing else []
    year = datetime.datetime.now().year
    years = [year] + ([year - 1] if datetime.datetime.now().month <= 2 else [])
    
    updated = dict(existing)
    for y in years:
        try:
            data = fetch_json(f"https://ctftime.org/api/v1/results/{y}/")
            for eid, ed in data.items():
                title = ed['title']
                score = next((s for s in ed.get('scores', []) if s.get('team_id') == 419270), None)
                if not score or (title in existing and title not in recent_names):
                    continue
                
                details = fetch_json(f"https://ctftime.org/api/v1/events/{eid}/")
                best = float(ed['scores'][0]['points']) if ed.get('scores') and ed['scores'][0].get('points') else 0.0
                place = int(score.get('place', 1))
                weight = float(details.get('weight', 0.0))
                rating = (float(score.get('points', 0.0)) / best + 1.0 / max(place, 1)) * weight if best > 0 else 0.0
                
                updated[title] = {
                    'name': title,
                    'date': details.get('start', '').split('T')[0] or f"{y}-01-01",
                    'place': place,
                    'points': float(score.get('points', 0.0)),
                    'rating': round(rating, 3)
                }
                time.sleep(0.5)
        except Exception:
            pass

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
        name_str = json.dumps(e['name'])
        lines.append(f"  {{ name: {name_str}, date: '{e['date']}', place: {e['place']}, points: {pts}, rating: {rtg} }},")
    lines.append("];")
    lines.append("")

    os.makedirs(os.path.dirname(path), exist_ok=True)
    temp_path = path + ".tmp"
    with open(temp_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines))
    os.replace(temp_path, path)

if __name__ == '__main__':
    main()
