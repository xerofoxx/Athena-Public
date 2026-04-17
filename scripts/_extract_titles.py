import re, os

files = ['interference','stastory','misclass','selfstr','selfmot','lineagemap',
         'hmap','fieldstr','fieldmot','realityrel','habitat','humwaves',
         'wavesurf','selfmulti','lvlloveplay','lvlmirror','lvlselfhome','realitygeo']
base = r'c:\Athena-Public\MONOLITHS'

for f in files:
    path = os.path.join(base, f'[{f}].md')
    try:
        with open(path, encoding='utf-8-sig') as fh:
            text = fh.read()
    except:
        with open(path, encoding='utf-16') as fh:
            text = fh.read()
    lines = text.split('\n')
    print(f'### [{f}]')
    for i, line in enumerate(lines):
        m = re.match(r'<PRINCIPLE id="(.+?)">', line)
        if m:
            pid = m.group(1)
            for j in range(i+1, min(i+6, len(lines))):
                m2 = re.match(r'^## (.+)', lines[j])
                if m2:
                    title = m2.group(1).strip()
                    print(f'- {pid}: {title}')
                    break
    print()
