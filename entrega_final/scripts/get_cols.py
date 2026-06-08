import json

with open('../notebooks/Pfinal.ipynb', 'r', encoding='utf-8') as f:
    nb = json.load(f)

for cell in nb['cells']:
    if cell['cell_type'] == 'code':
        source = "".join(cell['source'])
        if 'eda_wl_clean' in source:
            print("CELL SOURCE:")
            print(source)
            print("="*80)
