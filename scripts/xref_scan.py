"""
xref_scan.py — Read-only cross-reference scanner for Athena Docs
================================================================
Scans all .md principle files in Athena Docs/ and produces a
cross-reference map showing which files mention other frameworks
or principles. Does NOT modify any files.

Usage:
    python scripts/xref_scan.py

Output:
    _xref_report.md   (in workspace root)
"""

import re
import sys
from pathlib import Path
from collections import defaultdict
from datetime import datetime

# ── Configuration ──────────────────────────────────────────────
WORKSPACE = Path(__file__).resolve().parent.parent
ATHENA_DOCS = WORKSPACE / "Athena Docs"
OUTPUT_FILE = WORKSPACE / "_xref_report.md"

# Known framework codes (extracted from folder names)
FRAMEWORK_CODES = [
    "aaron", "bimodalmap", "fieldmot", "fieldstr", "habitat",
    "hmap", "humwaves", "interference", "lineagemap",
    "lvlloveplay", "lvlmirror", "lvlselfhome", "misclass",
    "realitygeo", "realityrel", "selfmot", "selfmulti",
    "selfstr", "stastory", "supposedto", "wavesurf",
]

# ── File Discovery ─────────────────────────────────────────────
def discover_principle_files():
    """
    Walk Athena Docs and collect all .md principle files.
    Returns list of (framework_code, principle_id, filepath) tuples.
    Handles both flat layout ([aaron]) and nested subfolder layout.
    """
    files = []
    
    for framework_dir in sorted(ATHENA_DOCS.iterdir()):
        if not framework_dir.is_dir():
            continue
        
        # Extract framework code from folder name: [code] Title → code
        m = re.match(r"\[([^\]]+)\]", framework_dir.name)
        if not m:
            continue
        fw_code = m.group(1)
        
        # Collect .md files — could be flat (directly in folder) or nested (in subfolder)
        md_files = list(framework_dir.glob("*.md"))
        for sub in framework_dir.iterdir():
            if sub.is_dir():
                md_files.extend(sub.glob("*.md"))
        
        for md_file in sorted(md_files):
            # Extract principle ID from filename or heading
            # Pattern: code-pNNN in filename
            pid_match = re.search(r"([a-z]+-p\d{3,4})", md_file.stem, re.IGNORECASE)
            if pid_match:
                principle_id = pid_match.group(1).lower()
            else:
                # Try extracting from the H1 heading inside the file
                principle_id = extract_pid_from_content(md_file)
                if not principle_id:
                    continue  # Not a principle file
            
            files.append((fw_code, principle_id, md_file))
    
    return files


def extract_pid_from_content(filepath):
    """Extract principle ID from # [code-pNNN] heading."""
    try:
        text = filepath.read_text(encoding="utf-8", errors="replace")
        m = re.search(r"^#\s*\[([a-z]+-p\d{3,4})\]", text, re.MULTILINE | re.IGNORECASE)
        if m:
            return m.group(1).lower()
    except Exception:
        pass
    return None


# ── Scanning ───────────────────────────────────────────────────
def scan_file_for_references(filepath, own_code):
    """
    Scan a file's text for mentions of other framework codes and principle IDs.
    Returns:
      - framework_mentions: dict { code: count }
      - principle_mentions: list of principle IDs (e.g., "hmap-p003")
      - title: extracted from first heading
    """
    try:
        text = filepath.read_text(encoding="utf-8", errors="replace")
    except Exception:
        return {}, [], "(unreadable)"
    
    # Extract title from first ## heading (or # heading)
    title = "(untitled)"
    title_match = re.search(r"^#{1,2}\s+(.+)$", text, re.MULTILINE)
    if title_match:
        raw = title_match.group(1).strip()
        # Clean up: remove [code-pNNN] prefix
        raw = re.sub(r"^\[.*?\]\s*", "", raw)
        if raw:
            title = raw
    
    framework_mentions = defaultdict(int)
    principle_mentions = []
    
    # --- Pattern 1: Explicit [code] mentions ---
    # e.g., [hmap], [selfstr], [habitat]
    bracket_pattern = re.compile(r"\[(" + "|".join(re.escape(c) for c in FRAMEWORK_CODES) + r")\]", re.IGNORECASE)
    for m in bracket_pattern.finditer(text):
        code = m.group(1).lower()
        if code != own_code:
            framework_mentions[code] += 1
    
    # --- Pattern 2: Explicit principle IDs ---
    # e.g., hmap-p003, selfstr-p017, habitat-p012
    pid_pattern = re.compile(
        r"\b(" + "|".join(re.escape(c) for c in FRAMEWORK_CODES) + r")-p(\d{3,4})\b", 
        re.IGNORECASE
    )
    for m in pid_pattern.finditer(text):
        code = m.group(1).lower()
        pid = f"{code}-p{m.group(2)}"
        if code != own_code:
            framework_mentions[code] += 1
            principle_mentions.append(pid)
    
    # --- Pattern 3: Unbracketed framework code as standalone word ---
    # More conservative: only match if it appears as a clear reference
    # (e.g., "the hmap framework" or "as described in selfstr")
    # We look for code preceded by context clues
    context_pattern = re.compile(
        r"(?:in|from|see|per|via|the)\s+(" + "|".join(re.escape(c) for c in FRAMEWORK_CODES) + r")\b",
        re.IGNORECASE
    )
    for m in context_pattern.finditer(text):
        code = m.group(1).lower()
        if code != own_code:
            framework_mentions[code] += 1
    
    return dict(framework_mentions), principle_mentions, title


def extract_key_concepts(filepath):
    """
    Extract significant concept terms from a file for thematic overlap detection.
    Pulls from headings, bold text, and RESONANCE_ANCHORS.
    """
    try:
        text = filepath.read_text(encoding="utf-8", errors="replace")
    except Exception:
        return set()
    
    concepts = set()
    
    # RESONANCE_ANCHORS line
    ra_match = re.search(r"RESONANCE_ANCHORS:\s*(.+)$", text, re.MULTILINE)
    if ra_match:
        for term in ra_match.group(1).split(","):
            term = term.strip().lower()
            if len(term) > 3:
                concepts.add(term)
    
    # All ## and ### headings (excluding generic ones)
    for m in re.finditer(r"^#{2,3}\s+(.+)$", text, re.MULTILINE):
        heading = m.group(1).strip().lower()
        # Skip generic section labels
        if heading in ("title", "subtitle", "free flow", "compression", "law"):
            continue
        if len(heading) > 4:
            concepts.add(heading)
    
    # Bold terms (**term**)
    for m in re.finditer(r"\*\*([^*]{4,60})\*\*", text):
        concepts.add(m.group(1).strip().lower())
    
    return concepts


# ── Report Generation ──────────────────────────────────────────
def generate_report(principle_files, scan_results, concept_map):
    """Generate the cross-reference report as markdown."""
    
    lines = []
    lines.append("# Athena Docs — Cross-Reference Report")
    lines.append(f"\n> Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')} | "
                 f"Files scanned: {len(principle_files)} | Read-only scan (no files modified)")
    lines.append("")
    
    # ── Section 1: Summary Statistics ──
    lines.append("---")
    lines.append("## 1. Framework Summary")
    lines.append("")
    
    fw_counts = defaultdict(int)
    for fw_code, pid, fpath in principle_files:
        fw_counts[fw_code] += 1
    
    lines.append("| Framework | Principles | Has Outbound Refs |")
    lines.append("|:----------|:----------:|:-----------------:|")
    
    for code in sorted(fw_counts.keys()):
        count = fw_counts[code]
        has_refs = any(
            scan_results[pid]["fw_mentions"]
            for _, pid, _ in principle_files
            if _ == code and pid in scan_results
        )
        ref_mark = "Yes" if has_refs else "—"
        lines.append(f"| `[{code}]` | {count} | {ref_mark} |")
    
    lines.append(f"\n**Total: {len(principle_files)} principle files across {len(fw_counts)} frameworks**")
    lines.append("")
    
    # ── Section 2: Explicit Cross-References ──
    lines.append("---")
    lines.append("## 2. Explicit Cross-References")
    lines.append("")
    lines.append("Files that mention other frameworks by code or principle ID.")
    lines.append("")
    
    has_any_xref = False
    for fw_code in sorted(fw_counts.keys()):
        fw_refs = []
        for own_code, pid, fpath in principle_files:
            if own_code != fw_code:
                continue
            if pid not in scan_results:
                continue
            result = scan_results[pid]
            if result["fw_mentions"]:
                fw_refs.append((pid, result))
        
        if fw_refs:
            has_any_xref = True
            lines.append(f"### [{fw_code}]")
            lines.append("")
            for pid, result in fw_refs:
                title = result["title"]
                lines.append(f"**{pid}** — {title}")
                for ref_code, count in sorted(result["fw_mentions"].items()):
                    lines.append(f"  - → `[{ref_code}]` ({count} mention{'s' if count > 1 else ''})")
                if result["principle_mentions"]:
                    lines.append(f"  - Specific principles: {', '.join(sorted(set(result['principle_mentions'])))}")
                lines.append("")
    
    if not has_any_xref:
        lines.append("**No explicit cross-framework references found in any .md principle file.**")
        lines.append("")
        lines.append("This means the 19 frameworks currently exist as isolated documents. ")
        lines.append("Cross-connections live in Aaron's head but aren't yet written into the files.")
        lines.append("")
    
    # ── Section 3: Thematic Overlap (Shared Concepts) ──
    lines.append("---")
    lines.append("## 3. Thematic Overlap — Shared Concepts Across Frameworks")
    lines.append("")
    lines.append("Concepts (from headings and bold text) that appear in 2+ frameworks.")
    lines.append("")
    
    # Build concept → {framework_code} mapping
    concept_to_frameworks = defaultdict(set)
    for (fw_code, pid, fpath), concepts in concept_map.items():
        for concept in concepts:
            concept_to_frameworks[concept].add(fw_code)
    
    # Filter to concepts shared across 2+ frameworks
    shared_concepts = {
        concept: sorted(fws)
        for concept, fws in concept_to_frameworks.items()
        if len(fws) >= 2
    }
    
    if shared_concepts:
        # Sort by number of frameworks (most shared first)
        sorted_concepts = sorted(shared_concepts.items(), key=lambda x: (-len(x[1]), x[0]))
        
        lines.append(f"Found **{len(sorted_concepts)}** concepts shared across multiple frameworks:")
        lines.append("")
        lines.append("| Concept | Frameworks | Count |")
        lines.append("|:--------|:-----------|:-----:|")
        
        # Show top 80 to keep manageable
        for concept, fws in sorted_concepts[:80]:
            fw_str = ", ".join(f"`{f}`" for f in fws)
            lines.append(f"| {concept} | {fw_str} | {len(fws)} |")
        
        if len(sorted_concepts) > 80:
            lines.append(f"| ... | *({len(sorted_concepts) - 80} more)* | |")
        lines.append("")
    else:
        lines.append("No shared concepts detected across frameworks.")
        lines.append("")
    
    # ── Section 4: Framework Connectivity Matrix ──
    lines.append("---")
    lines.append("## 4. Framework Connectivity Matrix")
    lines.append("")
    lines.append("How many shared concepts exist between each pair of frameworks.")
    lines.append("(Only pairs with 3+ shared concepts shown.)")
    lines.append("")
    
    # Build pairwise overlap count
    fw_list = sorted(fw_counts.keys())
    pair_overlaps = defaultdict(int)
    
    for concept, fws in concept_to_frameworks.items():
        if len(fws) < 2:
            continue
        fw_sorted = sorted(fws)
        for i in range(len(fw_sorted)):
            for j in range(i + 1, len(fw_sorted)):
                pair_overlaps[(fw_sorted[i], fw_sorted[j])] += 1
    
    # Show as sorted list (most connected pairs first)
    significant_pairs = [
        (pair, count) for pair, count in pair_overlaps.items() if count >= 3
    ]
    significant_pairs.sort(key=lambda x: -x[1])
    
    if significant_pairs:
        lines.append("| Framework A | Framework B | Shared Concepts |")
        lines.append("|:-----------|:-----------|:---------------:|")
        for (a, b), count in significant_pairs[:50]:
            lines.append(f"| `[{a}]` | `[{b}]` | {count} |")
        lines.append("")
    else:
        lines.append("No significant framework pairs found (threshold: 3+ shared concepts).")
        lines.append("")
    
    # ── Section 5: Isolated Frameworks ──
    lines.append("---")
    lines.append("## 5. Isolation Report")
    lines.append("")
    
    connected_fws = set()
    for (a, b), count in pair_overlaps.items():
        if count >= 3:
            connected_fws.add(a)
            connected_fws.add(b)
    
    isolated = [fw for fw in fw_list if fw not in connected_fws]
    if isolated:
        lines.append("Frameworks with fewer than 3 shared concepts with any other framework:")
        lines.append("")
        for fw in isolated:
            lines.append(f"- `[{fw}]` ({fw_counts[fw]} principles)")
        lines.append("")
    else:
        lines.append("All frameworks have at least 3 concept overlaps with another framework.")
        lines.append("")
    
    # ── Section 6: Recommendations ──
    lines.append("---")
    lines.append("## 6. Observations & Next Steps")
    lines.append("")
    lines.append("### What this scan reveals")
    lines.append("")
    
    if not has_any_xref:
        lines.append("- **No explicit cross-references exist** between the 504 principle files. "
                      "Each framework is self-contained.")
        lines.append("- **Thematic overlap does exist** (see Section 3) — the same concepts "
                      "appear across multiple frameworks but are never linked.")
        lines.append("- This means the interconnection structure is **implicit** — it lives in "
                      "the reading experience, not in the file metadata.")
        lines.append("")
    
    lines.append("### Possible next steps (all optional, all reversible)")
    lines.append("")
    lines.append("1. **Add metadata headers** to the 18 frameworks that lack them "
                 "(matching [aaron]'s format: FRAMEWORK_CODE, RESONANCE_ANCHORS, etc.)")
    lines.append("2. **Add `CROSS_REFERENCES:` fields** to principles that mention other "
                 "frameworks or share significant thematic overlap")
    lines.append("3. **Install Foam** for graph visualization of existing content "
                 "(read-only, shows connections as you add wiki-links)")
    lines.append("4. **Add wiki-links** incrementally: `[[hmap-p003]]` style references "
                 "where thematic overlap is strongest")
    lines.append("")
    
    return "\n".join(lines)


# ── Main ───────────────────────────────────────────────────────
def main():
    print(f"Scanning: {ATHENA_DOCS}")
    
    # Step 1: Discover all principle files
    principle_files = discover_principle_files()
    print(f"Found {len(principle_files)} principle files across "
          f"{len(set(f[0] for f in principle_files))} frameworks")
    
    # Step 2: Scan each file
    scan_results = {}
    concept_map = {}
    
    for i, (fw_code, pid, fpath) in enumerate(principle_files):
        fw_mentions, p_mentions, title = scan_file_for_references(fpath, fw_code)
        concepts = extract_key_concepts(fpath)
        
        scan_results[pid] = {
            "fw_code": fw_code,
            "title": title,
            "fw_mentions": fw_mentions,
            "principle_mentions": p_mentions,
            "filepath": str(fpath),
        }
        concept_map[(fw_code, pid, fpath)] = concepts
        
        if (i + 1) % 50 == 0:
            print(f"  Scanned {i + 1}/{len(principle_files)}...")
    
    print(f"  Scanned {len(principle_files)}/{len(principle_files)} — done")
    
    # Step 3: Generate report
    report = generate_report(principle_files, scan_results, concept_map)
    
    # Step 4: Write output
    OUTPUT_FILE.write_text(report, encoding="utf-8")
    print(f"\nReport written to: {OUTPUT_FILE}")
    print(f"Report size: {len(report):,} characters")


if __name__ == "__main__":
    main()
