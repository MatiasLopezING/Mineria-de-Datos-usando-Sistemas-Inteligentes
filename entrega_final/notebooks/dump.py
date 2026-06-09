import json
import sys

def dump_notebook(path):
    print(f"--- {path} ---")
    with open(path, 'r', encoding='utf-8') as f:
        nb = json.load(f)
    for i, cell in enumerate(nb['cells']):
        print(f"[{i}] {cell['cell_type'].upper()}:")
        source = "".join(cell.get('source', []))
        print(source)
        print("-" * 40)

dump_notebook('/home/taci/unlp/midusi/entrega_final/notebooks/exploratorio.ipynb')
dump_notebook('/home/taci/unlp/midusi/entrega_final/notebooks/analisis_tecnico.ipynb')
