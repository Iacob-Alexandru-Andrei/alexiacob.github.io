---
layout: about
title: About
permalink: /
subtitle: University of Cambridge · Flower Labs
profile: false
selected_papers: false
social: false
announcements:
  enabled: false
latest_posts:
  enabled: false
seo:
  links:
    - https://github.com/Iacob-Alexandru-Andrei
    - https://www.linkedin.com/in/alex-iacob-898775194/
    - https://scholar.google.com/citations?user=m86W6CQAAAAJ&hl=en
---

{% assign email_url = "" %}
{% assign cv_url = "" %}
{% assign scholar_url = "" %}
{% assign github_url = "" %}
{% assign linkedin_url = "" %}
{% for social in site.data.social_links %}
  {% if social.label == "Email" %}{% assign email_url = social.url %}{% endif %}
  {% if social.label == "CV PDF" %}{% assign cv_url = social.url %}{% endif %}
  {% if social.label == "Google Scholar" %}{% assign scholar_url = social.url %}{% endif %}
  {% if social.label == "GitHub" %}{% assign github_url = social.url %}{% endif %}
  {% if social.label == "LinkedIn" %}{% assign linkedin_url = social.url %}{% endif %}
{% endfor %}

<div class="ri-home-shell">
  <section class="ri-home-section ri-home-section--hero">
    <div class="ri-hero-shell">
      <div class="ri-hero-copy">
        <p class="ri-eyebrow">ML Research Scientist · PhD Candidate</p>
        <h2 class="ri-hero-title">Machine learning research from core methods to scalable systems.</h2>
        <p class="ri-hero-lede">
          I work on optimization and large-scale model training across geographically distributed
          infrastructure. My current projects emphasize efficient training and robust
          performance in realistic resource-constrained environments.
          For current work and activity, start with
          <a href="{{ '/publications/' | relative_url }}">papers</a>
          and
          <a href="{{ '/updates/' | relative_url }}">updates</a>.
        </p>

        <div class="ri-cta-row">
          <a class="ri-cta" href="{{ email_url }}">Email</a>
          <a class="ri-cta" href="{{ cv_url | relative_url }}">CV PDF</a>
          <a class="ri-cta" href="{{ scholar_url }}">Google Scholar</a>
          <a class="ri-cta" href="{{ github_url }}">GitHub</a>
          <a class="ri-cta" href="{{ linkedin_url }}">LinkedIn</a>
        </div>
      </div>

      <div class="ri-hero-media" aria-hidden="true">
        <img src="{{ '/assets/img/profile.jpg' | relative_url }}" alt="" loading="eager" decoding="async">
      </div>
    </div>
  </section>

  <section class="ri-home-section ri-home-section--featured">
    <h2>Selected Publications</h2>
    <div class="ri-grid ri-pub-grid">
      {% assign featured_shown = 0 %}
      {% for rank in (1..20) %}
        {% for pair in site.data.publication_meta %}
          {% assign bib_key = pair[0] %}
          {% assign meta = pair[1] %}
          {% if meta.featured and meta.featured_rank == rank %}
            {% include publication_card.html key=bib_key meta=meta %}
            {% assign featured_shown = featured_shown | plus: 1 %}
            {% if featured_shown == 5 %}{% break %}{% endif %}
          {% endif %}
        {% endfor %}
        {% if featured_shown == 5 %}{% break %}{% endif %}
      {% endfor %}
      <article class="ri-pub-card ri-pub-card--cta ri-cta-card">
        <h3><a href="{{ '/publications/' | relative_url }}">View Full Bibliography</a></h3>
        <p>Open the complete publication list with full citation details.</p>
      </article>
    </div>
  </section>

  {% assign recent_items = site.news | concat: site.posts | concat: site.linkedin_posts | concat: site.x_posts | sort: "date" | reverse %}
  <section class="ri-home-section ri-home-section--updates">
    <h2>Latest Updates</h2>
    <div class="ri-grid ri-updates-grid">
      {% if recent_items.size > 0 %}
        {% for item in recent_items limit: 5 %}
          {% assign channel_label = "Update" %}
          {% assign channel_class = "ri-channel-chip--update" %}
          {% if item.collection == "news" %}
            {% assign channel_label = "News" %}
            {% assign channel_class = "ri-channel-chip--news" %}
          {% elsif item.collection == "posts" %}
            {% assign channel_label = "Blog" %}
            {% assign channel_class = "ri-channel-chip--blog" %}
          {% elsif item.collection == "linkedin_posts" %}
            {% assign channel_label = "LinkedIn" %}
            {% assign channel_class = "ri-channel-chip--linkedin" %}
          {% elsif item.collection == "x_posts" %}
            {% assign channel_label = "X" %}
            {% assign channel_class = "ri-channel-chip--x" %}
          {% endif %}
          <article class="ri-update-card">
            <p class="ri-update-meta">
              <time datetime="{{ item.date | date_to_xmlschema }}">{{ item.date | date: "%Y-%m-%d" }}</time>
              <span class="ri-channel-chip {{ channel_class }}">{{ channel_label }}</span>
            </p>
            <h3><a href="{{ item.url | relative_url }}">{{ item.title | default: "Untitled update" }}</a></h3>
            {% if item.excerpt %}
              <p class="ri-update-excerpt">{{ item.excerpt | strip_html | truncate: 160 }}</p>
            {% endif %}
            {% if item.external_url and item.external_url != "" %}
              <p class="ri-update-link"><a href="{{ item.external_url }}" rel="noopener noreferrer">Open original post</a></p>
            {% endif %}
          </article>
        {% endfor %}
      {% else %}
        <article class="ri-update-card">
          <h3>No updates yet</h3>
          <p>Run the sync script to ingest LinkedIn and X items, or publish blog/news entries.</p>
        </article>
      {% endif %}
      <article class="ri-update-card ri-update-card--cta ri-cta-card">
        <h3><a href="{{ '/updates/' | relative_url }}">View All Updates</a></h3>
        <p>Browse the complete stream across news, writing, and social posts.</p>
      </article>
    </div>
  </section>
</div>
