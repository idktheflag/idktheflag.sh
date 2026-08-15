import urllib.request
import json
import os
import datetime
import time
import random

TEAM_ID = "419270"
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
        return {}
    try:
        with open(path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception:
        return {}

def save_json(path, data):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    temp_path = path + ".tmp"
    with open(temp_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
        f.write('\n')
    os.replace(temp_path, path)

def generate_ts(ts_path):
    lines = [
        "import statsData from './stats.json';",
        "",
        "export interface TeamStats {",
        "  globalRank: number;",
        "  countryRank: number;",
        "  ratingPoints: number;",
        "  eventsPlayed: number;",
        "}",
        "",
        "export const teamStats: TeamStats = statsData;",
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
    json_path = os.path.join(data_dir, 'stats.json')
    ts_path = os.path.join(data_dir, 'stats.ts')
    events_json_path = os.path.join(data_dir, 'events.json')
    public_api_path = os.path.join(project_root, 'public', 'api', 'stats.json')

    existing_stats = load_json(json_path)

    events_count = 34
    if os.path.exists(events_json_path):
        try:
            with open(events_json_path, 'r', encoding='utf-8') as f:
                events_list = json.load(f)
                events_count = len(events_list)
        except Exception:
            pass

    year = str(datetime.datetime.now().year)

    try:
        url = f"https://ctftime.org/api/v1/teams/{TEAM_ID}/"
        data = fetch_json_with_retry(url)
        rating_data = data.get('rating', {}).get(year, {})

        global_rank = rating_data.get('rating_place', existing_stats.get('globalRank', 63))
        rating_points = round(float(rating_data.get('rating_points', existing_stats.get('ratingPoints', 403.96))), 3)
        country_rank = rating_data.get('country_place', existing_stats.get('countryRank', 8))

        new_stats = {
            'globalRank': global_rank,
            'countryRank': country_rank,
            'ratingPoints': rating_points,
            'eventsPlayed': events_count
        }

        save_json(json_path, new_stats)
        generate_ts(ts_path)

        public_stats = {
            'team': 'idktheflag',
            'ctftimeId': int(TEAM_ID),
            'globalRank': global_rank,
            'countryRank': country_rank,
            'ratingPoints': rating_points,
            'eventsPlayed': events_count,
            'lastUpdated': datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')
        }
        save_json(public_api_path, public_stats)

        print(f"Successfully updated team stats in {json_path} and {public_api_path}")
    except Exception as err:
        print(f"Warning: Failed to update stats from CTFtime: {err}")
        if not os.path.exists(json_path):
            fallback_stats = {
                'globalRank': 63,
                'countryRank': 8,
                'ratingPoints': 403.96,
                'eventsPlayed': events_count
            }
            save_json(json_path, fallback_stats)
            generate_ts(ts_path)

if __name__ == '__main__':
    main()

