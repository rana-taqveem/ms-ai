import json
import sys

with open('621/assignment_01/main.ipynb', 'r', encoding='utf-8') as f:
    nb = json.load(f)

print(f"Total cells: {len(nb['cells'])}\n")

# Extract markdown cells for requirements
markdown_cells = [c for c in nb['cells'] if c['cell_type'] == 'markdown']
code_cells = [c for c in nb['cells'] if c['cell_type'] == 'code']

print(f"Markdown cells: {len(markdown_cells)}")
print(f"Code cells: {len(code_cells)}\n")

# Print first few markdown cells to understand structure
print("=" * 80)
print("FIRST 10 MARKDOWN CELLS (Requirements/Documentation):")
print("=" * 80)
for i, cell in enumerate(markdown_cells[:10]):
    content = ''.join(cell['source'])
    print(f"\n--- Cell {i} ---")
    print(content[:500])  # First 500 chars
    if len(content) > 500:
        print("...")
