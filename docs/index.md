---
layout: home
title: Hyperframes
---

# Hyperframes

**Hyperframes** is a research project exploring the intersection of sociological worlds, attention architectures, and narrative variation through computational and literary methods.

## Current Focus Areas

- **[Research](/research)** — Conceptual introductions to ongoing research in phenomenological worlds, attention systems, and intervention techniques
- **[Audiobooks](/audiobooks)** — Narrative audiobook projects generated through variational storytelling techniques
- **[Repository Guide](/guide)** — How to navigate and use this repository's tools and workflows

---

## Recent Updates

{% for post in site.posts limit:3 %}
- **{{ post.date | date: "%B %d, %Y" }}**: [{{ post.title }}]({{ post.url }})
{% endfor %}

---

## About

This site serves as a public portal to an evolving body of work that combines:
- Sociological and phenomenological analysis of cultural worlds
- Computational attention architectures
- Generative narrative variations and audiobook production
- Open research methodologies and reproducible workflows

All source materials, code, and documentation are available in the [GitHub repository](https://github.com/mostlycached/schema).
