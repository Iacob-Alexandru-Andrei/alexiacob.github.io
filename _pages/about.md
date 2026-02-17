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
    - https://scholar.google.com/citations?user=m86W6CQAAAAJ&hl=en
---

{% assign home = site.data.home %}
{% assign featured_keys = site.data.featured_publications %}
{% assign featured_limit = home.featured_publications.limit | default: 5 %}

<div class="ri-home-shell">
  <section class="ri-home-section ri-home-section--hero">
    <div class="ri-hero-shell">
      <div class="ri-hero-copy">
        <p class="ri-eyebrow">{{ home.hero.eyebrow }}</p>
        <h2 class="ri-hero-title">{{ home.hero.title }}</h2>
        <p class="ri-hero-lede">
          {{ home.hero.lede }}
          {{ home.hero.links_intro }}
          <a href="{{ home.hero.publications_url | relative_url }}">{{ home.hero.publications_label }}</a>
          and
          <a href="{{ home.hero.blog_url | relative_url }}">{{ home.hero.blog_label }}</a>.
        </p>

        <div class="ri-cta-row">
          {% for cta in home.hero.ctas %}
            {% assign link = site.data.social_links | where: "id", cta.link_id | first %}
            {% if link and link.url %}
              {% assign cta_href = link.url %}
              {% assign cta_prefix = link.url | slice: 0, 1 %}
              {% if cta_prefix == "/" %}
                {% assign cta_href = link.url | relative_url %}
              {% endif %}
              <a class="ri-cta" href="{{ cta_href }}">{{ cta.label }}</a>
            {% endif %}
          {% endfor %}
        </div>
      </div>

      <div class="ri-hero-media" aria-hidden="true">
        <img src="{{ '/assets/img/profile.jpg' | relative_url }}" alt="" loading="eager" decoding="async">
      </div>
    </div>
  </section>

  <section class="ri-home-section ri-home-section--featured">
    <h2>{{ home.featured_publications.title }}</h2>
    <div class="ri-grid ri-pub-grid">
      {% if featured_keys and featured_keys.size > 0 %}
        {% for bib_key in featured_keys limit: featured_limit %}
          {% assign meta = site.data.publication_meta[bib_key] %}
          {% include publication_card.html key=bib_key meta=meta %}
        {% endfor %}
      {% endif %}
      <article class="ri-pub-card ri-pub-card--cta ri-cta-card">
        <h3><a href="{{ '/publications/' | relative_url }}">Full Bibliography</a></h3>
      </article>
    </div>
  </section>

</div>
