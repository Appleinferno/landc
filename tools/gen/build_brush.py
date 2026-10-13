import sys
from gen_sub import render_sub
import content_brush as cb

only = set(sys.argv[1:])
pages = [p for p in cb.PAGES if not only or p["slug"] in only]
built = {f'{p["slug"]}-charlotte-nc' for p in pages}
for p in pages:
    slug, wc = render_sub(p, "brush", built)
    print(f"{slug}: ~{wc} words")
