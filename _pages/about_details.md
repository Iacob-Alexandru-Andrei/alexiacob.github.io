---
layout: page
title: Profile
description: Detailed background, affiliations, and contact channels.
permalink: /about/
---

<div class="ri-page-shell ri-page-shell--about">
  <section class="ri-page-section ri-panel">
    <h2>Overview</h2>
    <p>{{ site.data.profile.summary }}</p>
    {% for paragraph in site.data.profile.about %}
      <p>{{ paragraph }}</p>
    {% endfor %}
  </section>

  <section class="ri-page-section ri-panel">
    <h2>Affiliations</h2>
    <ul>
      {% for affiliation in site.data.profile.affiliations %}
        <li>{{ affiliation }}</li>
      {% endfor %}
    </ul>
  </section>

  <section class="ri-page-section ri-panel">
    <h2>Contact and Links</h2>
    <div class="ri-grid ri-link-grid">
      {% for social in site.data.social_links %}
        {% if social.placeholder %}
          <article class="ri-link-card ri-link-card-muted">
            <p>{{ social.label }}: configure</p>
          </article>
        {% else %}
          <article class="ri-link-card">
            <p><a href="{{ social.url }}">{{ social.label }}</a></p>
          </article>
        {% endif %}
      {% endfor %}
    </div>
  </section>
</div>
