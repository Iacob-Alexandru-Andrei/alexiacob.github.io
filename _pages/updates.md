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
    {% include updates_grid.html
      items=updates
      excerpt_chars=180
      empty_variant="panel"
      empty_title="No updates available yet"
      empty_text="Publish a news item, blog post, or synced social entry to populate this stream."
    %}
  </section>
</div>
