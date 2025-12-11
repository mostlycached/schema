---
layout: home
title: Hyperframes
---

A research project exploring the intersection of sociological worlds, attention architectures, and narrative variation through computational and literary methods.

## Current Focus Areas

- **[Rooms](/rooms)** — Immersive audiobook experiences as distinct narrative environments
- **[Upcoming](/upcoming)** — Kiln: the interactive, personalized evolution of Hyperframes

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
