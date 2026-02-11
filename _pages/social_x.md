---
layout: page
title: x posts
description: Markdown-backed X post library with editable external post links.
permalink: /social/x/
nav: false
---

{% assign entries = site.x_posts | sort: "date" | reverse %}
{% include social_collection_list.html
  entries=entries
  channel_name="X"
  collection_glob_label="_x_posts/*.md"
  empty_text="No X post entries found. Run the sync script."
%}
