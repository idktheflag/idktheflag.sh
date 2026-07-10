import urllib.request
import re
import os

def fetch_html(url):
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    with urllib.request.urlopen(req) as res:
        return res.read().decode('utf-8')

def main():
    url = "https://ctftime.org/team/419270"
    try:
        html = fetch_html(url)
    except Exception as e:
        print(f"Error: {e}")
        return

    pane_match = re.search(r'<div class="tab-pane[^"]*" id="rating_2026">(.*?)(?:<div class="tab-pane|<h3>Team members|</body>|$)', html, re.DOTALL)
    if not pane_match:
        return
    pane_content = pane_match.group(1)

    rating_match = re.search(r"Overall rating place:\s*<b>\s*(\d+)\s*</b>\s*with\s*<b>\s*([\d.]+)\s*</b>\s*pts", pane_content, re.DOTALL | re.IGNORECASE)
    if not rating_match:
        return

    global_rank = int(rating_match.group(1))
    rating_points = float(rating_match.group(2))

    events_played = len(re.findall(r'<td class="place(?:"|\s)', pane_content))

    d = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(d) if os.path.basename(d) == 'updates' else d
    stats_file = os.path.join(project_root, 'src', 'data', 'stats.ts')

    content = f"""export const teamStats = {{
  globalRank: {global_rank},
  countryRank: 12,
  ratingPoints: {rating_points},
  eventsPlayed: {events_played},
}};
"""
    try:
        os.makedirs(os.path.dirname(stats_file), exist_ok=True)
        with open(stats_file, 'w', encoding='utf-8') as f:
            f.write(content)
    except Exception as e:
        print(f"Error: {e}")

if __name__ == '__main__':
    main()
