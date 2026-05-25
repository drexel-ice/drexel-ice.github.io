---
layout: page
title: On-Chip Power Delivery with Run-Time Voltage Regulator Clustering
description: With the paradigm shift in computing systems from performance oriented design to energy efficiency, there is considerable research effort to optimize the core configuration by reducing the over-provis...
importance: 6
category: active
---

With the paradigm shift in computing systems from performance oriented design to energy efficiency, there is considerable research effort to optimize the core configuration by reducing the over-provisioning of core resources which was introduced in the early part of the last decade to boost performance. However, not much attention has been given to reduce the over-provisioning of the circuits delivering power to the cores. We are developing a power delivery system for homogeneous (and heterogeneous) chip multi processor (CMP) systems which are modified at run time by clustering multiple on-chip voltage regulators (OCVR) depending on the power demand of the workload. The OCVRs are designed to deliver up to the average power requirement of the typical workloads executed on a CMP platform. The power demand of a core cluster exceeding the average value is delivered by combining the output of multiple OCVRs through a high-speed switch network. Different OCVR topologies are also being analyzed to understand the impact on voltage regulator characteristics as the peak load current is reduced. The run-time OCVR clustering concept is also being extended for application to many-core systems by solving the energy efficiency optimization problem.
