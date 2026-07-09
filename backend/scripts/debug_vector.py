import tempfile
from pathlib import Path
import json
from app.knowledge.index_builder import IndexBuilder

tmp = Path(tempfile.mkdtemp())
proj = tmp / 'proj'
proj.mkdir()
(f:=proj/'a.py').write_text('''def foo():\n    return 1\n''')
print('proj', proj)
builder = IndexBuilder(proj)
res = builder.build(force=True)
print('build res:', res)
vec_path = proj / 'knowledge' / 'chunk_vectors.json'
print('vec exists', vec_path.exists())
if vec_path.exists():
    print(json.dumps(json.load(open(vec_path)), indent=2))
else:
    print('no vec file')
print('In-memory vectors count', len(builder.vector_store.vectors))
print('In-memory meta keys:', list(builder.vector_store.meta.keys()))
