---
layout: page
title: CV
description: Research CV with downloadable artifacts and concise role timelines.
permalink: /cv/
nav: true
nav_order: 2
---

<div class="ri-page-shell ri-page-shell--cv">
  <section class="ri-page-section ri-panel ri-cv-header">
    <div class="ri-cv-actions">
      <a class="ri-section-action" href="{{ '/assets/cv/Alex_Iacob_CV.pdf' | relative_url }}">Download CV PDF</a>
      <a class="ri-section-action ri-section-action--muted" href="{{ '/assets/cv/main.tex' | relative_url }}">View CV TeX Source</a>
    </div>
  </section>

  <section class="ri-page-section ri-panel ri-cv-section">
    <h2>Education</h2>
    <div class="ri-cv-timeline">
      {% for item in site.data.cv.education %}
        <article class="ri-cv-item">
          <p class="ri-cv-period">{{ item.period }}</p>
          <div class="ri-cv-body">
            <h3>{{ item.degree }} · {{ item.institution }}</h3>
            <ul>
              {% for detail in item.details %}
                <li>{{ detail }}</li>
              {% endfor %}
            </ul>
          </div>
        </article>
      {% endfor %}
    </div>
  </section>

  <section class="ri-page-section ri-panel ri-cv-section">
    <h2>Experience</h2>
    <div class="ri-cv-timeline">
      {% for item in site.data.cv.experience %}
        <article class="ri-cv-item">
          <p class="ri-cv-period">{{ item.period }}</p>
          <div class="ri-cv-body">
            <h3>{{ item.role }} · {{ item.organization }}</h3>
            <ul>
              {% for bullet in item.bullets %}
                <li>{{ bullet }}</li>
              {% endfor %}
            </ul>
          </div>
        </article>
      {% endfor %}
    </div>
  </section>

  <section class="ri-page-section ri-panel ri-cv-section">
    <h2>Skills</h2>
    <div class="ri-grid ri-skill-grid">
      {% for group in site.data.cv.skills %}
        <article class="ri-skill-card ri-cv-skill-card">
          <h3>{{ group.category }}</h3>
          <p>{{ group.items | join: ", " }}</p>
        </article>
      {% endfor %}
    </div>
  </section>

  <section class="ri-page-section ri-panel ri-cv-section">
    <h2>Selected Publications</h2>
    <ul class="ri-cv-publication-list">
      {% for item in site.data.cv.selected_publications %}
        <li>{{ item }}</li>
      {% endfor %}
    </ul>
    <p class="ri-section-action-wrap">
      <a class="ri-section-action" href="{{ '/publications/' | relative_url }}">View full publications</a>
    </p>
  </section>
</div>
