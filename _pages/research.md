---
layout: page
title: research
permalink: /research/
description: Research areas at the ICE Lab — 3-D ICs, hardware security, and near-threshold circuits.
nav: true
nav_order: 4
---

## 3D Integrated Circuits

<div class="row">
<div class="col-sm-8 mt-3 mt-md-0">

There are many design aspects that require consideration and analysis in the development of a three-dimensional integrated circuit. When considering power delivery, synchronization, and signalling in a TSV-based 3-D IC, the potential to integrate disparate technologies with independent voltage and peak power requirements, clock speeds, thermal design power, noise requirements, and a slew of other design considerations requires new methodologies and techniques beyond which are used for two-dimensional system-on-chip integrated circuits.

> **Sub-projects:** TSV modeling, synchronization, clock tree synthesis, power delivery, OCVR clustering, optical interconnect, thermal modeling
{: .block-tip}

[View 3-D IC projects]({{ '/projects/' | relative_url }}#active)

</div>
<div class="col-sm-4 mt-3 mt-md-0">
{% include figure.liquid loading="lazy" path="assets/img/research/3d-ics.jpg" title="3-D Integrated Circuits" class="img-fluid rounded z-depth-1" %}
</div>
</div>

---

## Hardware Security

<div class="row">
<div class="col-sm-4 mt-3 mt-md-0">
{% include figure.liquid loading="lazy" path="assets/img/research/hardware-security.jpg" title="Hardware Security" class="img-fluid rounded z-depth-1" %}
</div>
<div class="col-sm-8 mt-3 mt-md-0">

Modifications to integrated circuits (ICs) or the insertion of foreign intellectual property (i.e. hardware Trojans) pose a serious threat on US sovereignty as ICs are found in many commercial electronic devices as well as US assets that rely on ICs for computation or control such as our energy infrastructure, banking, or defense systems. The primary goal of our research group on hardware security and trust is to secure US electronic assets by assuring that the integrated circuits that are installed do not include functions that compromise the IC and the systems that rely on these ICs.

> **Sub-projects:** Run-time detection and countermeasures, design-for-trust algorithms and methodologies
{: .block-tip}

[View hardware security projects]({{ '/projects/' | relative_url }}#active)

</div>
</div>

---

## Sub/Near-Threshold Circuits with Current-Mode Logic

Since power and energy have not scaled similarly to the dimension of the transistor, it has become difficult to operate all transistors simultaneously for a given power budget and time (concept of dark silicon). One potential solution is to operate circuits in the sub-threshold or near-threshold regime. A reduction in supply voltage reduces dynamic power quadratically and static power exponentially. Our group explores near-threshold circuits (NTC) combined with dynamic current-mode logic (DCML) to trade off power and performance.

> **Sub-projects:** Power reduction using NTC with CML
{: .block-tip}

[View NTC/CML project]({{ '/projects/' | relative_url }}#active)
