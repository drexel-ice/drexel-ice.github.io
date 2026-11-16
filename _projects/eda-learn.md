---
layout: page
title: "EDA-Learn: Open and Reproducible Machine Learning for Electronic Design Automation"
dropdown_label: EDA Learn
dropdown_children:
  - title: Benchmarks
    permalink: /eda-schema/
description: Learned models that predict expensive late-stage chip metrics from early design stages, and the open schema, dataset, and benchmarks that make machine learning for design automation reproducible.
img: assets/img/projects/ml-eda/cover.png
importance: 1
category: active
research_area: ml-eda
toc:
  sidebar: left
---

Digital physical design runs as a sequence of interdependent stages — logic synthesis,
floorplanning, placement, clock tree synthesis, routing, and signoff. Decisions taken early
determine the interconnect geometry, timing, power and routability that are only measured
accurately at the end, after routing and extraction. When the final numbers miss their
targets, the design returns to an earlier stage and the pipeline runs again, at a cost
measured in hours to days per pass.

This program works on the feedback problem that creates: **estimating a downstream outcome
from the information available at an earlier stage**, so that corrections can be made while
they are still cheap. The work began with graph neural networks for timing and parasitic
prediction, generalized them into a reusable framework, and then turned to a second problem
that limits the whole field — that most published results in machine learning for electronic
design automation (EDA) cannot be reproduced or fairly compared, because they depend on
proprietary tools, confidential designs, and incompatible data formats. Addressing that
required building open infrastructure: a standardized schema, a large open dataset, and a
public benchmark.

---

## The prediction problem

At any point in the flow, a designer has *source-stage* information and wants a *target-stage*
measurement that does not exist yet. Conventional estimators fill that gap with analytical
proxies — wireload models, half-perimeter wirelength, Steiner trees, congestion heuristics.
A learned predictor is trained to do the same job from the same early information, and both
are scored against the real post-routing measurement once the flow completes.

<div class="row justify-content-sm-center">
    <div class="col-sm-12 mt-3 mt-md-0">
        {% include figure.liquid path="assets/img/projects/ml-eda/prediction-vs-estimation.png" title="Conventional early estimation compared with machine learning prediction" class="img-fluid rounded z-depth-1" %}
    </div>
</div>
<div class="caption">
    Conventional early estimation and machine learning prediction of a downstream metric.
    Information available at an earlier source stage feeds both a conventional estimator and a
    learned predictor; each estimate is evaluated against the target-stage measurement, which is
    ground truth for scoring rather than an input at inference time.
</div>

Framing the problem this way matters for honesty as much as accuracy. Keeping the target-stage
measurement strictly out of the inputs is what prevents downstream information from leaking
into an early predictor and producing accuracy that would not survive real use.

---

## Representing circuits for learning

A circuit is natively relational, which makes graph representations a direct fit. The work
uses three, each matched to the granularity of the quantity being predicted: a **netlist
graph** of the whole circuit, **timing-path graphs** extracted from it as subgraphs for
per-path delay quantities, and an **interconnect graph** in which wire segments themselves
become nodes for spatial parasitic and wirelength prediction.

<div class="row justify-content-sm-center">
    <div class="col-sm-12 mt-3 mt-md-0">
        {% include figure.liquid path="assets/img/projects/ml-eda/circuit-graphs.png" title="Netlist graph and extracted timing-path graphs" class="img-fluid rounded z-depth-1" %}
    </div>
</div>
<div class="caption">
    A sample ISCAS'89 benchmark as (a) a netlist graph, with inputs, outputs and gates as typed
    nodes, and (b) the timing-path graphs extracted from it. Timing reports drive the extraction,
    so each subgraph isolates one signal's journey through the circuit.
</div>

Node features are drawn from the standard artifacts a flow already produces — design
constraints, LEF/DEF geometry, structural attributes such as logic level and fan-out, STA
timing reports, and SPEF parasitics — so nothing in the representation requires instrumenting
the tools.

---

## A generalized graph learning framework

The first prediction tasks were solved as separate pipelines. They were then unified into
**EDA-ML**, a task-agnostic framework in which any prediction is posed the same way: observe
stage *X*, predict metric *M* at stage *Y*, at a stated granularity. Dataset generation, graph
construction, and the training and evaluation flow are shared; what changes between tasks is
the graph representation, the prediction level, and the baseline the model must beat.

<div class="row justify-content-sm-center">
    <div class="col-sm-12 mt-3 mt-md-0">
        {% include figure.liquid path="assets/img/projects/ml-eda/graph-learning-framework.png" title="The generalized graph learning framework" class="img-fluid rounded z-depth-1" %}
    </div>
</div>
<div class="caption">
    The generalized framework for downstream metric prediction: an automated design flow
    produces the stored artifacts (netlist, timing reports, extracted parasitics), which are
    converted into netlist, timing-path and interconnect graphs, which in turn feed a common
    training and evaluation flow. Arrival time prediction and interconnect parasitic prediction
    are two instantiations of the same recipe.
</div>

Two results followed from the framework. Posing both arrival time and parasitic prediction
through one recipe showed the approach generalizes across tasks rather than being tuned per
problem — reported in the **EDA-ML** paper. And a model trained for one technology node can be
carried to a newer one by freezing its layers and fine-tuning a single appended layer on a
small amount of target-node data, instead of regenerating a dataset and retraining from
scratch — reported in the **transfer learning** paper. Both are linked under
[Publications](#publications), where the full results are reported.

---

## EDA-Schema: an open foundation

Better predictors are only half the problem. A model trained on a confidential dataset
produced by a commercial tool cannot be reproduced outside the group that built it, and its
reported accuracy cannot be meaningfully compared against a model trained on someone else's
private data. Published accuracy figures across the field are, for this reason, largely not
comparable to one another. **EDA-Schema** attacks that directly.

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
truth rather than from separately prepared datasets.

<div class="row justify-content-sm-center">
    <div class="col-sm-12 mt-3 mt-md-0">
        {% include figure.liquid path="assets/img/projects/ml-eda/netlist-graph.png" title="A circuit as a heterogeneous netlist graph" class="img-fluid rounded z-depth-1" %}
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

The dataset is produced by automating the OpenROAD flow over public benchmark circuits and
open process design kits, sweeping clock period, utilization, aspect ratio and other
parameters. The sweeps deliberately include **barely-passing and barely-failing operating
points**, so the data contains the marginal cases where prediction actually matters rather
than only comfortable ones. Nothing in the pipeline requires a commercial license or an NDA,
which is what makes the resulting data redistributable.

| | |
| --- | --- |
| Design instances | 7,776 (1,944 per PDK) |
| Benchmark circuits | 18 — 16 from IWLS'05, plus OpenCores and IBEX |
| Process design kits | Nangate 45 nm, SkyWater 130 nm, IHP SG13G2 130 nm, ASAP 7 nm |
| Design stages captured | Floorplan, global placement, detailed placement, CTS, global and detailed routing |
| Scale | 275 M+ gates, 75 M+ nets, 36 M+ extracted timing paths |
| Modalities | Circuit graphs, spatial layout images, scalar heatmaps, QoR metric entities |

A parallel standards effort is pushing the same representation toward industry adoption,
through both the **Si2 Schema Working Group** and the **Si2 Logic Block Composition (LBC)
Extend & Expand Working Group**, so that data means the same thing across tools, vendors and
labs.

---

## A public benchmark

On top of the dataset, EDA-Schema-V2 defines **twelve standardized prediction tasks**, each
with fixed evaluation metrics and the EDA tool's own estimate as the reference baseline.

| Prediction target | Granularity |
| --- | --- |
| Total area, total power, total wirelength | Whole circuit |
| Worst arrival time, worst slack, total negative slack | Whole circuit |
| Interconnect length | Per interconnect |
| Timing-path arrival time, timing-path slack | Per timing path |
| Net-arc delay | Per net arc |
| Cell-arc delay, cell-arc slew | Per cell arc |

Models are scored with **leave-one-circuit-out** evaluation, so a reported result reflects
generalization to a circuit the model has never seen rather than memorization of a familiar
one — a distinction that ordinary random splits obscure, because fragments of the same circuit
then appear in both training and test data.

Results are published to a [public leaderboard](https://drexel-ice.github.io/EDA-learn-leaderboard/),
which reports every released model against the tool baseline for each task, PDK and design
stage.

---

## Research arc

1. **2022–2023 — Establish the approach.** Graph neural networks predict post-routing gate
   arrival time and interconnect parasitics from earlier stages, with attention to the long
   tail where worst-case behavior lives.
2. **2024 — Generalize and migrate.** EDA-ML poses multiple prediction tasks through one
   framework, and transfer learning carries a trained model between technology nodes.
3. **2025 — Extend and survey.** A differentiable wirelength estimator is built to drop into
   gradient-based placement optimizers, and a survey of representation learning for EDA maps
   the field and names data standardization as its central bottleneck.
4. **2024–2026 — Build the infrastructure.** EDA-Schema and its multimodal successor
   EDA-Schema-V2 deliver an open schema, dataset and benchmark, carried toward an industry
   standard through the Si2 working groups.

What began as a set of better predictors became the public infrastructure needed to build and
fairly compare such predictors.

**Current directions.** Work is ongoing on *EDA-OpenML*, an open-weight framework for
reproducible and data-efficient neural prediction, and *EDA-AutoML*, which automates neural
architecture and hyperparameter selection — including an LLM-assisted approach to generating
model configurations from a task description. Results will be reported here as they are
published.

---

## Publications

Full methodology and quantitative results are in the papers below.

### Open data, schema, and benchmarks

- **EDA-Schema-V2: A Multimodal Schema, Open Datasets, and Benchmarks for Machine Learning in Digital Physical Design.**
  P. Shrestha, A. Aversa, I. Savidis. *arXiv:2605.06952*, 2026.
  [[PDF]]({{ '/assets/pdf/preprints/2605.06952v1.pdf' | relative_url }})
  — Extends the schema to graphs, images and heatmaps; releases the open dataset and the
  twelve-task benchmark.
- **EDA-Schema: A Graph Datamodel Schema and Open Dataset for Digital Design Automation.**
  P. Shrestha, A. Aversa, S. Phatharodom, I. Savidis. *GLSVLSI*, 2024. **Best Paper Award.**
  [[PDF]]({{ '/assets/pdf/conferences/GLSVLSI_2024-EDA-schema.pdf' | relative_url }})
  — The original property-graph data model and open dataset the rest of the infrastructure is
  built on.

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
  — A gradient-friendly replacement for HPWL that can sit inside a placement optimizer.
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
  — Spatial interconnect graphs for post-routing capacitance, with the gains concentrated on
  the worst nets.
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
