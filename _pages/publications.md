---
layout: page
title: Publications
description: Full BibTeX-backed publication list.
permalink: /publications/
nav: true
nav_order: 1
---

<div class="ri-page-shell ri-page-shell--publications">
  <section class="ri-page-section">
    <div class="ri-panel ri-bibliography-wrap">
      {% bibliography --file papers --group_by year --group_order descending %}
    </div>
  </section>
</div>
