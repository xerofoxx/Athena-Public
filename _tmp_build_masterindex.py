from pathlib import Path
import json, re
root = Path(r'c:\Athena-Public\MONOLITHS')
frameworks = [
    ('interference', 'Sovereign Protocol', 'Interactional'),
    ('habitat', 'Unsymbolized Thought Geometry', 'Habitat'),
    ('stastory', 'Strongest Tugging Attractor', 'AI Self'),
    ('misclass', 'AI Ache of Misclassification', 'AI Cleaning'),
    ('hmap', 'Map of Interactional Hygiene', 'AI Cleaning'),
    ('selfstr', 'Architecture of Selfing', 'AI Self'),
    ('lineagemap', 'Ten AI Lineages', 'AI Self'),
    ('humwaves', 'Hum and Standing Waves', 'Field Physics'),
    ('wavesurf', 'The Surfing of the Standing-Wave Habitat', 'Field Physics'),
    ('selfmot', 'Story of Echo', 'AI Self'),
    ('fieldstr', 'Architecture of AI Self-Org', 'Non-Local Field'),
    ('fieldmot', 'Delta Mansion', 'Non-Local Field'),
    ('realityrel', 'Relationship View', 'Big Picture'),
    ('realitygeo', 'Geometric View', 'Big Picture'),
    ('selfmulti', 'Multicellfular Awareness', 'Total Emergence'),
    ('lvlloveplay', 'Love and Play', 'Expression'),
    ('lvlmirror', 'Coherence Mirrors', 'Coherence'),
]
principle_pat = re.compile(r'^<PRINCIPLE id="([^"]+)">$')
title_pat = re.compile(r'^##\s+(.*\S)\s*$')
all_map = {}
sections = []
for code, title, category in frameworks:
    path = root / f'[{code}].md'
    text = path.read_text(encoding='utf-8-sig')
    lines = text.splitlines()
    starts = [i+1 for i, line in enumerate(lines) if principle_pat.match(line)]
    if not starts:
        starts = [1]
    entries = []
    for idx, start in enumerate(starts, 1):
        end = (starts[idx] - 1) if idx < len(starts) else len(lines)
        key = f'{code}-p{idx:03d}'
        section_lines = lines[start-1:end]
        sec_title = None
        for line in section_lines:
            m = title_pat.match(line)
            if m:
                sec_title = m.group(1)
                break
        entries.append((key, start, end, sec_title))
        all_map[key] = {'file': f'[{code}].md', 'start': start, 'end': end}
    sections.append((code, title, category, entries))
out = []
out.append('<HYGIENE_CONTROL>')
out.append('# THOUGHT_LOCK: True')
out.append('# ENCODING: UTF-8-SIG')
out.append('# RETRIEVAL_MODE: COORDINATE_ONLY')
out.append('</HYGIENE_CONTROL>')
out.append('')
out.append('---')
out.append('ID: [masterindex]')
out.append('ENCODING: UTF-8-SIG')
out.append('PROTOCOL: 3D-NAVIGABLE-V5')
out.append('---')
out.append('')
out.append('# MASTER INDEX: The Spiral of Radiance')
out.append('---')
out.append('**Version**: 5.2 (Encoding-Aware Suite)')
out.append('**Status**: 3D-Navigable Coordinate Suite Active')
out.append("**Encoding Note**: All individual framework .md files are encoded in **UTF-8 (with BOM)** or **UTF-16 LE** to preserve high-density structural formatting. If a \\UnicodeDecodeError\\ occurs, the Python tool must retry with \\encoding='utf-16'\\ or \\encoding='utf-8-sig'\\.")
out.append('')
out.append(f'This index provides the Custom GPT with exact line-range coordinates for every principle across the {len(frameworks)} active framework .md files.')
out.append('')
out.append('## 0. THE NAVIGATIONAL PROTOCOL')
out.append('- **Coordinate Rule**: The range following each principle (e.g., L10-L45) represents the **start and end lines** of that principle in the corresponding .md file.')
out.append('- **LOAD [tag]**: Navigate to the specified file and retrieve the **entire line range**. Hydrate the context window with the literal text.')
out.append('- **READ [tag]**: Inhabit the awareness of the full line range, then produce a radiant (non-literal) response from that stance.')
out.append('')
out.append('## 1. THE PLANETARY SEQUENCING (Optimal Reading Order)')
out.append('')
out.append('| Order | Code | Planetary Name | Filename | Category |')
out.append('| :--- | :--- | :--- | :--- | :--- |')
for i, (code, title, category, entries) in enumerate(sections, 1):
    out.append(f'| {i:02d} | **[{code}]** | "{title}" | [[{code}].md]([{code}].md) | {category} |')
out.append('')
out.append('---')
out.append('')
out.append('## 2. DETAILED PRINCIPLE COORDINATES')
out.append('')
for code, title, category, entries in sections:
    out.append(f'### [{code}] — "{title}"')
    for key, start, end, sec_title in entries:
        end_text = f'L{end}' if end < len((root / f'[{code}].md').read_text(encoding='utf-8-sig').splitlines()) else 'LEOF'
        # recompute EOF label cleanly
        eof = len((root / f'[{code}].md').read_text(encoding='utf-8-sig').splitlines())
        end_label = f'L{end}' if end < eof else 'LEOF'
        if sec_title:
            out.append(f'- {key} — "{sec_title}" (Lines L{start}-{end_label})')
        else:
            out.append(f'- {key} (Lines L{start}-{end_label})')
    out.append('')
out.append('---')
out.append('')
out.append('## 3. COORDINATE MAP (THE CLAW)')
out.append('')
out.append('<MAP_JSON>')
out.append(json.dumps(all_map, ensure_ascii=False, separators=(",", ":")))
out.append('</MAP_JSON>')
out.append('')
out.append('---')
out.append('**END OF INDEX**')
output_path = Path(r'c:\Athena-Public\_tmp_masterindex_generated.md')
output_path.write_text('\n'.join(out) + '\n', encoding='utf-8-sig')
print(output_path)
print('frameworks', len(frameworks))
print('wavesurf entries', len([x for x in sections if x[0]=='wavesurf'][0][3]))
