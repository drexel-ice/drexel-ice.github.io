---
layout: page
title: EDA-Learn
dropdown_label: EDA Learn
dropdown_children:
  - title: EDA-Schema
    permalink: /eda-schema/
  - title: EDA-OpenML
    permalink: /eda-openml/
description: Open and Reproducible Machine Learning for Electronic Design Automation
img: assets/img/projects/ml-eda/cover.png
importance: 1
category: active
research_area: ml-eda
toc:
  sidebar: left
---

**EDA-Learn** is an integrated research ecosystem from Drexel ICE for reproducible machine
learning in electronic design automation, spanning design data, model development and
evaluation.

It has three main components:

1. **EDA-Schema** — RTL-to-GDSII generation, a stage-aware multimodal representation, datasets
   and twelve benchmark tasks. 4 PDKs × 108 configs, ~320 GB. **Public today.**
2. **EDA-ML / AutoML** — configuration-driven model development, optimization and evaluation
   against those tasks. *In development.*
3. **Leaderboard** — standardized comparison, every result tied to its dataset, task, config
   and artifact. **Live**, seeded with the EDA-OpenML results.

<div class="row justify-content-sm-center">
    <div class="col-sm-12 mt-3 mt-md-0">
        {% include figure.liquid path="assets/img/projects/ml-eda/eda-learn-ecosystem.svg" alt="Diagram of the EDA-Learn ecosystem, linking its data, modelling and evaluation components to the users and infrastructure around them." title="The EDA-Learn technical ecosystem" class="img-fluid rounded z-depth-1" zoomable=true %}
    </div>
</div>

---

## Downstream Metric Prediction

Physical design runs as a sequence of stages, and the metrics that decide whether a design
closes — wirelength, delay, slack, power, area — are only measured accurately near the end.
The prediction problem is to estimate a **target-stage** measurement from the information
already available at an earlier **source stage**.

Conventional tools answer it with analytical proxies. A learned predictor answers it from the
same early information, and both are scored against the measurement the flow eventually
produces — a measurement that never enters either one's inputs.

<div class="row justify-content-sm-center">
    <div class="col-sm-12 mt-3 mt-md-0">
        {% include figure.liquid path="assets/img/projects/ml-eda/prediction-problem.svg" alt="Diagram contrasting a conventional analytical estimate with a learned predictor: both read the same source-stage features, and both are scored against the measurement the flow eventually produces." title="Conventional early estimation compared with machine learning prediction" class="img-fluid rounded z-depth-1" zoomable=true %}
    </div>
</div>

<div class="caption">
    Both estimators read the same source-stage features and are scored against the same
    target-stage measurement, which is ground truth for scoring rather than an input at
    inference time.
</div>

EDA-Learn works on **twelve such problems**, spanning five levels of granularity. Each is
scored against OpenROAD's own early estimate of the detailed-route value, so the tool's
estimate is the baseline a model has to beat.

- **Circuit-level QoR:** total area, total power, total wirelength
- **Net-level routing:** interconnect wirelength
- **Design-level timing:** worst arrival time, worst slack, total negative slack
- **Path-level timing:** timing-path arrival time, timing-path slack
- **Arc-level timing:** net-arc delay, cell-arc delay, cell-arc slew

---

## EDA-Schema: Open Data and Standardized Benchmarks

EDA-Schema-V2 provides a unified, **stage-aware data model** for digital IC physical design, organizing circuit structure, physical layouts, and quality-of-results (QoR) metrics across the design flow, from synthesis through detailed routing.

<div class="row justify-content-sm-center">
    <div class="col-sm-9 mt-3 mt-md-0">
        {% include figure.liquid path="assets/img/projects/ml-eda/schema-er-diagram.png" alt="Entity relationship diagram of the EDA-Schema-V2 data model, with design-flow, structural and quality-of-results entities grouped by colour." title="The EDA-Schema-V2 data model" class="img-fluid rounded z-depth-1" zoomable=true %}
    </div>
</div>

<div class="caption">
    EDA-Schema-V2 data model: yellow entities represent the design flow hierarchy, blue entities capture circuit structure, and green entities store quality-of-results metrics.
</div>

- **Open dataset:** 7,776 physical design instances
  - 18 benchmark circuits across four open PDKs
  - Nangate 45 nm, SkyWater 130 nm, IHP SG13G2 130 nm, ASAP7 7 nm
  - Variations in clock period, core utilization and aspect ratio
  - Both timing-clean and timing-violating implementations
  - 275 M+ gates (82 M+ excluding fillers), 75 M+ nets, 36 M+ timing paths
  - ~320 GB of processed data

- **Multimodal data:** circuit graphs, spatial layout images and scalar heatmaps
  - Logical connectivity, physical geometry and electrical characteristics
  - Supports graph-based, image-based and multimodal learning

<div class="row justify-content-sm-center">
    <div class="col-sm-12 mt-3 mt-md-0">
        {% include figure.liquid path="assets/img/projects/ml-eda/spatial-modalities.png" alt="Six binary layout maps of the same circuit: combinational cell placement, sequential cell placement, pin locations, overall routing, metal 1 routing and metal 5 routing." title="Binary spatial maps of the circuit layout" class="img-fluid rounded z-depth-1" zoomable=true %}
    </div>
</div>

<div class="caption">
    Spatial representations of <code>ac97_ctrl</code> using Nangate 45 nm: (a) combinational cell placement, (b) sequential cell placement, (c) pin locations, (d) overall routing, (e) metal 1 routing, and (f) metal 5 routing.
</div>

- **Standardized benchmarks:** each task fixes what is predicted, from where, and how it is scored
  - Source stage, target stage, and the entity each sample refers to
  - MAE, MAPE and R², plus upper-tail error on the P95 and worst-5 subsets
  - Timing tasks add over- and under-estimation and true positive / negative rates
  - Leave-one-circuit-out evaluation, so a score refers to a circuit held out entirely

- **Reference baselines:** the EDA tool's own stage-specific estimate is stored beside every target
  - Every task, PDK and stage pair has a published error to beat
  - Makes "better than the tool" a measurable claim rather than an assertion

→ **[Data model, modalities, benchmark tasks and baseline errors]({{ '/eda-schema/' | relative_url }})**

---

## EDA-OpenML: Rapid Model Prototyping and Reproducible Evaluation

EDA-OpenML is an open-source, open-weight framework for **rapidly prototyping neural predictors** on the EDA-Schema benchmarks. A predictor is written as a single executable configuration, trained and scored under one circuit-disjoint protocol, and released with everything needed to reproduce it.

<div class="row justify-content-sm-center">
    <div class="col-sm-12 mt-3 mt-md-0">
        {% include figure.liquid path="assets/img/projects/ml-eda/openml-config-flow.svg" alt="Diagram: a YAML configuration file feeds the EDA-ML library, which parses it, builds and trains the model across eighteen folds and evaluates it, producing a released package and a leaderboard entry." title="One configuration file in, a released model package out" class="img-fluid rounded z-depth-1" zoomable=true %}
    </div>
</div>

<div class="caption">
    A complete predictor for post-route interconnect length from global placement. A problem is taken from the EDA-Schema benchmark and written as one configuration file; EDA-ML parses it, builds and trains the model across eighteen leave-one-circuit-out folds, and scores it against the EDA tool's own estimate; the run is released as one directory holding everything needed to reproduce or reuse it.
</div>

- **Executable configuration:** one YAML file specifies the entire predictor
  - Prediction problem: PDK, source and target stages, target quantity, EDA baseline
  - Ordered input features drawn from the EDA-Schema source entities
  - Network architecture, training hyperparameters and preprocessing
  - Parsed directly to build, train and evaluate the model, with no reimplementation

- **Circuit-disjoint evaluation:** leave-one-circuit-out cross-validation
  - Each of the eighteen benchmark circuits is withheld in turn
  - Fold-averaged metrics weight every circuit equally; sample-averaged metrics weight every prediction
  - Preprocessing statistics are fit within each fold, never across it

- **Fixed MLP reference:** one architecture and training recipe across every condition
  - 184 conditions spanning twelve tasks, four PDKs and four source stages, totalling 3,312 held-out-circuit evaluations
  - A controlled reference for comparison, not a model tuned per condition
  - Lower error than the EDA baseline in 88 conditions, including all twelve interconnect-length conditions

- **Open-weight release:** every run ships its own artifacts
  - Executable configuration, per-fold checkpoints, preprocessing statistics, predictions and metrics
  - Versioned by prediction condition, so a leaderboard entry traces back to the weights that produced it

→ **[Workflow, full results and data-efficiency analysis]({{ '/eda-openml/' | relative_url }})**

---

## Leaderboard: Standardized Comparison

Every released model is scored on the same benchmark, under the same protocol, against the same
reference, and the result is published as a single open comparison — so a claim of improvement is
checked rather than taken on trust.

→ **[Browse the EDA-Learn leaderboard](https://drexel-ice.github.io/EDA-learn-leaderboard/)**

<div class="row justify-content-sm-center">
    <div class="col-sm-12 mt-3 mt-md-0">
        {% include figure.liquid path="assets/img/projects/ml-eda/eda-learn-leaderboard.png" alt="The leaderboard: a grid of prediction tasks against PDKs and design stages, each cell green where the released model beats the EDA tool's estimate and red where the tool still leads." title="The EDA-Learn leaderboard" class="img-fluid rounded z-depth-1" zoomable=true %}
    </div>
</div>

<div class="caption">
    Released predictors against the OpenROAD estimate, by task, PDK and source stage. Green marks a condition where the model is more accurate than the tool, red one where the tool still leads.
</div>

- **One cell per prediction condition:** task × PDK × source stage
  - Twelve tasks, four PDKs and four source stages
  - Leave-one-circuit-out scores, so every number refers to circuits held out entirely
  - Fold-averaged and sample-averaged metrics are both reported, and switchable

- **Always against the tool:** the OpenROAD estimate for that same condition
  - A cell is coloured by whether the model beats it, not by raw error
  - Conditions where the tool is already exact, or defines no estimate, are marked rather than hidden

- **Traceable entries:** every number links back to what produced it
  - Per-condition ranking of the models submitted for it
  - Each entry resolves to its configuration, weights and evaluation report

---

## Publications

### Open data, schema, and benchmarks

- **EDA-Schema-V2: A Multimodal Schema, Open Datasets, and Benchmarks for Machine Learning in Digital Physical Design.**
  P. Shrestha, A. Aversa, I. Savidis. *arXiv:2605.06952*, 2026.
  [[PDF]]({{ '/assets/pdf/preprints/2605.06952v1.pdf' | relative_url }})
- **EDA-Schema: A Graph Datamodel Schema and Open Dataset for Digital Design Automation.**
  P. Shrestha, A. Aversa, S. Phatharodom, I. Savidis. *GLSVLSI*, 2024. **Best Paper Award.**
  [[PDF]]({{ '/assets/pdf/conferences/GLSVLSI_2024-EDA-schema.pdf' | relative_url }})

### Surveys and position papers

- **Representation Learning for Digital Integrated Circuit Design Automation.**
  P. Shrestha, I. Savidis. *ICCD*, 2025.
  [[PDF]]({{ '/assets/pdf/conferences/ICCD_2025-representation.pdf' | relative_url }})
- **Deep Representation Learning for Electronic Design Automation.**
  P. Shrestha, S. Phatharodom, A. Aversa, D. Blankenship, Z. Wu, I. Savidis. *arXiv:2505.02105*, 2025.
  [[PDF]]({{ '/assets/pdf/preprints/2505.02105v1.pdf' | relative_url }})

### Prediction models and frameworks

- **Differentiable Graph Neural Networks for Wirelength Estimation.**
  Z. Wu, P. Shrestha, S. Phatharodom, I. Savidis. *ISCAS*, 2025.
  [[PDF]]({{ '/assets/pdf/conferences/ISCAS_2025-differentiable.pdf' | relative_url }})
- **EDA-ML: Graph Representation Learning Framework for Digital IC Design Automation.**
  P. Shrestha, I. Savidis. *ISQED*, 2024.
  [[PDF]]({{ '/assets/pdf/conferences/ISQED_2024.pdf' | relative_url }})
- **Transfer Learning of Arrival Time Prediction Models from a 65 nm to a 28 nm Process Node.**
  P. Shrestha, I. Savidis. *DCAS*, 2024.
  [[PDF]]({{ '/assets/pdf/conferences/DCAS_2024.pdf' | relative_url }})
- **Graph Representation Learning for Parasitic Impedance Prediction of the Interconnect.**
  P. Shrestha, I. Savidis. *ISCAS*, 2023.
  [[PDF]]({{ '/assets/pdf/conferences/ISCAS_2023-parasitic.pdf' | relative_url }})
- **Modeling Graph Neural Networks for Gate Level Arrival Time Prediction of Long Tailed Datasets.**
  P. Shrestha, S. Phatharodom, I. Savidis. *GOMACTech*, 2023.
  [[PDF]]({{ '/assets/pdf/conferences/GOMACTech_2023.pdf' | relative_url }})
- **Graph Representation Learning for Gate Arrival Time Prediction.**
  P. Shrestha, S. Phatharodom, I. Savidis. *MLCAD*, 2022.
  [[PDF]]({{ '/assets/pdf/conferences/MLCAD_2022.pdf' | relative_url }})

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

- **[EDA-Schema](https://github.com/drexel-ice/EDA-schema)** — schema implementation, query and
  visualization tooling, and dataset loaders, with a columnar ParquetDB backend. CC BY-NC-SA 4.0.
- **[Open dataset](https://github.com/drexel-ice/EDA-schema#open-dataset)** — download links and
  the full dataset specification.
- **[EDA-Learn leaderboard](https://drexel-ice.github.io/EDA-learn-leaderboard/)** — released
  models and evaluation results for each task, PDK and design stage, scored against the
  OpenROAD reference baseline.
