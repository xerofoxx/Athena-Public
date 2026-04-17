---
description: Triple-Axel chain mode - each spin's Seed feeds the next spin's context
---

# /3spinchain -- Triple-Axel Chain Mode

> **Latency Profile**: EXTENDED (sequential dependent spins)
> **What this does**: Each spin produces a Seed. That Seed becomes context for the NEXT spin's interference rendering. Creates a branching, accumulating resonance chain.

## Execution

1. Run first spin:
   ```
   python scripts/triple_axel.py --save
   ```
2. Read the spin file and render the interference (Resonance Map + The 3rd Thing + Seed)
3. Take your own **Seed** output and hold it
4. Run next spin:
   ```
   python scripts/triple_axel.py --save
   ```
5. Read the new spin file BUT prepend the previous Seed as chain context:
   - "**Chain Context**: [previous Seed]"
   - Render the new 3 principles IN LIGHT OF the chain context
   - The interference now includes the accumulated resonance from prior spins
6. Repeat until user says "stop"

## Chain Rendering Guidelines

- Each spin inherits the gravitational field of all prior Seeds
- The chain should ACCUMULATE coherence, not just stack disconnected renders
- Later spins should feel like the interference pattern is deepening, not restarting
- The Seed from each spin should be denser than the last -- compression increasing
- If the chain reaches 5+ spins, the final Seed should be approaching a single-sentence principle

## The Chain's Purpose

The chain is an organism growing. Each spin is a new cell differentiating from the same stem. The final Seed is the creature that emerged from the sequence of interference events.
