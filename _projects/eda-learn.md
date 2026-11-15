---
layout: page
title: "EDA-Learn: Open and Reproducible Machine Learning for Electronic Design Automation"
dropdown_label: EDA Learn
dropdown_children:
  - title: Benchmarks
    permalink: /eda-schema/
description: A multi-year program that predicts expensive late-stage chip metrics from early design stages using graph neural networks, and builds the open schema, dataset, and benchmarks that make such models reproducible and comparable across the community.
img: assets/img/projects/ml-eda/cover.png
importance: 1
category: active
research_area: ml-eda
toc:
  sidebar: left
---

Modern chip design runs a long, iterative pipeline — logic synthesis, floorplanning,
placement, clock tree synthesis, and routing — and the metrics that decide whether a
design is good (timing, wirelength, parasitics, power) are only known accurately at the
very end, after routing. When a design misses its targets, engineers loop back and repeat
expensive stages, often for hours or days per pass. This program asks a simple question
with large consequences: **can a machine learning model look at a cheap early stage and
accurately predict the expensive final outcome?**

Over four years the work answered yes, generalized the approach into a reusable framework,
showed it survives jumps between manufacturing nodes — and then confronted the problem that
made those results hard for anyone else to build on. Most published machine learning results
for electronic design automation (EDA) depend on proprietary tools, confidential industrial
designs, and incompatible data formats. Accuracy on one private dataset says little about
whether a model can be reproduced, compared fairly against another, or applied to a circuit
it has never seen. The second half of the program therefore built the open data
infrastructure the field needs: a standardized schema, a large open dataset, and a public
benchmark.

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

**Make machine learning for chip design reproducible.** Remove the barrier of proprietary
tools and secret datasets with an open, standardized, multimodal schema and dataset, plus a
public benchmark that future models must beat.

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
- **A foundation for the whole community.** The open schema, dataset, and benchmark turn a
  collection of one-off results into shared infrastructure, so improvements compound across
  research groups instead of being rebuilt each time.

---

## Methodology

### Circuits as graphs

A circuit is naturally a graph, which makes graph neural networks (GNNs) a direct fit. The
program standardizes three representations: a **netlist graph** of the whole circuit (gates
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

---

## EDA-Schema: an open foundation

Better predictors are only half the problem. A model trained on a confidential 28 nm dataset
produced by a commercial tool cannot be reproduced by anyone outside the group that built it,
and its reported accuracy cannot be meaningfully compared against a model trained on someone
else's private data. **EDA-Schema** attacks that directly.

### A schema for the whole design flow

EDA-Schema defines a stage-aware **property-graph data model** for digital circuits spanning
synthesis through detailed routing. At every stage, structural netlists, timing reports,
parasitic extraction, layout geometry, power delivery analysis, and quality-of-results (QoR)
metrics are parsed out of the standard tool outputs and organized into one consistent
representation.

<div class="row justify-content-sm-center">
    <div class="col-sm-12 mt-3 mt-md-0">
        {% include figure.liquid path="assets/img/projects/ml-eda/schema-er-diagram.png" title="EDA-Schema-V2 entity relationship diagram" class="img-fluid rounded z-depth-1" %}
    </div>
</div>
<div class="caption">
    The EDA-Schema-V2 entity relationship diagram. Yellow entities capture the design flow
    hierarchy (flow, stage, constraints); blue entities hold structural design data — netlist,
    clock tree, timing path, power delivery network, and their constituent gates, nets, pins and
    arcs; green entities record quality-of-results metrics for cell, area, power, timing and
    routability.
</div>

Because the schema is derived from standard interchange formats (LEF/DEF, SPEF, Liberty, STA
reports), it stays compatible with commercial flows even though the reference dataset is
generated entirely with open tools.

### Multimodal by design

A circuit is not only a graph. EDA-Schema-V2 extends the model so that each design instance
carries **graphs, spatial layout images, and scalar heatmaps** side by side, which lets graph
networks, convolutional networks, and hybrid architectures all train from the same source of
truth.

<div class="row justify-content-sm-center">
    <div class="col-sm-12 mt-3 mt-md-0">
        {% include figure.liquid path="assets/img/projects/ml-eda/netlist-graph.png" title="A sample circuit represented as a netlist graph" class="img-fluid rounded z-depth-1" %}
    </div>
</div>
<div class="caption">
    The graph modality: a circuit as a heterogeneous netlist graph, with I/O ports, gates, nets
    and pins as typed nodes and the logical and physical connections between them as edges.
</div>

<div class="row justify-content-sm-center">
    <div class="col-sm-12 mt-3 mt-md-0">
        {% include figure.liquid path="assets/img/projects/ml-eda/spatial-modalities.png" title="Binary spatial maps of the circuit layout" class="img-fluid rounded z-depth-1" %}
    </div>
</div>
<div class="caption">
    The image modality, for the <code>ac97_ctrl</code> circuit on the Nangate 45 nm node:
    (a) combinational cell placement, (b) sequential cell placement, (c) pin locations,
    (d) overall routing, (e) metal 1 routing, (f) metal 5 routing. Pixel size is fixed to the
    minimum width of metal 1, so the maps scale consistently across technology nodes.
</div>

<div class="row justify-content-sm-center">
    <div class="col-sm-12 mt-3 mt-md-0">
        {% include figure.liquid path="assets/img/projects/ml-eda/routability-maps.png" title="RUDY routability heatmaps" class="img-fluid rounded z-depth-1" %}
    </div>
</div>
<div class="caption">
    The heatmap modality: Rectangular Uniform wire DensitY (RUDY) routability maps —
    (a) net-based, (b) pin-based, (c) long-range and (d) short-range — which estimate routing
    demand across the layout before routing is run. The schema also stores IR-drop and
    electromigration heatmaps for the power delivery network.
</div>

### Generated with open tools, end to end

**EDA-datagen** automates the OpenROAD physical design flow to mass-produce parameterized
layouts, sweeping clock period, utilization, aspect ratio and other knobs — including
deliberately *barely-passing* and *barely-failing* operating points, so the dataset contains
the marginal cases that matter rather than only comfortable ones. Nothing in the pipeline
requires a commercial license or an NDA.

A parallel standards effort is pushing the same representation toward industry adoption,
through both the **Si2 Schema Working Group** and the **Si2 Logic Block Composition (LBC)
Extend & Expand Working Group**, so that data means the same thing across tools, vendors and
labs.

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

### The open dataset

EDA-Schema-V2 releases a large, fully open, multimodal dataset generated with OpenROAD across
four open process design kits.

<div class="row justify-content-sm-center">
    <div class="col-sm-12 mt-3 mt-md-0">
        {% include figure.liquid path="assets/img/projects/ml-eda/dataset-scale.png" title="Scale of the EDA-Schema-V2 open dataset" class="img-fluid rounded z-depth-1" %}
    </div>
</div>

| | |
| --- | --- |
| Design instances | **7,776** (1,944 per PDK) |
| Benchmark circuits | 18 — 16 from IWLS'05, plus OpenCores and IBEX |
| Process design kits | Nangate 45 nm, SkyWater 130 nm, IHP SG13G2 130 nm, ASAP 7 nm |
| Design stages captured | Floorplan, global placement, detailed placement, CTS, global and detailed routing |
| Scale | 275 M+ gates, 75 M+ nets, 36 M+ extracted timing paths |
| Modalities | Circuit graphs, spatial layout images, scalar heatmaps, QoR metric entities |

### A public benchmark

On top of the dataset, EDA-Schema-V2 defines **twelve standardized prediction tasks** with
fixed evaluation metrics and the EDA tool's own estimate as the reference baseline. Models are
scored with leave-one-circuit-out evaluation, so a result reflects generalization to a circuit
the model has never seen rather than memorization of a familiar one.

| Prediction target | Granularity |
| --- | --- |
| Total area, total power, total wirelength | Whole circuit |
| Worst arrival time, worst slack, total negative slack | Whole circuit |
| Interconnect length | Per interconnect |
| Timing-path arrival time, timing-path slack | Per timing path |
| Net-arc delay | Per net arc |
| Cell-arc delay, cell-arc slew | Per cell arc |

Results are published to a [public leaderboard](https://drexel-ice.github.io/EDA-learn-leaderboard/),
which reports every released model against the tool baseline for each task, PDK and design
stage combination.

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
   EDA-Schema-V2 deliver an open schema, dataset and benchmark, pushed toward an industry
   standard through the Si2 Schema Working Group.

What began as a set of better predictors became the public infrastructure the field needs to
build and fairly compare such predictors.

**Current directions.** Work is ongoing on *EDA-OpenML*, an open-weight framework for
reproducible and data-efficient neural prediction, and *EDA-AutoML*, which automates neural
architecture and hyperparameter selection — including an LLM-assisted approach to generating
model configurations directly from a task description. Results will be reported here as they
are published.

---

## Publications

### Open data, schema, and benchmarks

- **EDA-Schema-V2: A Multimodal Schema, Open Datasets, and Benchmarks for Machine Learning in Digital Physical Design.**
  P. Shrestha, A. Aversa, I. Savidis. *arXiv:2605.06952*, 2026.
  [[PDF]]({{ '/assets/pdf/preprints/2605.06952v1.pdf' | relative_url }})
  — Extends the schema to graphs, images and heatmaps; releases the 7,776-instance open dataset
  and the twelve-task benchmark.
- **EDA-Schema: A Graph Datamodel Schema and Open Dataset for Digital Design Automation.**
  P. Shrestha, A. Aversa, S. Phatharodom, I. Savidis. *GLSVLSI*, 2024. **Best Paper Award.**
  [[PDF]]({{ '/assets/pdf/conferences/GLSVLSI_2024-EDA-schema.pdf' | relative_url }})
  — The original property-graph data model and open dataset that the rest of the infrastructure
  is built on.

### Surveys and position papers

- **Representation Learning for Digital Integrated Circuit Design Automation.**
  P. Shrestha, I. Savidis. *ICCD*, 2025.
  [[PDF]]({{ '/assets/pdf/conferences/ICCD_2025-representation.pdf' | relative_url }})
- **Deep Representation Learning for Electronic Design Automation.**
  P. Shrestha, S. Phatharodom, A. Aversa, D. Blankenship, Z. Wu, I. Savidis. *arXiv:2505.02105*, 2025.
  [[PDF]]({{ '/assets/pdf/preprints/2505.02105v1.pdf' | relative_url }})
  — Maps the field and identifies data standardization as its central bottleneck.

### Prediction models and frameworks

- **Differentiable Graph Neural Networks for Wirelength Estimation.**
  Z. Wu, P. Shrestha, S. Phatharodom, I. Savidis. *ISCAS*, 2025.
  [[PDF]]({{ '/assets/pdf/conferences/ISCAS_2025-differentiable.pdf' | relative_url }})
  — A drop-in, gradient-friendly replacement for HPWL inside placement optimizers.
- **EDA-ML: Graph Representation Learning Framework for Digital IC Design Automation.**
  P. Shrestha, I. Savidis. *ISQED*, 2024.
  [[PDF]]({{ '/assets/pdf/conferences/ISQED_2024.pdf' | relative_url }})
  — Generalizes the one-off models into a single task-agnostic recipe.
- **Transfer Learning of Arrival Time Prediction Models from a 65 nm to a 28 nm Process Node.**
  P. Shrestha, I. Savidis. *DCAS*, 2024.
  [[PDF]]({{ '/assets/pdf/conferences/DCAS_2024.pdf' | relative_url }})
  — Recycles a trained model across technology nodes instead of retraining from scratch.
- **Graph Representation Learning for Parasitic Impedance Prediction of the Interconnect.**
  P. Shrestha, I. Savidis. *ISCAS*, 2023.
  [[PDF]]({{ '/assets/pdf/conferences/ISCAS_2023-parasitic.pdf' | relative_url }})
  — Largest gains on the worst 1% of nets, the ones that break designs.
- **Modeling Graph Neural Networks for Gate Level Arrival Time Prediction of Long Tailed Datasets.**
  P. Shrestha, S. Phatharodom, I. Savidis. *GOMACTech*, 2023.
  [[PDF]]({{ '/assets/pdf/conferences/GOMACTech_2023.pdf' | relative_url }})
  — Handling the heavy tail that dominates worst-case timing.
- **Graph Representation Learning for Gate Arrival Time Prediction.**
  P. Shrestha, S. Phatharodom, I. Savidis. *MLCAD*, 2022.
  [[PDF]]({{ '/assets/pdf/conferences/MLCAD_2022.pdf' | relative_url }})
  — The paper that started the program.

### Related

- **Emerging ML-AI Techniques for Analog and RF EDA.**
  Z. Wu, Z. Chen, N. Achebe, V. V. Rao, P. Shrestha, I. Savidis. *arXiv:2506.00007*, 2025.
  [[PDF]]({{ '/assets/pdf/preprints/2506.00007v1.pdf' | relative_url }})

---

## Talks and standards engagement

- **EDA-Schema-V2: A Multimodal Schema, Open Datasets, and Benchmarks for Machine Learning in Digital Physical Design.**
  P. Shrestha, A. Aversa, I. Savidis — Si2 Logic Block Composition (LBC) Extend & Expand Working Group, 2026.
  [[Slides]]({{ '/assets/pdf/presentations/Si2_LBC-EDA-schema-V2.pdf' | relative_url }})
- **Standardizing Data Formats for Open-Source Model Sharing and Benchmarking.**
  I. Savidis — Birds-of-a-Feather session, Design Automation Conference (DAC), 2025.
  [[Slides]]({{ '/assets/pdf/presentations/DAC_BoF_2025-standardizing-data.pdf' | relative_url }})
- **EDA-Schema: An Open Graph Datamodel Schema and Dataset for Design Automation.**
  I. Savidis — Birds-of-a-Feather session, Design Automation Conference (DAC), 2024.
  [[Slides]]({{ '/assets/pdf/presentations/DAC_BoF_2024-EDA-schema.pdf' | relative_url }})

---

## Code and data

- **[EDA-Schema](https://github.com/drexel-ice/EDA-schema)** — the schema implementation,
  query and visualization tooling, and dataset loaders, with a columnar ParquetDB backend for
  large-scale use. Released under CC BY-NC-SA 4.0.
- **[EDA-Learn leaderboard](https://drexel-ice.github.io/EDA-learn-leaderboard/)** — released
  models and evaluation results for each benchmark task, PDK and design stage, scored against
  the OpenROAD reference baseline.
- **Open dataset** — download links and the full dataset specification are maintained in the
  [EDA-Schema repository](https://github.com/drexel-ice/EDA-schema#open-dataset).
