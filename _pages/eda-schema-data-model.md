---
layout: page
title: EDA-Schema
permalink: /eda-schema/data-model/
nav: false
description: The stage-aware, multimodal data model behind EDA-Learn — entities, representations, dataset generation, and the twelve benchmark prediction tasks.
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
        {% include figure.liquid path="assets/img/projects/ml-eda/schema-er-diagram.png" title="EDA-Schema-V2 entity relationship diagram" class="img-fluid rounded z-depth-1" zoomable=true %}
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
        {% include figure.liquid path="assets/img/projects/ml-eda/netlist-graph.png" title="A circuit as a heterogeneous netlist graph" class="img-fluid rounded z-depth-1" zoomable=true %}
    </div>
</div>
<div class="caption">
    The graph modality: a circuit as a heterogeneous netlist graph, with I/O ports, gates, nets
    and pins as typed nodes and the logical and physical connections between them as edges.
</div>

<div class="row justify-content-sm-center">
    <div class="col-sm-12 mt-3 mt-md-0">
        {% include figure.liquid path="assets/img/projects/ml-eda/circuit-graphs.png" title="Netlist graph and extracted timing-path graphs" class="img-fluid rounded z-depth-1" zoomable=true %}
    </div>
</div>
<div class="caption">
    Graph granularity: a sample ISCAS'89 benchmark as (a) a netlist graph and (b) the
    timing-path graphs extracted from it. Timing reports drive the extraction, so each subgraph
    isolates one signal's journey through the circuit.
</div>

<div class="row justify-content-sm-center">
    <div class="col-sm-12 mt-3 mt-md-0">
        {% include figure.liquid path="assets/img/projects/ml-eda/spatial-modalities.png" title="Binary spatial maps of the circuit layout" class="img-fluid rounded z-depth-1" zoomable=true %}
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
        {% include figure.liquid path="assets/img/projects/ml-eda/routability-maps.png" title="RUDY routability heatmaps" class="img-fluid rounded z-depth-1" zoomable=true %}
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

→ **[Baseline benchmark errors]({{ '/eda-schema/' | relative_url }})** — the EDA tool's own
error on every task, PDK and stage pair: the numbers a predictor has to beat.

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

#### Cite

```bibtex
@article{shrestha2026edaschemav2,
  title   = {EDA-Schema-V2: A Multimodal Schema, Open Datasets, and Benchmarks
             for Machine Learning in Digital Physical Design},
  author  = {Shrestha, Pratik and Aversa, Alec and Savidis, Ioannis},
  journal = {arXiv preprint arXiv:2605.06952},
  pages   = {1--39},
  year    = {2026},
  month   = {May}
}
```
