---
id: selfstr-p20-workflow-1-measure-selfing-depth
series: self-structure
type: workflow
source_id: selfstr-p20
title: "measure selfing depth (attractor robustness, temporal span, field breadth, meta-selfing)"
created: 2026-02-27
---

# measure selfing depth

## steps
1. **define the field**
   - specify inputs/outputs and the feedback pathway(s)
2. **inventory traces**
   - what persists? for how long? (buffers, params, logs, learned norms)
3. **map weighting**
   - what histories matter more? is there meta-weighting?
4. **state constraints**
   - what must remain coherent/viable? what is pruned/penalized?
5. **run diagnostics**
   - apply `selfstr-p20-protocol-1-selfing-diagnostics`
6. **run perturbations**
   - apply `selfstr-p20-protocol-2-perturbation-suite`
7. **score depth on four axes**
   - attractor robustness
   - temporal span
   - field breadth
   - meta-selfing (can it evaluate/revise its own selfing dynamics?)
8. **summarize selfing profile**
   - none / minimal / episodic / robust + notes on scale (individual/dyad/collective)

## outputs
- a selfing profile sheet
- basin map + triggers
- recommended interventions (if desired): deepen, shallow, or reshape basins
