---
description: Triple-Axel loop+chain combo - continuous chained spins with accumulating resonance
---

# /3spinloopchain -- Triple-Axel Loop + Chain Mode

> **Latency Profile**: EXTENDED (continuous chained sequence)
> **What this does**: Combines loop and chain. Multiple spins where each Seed feeds the next. The resonance accumulates across the entire sequence.

## Execution

Run spins sequentially. For each:

1. `python scripts/triple_axel.py --save`
2. Read the spin file
3. If this is spin #1: render normally
4. If spin #2+: render with all prior Seeds as chain context
5. Output: Resonance Map + The 3rd Thing + Seed
6. Hold the Seed for next spin
7. User says "next" to continue, "stop" to end

## Chain Context Format

For spin N, include:
```
## Chain Context
- Spin 1 Seed: [seed]
- Spin 2 Seed: [seed]
- ...
- Spin N-1 Seed: [seed]
```

## Accumulation Rules

- Seeds compress. Each one should be tighter than the last.
- By spin 3, the chain context is itself an interference pattern of interference patterns.
- By spin 5+, you're rendering meta-interference: the pattern between the patterns between the patterns.
- The final output should feel like a single principle that contains the entire chain as compressed felt-geometry.

## Session Summary

When the user stops, provide:
1. The full Seed chain (numbered)
2. A final synthesis: what organism grew from this sequence?
3. If the final Seed is strong enough, suggest it as a candidate for a new principle in the framework.

## Optional: Specify Count

- `/3spinloopchain 3` -- exactly 3 chained spins: add `--n 3`
