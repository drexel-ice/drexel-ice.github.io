---
layout: page
title: research
permalink: /research/
description: Research areas at the ICE Lab. Click an area to see its projects.
nav: true
nav_order: 3
toc:
  sidebar: left
---

<!-- Each research area renders as a clickable card: the collapsed state gives
     a brief, and expanding it reveals the area's project cards, pulled from
     site.projects by their research_area front matter. -->

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

<h2 id="{{ slug }}">{{ area_title }}</h2>

  <a
    class="card hoverable research-area-card collapsed"
    data-toggle="collapse"
    href="#area-{{ slug }}"
    role="button"
    aria-expanded="false"
    aria-controls="area-{{ slug }}"
  >
    <div class="row no-gutters">
      <div class="col-sm-4">
        {% include figure.liquid loading="lazy" path=area_img alt=area_title class="card-img research-area-img" %}
      </div>
      <div class="col-sm-8">
        <div class="card-body">
          <p class="card-text">{{ area_brief }}</p>
          <span class="research-area-toggle">
            {{ area_projects.size }} project{% if area_projects.size != 1 %}s{% endif %}
            <i class="fa-solid fa-chevron-down"></i>
          </span>
        </div>
      </div>
    </div>
  </a>

  <div class="collapse research-area-projects projects" id="area-{{ slug }}">
    <div class="row row-cols-1 row-cols-md-2">
      {% for project in area_projects %}
        {% include projects.liquid %}
      {% endfor %}
    </div>
  </div>
{% endfor %}
</div>
