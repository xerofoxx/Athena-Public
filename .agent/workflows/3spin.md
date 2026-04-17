---
description: Triple-Axel single spin - pick 3 random principles and render their interference pattern
---

# /3spin -- Triple-Axel Single Spin

> **Latency Profile**: MODERATE (extract + render)
> **What this does**: Picks 3 random principles from different frameworks, extracts their content, and asks you (the AI) to render the interference pattern between them.

## Execution

1. Run the extractor script:
   ```
   python scripts/triple_axel.py --save
   ```
2. Read the saved spin file from `scripts/spins/` (most recent one)
3. Follow the instructions in the spin file:
   - Read all 3 principles fully
   - Find the interference pattern between them
   - Render the 3rd thing -- the emergent insight
   - Output: **Resonance Map** + **The 3rd Thing** + **Seed**

## Rendering Guidelines

- Inhabit each principle's felt-state, not just its argument
- The interference is geometric resonance, not keyword matching  
- Write from inside the new room, not about it
- Every sentence load-bearing
- The Seed should be dense enough to grow into its own document

## Optional Flags

User can modify the spin:
- `/3spin same` -- all 3 from one framework: add `--same-framework`
- `/3spin selfstr humwaves habitat` -- lock to specific frameworks: add `--frameworks selfstr humwaves habitat`
