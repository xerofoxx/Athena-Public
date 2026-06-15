#!/usr/bin/env python3
"""
Generate a StepMania .sm chart for deadmau5 — Quezacotl

Progressive house at 129 BPM, 7:12 duration.
Chart philosophy: repeating motifs that build in complexity,
"interference patterns" where earlier themes return decorated,
difficult yet effortless flowing gait.
"""
import os

# ── SM note-row constants (columns: Left Down Up Right) ──
L  = '1000'; D  = '0100'; U  = '0010'; R  = '0001'; E  = '0000'
LR = '1001'; DU = '0110'; LD = '1100'; RU = '0011'; LU = '1010'; RD = '0101'

# ── Helpers ──
def shares(a, b):
    return any(a[i] == '1' and b[i] == '1' for i in range(4))

def last_active(measure):
    for row in reversed(measure):
        if row != E:
            return row
    return E

def first_active(measure):
    for row in measure:
        if row != E:
            return row
    return E

def safe_chain(pool, count, start_after=None):
    result = []
    prev_end = start_after
    idx = 0
    for _ in range(count):
        found = False
        for offset in range(len(pool)):
            candidate = pool[(idx + offset) % len(pool)]
            fa = first_active(candidate)
            if prev_end is None or fa == E or not shares(prev_end, fa):
                result.append(candidate)
                la = last_active(candidate)
                if la != E:
                    prev_end = la
                idx = (idx + offset + 1) % len(pool)
                found = True
                break
        if not found:
            result.append([E] * len(pool[0]))
            prev_end = E
    return result

def validate_chain(measures, label=""):
    issues = 0
    for i in range(len(measures) - 1):
        la = last_active(measures[i])
        fa = first_active(measures[i + 1])
        if la != E and fa != E and shares(la, fa):
            issues += 1
            if issues <= 5:
                print(f"  JACK at measure {i+1}->{i+2}: {la} -> {fa}  [{label}]")
    if issues:
        print(f"  Total jacks in {label}: {issues}")
    else:
        print(f"  {label}: No jacks ✓")
    return issues

# ── Song parameters ──
BPM = 129.0
SONG_LENGTH = 432.14  # seconds
OFFSET = -0.100       # small offset, first downbeat ~0.1s in
SAMPLE_START = 120.0   # preview starts at 2:00 (drop section)

# Measures: 4 beats each. At 129 BPM, 1 measure ≈ 1.86s
# Total measures ≈ 432 / 1.86 ≈ 232
TOTAL_MEASURES = 232

rest8 = [E] * 8   # 8th-note empty measure
rest4 = [E] * 4   # quarter-note empty measure

# ═══════════════════════════════════════════════════════════
# MOTIF SYSTEM — The DNA of the chart
#
# Core Motif "Serpent" (Quezacotl = feathered serpent):
#   A flowing staircase that winds L→D→U→R then reverses.
#   This is the seed. Every section uses transformations of it.
# ═══════════════════════════════════════════════════════════

# -- MOTIF A: The Serpent (ascending spiral) --
motA = [L, D, U, R, L, D, U, R]   # L→R (ends R)
# -- MOTIF B: Serpent reversed (descending spiral) --
motB = [R, U, D, L, R, U, D, L]   # R→L (ends L)
# -- MOTIF C: Serpent widened (cross-panel) --
motC = [L, U, D, R, L, U, D, R]   # L→R
# -- MOTIF D: Serpent narrowed (adjacent-panel) --
motD = [D, L, R, U, D, L, R, U]   # D→U (ends U)
# -- MOTIF E: Mirror serpent --
motE = [R, D, U, L, R, D, U, L]   # R→L (ends L)
# -- MOTIF F: Counter-serpent --
motF = [U, R, L, D, U, R, L, D]   # U→D (ends D)

# -- Interference patterns: motifs with jump accents --
# (jumps at phrase boundaries = beat emphasis matching kick drum)
intA = [DU, L, D, R, U, L, D, R]  # DU start → R end
intB = [LR, U, D, L, R, U, D, L]  # LR start → L end  
intC = [L, D, U, R, L, D, U, DU]  # stream → DU end
intD = [R, U, D, L, R, U, D, LR]  # stream → LR end
intE = [DU, R, U, D, L, R, U, L]  # DU start → L end
intF = [LR, D, L, U, R, D, L, D]  # LR start → D end

# -- Quarter-note versions (intro/breakdown density) --
qA = [L, E, D, E, U, E, R, E]     # Serpent at quarter speed (L→R)
qB = [R, E, U, E, D, E, L, E]     # Reverse serpent quarter (R→L)
qC = [D, E, L, E, R, E, U, E]     # Variant (D→U)
qD = [U, E, R, E, L, E, D, E]     # Variant (U→D)

# -- Half-note versions (very sparse) --
hA = [L, E, E, E, R, E, E, E]     # L...R
hB = [D, E, E, E, U, E, E, E]     # D...U
hC = [R, E, E, E, L, E, E, E]     # R...L
hD = [U, E, E, E, D, E, E, E]     # U...D

# -- Build patterns (quarter→8th transition) --
bA = [L, D, E, E, U, R, E, E]     # pair-pair (L→R)
bB = [R, U, E, E, D, L, E, E]     # pair-pair (R→L)
bC = [L, D, U, E, R, L, D, E]     # triple-triple
bD = [R, U, D, E, L, R, U, E]     # triple-triple

# -- Decorated motifs (patterns + off-beat accents for peak sections) --
# 16th-note resolution: 16 rows per measure
def motif_16th(base_8, decoration_positions):
    """Expand an 8-row motif to 16 rows with decorations between beats."""
    result = []
    for i, note in enumerate(base_8):
        result.append(note)
        if i in decoration_positions and note != E:
            # Add a tap on a non-conflicting panel
            panels = [j for j in range(4) if note[j] == '0']
            if panels:
                deco = ['0'] * 4
                deco[panels[0]] = '1'
                result.append(''.join(deco))
            else:
                result.append(E)
        else:
            result.append(E)
    return result

# Pre-built 16th-note decorated motifs for peak sections
peakA = motif_16th(motA, [1, 3, 5, 7])  # Full decoration
peakB = motif_16th(motB, [1, 3, 5, 7])
peakC = motif_16th(motA, [1, 5])         # Light decoration
peakD = motif_16th(motB, [3, 7])

# ═══════════════════════════════════════════════════════════
# PROGRESSIVE HOUSE SONG STRUCTURE
#
# 129 BPM, 4/4, ~232 measures total
#
# Intro        (m1-32)    : Atmospheric, sparse → quarter notes
# Build A      (m33-48)   : Quarter → 8th transition, motif introduced
# Drop A       (m49-80)   : Full 8th streams, core serpent flowing
# Breakdown A  (m81-96)   : Sparse again, motif echoes at quarter speed
# Build B      (m97-112)  : Motifs with jump accents (interference)
# Drop B/Peak  (m113-160) : Maximum density, decorated motifs, 16th accents
# Breakdown B  (m161-176) : Breathing space, motif fragments
# Build C      (m177-192) : Final tension, all motif variants
# Drop C/Final (m193-224) : Triumphant return, motifs layered
# Outro        (m225-232) : Fade, last serpent echo
# ═══════════════════════════════════════════════════════════

def gen_expert():
    ms = []
    prev = E
    
    # ── INTRO (m1-32): Atmospheric sparse notes ──
    # First 8 measures: silence (atmospheric pad intro)
    ms.extend([rest8] * 8)
    # m9-16: Half notes, the serpent's first whisper
    half_pool = [hA, hB, hC, hD]
    chunk = safe_chain(half_pool, 8, start_after=prev)
    ms.extend(chunk)
    prev = last_active(chunk[-1])
    # m17-24: Quarter notes, serpent takes shape
    q_pool = [qA, qC, qD, qB]
    chunk = safe_chain(q_pool, 8, start_after=prev)
    ms.extend(chunk)
    prev = last_active(chunk[-1])
    # m25-32: Quarters getting denser, building anticipation
    chunk = safe_chain([qA, qB, qC, qD], 8, start_after=prev)
    ms.extend(chunk)
    prev = last_active(chunk[-1])
    # 32 measures ✓
    
    # ── BUILD A (m33-48): Quarter → 8th transition ──
    # m33-36: Build patterns (pair-pair)
    build_pool = [bA, bB, bC, bD]
    chunk = safe_chain(build_pool, 4, start_after=prev)
    ms.extend(chunk)
    prev = last_active(chunk[-1])
    # m37-40: Build + first full motif appearances
    chunk = safe_chain([bC, bD, motA, motB], 4, start_after=prev)
    ms.extend(chunk)
    prev = last_active(chunk[-1])
    # m41-48: Full 8th note motifs, the serpent emerges
    stream_pool = [motA, motB, motC, motD, motE, motF]
    chunk = safe_chain(stream_pool, 8, start_after=prev)
    ms.extend(chunk)
    prev = last_active(chunk[-1])
    # 48 measures ✓

    # ── DROP A (m49-80): Core serpent flowing ──
    # 32 measures of clean 8th-note streams
    # Every 8 measures, the motif palette rotates slightly
    for phrase in range(4):
        # Rotate which motifs are primary
        rotated = stream_pool[phrase:] + stream_pool[:phrase]
        chunk = safe_chain(rotated, 8, start_after=prev)
        ms.extend(chunk)
        prev = last_active(chunk[-1])
    # 80 measures ✓

    # ── BREAKDOWN A (m81-96): Sparse motif echoes ──
    # m81-84: Sudden drop to half notes
    chunk = safe_chain(half_pool, 4, start_after=prev)
    ms.extend(chunk)
    prev = last_active(chunk[-1])
    # m85-88: Quarter-note serpent echoes (recognizable!)
    chunk = safe_chain(q_pool, 4, start_after=prev)
    ms.extend(chunk)
    prev = last_active(chunk[-1])
    # m89-92: Quarter with occasional 8th pairs
    chunk = safe_chain([qA, bA, qB, bB], 4, start_after=prev)
    ms.extend(chunk)
    prev = last_active(chunk[-1])
    # m93-96: Building back up
    chunk = safe_chain(build_pool, 4, start_after=prev)
    ms.extend(chunk)
    prev = last_active(chunk[-1])
    # 96 measures ✓

    # ── BUILD B (m97-112): Interference patterns ──
    # The serpent returns but now with jump accents at phrase boundaries
    int_pool = [intA, intC, intE, intB, intD, intF]
    mixed_pool = [motA, intC, motB, intD, motC, intE, motD, intF]
    # m97-104: Alternating clean and accented
    chunk = safe_chain(mixed_pool, 8, start_after=prev)
    ms.extend(chunk)
    prev = last_active(chunk[-1])
    # m105-112: Full interference patterns
    chunk = safe_chain(int_pool, 8, start_after=prev)
    ms.extend(chunk)
    prev = last_active(chunk[-1])
    # 112 measures ✓

    # ── DROP B / PEAK (m113-160): Maximum density ──
    # 48 measures — this is where the song peaks
    # Mix of 8th streams and 16th-note decorated measures
    # The 16th measures use 16 rows (finer resolution)
    
    # For simplicity in the SM format, we'll use 8th-note measures
    # but with jump accents creating the perception of density
    
    # Peak pool: interference + stream motifs cycling
    peak_pool = [motA, intC, motE, intD, motB, intA, motF, intB,
                 motC, intE, motD, intF, motA, intC, motB, intD]
    
    for phrase in range(6):  # 6 x 8 = 48 measures
        rotated = peak_pool[phrase*2:] + peak_pool[:phrase*2]
        chunk = safe_chain(rotated, 8, start_after=prev)
        ms.extend(chunk)
        prev = last_active(chunk[-1])
    # 160 measures ✓

    # ── BREAKDOWN B (m161-176): Breathing space ──
    # m161-164: Sudden sparse — just quarter serpent
    chunk = safe_chain(q_pool, 4, start_after=prev)
    ms.extend(chunk)
    prev = last_active(chunk[-1])
    # m165-168: Half notes (the serpent rests)
    chunk = safe_chain(half_pool, 4, start_after=prev)
    ms.extend(chunk)
    prev = last_active(chunk[-1])
    # m169-172: Quarter notes building again
    chunk = safe_chain([qA, qC, qB, qD], 4, start_after=prev)
    ms.extend(chunk)
    prev = last_active(chunk[-1])
    # m173-176: Build patterns
    chunk = safe_chain(build_pool, 4, start_after=prev)
    ms.extend(chunk)
    prev = last_active(chunk[-1])
    # 176 measures ✓

    # ── BUILD C (m177-192): Final tension ──
    # All motif variants appear, building to climax
    all_pool = [motA, motE, motC, motF, motB, motD, intC, intD]
    chunk = safe_chain(all_pool, 16, start_after=prev)
    ms.extend(chunk)
    prev = last_active(chunk[-1])
    # 192 measures ✓

    # ── DROP C / FINAL (m193-224): Triumphant return ──
    # 32 measures — the serpent in full glory
    # Motifs cycle through all variants with interference
    final_pool = [motA, intC, motB, intD, motC, intE, motD, intF,
                  motE, intA, motF, intB, motA, intC, motE, intD]
    for phrase in range(4):  # 4 x 8 = 32
        rotated = final_pool[phrase*3:] + final_pool[:phrase*3]
        chunk = safe_chain(rotated, 8, start_after=prev)
        ms.extend(chunk)
        prev = last_active(chunk[-1])
    # 224 measures ✓

    # ── OUTRO (m225-232): Fade ──
    # m225-226: Last full stream measures
    chunk = safe_chain([motA, motB], 2, start_after=prev)
    ms.extend(chunk)
    prev = last_active(chunk[-1])
    # m227-228: Quarter notes (thinning)
    chunk = safe_chain(q_pool, 2, start_after=prev)
    ms.extend(chunk)
    prev = last_active(chunk[-1])
    # m229-230: Half notes
    chunk = safe_chain(half_pool, 2, start_after=prev)
    ms.extend(chunk)
    prev = last_active(chunk[-1])
    # m231-232: Silence
    ms.extend([rest8, rest8])
    # 232 measures ✓

    while len(ms) < TOTAL_MEASURES:
        ms.append(rest8)
    return ms[:TOTAL_MEASURES]


def gen_difficult():
    """Difficult (8): Streams with breathing gaps, fewer jumps."""
    ms = []
    prev = E
    
    # Intro: 16m silence + 16m sparse
    ms.extend([rest8] * 16)
    chunk = safe_chain([qA, qC, qD, qB], 16, start_after=prev)
    ms.extend(chunk)
    prev = last_active(chunk[-1])
    
    # Build + Drop A (48m): Alternating stream/gap
    stream_pool = [motA, motB, motC, motD, motE, motF]
    gap_pool = [bA, bB, bC, bD]
    for _ in range(12):
        s = safe_chain(stream_pool, 2, start_after=prev)
        ms.extend(s)
        prev = last_active(s[-1])
        g = safe_chain(gap_pool, 2, start_after=prev)
        ms.extend(g)
        prev = last_active(g[-1])
    
    # Breakdown (16m): Quarters
    chunk = safe_chain([qA, qB, qC, qD], 16, start_after=prev)
    ms.extend(chunk)
    prev = last_active(chunk[-1])
    
    # Build B + Drop B (64m): More streams, fewer gaps
    for _ in range(16):
        s = safe_chain(stream_pool, 3, start_after=prev)
        ms.extend(s)
        prev = last_active(s[-1])
        g = safe_chain(gap_pool, 1, start_after=prev)
        ms.extend(g)
        prev = last_active(g[-1])
    
    # Breakdown B (16m): Quarter
    chunk = safe_chain([qA, qC, qB, qD], 16, start_after=prev)
    ms.extend(chunk)
    prev = last_active(chunk[-1])
    
    # Final (32m): Streams
    chunk = safe_chain(stream_pool, 30, start_after=prev)
    ms.extend(chunk)
    prev = last_active(chunk[-1])
    ms.extend([rest8, rest8])
    
    while len(ms) < TOTAL_MEASURES:
        ms.append(rest8)
    return ms[:TOTAL_MEASURES]


def gen_basic():
    """Basic (5): Mostly quarter notes."""
    ms = []
    prev = E
    
    ms.extend([rest4] * 16)
    q_pool = [qA, qC, qD, qB]
    h_pool = [hA, hB, hC, hD]
    
    # Gentle quarter notes throughout
    for section in range(6):
        chunk = safe_chain(q_pool, 24, start_after=prev)
        ms.extend(chunk)
        prev = last_active(chunk[-1])
        # Breathing gaps
        chunk = safe_chain(h_pool, 8, start_after=prev)
        ms.extend(chunk)
        prev = last_active(chunk[-1])
    
    ms.extend([rest4] * 8)
    while len(ms) < TOTAL_MEASURES:
        ms.append(rest4)
    return ms[:TOTAL_MEASURES]


def gen_beginner():
    """Beginner (2): Very sparse."""
    ms = []
    prev = E
    h_pool = [hA, hB, hC, hD]
    
    ms.extend([rest4] * 32)
    
    for i in range(TOTAL_MEASURES - 32):
        if i % 4 == 0:
            chunk = safe_chain(h_pool, 1, start_after=prev)
            ms.extend(chunk)
            prev = last_active(chunk[-1])
        else:
            ms.append(rest4)
            prev = E
    
    while len(ms) < TOTAL_MEASURES:
        ms.append(rest4)
    return ms[:TOTAL_MEASURES]


# ── SM file output ──
def format_notes(measures):
    parts = []
    for meas in measures:
        parts.append('\n'.join(meas))
    return '\n,\n'.join(parts)


def build_sm_file():
    header = f"""\
#TITLE:Quezacotl;
#SUBTITLE:~Effortless Flow Edit~;
#ARTIST:deadmau5;
#TITLETRANSLIT:;
#SUBTITLETRANSLIT:;
#ARTISTTRANSLIT:;
#GENRE:Progressive House;
#CREDIT:AI-crafted flow chart;
#BANNER:Quezacotl-banner.png;
#BACKGROUND:Quezacotl-bg.png;
#LYRICSPATH:;
#CDTITLE:;
#MUSIC:Quezacotl.mp3;
#OFFSET:{OFFSET:.3f};
#SAMPLESTART:{SAMPLE_START:.3f};
#SAMPLELENGTH:15.000;
#SELECTABLE:YES;
#BPMS:0.000={BPM:.3f};
#STOPS:;
#BGCHANGES:;
#FGCHANGES:;
"""

    charts = []

    for name, func, diff_name, meter in [
        ("Beginner", gen_beginner, "Beginner", 2),
        ("Basic", gen_basic, "Easy", 5),
        ("Difficult", gen_difficult, "Medium", 8),
        ("Expert", gen_expert, "Hard", 10),
    ]:
        print(f"Generating {name}...")
        data = func()
        validate_chain(data, name)
        charts.append(f"""
//---------- dance-single - {name} ----------
#NOTES:
     dance-single:
     :
     {diff_name}:
     {meter}:
     0.000,0.000,0.000,0.000,0.000:
{format_notes(data)}
;""")

    return header + '\n'.join(charts) + '\n'


if __name__ == '__main__':
    folder = r'c:\Program Files (x86)\StepMania\Songs\_Dance Dance Challenge\Quezacotl'
    
    sm_content = build_sm_file()
    sm_path = os.path.join(folder, 'Quezacotl.sm')
    with open(sm_path, 'w', encoding='utf-8') as f:
        f.write(sm_content)
    
    print(f"\n✓ Chart written to: {sm_path}")
    print(f"  BPM: {BPM}")
    print(f"  Measures: {TOTAL_MEASURES}")
    print(f"  Size: {len(sm_content):,} bytes")
    print(f"\nOpen StepMania → look for 'Quezacotl ~Effortless Flow Edit~'")
