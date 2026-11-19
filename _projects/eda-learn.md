---
layout: page
title: "EDA-Learn: Open and Reproducible Machine Learning for Electronic Design Automation"
dropdown_label: EDA Learn
dropdown_children:
  - title: EDA-Schema
    permalink: /eda-schema/data-model/
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

Digital physical design runs as a chain of stages — synthesis, floorplanning, placement, clock
tree synthesis, routing, signoff. Timing, power, area and routability are only measured
accurately at the end. Miss a target and the flow runs again, at hours to days per pass.

**EDA-Learn** is an open, reproducible framework for predicting those late-stage outcomes from
early-stage information — and for making such predictions comparable between research groups.

---

## The prediction problem

- **Given** the information that exists at a *source* stage — say, global placement.
- **Predict** a quantity measured only at a later *target* stage — say, post-route wirelength.
- **Beat** the tool's own analytical estimate for that quantity: wireload models, half-perimeter
  wirelength, Steiner trees, congestion heuristics.
- **Score** both against the real target-stage measurement, once the flow completes.

<div class="row justify-content-sm-center">
    <div class="col-sm-12 mt-3 mt-md-0">
        {% include figure.liquid path="assets/img/projects/ml-eda/prediction-vs-estimation.png" title="Conventional early estimation compared with machine learning prediction" class="img-fluid rounded z-depth-1" zoomable=true %}
    </div>
</div>
<div class="caption">
    Conventional early estimation and machine learning prediction of a downstream metric.
    Information available at an earlier source stage feeds both a conventional estimator and a
    learned predictor; each estimate is evaluated against the target-stage measurement, which is
    ground truth for scoring rather than an input at inference time.
</div>

Target-stage measurements are kept strictly out of the inputs. That is what prevents downstream
information from leaking into an early predictor and producing accuracy that would not survive
real use.

---

## The closed-data problem

Learned prediction has been demonstrated repeatedly across power, wirelength, timing,
parasitics, routability and power integrity. The published results still cannot be reproduced or
ranked against one another. Across a survey of fifteen representative studies:

| | |
| --- | --- |
| **10 of 15** | depend on commercial implementation tools |
| **6 of 15** | report on a proprietary or unnamed process technology |
| **12** | distinct network architectures across the fifteen studies |
| **no two** | share a circuit set, a technology, a toolchain *and* an evaluation protocol |

Three consequences follow:

- Accuracy figures drawn from different circuits, nodes and toolchains are **not comparable**.
- The contribution of a representation or an architecture to a reported number **cannot be
  isolated**.
- A model trained on confidential data **cannot be rerun** outside the group that built it.

Open tools and datasets already exist — OpenROAD, CircuitNet, CircuitOps. The gap is not raw
openness. It is that the design data, the evaluation procedure and the model configuration are
each specified separately, so nothing downstream is attributable. **This is a specification
problem, not a modeling problem.**

---

## EDA-Learn

Four layers, each defined on top of the one above it, so that a reported result is attributable
to a representation or an architecture rather than to the data it happened to be trained on.

| Layer | What it pins down | Status |
| --- | --- | --- |
| **[EDA-Schema]({{ '/eda-schema/data-model/' | relative_url }})** | Stage-aware multimodal data model, open dataset, twelve benchmark tasks | Published — GLSVLSI 2024 (Best Paper), arXiv 2026 |
| **EDA-OpenML** | Executable model configurations, circuit-disjoint evaluation, open-weight release | Results below; manuscript in preparation |
| **EDA-AutoML** | Automated architecture and hyperparameter selection inside that protocol | In progress |
| **Neural Architect Agent** | One-shot LLM-generated configuration, replacing the search loop | In progress |

The program began with graph neural networks for gate arrival time and interconnect parasitic
prediction, which were unified into the task-agnostic **EDA-ML** framework — observe stage *X*,
predict metric *M* at stage *Y*, at a stated granularity. EDA-Schema and EDA-OpenML generalize
that recipe onto open data and an open evaluation protocol.

<div class="row justify-content-sm-center">
    <div class="col-sm-12 mt-3 mt-md-0">
        {% include figure.liquid path="assets/img/projects/ml-eda/graph-learning-framework.png" title="The generalized graph learning framework" class="img-fluid rounded z-depth-1" zoomable=true %}
    </div>
</div>
<div class="caption">
    The generalized framework the program grew out of: an automated design flow produces the
    stored artifacts (netlist, timing reports, extracted parasitics), which are converted into
    netlist, timing-path and interconnect graphs, which in turn feed a common training and
    evaluation flow.
</div>

---

## EDA-Schema — the open foundation

A stage-aware **property-graph data model** for digital physical design, a large dataset
generated entirely with open tools, and twelve standardized prediction tasks.

| | |
| --- | --- |
| Design instances | 7,776 (1,944 per PDK) |
| Benchmark circuits | 18 — 16 from IWLS'05, plus OpenCores and IBEX |
| Process design kits | Nangate 45 nm, SkyWater 130 nm, IHP SG13G2 130 nm, ASAP 7 nm |
| Modalities | Circuit graphs, spatial layout images, scalar heatmaps, QoR metrics |
| Benchmark tasks | 12, from whole-circuit area and power down to per-cell-arc delay |
| Evaluation | Leave-one-circuit-out, against the EDA tool's own estimate |

- Parsed from standard formats (LEF/DEF, SPEF, Liberty, STA reports), so it stays compatible
  with commercial flows.
- Every attribute records the stage at which it becomes available, making the information
  boundary of a task part of its definition.
- Sweeps include **barely-passing and barely-failing operating points**, not only comfortable
  ones.
- Carried toward industry adoption through the **Si2 Schema** and **Si2 LBC Extend & Expand**
  working groups.

→ **[Data model, modalities and benchmark tasks in detail]({{ '/eda-schema/data-model/' | relative_url }})**
&nbsp;·&nbsp; **[Baseline benchmark errors]({{ '/eda-schema/' | relative_url }})**

---

## EDA-OpenML — reproducible neural prediction

An open-source, open-weight framework in which the prediction problem and the model are
specified separately, and the model is specified as an **executable configuration** — input
features, architecture, hyperparameters, preprocessing, evaluation settings.

<div class="row justify-content-sm-center">
    <div class="col-sm-12 mt-3 mt-md-0">
        {% include figure.liquid path="assets/img/projects/ml-eda/openml-workflow.png" title="The EDA-OpenML workflow" class="img-fluid rounded z-depth-1" zoomable=true %}
    </div>
</div>
<div class="caption">
    The EDA-OpenML workflow. A prediction problem drawn from EDA-Schema-V2 and an executable
    model configuration are combined, evaluated under circuit-level leave-one-circuit-out
    cross-validation, aggregated both fold-averaged and sample-averaged, and released as a
    package containing the configuration, the per-fold weights, the predictions and the metrics.
</div>

A single **Fixed MLP** — one architecture, one training configuration — is run across every
task, PDK and source stage as a controlled reference rather than as a tuned model.

- Lower fold-averaged error than the stage-specific EDA reference in **88 of 184** conditions.
- **Interconnect length** is the strongest case: favorable in all twelve PDK-stage conditions,
  and better on *all eighteen* held-out circuits in ten of them.
- NG45 interconnect length, global placement → detailed routing: MAE **4.69 µm → 3.39 µm**
  (−27.7% against HPWL), sample-averaged MAE −32.0%, R² **0.735 → 0.887**, winning on 15 of 18
  circuits.
- **No single configuration transfers uniformly.** Total negative slack, total power and
  cell-arc prediction are not consistently favorable — reported rather than aggregated away.

<div class="row justify-content-sm-center">
    <div class="col-sm-12 mt-3 mt-md-0">
        {% include figure.liquid path="assets/img/projects/ml-eda/openml-ng45-interconnect-mae.png" title="Per-circuit MAE, HPWL baseline versus Fixed MLP" class="img-fluid rounded z-depth-1" zoomable=true %}
    </div>
</div>
<div class="caption">
    Per-circuit mean absolute error for NG45 interconnect length predicted from global
    placement, HPWL baseline against the Fixed MLP, one bar pair per held-out circuit. The ratio
    above each pair is the model's error relative to the baseline; <code>i2c</code>,
    <code>simple_spi</code> and <code>ss_pcm</code> are the three circuits where the model loses.
</div>

**Data efficiency** is measured along two separate axes: *utilization* (what fraction of
existing samples is used for training) and *acquisition* (how many physical design runs are
generated in the first place). Accuracy frequently approaches the full-data result on
substantially less of both, with diminishing returns following power-law-like curves whose
exponent depends on the target and the source stage.

Every released model package carries its executable configuration, trained weights for each
fold, preprocessing statistics, out-of-fold predictions and evaluation metrics. Results are
published to a [public leaderboard](https://drexel-ice.github.io/EDA-learn-leaderboard/).

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

- **[EDA-Schema](https://github.com/drexel-ice/EDA-schema)** — schema implementation, query and
  visualization tooling, and dataset loaders, with a columnar ParquetDB backend. CC BY-NC-SA 4.0.
- **[Open dataset](https://github.com/drexel-ice/EDA-schema#open-dataset)** — download links and
  the full dataset specification.
- **[EDA-Learn leaderboard](https://drexel-ice.github.io/EDA-learn-leaderboard/)** — released
  models and evaluation results for each task, PDK and design stage, scored against the
  OpenROAD reference baseline.
