"""Render the public resource catalog. No network access or credentials required."""
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def render():
    data = json.loads((ROOT / 'data/resources.json').read_text())
    rows = data['resources']
    categories = data['categories']
    assert len({r['repo'] for r in rows}) == len(rows), 'Duplicate repository'
    assert all(r['category'] in {c['id'] for c in categories} for r in rows)
    assert all(r['description'].strip() and r['url'] == 'https://github.com/' + r['repo'] for r in rows)
    lines = ['# Resources', '', 'A categorized collection of my starred GitHub projects, with short English descriptions.', '', '## Contents', '']
    for category in categories:
        count = sum(r['category'] == category['id'] for r in rows)
        slug = re.sub(r'[^a-z0-9 -]', '', category['name'].lower()).replace(' ', '-')
        lines.append(f"- [{category['name']}](#{slug}) ({count})")
    lines += ['', '## About this collection', '', 'Projects are grouped by their primary purpose. Editor-specific extensions stay with their editor; other tools are grouped by what they do rather than how their interface looks.', '', 'The collection is reviewed weekly alongside [my GitHub Stars](https://github.com/stars/tp6gw94). Inclusion is a bookmark, not an endorsement or a guarantee of maintenance, security, or licensing suitability. See each project for its current documentation and license.', '', '<!-- START RESOURCES -->']
    for category in categories:
        lines += ['', '## ' + category['name'], '']
        for row in sorted((r for r in rows if r['category'] == category['id']), key=lambda r: r['repo'].lower()):
            lines.append(f"- [{row['repo']}]({row['url']}) — {row['description']}")
    lines += ['', '<!-- END RESOURCES -->', '', '## Updating', '', 'The catalog data lives in `data/resources.json`. After editing it, run `python3 scripts/build_readme.py` to regenerate this README. The script runs locally and does not require GitHub credentials.', '']
    return '\n'.join(lines)

if __name__ == '__main__':
    (ROOT / 'README.md').write_text(render())
