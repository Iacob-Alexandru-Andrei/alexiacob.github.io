---
layout: page
title: linkedin posts
description: Markdown-backed LinkedIn post library with editable external post links.
permalink: /social/linkedin/
nav: false
---

{% assign entries = site.linkedin_posts | sort: "date" | reverse %}
{% include social_collection_list.html
  entries=entries
  channel_name="LinkedIn"
  collection_glob_label="_linkedin_posts/*.md"
  empty_text="No LinkedIn post entries found. Run the sync script."
%}
