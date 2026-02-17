---
layout: page
title: Blog
description: Featured-first technical writing feed with RSS output.
permalink: /blog/
nav: true
nav_order: 3
---

{% assign featured_posts = site.posts | where_exp: "post", "post.featured == true" | sort: "date" | reverse %}
{% assign other_posts = site.posts | where_exp: "post", "post.featured != true" | sort: "date" | reverse %}
{% assign ordered_posts = featured_posts | concat: other_posts %}

<div class="ri-page-shell ri-page-shell--blog">
  <section class="ri-page-section">
    {% if ordered_posts.size > 0 %}
      <div class="ri-grid ri-blog-grid">
        {% for post in ordered_posts %}
          <article class="ri-update-card">
            <p class="ri-update-meta">
              <time datetime="{{ post.date | date_to_xmlschema }}">{{ post.date | date: "%Y-%m-%d" }}</time>
              {% if post.featured %}<span class="ri-channel-chip ri-channel-chip--blog">Featured</span>{% endif %}
            </p>
            <h2><a href="{{ post.url | relative_url }}">{{ post.title }}</a></h2>
            {% if post.excerpt %}
              <p>{{ post.excerpt | strip_html | truncate: 180 }}</p>
            {% endif %}
          </article>
        {% endfor %}
      </div>
    {% else %}
      <article class="ri-panel ri-empty-state ri-blog-empty">
        <h2>No posts published yet</h2>
        <p>Long-form notes will appear here. The live RSS endpoint is available at <a href="{{ '/feed.xml' | relative_url }}">/feed.xml</a>.</p>
        <ul class="ri-blog-empty-list">
          <li>Planned topics: optimization, distributed training, and practical ML systems.</li>
          <li>Selected publications and CV are available from the top navigation.</li>
        </ul>
      </article>
    {% endif %}
  </section>
</div>
