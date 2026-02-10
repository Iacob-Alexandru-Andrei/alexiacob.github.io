---
layout: page
title: Updates
description: Unified stream of research news, blog writing, and social posts.
permalink: /updates/
nav: true
nav_order: 4
---

{% assign updates = site.news | concat: site.posts | concat: site.linkedin_posts | concat: site.x_posts | sort: "date" | reverse %}

<div class="ri-page-shell ri-page-shell--updates">
  <section class="ri-page-section">
    {% if updates.size > 0 %}
      <div class="ri-grid ri-updates-grid">
        {% for item in updates %}
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
              <p class="ri-update-excerpt">{{ item.excerpt | strip_html | truncate: 180 }}</p>
            {% endif %}
            {% if item.external_url and item.external_url != "" %}
              <p class="ri-update-link"><a href="{{ item.external_url }}" rel="noopener noreferrer">Open original post</a></p>
            {% endif %}
          </article>
        {% endfor %}
      </div>
    {% else %}
      <div class="ri-panel ri-empty-state">
        <h2>No updates available yet</h2>
        <p>Publish a news item, blog post, or synced social entry to populate this stream.</p>
      </div>
    {% endif %}
  </section>
</div>
