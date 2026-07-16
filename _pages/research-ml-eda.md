---
layout: research-area
title: Machine Learning for EDA
description: Predicting late-stage chip metrics from early design stages, and the open data infrastructure to make it reproducible.
permalink: /research/ml-eda/
research_area: ml-eda
---

<div class="row">
<div class="col-sm-8 mt-3 mt-md-0">

Modern chip design runs a long, iterative pipeline - logic synthesis, floorplanning, placement, clock tree synthesis, and routing - and the metrics that decide whether a design is good are only known accurately after routing.
When a design misses its targets, engineers loop back and repeat expensive stages, often for hours or days per pass.
Our group develops graph neural networks that observe a cheap early design stage and accurately predict the expensive final outcome - gate arrival times, interconnect parasitics, and wirelength - so that corrections can be made while they are still cheap.
The models are unified in a task-agnostic framework, and transfer learning lets a model trained on one technology node migrate to a newer node for a fraction of the retraining cost.

Alongside the models, the group builds the open infrastructure the field needs to make machine learning for EDA reproducible: the EDA-Schema property-graph data model for circuits, automated dataset generation with open-source tools and process design kits, and public quality-of-results prediction benchmarks that future models can be compared against.

</div>
<div class="col-sm-4 mt-3 mt-md-0">
{% include figure.liquid loading="lazy" path="assets/img/projects/ml-eda/cover.png" title="Machine Learning for EDA" class="img-fluid rounded z-depth-1" %}
</div>
</div>
