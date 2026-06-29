import urllib.request
import re
import os
import sys

def get_event_date(event_url):
    req = urllib.request.Request(event_url, headers={'User-Agent': 'Mozilla/5.0'})
    with urllib.request.urlopen(req) as response:
        html = response.read().decode('utf-8')
    date_match = re.search(r'(\w+),\s+(\d{1,2})\s+([A-Za-z.]+)\s+(\d{4}),\s+\d{2}:\d{2}', html)
    if date_match:
        day_str = date_match.group(2)
        month_str = date_match.group(3)
        year_str = date_match.group(4)
        months_map = {
            'jan': '01', 'feb': '02', 'mar': '03', 'apr': '04',
            'may': '05', 'jun': '06', 'jul': '07', 'aug': '08',
            'sep': '09', 'oct': '10', 'nov': '11', 'dec': '12'
        }
        m_key = month_str.replace('.', '').strip()[:3].lower()
        month = months_map.get(m_key, '01')
        day = int(day_str)
        return f"{year_str}-{month}-{day:02d}"
    return None

def main():
    url = "https://ctftime.org/team/419270"
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    with urllib.request.urlopen(req) as response:
        html = response.read().decode('utf-8')
    tab_start = html.find('id="rating_')
    start = html.find('<table class="table table-striped">', tab_start)
    end = html.find('</table>', start)
    table_html = html[start:end]
    row_pattern = re.compile(r'<tr[^>]*>(.*?)</tr>', re.DOTALL | re.IGNORECASE)
    td_pattern = re.compile(r'<td[^>]*>(.*?)</td>', re.DOTALL | re.IGNORECASE)
    tag_pattern = re.compile(r'<[^>]+>')
    events = []
    for row in row_pattern.findall(table_html):
        tds = td_pattern.findall(row)
        if len(tds) >= 5:
            place_str = tag_pattern.sub('', tds[1]).strip()
            m_place = re.search(r'\d+', place_str)
            place = int(m_place.group(0)) if m_place else 0
            name = tag_pattern.sub('', tds[2]).strip()
            if not name:
                continue
            points_str = tag_pattern.sub('', tds[3]).strip()
            rating_str = tag_pattern.sub('', tds[4]).strip()
            event_path = ""
            href_match = re.search(r'href=["\'](/event/\d+)["\']', tds[2])
            if href_match:
                event_path = href_match.group(1)
            pts_match = re.search(r'[-+]?\d*\.\d+|\d+', points_str)
            rtg_match = re.search(r'[-+]?\d*\.\d+|\d+', rating_str)
            points = float(pts_match.group(0)) if pts_match else 0.0
            rating = float(rtg_match.group(0)) if rtg_match else 0.0
            events.append({
                'name': name,
                'place': place,
                'points': points,
                'rating': rating,
                'event_path': event_path
            })
    events.reverse()
    for e in events:
        date = None
        if e['event_path']:
            event_url = "https://ctftime.org" + e['event_path']
            date = get_event_date(event_url)
        e['date'] = date or '2026-01-01'
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
    for e in events:
        pts = int(e['points']) if e['points'].is_integer() else e['points']
        rtg = int(e['rating']) if e['rating'].is_integer() else e['rating']
        lines.append(f"  {{ name: '{e['name']}', date: '{e['date']}', place: {e['place']}, points: {pts}, rating: {rtg} }},")
    lines.append("];")
    if len(sys.argv) > 1:
        events_ts_path = sys.argv[1]
    else:
        script_dir = os.path.dirname(os.path.abspath(__file__))
        candidate_dir = os.path.join(script_dir, 'src', 'data')
        if os.path.isdir(candidate_dir):
            events_ts_path = os.path.join(candidate_dir, 'events.ts')
        else:
            events_ts_path = os.path.join(script_dir, 'events.ts')

    output_dir = os.path.dirname(os.path.abspath(events_ts_path))
    if output_dir:
        os.makedirs(output_dir, exist_ok=True)

    with open(events_ts_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines))

if __name__ == '__main__':
    main()
