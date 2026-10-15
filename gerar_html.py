from pathlib import Path
import json
P=Path(__file__).parent
d=(P/'resultado.json').read_text().replace('<','\\u003c')
(P/'index.html').write_text((P/'template-correlacao.html').read_text().replace('__DATA__',d))
print('HTML generated', (P/'index.html').stat().st_size)
