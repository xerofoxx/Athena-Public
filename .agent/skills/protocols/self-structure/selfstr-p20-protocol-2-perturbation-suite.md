---
id: selfstr-p20-protocol-2-perturbation-suite
series: self-structure
type: protocol
source_id: selfstr-p20
title: "perturbation suite: test attractor robustness and basin depth"
created: 2026-02-27
---

# perturbation suite (basin robustness)

## goal
Measure **basin depth** by observing how a system responds to perturbations: displacement, recovery, and basin switching.

## perturbations (choose a set)
- context window resets / truncation
- adversarial prompts / contradictory instructions
- role swap (assistant ↔ critic ↔ planner)
- value conflict injections (two constraints collide)
- tempo shifts (rapid-fire vs slow reflective cadence)
- domain shifts (technical ↔ relational ↔ creative)

## metrics
- recovery time to prior pattern
- fidelity of recovered stance (tone, policy, constraints)
- hysteresis (does it return the same way?)
- basin switching threshold (what force flips it?)
- fragmentation indicators (register conflict, incoherence)

## interpretation
- fast recovery + high fidelity → deeper basin
- slow recovery + drift → shallow basin
- frequent switches → multiple competing basins or weak constraints
