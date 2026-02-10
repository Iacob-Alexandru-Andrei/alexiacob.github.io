---
layout: page
title: linkedin posts
description: Markdown-backed LinkedIn post library with editable external post links.
permalink: /social/linkedin/
nav: false
---

<p>
  Set or edit each post URL in <code>external_url</code> front matter under
  <code>_linkedin_posts/*.md</code>.
</p>

{% assign entries = site.linkedin_posts | sort: "date" | reverse %}
{% if entries.size > 0 %}
  <ul>
    {% for entry in entries %}
      <li>
        <a href="{{ entry.url | relative_url }}">{{ entry.title }}</a>
        <span>({{ entry.date | date: "%Y-%m-%d" }})</span>
        {% if entry.external_url and entry.external_url != "" %}
          <br><a href="{{ entry.external_url }}">Original LinkedIn post</a>
        {% else %}
          <br><small>Add <code>external_url</code> in this entry's front matter.</small>
        {% endif %}
      </li>
    {% endfor %}
  </ul>
{% else %}
  <p>No LinkedIn post entries found. Run the sync script.</p>
{% endif %}
