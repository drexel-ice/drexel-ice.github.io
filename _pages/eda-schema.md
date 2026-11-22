---
layout: page
title: EDA-Schema
permalink: /eda-schema/
nav: false
description: The open data foundation of EDA-Learn — the stage-aware multimodal data model, the dataset, the twelve benchmark tasks, and the baseline errors a predictor has to beat.
toc:
  sidebar: left
---

EDA-Schema is the open data foundation of [EDA-Learn]({{ '/projects/eda-learn/' | relative_url }}).
It defines how a digital design is recorded at every stage of the flow, generates a large open
dataset from that definition, and fixes twelve prediction tasks on top of it.

- **Standard inputs only.** Everything is parsed from LEF/DEF, SPEF, Liberty and STA reports,
  so the schema stays compatible with commercial flows without instrumenting any tool.
- **Stage-aware.** Each attribute records the stage at which it becomes available, which makes
  the information boundary of a prediction task part of the task definition.
- **Multimodal.** Graphs, layout images and heatmaps sit side by side for every design instance.
- **Open end to end.** Generated with OpenROAD and open PDKs, so the data is redistributable.

---

## The data model

A stage-aware **property graph** spanning synthesis through detailed routing. Structural
netlists, timing reports, parasitics, layout geometry, power delivery analysis and
quality-of-results (QoR) metrics are organized into one consistent representation.

<div class="row justify-content-sm-center">
    <div class="col-sm-12 mt-3 mt-md-0">
        {% include figure.liquid path="assets/img/projects/ml-eda/schema-er-diagram.png" alt="Entity relationship diagram of EDA-Schema-V2: design-flow entities, structural design entities and quality-of-results metric entities joined into one connected graph." title="EDA-Schema-V2 entity relationship diagram" class="img-fluid rounded z-depth-1" zoomable=true %}
    </div>
</div>
<div class="caption">
    The EDA-Schema-V2 entity relationship diagram. Yellow entities capture the design flow
    hierarchy (flow, stage, constraints); blue entities hold structural design data — netlist,
    clock tree, timing path, power delivery network, and their constituent gates, nets, pins and
    arcs; green entities record quality-of-results metrics for cell, area, power, timing and
    routability.
</div>

---

## Three modalities

| Modality | What it holds | Used for |
| --- | --- | --- |
| **Graph** | Heterogeneous netlist graph; timing-path subgraphs; interconnect graph with wire segments as nodes | Graph neural networks, per-path and per-net prediction |
| **Image** | Binary spatial maps of cell placement, pins and per-layer routing | Convolutional and hybrid models |
| **Heatmap** | RUDY routability maps; IR-drop and electromigration maps | Routability and power-integrity prediction |

<div class="row justify-content-sm-center">
    <div class="col-sm-12 mt-3 mt-md-0">
        {% include figure.liquid path="assets/img/projects/ml-eda/netlist-graph.png" alt="A circuit drawn as a heterogeneous graph, with I/O ports, gates, nets and pins as differently typed nodes joined by their logical and physical connections." title="A circuit as a heterogeneous netlist graph" class="img-fluid rounded z-depth-1" zoomable=true %}
    </div>
</div>
<div class="caption">
    The graph modality: a circuit as a heterogeneous netlist graph, with I/O ports, gates, nets
    and pins as typed nodes and the logical and physical connections between them as edges.
</div>

<div class="row justify-content-sm-center">
    <div class="col-sm-12 mt-3 mt-md-0">
        {% include figure.liquid path="assets/img/projects/ml-eda/circuit-graphs.png" alt="A benchmark circuit shown as a full netlist graph beside the smaller timing-path graphs extracted from it." title="Netlist graph and extracted timing-path graphs" class="img-fluid rounded z-depth-1" zoomable=true %}
    </div>
</div>
<div class="caption">
    Graph granularity: a sample ISCAS'89 benchmark as (a) a netlist graph and (b) the
    timing-path graphs extracted from it. Timing reports drive the extraction, so each subgraph
    isolates one signal's journey through the circuit.
</div>

<div class="row justify-content-sm-center">
    <div class="col-sm-12 mt-3 mt-md-0">
        {% include figure.liquid path="assets/img/projects/ml-eda/spatial-modalities.png" alt="Six binary layout maps of the same circuit: combinational cell placement, sequential cell placement, pin locations, overall routing, metal 1 routing and metal 5 routing." title="Binary spatial maps of the circuit layout" class="img-fluid rounded z-depth-1" zoomable=true %}
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
        {% include figure.liquid path="assets/img/projects/ml-eda/routability-maps.png" alt="Four RUDY routability heatmaps of one layout — net-based, pin-based, long-range and short-range — showing where routing demand concentrates before routing is run." title="RUDY routability heatmaps" class="img-fluid rounded z-depth-1" zoomable=true %}
    </div>
</div>
<div class="caption">
    The heatmap modality: Rectangular Uniform wire DensitY (RUDY) routability maps —
    (a) net-based, (b) pin-based, (c) long-range and (d) short-range — which estimate routing
    demand across the layout before routing is run.
</div>

---

## The dataset

Produced by automating the OpenROAD flow over public benchmark circuits and open PDKs, sweeping
clock period, utilization, aspect ratio and other parameters. The sweeps deliberately include
**barely-passing and barely-failing operating points**, so the data contains the marginal cases
where prediction matters rather than only comfortable ones.

| | |
| --- | --- |
| Design instances | 7,776 (1,944 per PDK) |
| Benchmark circuits | 18 — 16 from IWLS'05, plus OpenCores and IBEX |
| Process design kits | Nangate 45 nm, SkyWater 130 nm, IHP SG13G2 130 nm, ASAP 7 nm |
| Design stages captured | Floorplan, global placement, detailed placement, CTS, global and detailed routing |
| Scale | 275 M+ gates, 75 M+ nets, 36 M+ extracted timing paths |
| Licence | CC BY-NC-SA 4.0 |

---

## The twelve benchmark tasks

Each task fixes a prediction target, a granularity, evaluation metrics, and the EDA tool's own
estimate as the reference baseline.

| Prediction target | Granularity |
| --- | --- |
| Total area, total power, total wirelength | Whole circuit |
| Worst arrival time, worst slack, total negative slack | Whole circuit |
| Interconnect length | Per interconnect |
| Timing-path arrival time, timing-path slack | Per timing path |
| Net-arc delay | Per net arc |
| Cell-arc delay, cell-arc slew | Per cell arc |

Models are scored with **leave-one-circuit-out** evaluation, so a reported result reflects
generalization to a circuit the model has never seen. Ordinary random splits obscure this,
because fragments of the same circuit then appear in both training and test data.

---

## Baseline benchmark errors

Every task, PDK and stage pair has a published reference error: the EDA tool's own estimate,
scored the same way a model is. These are the numbers a predictor has to beat.

{% include table8.html %}

<div class="caption" markdown="1">
**Table 8.** Averaged baseline prediction error between design stages.
Stage labels abbreviate "→ detailed route." Within each metric, MAE / MAPE
are mean absolute / mean absolute percentage error and R² is the
coefficient of determination; for timing metrics, MPE / MNE are mean
positive / negative error and TPR / TNR are true positive / negative
rate. **P95** and **TOP5** denote the 95th-percentile and worst-5
subsets. *n/a — cells not yet placed*: wirelength is undefined before
placement. *no ± error (n_p = n_n = 0)*: at global route the slack
estimate has no over- or under-estimates. *&gt;10000%* and *&lt;-1* are
unstable metrics thresholded by the paper, not literal magnitudes.
</div>

→ **[EDA-Learn leaderboard](https://drexel-ice.github.io/EDA-learn-leaderboard/)** — released
models scored against these baselines, per task, PDK and design stage.

---

## Standardization

The same representation is being carried toward industry adoption through the **Si2 Schema
Working Group** and the **Si2 Logic Block Composition (LBC) Extend & Expand Working Group**, so
that design data means the same thing across tools, vendors and labs.

---

## Get it

- **[EDA-Schema on GitHub](https://github.com/drexel-ice/EDA-schema)** — schema implementation,
  query and visualization tooling, dataset loaders, columnar ParquetDB backend.
- **[Open dataset](https://github.com/drexel-ice/EDA-schema#open-dataset)** — download links and
  the full dataset specification.

### Cite

If you use these datasets or benchmarks, please cite:

```bibtex
@article{shrestha2026edaschemav2,
  title   = {EDA-Schema-V2: A Multimodal Schema, Open Datasets,
             and Benchmarks for Machine Learning in Digital
             Physical Design},
  author  = {Shrestha, Pratik and Aversa, Alec and
             Savidis, Ioannis},
  journal = {arXiv preprint arXiv:2605.06952},
  pages   = {1--39},
  year    = {2026},
  month   = {May}
}
```
