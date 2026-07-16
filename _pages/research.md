---
layout: page
title: research
permalink: /research/
description: Research areas at the ICE Lab. Click an area to explore it and its projects.
nav: true
nav_order: 3
---

<!-- Each research area renders as a clickable card linking to its dedicated
     page under /research/<slug>/, which carries the full description and the
     area's project cards (selected by research_area front matter). -->

{% assign research_areas = "" | split: "" %}
{% capture area_3d %}3d-ics|3-D Integrated Circuits|assets/img/research/3d-ics.jpg|Power delivery, synchronization, and signaling for TSV-based and heterogeneous 3-D stacks. The lab's seminal TSV electrical models, fabricated multi-plane test circuits, thermal analysis, and free-space optical interconnects established early ground work for three-dimensional systems.{% endcapture %}
{% capture area_hw %}hardware-security|Hardware Security & Trust|assets/img/research/hardware-security.jpg|Securing integrated circuits against hardware Trojans, IP piracy, and reverse engineering. The group develops logic locking and analog parameter obfuscation, SAT-attack resilience analysis, and run-time detection with countermeasures - the subject of a 2018 NSF CAREER award.{% endcapture %}
{% capture area_ml %}ml-eda|Machine Learning for EDA|assets/img/projects/ml-eda/cover.png|Graph neural networks that predict expensive late-stage chip metrics - timing, parasitics, wirelength - from early design stages, transfer learning across technology nodes, and the open EDA-Schema data infrastructure and benchmarks that make ML-for-EDA results reproducible.{% endcapture %}
{% capture area_ntc %}ntc-cml|Sub/Near-Threshold Circuits with CML|assets/img/icelab_logo.png|Operating circuits near the transistor threshold voltage for quadratic power savings, then recovering performance with dynamic current-mode logic. The group designs resilient near-threshold circuits and methodologies that trade off power and throughput.{% endcapture %}
{% assign research_areas = research_areas | push: area_3d | push: area_hw | push: area_ml | push: area_ntc %}

<div class="research-areas">
{% for area in research_areas %}
  {% assign parts = area | split: "|" %}
  {% assign slug = parts[0] %}
  {% assign area_title = parts[1] %}
  {% assign area_img = parts[2] %}
  {% assign area_brief = parts[3] %}
  {% assign area_projects = site.projects | where: "research_area", slug | sort: "importance" %}
  {% capture area_url %}/research/{{ slug }}/{% endcapture %}

<h2 id="{{ slug }}">{{ area_title }}</h2>

  <a class="card hoverable research-area-card" href="{{ area_url | relative_url }}">
    <div class="row no-gutters">
      <div class="col-sm-4">
        {% include figure.liquid loading="lazy" path=area_img alt=area_title class="card-img research-area-img" %}
      </div>
      <div class="col-sm-8">
        <div class="card-body">
          <p class="card-text">{{ area_brief }}</p>
          <span class="research-area-toggle">
            {{ area_projects.size }} project{% if area_projects.size != 1 %}s{% endif %}
            <i class="fa-solid fa-arrow-right"></i>
          </span>
        </div>
      </div>
    </div>
  </a>
{% endfor %}
</div>
