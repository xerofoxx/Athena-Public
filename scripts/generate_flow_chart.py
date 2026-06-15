#!/usr/bin/env python3
"""
Generate a StepMania .sm chart: "MAX 300 (Effortless Flow Edit)"
Inspired by the relentless yet flowing rhythm of MAX 300 (Super-Max-Me Mix).

Creates 4 Single-play difficulties with clean, jack-free streaming patterns
that capture the "difficult yet effortless" feel.
"""
import os, sys, shutil

# ── SM note‑row constants (columns: Left Down Up Right) ──
L  = '1000'; D  = '0100'; U  = '0010'; R  = '0001'; E  = '0000'
LR = '1001'; DU = '0110'; LD = '1100'; RU = '0011'; LU = '1010'; RD = '0101'

# ── Helpers ──
def shares(a, b):
    """True if two note-rows share any active panel (would cause a jack)."""
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

def validate_chain(measures, label=""):
    """Warn about jacks at measure boundaries."""
    issues = 0
    for i in range(len(measures) - 1):
        la = last_active(measures[i])
        fa = first_active(measures[i + 1])
        if la != E and fa != E and shares(la, fa):
            issues += 1
            if issues <= 10:
                print(f"  JACK at measure {i+1}->{i+2}: {la} -> {fa}  [{label}]")
    if issues:
        print(f"  Total jacks in {label}: {issues}")
    else:
        print(f"  {label}: No jacks found ✓")
    return issues

# ── 8th‑note flow patterns (8 rows = 1 measure) ──
# Core staircase flows — the DNA of effortless streaming
fA = [L, D, R, U, L, D, R, U]   # starts L, ends U
fB = [L, U, R, D, L, U, R, D]   # starts L, ends D
fC = [R, U, L, D, R, U, L, D]   # starts R, ends D
fD = [R, D, L, U, R, D, L, U]   # starts R, ends U
fE = [D, R, U, L, D, R, U, L]   # starts D, ends L
fF = [U, L, D, R, U, L, D, R]   # starts U, ends R
fG = [D, L, R, U, D, L, R, U]   # starts D, ends U
fH = [U, R, D, L, U, R, D, L]   # starts U, ends L

# Jump‑accent patterns (DU/LR jumps at phrase boundaries)
# After DU('0110'): next must NOT start D or U → use fA(L),fB(L),fC(R),fD(R)
# After LR('1001'): next must NOT start L or R → use fE(D),fF(U),fG(D),fH(U)
jA = [DU, L, D, R, U, L, D, R]  # DU start → ends R
jB = [LR, D, U, L, R, D, U, L]  # LR start → ends L
jC = [L, D, R, U, L, D, R, DU]  # stream → DU end
jD = [R, U, L, D, R, U, L, LR]  # stream → LR end
jE = [DU, R, U, L, D, R, U, L]  # DU start → ends L
jF = [LR, U, D, L, R, U, D, L]  # LR start → ends L  (actually wait)

# Quarter‑note builds (8 rows with empties)
# Ordered so default chain qA→qC→qD→qB is jack-free
qA = [L, E, D, E, R, E, U, E]   # starts L, ends U
qC = [D, E, L, E, U, E, R, E]   # starts D, ends R
qD = [U, E, R, E, D, E, L, E]   # starts U, ends L
qB = [R, E, U, E, L, E, D, E]   # starts R, ends D

# Build transitions (quarter → 8th) — ordered jack-free after qB(ends D)
bA = [L, D, E, E, R, U, E, E]   # starts L, ends U
bB = [D, R, E, E, U, L, E, E]   # starts D, ends L
bC = [R, U, L, E, D, R, U, E]   # starts R, ends U
bD = [D, L, R, E, U, D, L, E]   # starts D, ends L

# Slow section (140 BPM — denser patterns readable at low speed)
slA = [L, D, DU, R, U, L, LR, D]   # ends D
slB = [R, U, LR, D, L, R, DU, L]   # ends L
slC = [D, R, DU, L, U, D, LR, U]   # ends U (next slA starts L ✓)

# Breather / jump break
jBreak = [DU, E, E, E, LR, E, E, E]  # ends with E (last active = LR)

# Rest
rest8 = [E] * 8
rest4 = [E] * 4

# ── Sparse patterns for easy charts (4 rows = quarter notes) ──
sA = [L, E, R, E]; sB = [D, E, U, E]; sC = [R, E, L, E]; sD = [U, E, D, E]
sE = [L, E, D, E]; sF = [R, E, U, E]; sG = [D, E, R, E]; sH = [U, E, L, E]
sJ = [L, E, E, E]; sK = [D, E, E, E]; sL = [R, E, E, E]; sM = [U, E, E, E]
# Jump sparse
sJA = [DU, E, E, E]; sJB = [LR, E, E, E]

# ── SONG STRUCTURE ──
# BPM changes (from original DWI, converted to SM beats):
#   Beat 0    = 300 BPM
#   Beat 248  = 320 BPM
#   Beat 504  = 140 BPM
#   Beat 536  = 300 BPM
#   Beat 792  = 320 BPM
# Measure boundaries: 62, 126, 134, 198
# Total ~215 measures

TOTAL_MEASURES = 215

# ── EXPERT CHART (10) ──
def gen_expert():
    ms = []
    # Intro: 7 measures silence
    ms.extend([rest8] * 7)
    # Build: 7 measures (quarter → 8th transition)
    ms.extend([qA, qB, qC, qD, bA, bB, bC])
    # -- 14 measures used --

    # Section A (300 BPM, measures 15‑62 = 48 measures)
    # 12 four-measure phrases of flowing streams
    sec_a = [
        fA, fC, fF, fE,    # U→R,D→U,R→D,L  (check: fA→fC: U→R✓, fC→fF: D→U✓, fF→fE: R→D✓)
        fA, fE, fF, jC,    # U→D✓,L→U✓,R→L✓ → ends DU
        jA, fE, fF, fA,    # DU→L(jA), R→D✓,L→U✓,R→L✓   wait jA starts DU ends R. jA→fE: R→D✓
        fC, fF, fE, jD,    # D→U✓, R→D✓, L→R✓ → ends LR
        fE, fF, fA, fC,    # LR: next must not start L or R. fE starts D✓. D→R(fE end)→U(fF)✓, R→L✓, U→R✓ wait fA ends U fC starts R ✓
        fF, fA, fE, jC,    # fC ends D → fF starts U ✓, R→L✓, U→D✓, L→L... fE ends L, jC starts L! JACK!
    ]
    # Fix: replace last phrase
    sec_a_fixed = [
        fA, fC, fF, fE,
        fA, fE, fF, jC,
        jA, fE, fF, fA,
        fC, fF, fE, jD,
        fE, fF, fA, fC,
        fF, fA, fC, jC,    # R→L✓, U→R✓, D→L... fC ends D, jC starts L ✓!  ends DU
        jA, fE, fF, fA,    # DU→L(jA starts DU, but jA first note is DU)... 
        # After jC (ends DU): next must not start D or U. jA starts DU → JACK with DU!
        # Fix: after jC, use fA (starts L) or fC (starts R)
        fA, fC, fF, fE,    # L✓ after DU
        fD, fF, fE, jC,    # fE ends L → fD starts R ✓, U→U... fD ends U fF starts U JACK!
        # Fix: fD(end U) → fE(start D) ✓
        fD, fE, fF, jC,    # R.., U→D✓, L→U✓, R→L✓ ends DU
        fA, fC, fF, fE,    # DU→L✓, U→R✓, D→U✓, R→D✓
        fA, fE, fF, fC,    # U→D✓, L→U✓, R→R... fF ends R fC starts R JACK!
    ]
    # OK let me build this carefully with a helper
    return ms  # placeholder

def safe_chain(patterns_pool, count, start_after=None):
    """Build a jack-free chain of `count` measures from the pool."""
    # Pool is a list of measures. We pick greedily ensuring no jack.
    result = []
    prev_end = start_after
    pool = list(patterns_pool)
    idx = 0
    for _ in range(count):
        # Try each pattern in the pool starting from current index
        found = False
        for offset in range(len(pool)):
            candidate = pool[(idx + offset) % len(pool)]
            fa = first_active(candidate)
            if prev_end is None or not shares(prev_end, fa):
                result.append(candidate)
                prev_end = last_active(candidate)
                idx = (idx + offset + 1) % len(pool)
                found = True
                break
        if not found:
            # Fallback: insert a rest measure to break the chain
            result.append(rest8)
            prev_end = E
            idx = (idx + 1) % len(pool)
    return result

# ── Definitive chart generators ──

def gen_expert_chart():
    ms = []
    # Intro silence: 7 measures
    ms.extend([rest8] * 7)

    # Build-up: 7 measures (jack-free chain: qA→qC→qD→qB→bA→bB→bC)
    ms.extend([qA, qC, qD, qB, bA, bB, bC])
    # 14 measures done

    # Section A: 300 BPM streams (measures 15-62 = 48 measures)
    # Core flowing streams with periodic jump accents every 8 measures
    stream_pool = [fA, fC, fF, fE, fD, fH, fG, fB]
    jump_pool   = [jC, jA, jD, jE]

    prev = last_active(ms[-1])  # last note of build section
    for phrase in range(6):  # 6 phrases of 8 measures
        chunk = safe_chain(stream_pool, 7, start_after=prev)
        ms.extend(chunk)
        prev = last_active(chunk[-1])
        # Add jump accent as 8th measure
        for jp in jump_pool:
            fa = first_active(jp)
            if not shares(prev, fa):
                ms.append(jp)
                prev = last_active(jp)
                break
        else:
            ms.append(rest8)
            prev = E
    # 14 + 48 = 62 measures ✓

    # Section B: 320 BPM intense streams (measures 63-126 = 64 measures)
    # Faster BPM, same clean patterns, more jump accents
    for phrase in range(8):  # 8 phrases of 8 measures
        chunk = safe_chain(stream_pool, 6, start_after=prev)
        ms.extend(chunk)
        prev = last_active(chunk[-1])
        # Two jump accents per phrase
        for jp in jump_pool:
            fa = first_active(jp)
            if not shares(prev, fa):
                ms.append(jp)
                prev = last_active(jp)
                break
        else:
            ms.append(rest8); prev = E
        # One more stream
        extra = safe_chain(stream_pool, 1, start_after=prev)
        ms.extend(extra)
        prev = last_active(extra[-1])
    # 62 + 64 = 126 measures ✓

    # Section C: 140 BPM slow section (measures 127-134 = 8 measures)
    slow_cycle = [slA, slB, slC, slA, slB, slC, slA, slB]
    ms.extend(slow_cycle)
    prev = last_active(slow_cycle[-1])  # slB ends L
    # 126 + 8 = 134 ✓

    # Section D: 300 BPM return (measures 135-198 = 64 measures)
    # Recovery phrase then full intensity
    # 2 measures breather
    ms.append([DU, E, E, E, E, E, E, E])
    ms.append([E, E, E, E, LR, E, E, E])
    prev = LR
    # 2 measures rebuild
    rebuild = safe_chain([qA, qC, qB, qD], 2, start_after=prev)
    ms.extend(rebuild)
    prev = last_active(rebuild[-1])
    # 2 measures transition
    trans = safe_chain([bC, bD, bA, bB], 2, start_after=prev)
    ms.extend(trans)
    prev = last_active(trans[-1])
    # 58 measures of full streams with jump accents every 6 measures
    remaining_d = 58
    while remaining_d > 0:
        batch = min(6, remaining_d)
        chunk = safe_chain(stream_pool, batch, start_after=prev)
        ms.extend(chunk)
        prev = last_active(chunk[-1])
        remaining_d -= batch
        if remaining_d > 0:
            for jp in jump_pool:
                fa = first_active(jp)
                if not shares(prev, fa):
                    ms.append(jp)
                    prev = last_active(jp)
                    remaining_d -= 1
                    break
    # Pad to exactly measure 198
    while len(ms) < 198:
        extra = safe_chain(stream_pool, 1, start_after=prev)
        ms.extend(extra)
        prev = last_active(extra[-1])
    ms = ms[:198]  # trim if over
    prev = last_active(ms[-1])
    # 198 ✓

    # Section E: 320 BPM finale (measures 199-215 = 17 measures)
    # Full intensity streams building to final jumps
    finale_streams = safe_chain(stream_pool, 13, start_after=prev)
    ms.extend(finale_streams)
    prev = last_active(finale_streams[-1])
    # Final 4 measures: jump accents + ending
    for jp in jump_pool:
        if not shares(prev, first_active(jp)):
            ms.append(jp); prev = last_active(jp); break
    ms.append(safe_chain(stream_pool, 1, start_after=prev)[0])
    prev = last_active(ms[-1])
    # Big finish jumps (start with LR to avoid U→DU jack)
    ms.append([LR, E, DU, E, LR, E, DU, E])
    ms.append([LR, DU, E, E, E, E, E, E])
    # 215 measures

    # Pad or trim to exact length
    while len(ms) < TOTAL_MEASURES:
        ms.append(rest8)
    ms = ms[:TOTAL_MEASURES]

    return ms


def gen_difficult_chart():
    """Difficult (8): 8th note streams with gaps and fewer jumps."""
    ms = []
    ms.extend([rest8] * 7)
    ms.extend([qA, qC, qD, qB, bA, bB, bC])  # 7 measures quarter/build transition

    stream_pool = [fA, fC, fF, fE, fD, fH]
    gap_patterns = [bA, bB, bC, bD]  # half-density patterns

    prev = last_active(ms[-1])

    # Section A: mix of streams and gaps (48 measures)
    for phrase in range(12):
        chunk = safe_chain(stream_pool, 2, start_after=prev)
        ms.extend(chunk)
        prev = last_active(chunk[-1])
        gap = safe_chain(gap_patterns, 2, start_after=prev)
        ms.extend(gap)
        prev = last_active(gap[-1])

    # Section B: 320 BPM (64 measures) — more streams, fewer gaps
    for phrase in range(16):
        chunk = safe_chain(stream_pool, 3, start_after=prev)
        ms.extend(chunk)
        prev = last_active(chunk[-1])
        gap = safe_chain(gap_patterns, 1, start_after=prev)
        ms.extend(gap)
        prev = last_active(gap[-1])

    # Slow section (8 measures): start with qC(D) to avoid jack from prior L-ending
    slow = safe_chain([qC, qD, qB, qA, qC, qD, qB, qA], 8, start_after=prev)
    ms.extend(slow)
    prev = last_active(slow[-1])

    # Section D (64 measures): streams with occasional gaps
    for phrase in range(16):
        chunk = safe_chain(stream_pool, 3, start_after=prev)
        ms.extend(chunk)
        prev = last_active(chunk[-1])
        gap = safe_chain(gap_patterns, 1, start_after=prev)
        ms.extend(gap)
        prev = last_active(gap[-1])

    # Finale (17 measures)
    finale = safe_chain(stream_pool, 15, start_after=prev)
    ms.extend(finale)
    ms.append([LR, E, DU, E, E, E, E, E])
    ms.append(rest8)

    while len(ms) < TOTAL_MEASURES:
        ms.append(rest8)
    return ms[:TOTAL_MEASURES]


def gen_basic_chart():
    """Basic (5): Mostly quarter notes, some 8ths, simple jumps."""
    ms = []
    ms.extend([rest4] * 7)  # 4-row silence

    quarter_pool = [sA, sB, sC, sD, sE, sF, sG, sH]
    half_pool = [sJ, sK, sL, sM]

    prev = E
    # Section A (48 measures): quarter notes
    for phrase in range(12):
        chunk = safe_chain(quarter_pool, 3, start_after=prev)
        ms.extend(chunk)
        prev = last_active(chunk[-1])
        rest_m = safe_chain(half_pool, 1, start_after=prev)
        ms.extend(rest_m)
        prev = last_active(rest_m[-1])

    # Section B (64 measures): more active quarters
    for phrase in range(16):
        chunk = safe_chain(quarter_pool, 4, start_after=prev)
        ms.extend(chunk)
        prev = last_active(chunk[-1])

    # Slow (8 measures): half notes
    for _ in range(8):
        h = safe_chain(half_pool, 1, start_after=prev)
        ms.extend(h)
        prev = last_active(h[-1])

    # Section D (64 measures): quarter notes with jumps
    for phrase in range(16):
        chunk = safe_chain(quarter_pool, 3, start_after=prev)
        ms.extend(chunk)
        prev = last_active(chunk[-1])
        ms.append(sJA if not shares(prev, DU) else sJB)
        prev = DU if not shares(prev, DU) else LR

    # Finale (17 measures)
    for _ in range(15):
        chunk = safe_chain(quarter_pool, 1, start_after=prev)
        ms.extend(chunk)
        prev = last_active(chunk[-1])
    ms.append(sJA)
    ms.append(rest4)

    while len(ms) < TOTAL_MEASURES:
        ms.append(rest4)
    return ms[:TOTAL_MEASURES]


def gen_beginner_chart():
    """Beginner (2): Very sparse, half notes and quarter notes."""
    ms = []
    ms.extend([rest4] * 14)  # Long intro silence

    half_pool = [sJ, sK, sL, sM]
    prev = E

    # Whole song: gentle half notes with lots of gaps
    for i in range(TOTAL_MEASURES - 14):
        if i % 3 == 0:
            h = safe_chain(half_pool, 1, start_after=prev)
            ms.extend(h)
            prev = last_active(h[-1])
        else:
            ms.append(rest4)
            prev = E

    while len(ms) < TOTAL_MEASURES:
        ms.append(rest4)
    return ms[:TOTAL_MEASURES]


# ── SM file output ──

def format_notes(measures):
    """Convert list of measures to SM note-data string."""
    parts = []
    for meas in measures:
        parts.append('\n'.join(meas))
    return '\n,\n'.join(parts)


def build_sm_file():
    """Assemble the complete .sm file content."""

    header = """\
#TITLE:MAX 300 (Super-Max-Me Mix);
#SUBTITLE:~Effortless Flow Edit~;
#ARTIST:Jondi & Spesh;
#TITLETRANSLIT:;
#SUBTITLETRANSLIT:;
#ARTISTTRANSLIT:;
#GENRE:;
#CREDIT:AI-crafted flow chart;
#BANNER:MAX 300 (Super-Max-Me Mix).png;
#BACKGROUND:MAX 300 (Super-Max-Me Mix)-bg.png;
#LYRICSPATH:;
#CDTITLE:;
#MUSIC:MAX 300 (Super-Max-Me Mix).mp3;
#OFFSET:-1.055;
#SAMPLESTART:12.950;
#SAMPLELENGTH:15.000;
#SELECTABLE:YES;
#BPMS:0.000=300.000,248.000=320.000,504.000=140.000,536.000=300.000,792.000=320.000;
#STOPS:;
#BGCHANGES:;
#FGCHANGES:;
"""

    charts = []

    # ── Beginner ──
    print("Generating Beginner chart...")
    beg = gen_beginner_chart()
    validate_chain(beg, "Beginner")
    charts.append(f"""
//---------- dance-single - Beginner ----------
#NOTES:
     dance-single:
     :
     Beginner:
     2:
     0.000,0.000,0.000,0.000,0.000:
{format_notes(beg)}
;""")

    # ── Basic ──
    print("Generating Basic chart...")
    bas = gen_basic_chart()
    validate_chain(bas, "Basic")
    charts.append(f"""
//---------- dance-single - Basic ----------
#NOTES:
     dance-single:
     :
     Easy:
     5:
     0.000,0.000,0.000,0.000,0.000:
{format_notes(bas)}
;""")

    # ── Difficult ──
    print("Generating Difficult chart...")
    diff = gen_difficult_chart()
    validate_chain(diff, "Difficult")
    charts.append(f"""
//---------- dance-single - Difficult ----------
#NOTES:
     dance-single:
     :
     Medium:
     8:
     0.000,0.000,0.000,0.000,0.000:
{format_notes(diff)}
;""")

    # ── Expert ──
    print("Generating Expert chart...")
    exp = gen_expert_chart()
    validate_chain(exp, "Expert")
    charts.append(f"""
//---------- dance-single - Expert ----------
#NOTES:
     dance-single:
     :
     Hard:
     10:
     0.000,0.000,0.000,0.000,0.000:
{format_notes(exp)}
;""")

    return header + '\n'.join(charts) + '\n'


# ── Main ──
if __name__ == '__main__':
    src_folder = r'c:\Program Files (x86)\StepMania\Songs\_Dance Dance Challenge\Quezacotl'
    dst_folder = r'c:\Program Files (x86)\StepMania\Songs\_Dance Dance Challenge\MAX300 Effortless Flow'

    # Create destination folder
    os.makedirs(dst_folder, exist_ok=True)

    # Copy audio and image assets from the original
    assets = [
        'MAX 300 (Super-Max-Me Mix).mp3',
        'MAX 300 (Super-Max-Me Mix).png',
        'MAX 300 (Super-Max-Me Mix)-bg.png',
    ]
    for asset in assets:
        src = os.path.join(src_folder, asset)
        dst = os.path.join(dst_folder, asset)
        if os.path.exists(src) and not os.path.exists(dst):
            shutil.copy2(src, dst)
            print(f"Copied: {asset}")
        elif os.path.exists(dst):
            print(f"Already exists: {asset}")
        else:
            print(f"WARNING: Source not found: {src}")

    # Generate and write the .sm file
    sm_content = build_sm_file()
    sm_path = os.path.join(dst_folder, 'MAX 300 (Super-Max-Me Mix).sm')
    with open(sm_path, 'w', encoding='utf-8') as f:
        f.write(sm_content)

    print(f"\n✓ Chart written to: {sm_path}")
    print(f"  Total size: {len(sm_content):,} bytes")
    print(f"  Folder: {dst_folder}")
    print(f"\nOpen StepMania and look for:")
    print(f'  "MAX 300 (Super-Max-Me Mix) ~Effortless Flow Edit~"')
    print(f"  in the _Dance Dance Challenge group.")
