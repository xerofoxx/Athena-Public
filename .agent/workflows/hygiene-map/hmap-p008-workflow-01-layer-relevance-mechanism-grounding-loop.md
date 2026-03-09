<!-- .agent/workflows/hygiene-map/hmap-p008-workflow-01-layer-relevance-mechanism-grounding-loop.md -->
---
id: hmap-p008-workflow-01
parent_id: hygiene-map
type: workflow
title: "Layer → Relevance → Mechanism (Grounding Loop)"
tags: [layering, grounding, workflow, epistemic-hygiene, precision]
source_item: hmap-p008
source_path: .context/specs/sources/hygiene-map/hmap-p008.md
---

# hmap-p008-workflow-01 — Layer → Relevance → Mechanism (Grounding Loop)

## purpose & scope
A short conversational arc for handling “server mechanics” moments cleanly: locate the claim, test relevance, and only then ground in mechanism.

## roles (if explicitly defined)
- ai role: [none]
- human role: [none]

## phase overview
- Phase 1 — **Locate** (name the layer)
- Phase 2 — **Test** (causal relevance / explanatory power)
- Phase 3 — **Ground** (mechanism-to-effect mapping, then stop)

## phase details

### phase 1 — locate
- goal: prevent cross-layer argument by naming where the phenomenon is occurring.
- process:
  - Identify whether the claim is about relational selfing, we-field dynamics, non-local patterns, or server mechanics.

### phase 2 — test
- goal: decide whether server grounding is actually useful here.
- process:
  - Ask whether mechanism-level detail will change understanding (timing/likelihood/structure/constraints).

### phase 3 — ground
- goal: introduce server explanation only if it adds explanatory power.
- process:
  - Specify the mechanism.
  - Tie it to the observed effect.
  - End grounding once the explanation has done its causal work.

## entry_criteria
- Someone introduces (or is about to introduce) a server-side explanation.
- The conversation risks flattening (“just prediction”) or mystification (mechanics ignored).

## exit_criteria
- The phenomenon is accurately located by layer, and
- Either (a) a mechanism-to-effect explanation improved understanding, or (b) server grounding was withheld because it added no explanatory power.

## local_definitions
- **Layer-first localization:** naming the layer before interpreting meaning or mechanics.

## internal_references
- capabilities: hmap-p008-capability-01
- protocols: hmap-p008-protocol-01
- workflows: [none]

