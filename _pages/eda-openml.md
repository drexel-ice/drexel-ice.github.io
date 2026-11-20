---
layout: page
title: EDA-OpenML
permalink: /eda-openml/
nav: false
description: The open-source, open-weight framework behind EDA-Learn — executable model configurations, circuit-disjoint evaluation, data-efficiency analysis, and released model packages.
toc:
  sidebar: left
---

EDA-OpenML is the prediction layer of [EDA-Learn]({{ '/projects/eda-learn/' | relative_url }}).
It takes the tasks defined by [EDA-Schema]({{ '/eda-schema/data-model/' | relative_url }}) and
fixes everything that normally varies silently between papers: what the model is, how it was
trained, how it was scored, and what gets released afterwards.

The separation it enforces is between the **prediction problem** and the **model**. The problem
comes from the benchmark. The model is an **executable configuration** — a file, not a prose
description — so the same predictor can be rebuilt, rerun and reused across targets, PDKs and
design stages.

*Manuscript in preparation. The results below are reported from the dissertation chapter.*

---

## The workflow

<div class="row justify-content-sm-center">
    <div class="col-sm-12 mt-3 mt-md-0">
        {% include figure.liquid path="assets/img/projects/ml-eda/openml-workflow.svg" title="The EDA-OpenML workflow" class="img-fluid rounded z-depth-1" zoomable=true %}
    </div>
</div>
<div class="caption">
    A prediction problem drawn from EDA-Schema-V2 and an executable model configuration are
    combined, evaluated under circuit-level leave-one-circuit-out cross-validation, aggregated
    both fold-averaged and sample-averaged, and released as a package containing the
    configuration, the per-fold weights, the predictions and the metrics.
</div>

| Stage | What it pins down |
| --- | --- |
| **Prediction problem** | PDK, source stage, target stage, prediction target, source data, and the EDA tool's own estimate as reference |
| **Executable configuration** | Ordered input features, network architecture, training hyperparameters, preprocessing |
| **Evaluation** | Leave-one-circuit-out folds, metrics, and both fold- and sample-averaged aggregation |
| **Model package** | Configuration, per-fold weights, preprocessing statistics, out-of-fold predictions, metrics |

---

## Circuit-disjoint evaluation

- One **complete circuit** is excluded from fitting in each fold and used only for evaluation —
  eighteen folds per prediction condition.
- **Fold-averaged** metrics weight every held-out circuit equally. **Sample-averaged** metrics
  pool all out-of-fold predictions. Both are reported.
- A random split would place different parameterizations of the *same* circuit on both sides of
  the partition, so it measures interpolation rather than transfer to an unseen topology.

---

## The Fixed MLP reference

A single multilayer perceptron — one architecture, one training configuration — is run across
every task, PDK and source stage. It is a **controlled reference**, not a model tuned per
condition, which is what makes differences between conditions attributable to the condition.

Across **184** prediction conditions:

- Lower fold-averaged MAE than the stage-specific EDA reference in **88** of them.
- **81** improve on a majority of held-out circuits; 63 on at least twelve; 32 on at least
  fifteen; **15 on all eighteen**.
- Fold-averaged and sample-averaged comparisons agree in **169 of 184** conditions (91.8%).

| Prediction target | How it behaves |
| --- | --- |
| **Interconnect length** | Strongest case — favorable in all twelve PDK-stage conditions, ten of them better on *all eighteen* held-out circuits |
| **Timing-path arrival time** | Twelve of sixteen conditions improve on a majority of circuits; stronger at earlier source stages than at CTS |
| **Net-arc delay** | Twelve of sixteen conditions improve on at least twelve circuits |
| **Total area** | Favorable in aggregate, but condition- and circuit-level medians differ by 21 points |
| **Total negative slack, total power, cell-arc** | Not consistently favorable under a single fixed configuration |

**No single configuration transfers uniformly across EDA prediction problems.** That is the
chapter's own conclusion, and it is the reason the next layer of the framework — automated
configuration selection — exists.

---

## Worked case: NG45 interconnect length

Predicting post-detailed-routing interconnect length from global placement on Nangate 45 nm,
against the tool's half-perimeter wirelength (HPWL) estimate, over all eighteen circuits.

| | HPWL baseline | Fixed MLP |
| --- | --- | --- |
| Fold-averaged MAE | 4.6943 µm | **3.3921 µm** (−27.7%) |
| Sample-averaged MAE | — | **−32.0%** |
| Sample-averaged R² | 0.7353 | **0.8873** |
| Circuits with lower MAE | — | **15 of 18** |
| Circuits with higher R² | — | 13 of 18 |

- Median circuit-level MAE improvement **26.0%**, interquartile range 5.4–38.6%. The positive
  median with 15 of 18 wins means the aggregate gain is spread across circuits rather than
  driven by a few.
- Upper-tail error improves more than the mean: median **37.1%** on MAE<sub>top5</sub> (18 of 18
  circuits) and **27.3%** on MAE<sub>P95</sub> (17 of 18). The worst nets are where early
  estimation hurts most.
- Three circuits lose: `i2c`, `simple_spi` and `ss_pcm`. The largest degradation is `ss_pcm`,
  MAE 2.9623 → 3.2821 µm with R² falling from 0.4219 to −0.7551.

<div class="row justify-content-sm-center">
    <div class="col-sm-12 mt-3 mt-md-0">
        {% include figure.liquid path="assets/img/projects/ml-eda/openml-ng45-interconnect-mae.png" title="Per-circuit MAE, HPWL baseline versus Fixed MLP" class="img-fluid rounded z-depth-1" zoomable=true %}
    </div>
</div>
<div class="caption">
    Per-circuit mean absolute error for NG45 interconnect length predicted from global
    placement: HPWL baseline against the Fixed MLP, one bar pair per held-out circuit. The ratio
    above each pair is the model's error relative to the baseline.
</div>

---

## Data efficiency

Labelled physical design data is expensive because producing it means running the flow. Two
costs are therefore measured **separately**, since conflating them hides which one is binding:

| Axis | What is varied | What it costs |
| --- | --- | --- |
| **Utilization** | Fraction of already-generated samples used for training | Model development time |
| **Acquisition** | Number of generated physical design configurations | EDA tool runtime — the expensive one |

<div class="row justify-content-sm-center">
    <div class="col-sm-12 mt-3 mt-md-0">
        {% include figure.liquid path="assets/img/projects/ml-eda/openml-utilization-scaling.png" title="Utilization scaling for interconnect length prediction by source stage" class="img-fluid rounded z-depth-1" zoomable=true %}
    </div>
</div>
<div class="caption">
    Utilization scaling for interconnect length prediction, by source stage: the fold-averaged
    MAE gap to the full-data result as the retained fraction of training samples is reduced.
    Median across PDKs with the first and third quartiles. The gap closes well before the full
    dataset is used, and later source stages need less data to get there.
</div>

- For interconnect prediction, accuracy frequently approaches the full-data result on
  **substantially less** of both axes.
- Timing-path prediction depends strongly on the source stage: floorplan needs larger budgets,
  while later-stage arrival-time prediction approaches the full-data result with far less.
- Slack scaling is **less regular** at later stages — the marginal value of more data depends on
  the target, not only on how much there is.
- Diminishing returns are summarized with power-law-like fits, *Q*(*B*) = *C·B*<sup>−*b*</sup>.
  The fitted parameters describe the evaluated model, stage and scaling procedure; they are not
  universal constants.

---

## What gets released

Every model package carries:

- the **executable configuration** that produced it,
- a **trained model for each LOCO fold**,
- **preprocessing statistics**,
- **out-of-fold predictions**,
- **evaluation metrics and reports**.

A canonical directory hierarchy and semantic analysis versions tie each released checkpoint to
the prediction condition and evaluation result it belongs to, so a number on the leaderboard
can be traced back to the weights that produced it.

→ **[EDA-Learn leaderboard](https://drexel-ice.github.io/EDA-learn-leaderboard/)** — released
models scored against the OpenROAD reference baseline, per task, PDK and design stage.
