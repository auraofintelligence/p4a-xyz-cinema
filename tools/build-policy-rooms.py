"""Publish reviewed room HTML from content/rooms, preserving the shared chrome."""
from pathlib import Path
import sys
from web_link_policy import external_links

ROOT = Path(__file__).resolve().parents[1]
for source in sorted((ROOT / 'content/rooms').glob('*.html')):
    if len(sys.argv) > 1 and source.stem not in sys.argv[1:]:
        continue
    (ROOT / 'pages' / source.name).write_text(external_links(source.read_text(encoding='utf-8')), encoding='utf-8')
    print('Published', source.name)
