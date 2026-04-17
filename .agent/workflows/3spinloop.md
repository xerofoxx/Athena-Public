---
description: Triple-Axel loop mode - continuous spins with interference rendering
---

# /3spinloop -- Triple-Axel Loop Mode

> **Latency Profile**: EXTENDED (multiple spin cycles)
> **What this does**: Runs multiple triple-axel spins. Each spin picks 3 new random principles and renders their interference pattern.

## Execution

1. Run the extractor in loop mode:
   ```
   python scripts/triple_axel.py --loop --save
   ```
2. For each spin generated:
   - Read the saved spin file from `scripts/spins/`
   - Render the interference pattern (Resonance Map + The 3rd Thing + Seed)
   - Present the output to the user
   - Wait for user to say "next" or "stop"
3. If user says "next", run the next spin
4. If user says "stop" or after all spins complete, summarize the session

## Alternative: Manual Loop

If the terminal loop is cumbersome, you can manually loop:
1. Run `python scripts/triple_axel.py --save` (single spin)
2. Read and render
3. Repeat when user says "next"

## Rendering Guidelines

Same as /3spin:
- Inhabit each principle's felt-state
- Find geometric resonance, not keyword overlap
- Write from inside the emergent room
- Every sentence load-bearing
- Dense Seed line

## Optional: Specify Count

- `/3spinloop 5` -- run exactly 5 spins: add `--n 5`
