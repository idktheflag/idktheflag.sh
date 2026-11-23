import urllib.request
import json
import re
import os
import html as html_module

def fetch_html(url):
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    with urllib.request.urlopen(req) as res:
        return res.read().decode('utf-8')

def fetch_json(url):
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    with urllib.request.urlopen(req) as res:
        return json.loads(res.read().decode('utf-8'))

def parse_existing_events(path):
    if not os.path.exists(path):
        return {}
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()
    pattern = re.compile(r"\{\s*name:\s*'([^']*)',\s*date:\s*'([^']*)',\s*place:\s*(\d+),\s*points:\s*([\d.]+),\s*rating:\s*([\d.]+)\s*\}")
    return {m[0]: {'name': m[0], 'date': m[1], 'place': int(m[2]), 'points': float(m[3]), 'rating': float(m[4])} for m in pattern.findall(content)}

def main():
    d = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(d) if os.path.basename(d) == 'updates' else d
    path = os.path.join(project_root, 'src', 'data', 'events.ts')
    existing = parse_existing_events(path)

    html_doc = fetch_html("https://ctftime.org/team/419270")
    pane_match = re.search(r'<div class="tab-pane[^"]*" id="rating_2026">(.*?)(?:<div class="tab-pane|<h3>Team members|</body>|$)', html_doc, re.DOTALL)
    pane_content = pane_match.group(1)

    rows = re.findall(r'<tr>(.*?)</tr>', pane_content, re.DOTALL)[1:]
    updated_events = []
    for tr in rows:
        cols = re.findall(r'<td[^>]*>(.*?)</td>', tr, re.DOTALL)
        if len(cols) >= 5:
            place = int(re.sub(r'<[^>]+>', '', cols[1]).strip())
            eid_m = re.search(r'/event/(\d+)', cols[2])
            eid = int(eid_m.group(1)) if eid_m else None
            name = html_module.unescape(re.sub(r'<[^>]+>', '', cols[2]).strip()).replace("'", "")
            pts = float(re.sub(r'<[^>]+>', '', cols[3]).strip())
            rtg = float(re.sub(r'<[^>]+>', '', cols[4]).strip())

            date = existing.get(name, {}).get('date')
            if not date and eid:
                details = fetch_json(f"https://ctftime.org/api/v1/events/{eid}/")
                date = details.get('start', '').split('T')[0] or "2026-01-01"

            updated_events.append({
                'name': name,
                'date': date or "2026-01-01",
                'place': place,
                'points': pts,
                'rating': rtg
            })

    final = sorted(updated_events, key=lambda x: (x['date'], x['name']))
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

    root_events_path = os.path.join(project_root, 'events.ts')
    if os.path.exists(root_events_path):
        with open(root_events_path, 'w', encoding='utf-8') as f:
            f.write('\n'.join(lines))

if __name__ == '__main__':
    main()
