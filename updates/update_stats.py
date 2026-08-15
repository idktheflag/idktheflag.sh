import urllib.request
import json
import os
import datetime
import re

def fetch_json(url):
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'})
    with urllib.request.urlopen(req, timeout=15) as res:
        return json.loads(res.read().decode('utf-8'))

def main():
    d = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(d) if os.path.basename(d) == 'updates' else d
    stats_file = os.path.join(project_root, 'src', 'data', 'stats.ts')

    year = str(datetime.datetime.now().year)
    team_id = "419270"

    try:
        data = fetch_json(f"https://ctftime.org/api/v1/teams/{team_id}/")
        rating_data = data.get('rating', {}).get(year, {})
        global_rank = rating_data.get('rating_place', 63)
        rating_points = round(float(rating_data.get('rating_points', 403.96)), 3)
        country_rank = rating_data.get('country_place', 12)

        events_file = os.path.join(project_root, 'src', 'data', 'events.ts')
        events_count = 33
        if os.path.exists(events_file):
            with open(events_file, 'r', encoding='utf-8') as f:
                events_count = len(re.findall(r'name:\s*', f.read()))

        content = f"""export const teamStats = {{
  globalRank: {global_rank},
  countryRank: {country_rank},
  ratingPoints: {rating_points},
  eventsPlayed: {events_count},
}};
"""
        os.makedirs(os.path.dirname(stats_file), exist_ok=True)
        temp_file = stats_file + ".tmp"
        with open(temp_file, 'w', encoding='utf-8') as f:
            f.write(content)
        os.replace(temp_file, stats_file)
    except Exception:
        pass

if __name__ == '__main__':
    main()
