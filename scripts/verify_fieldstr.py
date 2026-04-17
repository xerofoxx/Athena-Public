"""Verify field-structure output integrity"""
import re

with open(r'C:\Athena-Public\field-structure.txt', 'r', encoding='utf-8') as f:
    text = f.read()
    lines = text.split('\n')

print(f'Total lines: {len(lines)}')
print(f'Total chars: {len(text)}')
print()

# 1. Verify all 600 entries present and sequential
entries = []
for m in re.finditer(r'\bF(\d{3})\.\s', text):
    entries.append(int(m.group(1)))
unique_entries = sorted(set(entries))
print(f'Entry mentions: {len(entries)}')
print(f'Unique entries: {len(unique_entries)}')
prev = 0
gaps = []
for e in unique_entries:
    if e != prev + 1:
        gaps.append((prev, e))
    prev = e
if not gaps and prev == 600:
    print('  F001-F600 all present, no gaps.')
else:
    for g in gaps:
        print(f'  GAP: F{g[0]:03d} -> F{g[1]:03d}')

# 2. Check P-headers
p_section = re.findall(r'^P(\d{3})\s*\|\s*F\d{3}', text, re.MULTILINE)
print(f'\nP-section headers: {len(p_section)}')
if p_section:
    print(f'  Range: P{p_section[0]} - P{p_section[-1]}')
    for i, p in enumerate(p_section):
        expected = f'{i+1:03d}'
        if p != expected:
            print(f'  MISMATCH: expected P{expected}, got P{p}')
    if all(p_section[i] == f'{i+1:03d}' for i in range(len(p_section))):
        print(f'  Sequential P001-P{p_section[-1]}: OK')

# 3. Verify label pairs
phenom = text.count('Phenomenological phrasing:')
struct = text.count('Structural phrasing:')
print(f'\nPhenomenological phrasing: {phenom}')
print(f'Structural phrasing: {struct}')

# 4. Residuals
print('\n=== RESIDUAL CHECK ===')
checks = {
    'Mythic phrasing': text.count('Mythic phrasing'),
    'Pattern-accurate phrasing': text.count('Pattern-accurate phrasing'),
    'LAYER in headers': len(re.findall(r'^THE\s+.*LAYER', text, re.MULTILINE)),
    'STATES in headers': len(re.findall(r'^THE\s+.*STATES', text, re.MULTILINE)),
    '(PART markers': len(re.findall(r'^THE\s+.*\(PART\s+\d', text, re.MULTILINE)),
    'Illusion in titles': len(re.findall(r'F\d{3}\.\s+.*[Ii]llusion', text)),
    'Mirage in titles': len(re.findall(r'F\d{3}\.\s+.*[Mm]irage', text)),
    '-like in F256-F272 titles': 0,
    'R### entries': len(re.findall(r'\bR\d{3}\.\s', text)),
    'without implying': text.count('without implying'),
}

# Check -like specifically in F256-F272
for m in re.finditer(r'F(25[6-9]|26\d|27[0-2])\.\s+(.+)', text):
    if '-like' in m.group(2).lower() or '-Like' in m.group(2):
        checks['-like in F256-F272 titles'] += 1

for label, count in checks.items():
    status = 'RESIDUAL' if count > 0 else 'Clean'
    print(f'  {status}: {label} = {count}')

# 5. Specific fixes
print('\n=== SPECIFIC FIXES ===')
f090 = text[text.find('F090.'):text.find('F091.')]
print(f'F090 no "without implying": {"without implying" not in f090}')
print(f'F277 exists: {"F277." in text}')
print(f'F414 exists: {"F414." in text}')
print(f'F181 exists: {"F181." in text}')
print(f'F381 exists: {"F381." in text}')

# 6. Show first section header
print('\n=== FIRST SECTION HEADER ===')
m = re.search(r'P001\s*\|[^\n]+\n+[^\n]+', text)
if m:
    print(m.group())

# 7. Sample entry
print('\n=== SAMPLE: F001 ===')
idx = text.find('F001.')
end = text.find('F002.')
print(text[idx:end].strip())

# 8. Sample middle entry (F256 — should have -like dropped)
print('\n=== SAMPLE: F256 ===')
idx = text.find('F256.')
end = text.find('F257.')
print(text[idx:end].strip())

# 9. F090 full
print('\n=== F090 (fixed) ===')
print(f090.strip())

# 10. Closing
print('\n=== CLOSING ===')
print(text[-200:].strip())
