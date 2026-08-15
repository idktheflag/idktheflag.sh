import urllib.request
import json
import os
import datetime
import time
import random

TEAM_ID = 419270
USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 idktheflag-updater/1.0'

def fetch_json_with_retry(url, max_retries=3):
    req = urllib.request.Request(url, headers={'User-Agent': USER_AGENT})
    for attempt in range(max_retries):
        try:
            with urllib.request.urlopen(req, timeout=15) as res:
                return json.loads(res.read().decode('utf-8'))
        except Exception as err:
            if attempt == max_retries - 1:
                print(f"Error fetching {url} after {max_retries} attempts: {err}")
                raise err
            sleep_time = (2 ** attempt) + random.uniform(0.5, 1.5)
            print(f"Warning: Fetch {url} failed ({err}). Retrying in {sleep_time:.2f}s...")
            time.sleep(sleep_time)

def load_json(path):
    if not os.path.exists(path):
        return []
    try:
        with open(path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception:
        return []

def save_json(path, data):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    temp_path = path + ".tmp"
    with open(temp_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
        f.write('\n')
    os.replace(temp_path, path)

def generate_ts(ts_path, events_data):
    lines = [
        "import eventsData from './events.json';",
        "",
        "export interface CtfEvent {",
        "  name: string;",
        "  date: string;",
        "  place: number;",
        "  points: number;",
        "  rating: number;",
        "  ctftimeUrl?: string;",
        "}",
        "",
        "export const events: CtfEvent[] = eventsData as CtfEvent[];",
        ""
    ]
    os.makedirs(os.path.dirname(ts_path), exist_ok=True)
    temp_ts = ts_path + ".tmp"
    with open(temp_ts, 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines))
    os.replace(temp_ts, ts_path)

def main():
    d = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(d) if os.path.basename(d) == 'updates' else d
    data_dir = os.path.join(project_root, 'src', 'data')
    json_path = os.path.join(data_dir, 'events.json')
    ts_path = os.path.join(data_dir, 'events.ts')
    public_api_path = os.path.join(project_root, 'public', 'api', 'events.json')

    existing_list = load_json(json_path)
    existing_map = {item['name']: item for item in existing_list}

    year = datetime.datetime.now().year
    years = [year] + ([year - 1] if datetime.datetime.now().month <= 2 else [])

    updated_map = dict(existing_map)

    for y in years:
        try:
            url = f"https://ctftime.org/api/v1/results/{y}/"
            data = fetch_json_with_retry(url)
            for eid, ed in data.items():
                title = ed.get('title', '')
                if not title:
                    continue
                
                scores = ed.get('scores', [])
                score = next((s for s in scores if s.get('team_id') == TEAM_ID), None)
                if not score:
                    continue
                
                real_ctftime_url = f"https://ctftime.org/event/{eid}"
                
                start_date = existing_map.get(title, {}).get('date', f"{y}-01-01")
                rating = existing_map.get(title, {}).get('rating', 0.0)
                
                try:
                    event_url = f"https://ctftime.org/api/v1/events/{eid}/"
                    details = fetch_json_with_retry(event_url, max_retries=1)
                    if details.get('start'):
                        start_date = details.get('start', '').split('T')[0]
                    weight = float(details.get('weight', 0.0))
                    
                    best_points = float(scores[0]['points']) if scores and scores[0].get('points') else 0.0
                    place = int(score.get('place', 1))
                    points = float(score.get('points', 0.0))
                    if best_points > 0:
                        rating = round((points / best_points + 1.0 / max(place, 1)) * weight, 3)
                except Exception as detail_err:
                    print(f"Notice: Could not fetch details for event {eid} ({title}): {detail_err}")

                place = int(score.get('place', existing_map.get(title, {}).get('place', 1)))
                points = float(score.get('points', existing_map.get(title, {}).get('points', 0.0)))
                
                updated_map[title] = {
                    'name': title,
                    'date': start_date,
                    'place': place,
                    'points': int(points) if points.is_integer() else round(points, 4),
                    'rating': rating,
                    'ctftimeUrl': real_ctftime_url
                }
                time.sleep(0.3)
        except Exception as err:
            print(f"Warning: Failed to process events for year {y}: {err}")

    sorted_events = sorted(updated_map.values(), key=lambda x: x['date'])
    save_json(json_path, sorted_events)
    generate_ts(ts_path, sorted_events)
    save_json(public_api_path, sorted_events)
    print(f"Successfully updated {len(sorted_events)} events in {json_path} and {public_api_path}")

if __name__ == '__main__':
    main()

