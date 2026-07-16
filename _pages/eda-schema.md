---
layout: page
title: benchmarks
permalink: /eda-schema/
nav: false
description: Baseline quality-of-results prediction-error benchmarks from EDA-Schema-V2 — the error any ML predictor should aim to beat.
---

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

#### Cite

If you use these datasets or benchmarks, please cite:

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
