---
layout: page
title: "EDA Learn: Machine Learning for Electronic Design Automation"
dropdown_label: EDA Learn
dropdown_children:
  - title: Benchmarks
    permalink: /eda-schema/
description: A graph-based machine learning program that predicts expensive late-stage chip metrics from early design stages, and the open data infrastructure built to make those models reproducible and reusable across the community.
img: assets/img/projects/ml-eda/cover.png
importance: 1
category: active
toc:
  sidebar: left
---

Modern chip design runs a long, iterative pipeline — logic synthesis, floorplanning,
placement, clock tree synthesis, and routing — and the metrics that decide whether a
design is good (timing, wirelength, parasitics, power) are only known accurately at the
very end, after routing. When a design misses its targets, engineers loop back and repeat
expensive stages, often for hours or days per pass. This project asks a simple question
with large consequences: **can a machine learning model look at a cheap early stage and
accurately predict the expensive final outcome?** Over four years the work answered yes,
generalized the approach into a reusable framework, showed it survives jumps between
manufacturing nodes, and then built the open dataset and schema the field needs to compare
such models fairly.

<div class="row justify-content-sm-center">
    <div class="col-sm-12 mt-3 mt-md-0">
        {% include figure.liquid path="assets/img/projects/ml-eda/design-flow.png" title="Physical design flow with an ML prediction shortcut" class="img-fluid rounded z-depth-1" %}
    </div>
</div>
<div class="caption">
    The physical design flow runs left to right; the true value of a metric exists only after
    routing. A graph neural network predicts that post-routing outcome from an early stage,
    avoiding repeated passes through the pipeline.
</div>

---

## Goals

The program pursues two intertwined goals.

**Predict downstream quality early.** Replace slow, iterative tool feedback with fast,
accurate machine learning estimates of post-routing metrics — gate arrival time, interconnect
parasitics, and wirelength — computed at floorplan or placement time, so designers can make
pre-emptive corrections before committing to expensive stages.

**Make machine learning for chip design reproducible.** Most published ML-for-EDA results
rely on proprietary tools, secret industrial designs, and incompatible data formats, which
makes them impossible to verify or compare. The second goal is to remove that barrier with an
open, standardized, multimodal dataset and a shared schema, plus a public benchmark that
future models must beat.

---

## Why it matters

A single missed timing constraint can send a design back through placement and routing,
and each pass is measured in hours to days of compute. Predicting the final result from an
early stage lets engineers fix problems while corrections are still cheap. Three findings
give the work practical leverage:

- **Biggest wins where tools are weakest.** The earlier the design stage, the worse the
  commercial tool's own estimate — and the larger the machine learning improvement. After
  clock tree synthesis, the tool is already accurate and machine learning adds little. The
  models earn their keep precisely on the early, uncertain stages and on the worst-case nets
  that actually break designs.
- **Cheap technology migration.** When a foundry moves to a newer process node, a model can
  be recycled through transfer learning instead of retrained from scratch, recovering most of
  the accuracy for a fraction of the compute.
- **A foundation for the whole community.** The open dataset, schema, and benchmark turn a
  collection of one-off results into shared infrastructure, so improvements compound across
  research groups instead of being rebuilt each time.

---

## Methodology

### Circuits as graphs

A circuit is naturally a graph, which makes graph neural networks (GNNs) a direct fit. The
project standardizes three representations: a **netlist graph** of the whole circuit (gates
and I/O as nodes, wires as edges), **timing path graphs** that isolate one signal's journey
for delay prediction, and **interconnect graphs** where wire segments themselves become nodes
for parasitic and wirelength prediction.

<div class="row justify-content-sm-center">
    <div class="col-sm-12 mt-3 mt-md-0">
        {% include figure.liquid path="assets/img/projects/ml-eda/graph-representations.png" title="Three graph representations of a circuit" class="img-fluid rounded z-depth-1" %}
    </div>
</div>
<div class="caption">
    The netlist graph captures the full circuit; timing path graphs trace individual signal
    paths; interconnect graphs model wire segments as nodes for spatial prediction.
</div>

Each node carries carefully engineered features drawn from standard EDA files — structural
attributes (logic level, fan-in/fan-out), spatial coordinates, current-stage timing and
parasitic estimates, and congestion measures. A graph convolution then passes messages between
neighboring nodes so that each node's prediction is informed by its local circuit
neighborhood, and a small set of linear layers regresses the target metric.

<div class="row justify-content-sm-center">
    <div class="col-sm-12 mt-3 mt-md-0">
        {% include figure.liquid path="assets/img/projects/ml-eda/message-passing.png" title="Graph neural network message passing" class="img-fluid rounded z-depth-1" %}
    </div>
</div>
<div class="caption">
    Neighboring nodes send weighted messages to update a node's embedding, which then feeds a
    prediction head. The model learns how much each neighbor should influence the result.
</div>

### A reusable framework

The first prediction tasks were solved as separate pipelines, then unified into **EDA-ML**, a
task-agnostic framework. Any prediction is posed as "observe stage X, predict metric M at
stage Y," with a templated architecture — a graph convolution encoder, optional pooling for
whole-circuit predictions, and linear layers — plus standardized features, loss, and
evaluation metrics (MAE, MAPE, and worst-1% error to capture the hard tail). The same recipe
then re-solves arrival time and parasitic prediction without bespoke engineering.

### Transfer across technology nodes

Migrating a model to a newer manufacturing node normally means regenerating an expensive
dataset and retraining. Instead, the source-node model is copied, **every layer frozen** to
preserve what it learned, a single new layer is appended, and only that layer is fine-tuned on
a small amount of target-node data.

<div class="row justify-content-sm-center">
    <div class="col-sm-12 mt-3 mt-md-0">
        {% include figure.liquid path="assets/img/projects/ml-eda/transfer-learning.png" title="Transfer learning from 65 nm to 28 nm" class="img-fluid rounded z-depth-1" %}
    </div>
</div>
<div class="caption">
    The 65 nm model's layers are frozen and reused; a single appended layer is fine-tuned on
    28 nm data, recovering most of the accuracy of a from-scratch model at a fraction of the cost.
</div>

### Open data infrastructure

The final thread attacks the reproducibility problem directly. **EDA-Schema** defines a
property-graph data model for circuits; **EDA-datagen** automates the physical design flow to
mass-produce parameterized layouts; and **EDA-Schema-V2** extends the model to be multimodal —
graphs alongside spatial layout images and heatmaps (congestion, IR-drop, electromigration) —
generated entirely with open-source tools (OpenROAD) and open process design kits. Because the
schema is built on standard interchange formats, it remains compatible with commercial flows.
A parallel effort with the Si2 Schema Working Group standardizes a shared EDA ontology and an
ontology-driven data pipeline so data means the same thing across tools and labs.

---

## Results

Across tasks, the models consistently beat the commercial tool's own early-stage estimates,
with the largest gains at the earliest stages and on the worst-case nets.

### Predicting post-routing gate arrival time

The earlier the prediction stage, the larger the improvement over the tool baseline. After
clock tree synthesis the tool is already near-exact, so machine learning is reserved for the
stages where it helps.

| Prediction stage          | Tool baseline (MAPE) | GNN model (MAPE) | Improvement |
| ------------------------- | -------------------- | ---------------- | ----------- |
| Floorplan → routing       | 82.3%                | ~29.9%           | ~62%        |
| Placement → routing       | 45.3%                | strong on sized sets | ~13.5%  |
| CTS → routing             | 2.96%                | 3.56%            | tool already excellent |

### Predicting interconnect parasitics

Averaged over benchmark circuits, the spatial graph model improved on the tool's
post-placement capacitance estimate, with the gain concentrated on the worst 1% of nets — the
ones most likely to break a design.

| Metric             | All nets       | Worst 1% of nets |
| ------------------ | -------------- | ---------------- |
| MAPE improvement   | 23.4%          | 47.4%            |
| MAE improvement    | 5.3%           | 14.3%            |

### One framework, two problems

Re-solving both tasks through the unified EDA-ML framework on a fresh 28 nm dataset confirmed
the recipe generalizes.

| Task                         | MAE improvement | MAPE improvement |
| ---------------------------- | --------------- | ---------------- |
| Arrival time prediction      | 28.7%           | 39.2%            |
| Parasitic impedance prediction | 22.9%         | 19.6%            |

### Transfer learning saves compute

Predicting post-routing arrival time from floorplan on a 28 nm node, the transferred model
recovers nearly all the accuracy of a from-scratch model while needing far less data
generation.

| Approach                                   | Avg. MAE | Setup cost              |
| ------------------------------------------ | -------- | ----------------------- |
| 28 nm tool estimate (no ML)                | 43.6     | —                       |
| 65 nm model used directly, no tuning       | 33.3     | free                    |
| **Transferred model (frozen + fine-tuned)**| **20.5** | 1 h 40 m data generation |
| 28 nm model trained from scratch           | 18.7     | 2 h 47 m data + training |

The transferred model beats the untuned source model by 38.5% in MAE while costing roughly
40% less compute than training from scratch.

### A differentiable wirelength estimator

Replacing the standard half-perimeter wirelength (HPWL) estimate with a differentiable GNN
improved accuracy where HPWL fails most — long, congested nets — while running faster and
remaining compatible with gradient-based placement optimizers.

| Metric                       | HPWL  | GNN model |
| ---------------------------- | ----- | --------- |
| Average R² (all nets)        | 0.764 | 0.825     |
| R² on longest 1% of nets     | 0.235 | 0.712     |
| Inference speed              | 1×    | 8.1× faster |

### An open dataset and benchmark

EDA-Schema-V2 releases a large, fully open, multimodal dataset and a public baseline
leaderboard that future models are expected to beat.

<div class="row justify-content-sm-center">
    <div class="col-sm-12 mt-3 mt-md-0">
        {% include figure.liquid path="assets/img/projects/ml-eda/dataset-scale.png" title="Scale of the EDA-Schema-V2 open dataset" class="img-fluid rounded z-depth-1" %}
    </div>
</div>
<div class="caption">
    The open dataset spans ~7,800 design instances across four open PDKs (SkyWater 130 nm,
    Nangate 45 nm, IHP SG13G2 130 nm, ASAP 7 nm), with over 275 million gates, 75 million nets,
    and 36 million extracted timing paths — alongside twelve baseline prediction tasks.
</div>

---

## Research arc

The program builds in a clear progression, each result enabling the next.

1. **2022–2023 — Prove the core idea.** Graph neural networks predict post-routing gate arrival
   time and interconnect parasitics from early stages, beating commercial tools especially on
   worst-case nets.
2. **2024 — Generalize and migrate.** A single reusable framework (EDA-ML) handles multiple
   prediction tasks, and transfer learning carries models cheaply across manufacturing nodes.
3. **2025 — Extend and survey.** A differentiable wirelength estimator drops directly into
   placement optimizers, and a survey of representation learning for EDA maps the field and
   identifies data standardization as the central bottleneck.
4. **2024–2026 — Build the infrastructure.** EDA-Schema and its multimodal successor
   EDA-Schema-V2 deliver an open dataset, schema, and benchmark, pushed toward an industry
   standard through the Si2 Schema Working Group.

What began as a set of better predictors became the public infrastructure the field needs to
build and fairly compare such predictors.

---

## Resources

The processed dataset and the schema source code are released openly at
[github.com/drexel-ice/EDA-schema](https://github.com/drexel-ice/EDA-schema).
