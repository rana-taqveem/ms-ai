import json

with open('621/assignment_01/25280030.ipynb', 'r', encoding='utf-8') as f:
    nb = json.load(f)

print(f"Total cells: {len(nb['cells'])}\n")

for i, cell in enumerate(nb['cells']):
    ctype = cell['cell_type']
    source = ''.join(cell['source'])
    print(f"=== Cell {i} ({ctype}) ===")
    print(source)
    print()
