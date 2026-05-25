---
layout: page
title: Clock Tree Synthesis (CTS) for 3-D Integrated Circuits
description: Recent work has explored CTS for 3-D ICs by extending algorithms devised for 2D ICs such as the Methods of Means and Medians (MMM), Nearest Neighbor Graph (NNG) and Deferred Merging Algorithm (DME) fo...
img: assets/img/research/3d-ics.jpg
importance: 8
category: active
---

Recent work has explored CTS for 3-D ICs by extending algorithms devised for 2D ICs such as the Methods of Means and Medians (MMM), Nearest Neighbor Graph (NNG) and Deferred Merging Algorithm (DME) for 3-D ICs. However, CTS for heterogeneous 3-D ICs has not been explored. We are developing algorithms to complete CTS for heterogeneous 3-D ICs to optimize power and minimize the skew, slew, and TSV count. In addition, TSV based 3-D IC have a large power density due to the proximity of dies. Since the power density of a 3-D IC impacts the overall system performance, the relative order of die placement in the 3-D stack can be used to manage thermals and potentially reduce the power density of the whole stack. Since the CDN consumes the majority of the power in an IC, the CTS step is ideal to find the optimum die ordering in the 3-D stack. We propose an algorithm for die ordering to minimize the power density of the overall stack. The optimal die location is then determined to place the clock source of the overall stack.
