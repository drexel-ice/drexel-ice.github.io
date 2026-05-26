# Adding Content to the ICE Lab Website

This guide is for lab members who want to add news, team profiles, projects, or publications **without writing code**. Changes go live automatically after a pull request is merged to `main`.

## How the site is organized

| What you see on the site | Where the content lives |
| ------------------------ | ----------------------- |
| Homepage mission & PI info | `_pages/about.md` |
| Research overview | `_pages/research.md` |
| Project cards | `_projects/*.md` |
| Team page | `_team/*.md` |
| Short homepage announcements | `_news/YYYY-MM-DD-title.md` |
| Homepage featured slider | `_data/featured_slides.yml` |
| Full news archive (blog) | `_posts/YYYY-MM-DD-title.md` |
| Publications list | `_bibliography/papers.bib` |
| PDF reprints | `assets/pdf/` |
| Photos | `assets/img/team/`, `assets/img/research/`, `assets/img/projects/` |

**Homepage vs blog vs news**

- `_news/` — brief inline items on the homepage (awards, paper acceptances, recruiting). Use `inline: true`.
- `_posts/` — full archive entries on the [News](/icelab-website/blog/) page with dates and pagination.
- For major announcements, add both: a `_news/` highlight and a `_posts/` archive entry.

---

## Step-by-step workflows

### Add a homepage announcement

1. Create `_news/2026-06-01-your-title.md`:

```markdown
---
layout: post
date: 2026-06-01
inline: true
related_posts: false
---

**Paper accepted at ISCAS 2026** — Our work on hardware obfuscation was accepted. Congrats to the team!
```

2. Open a pull request. CI will build the site and check formatting.

### Update the homepage featured slider

The rotating banner at the top of the homepage is configured in `_data/featured_slides.yml`. Each slide needs:

- `image` — path to a photo in `assets/img/` (place banner images in `assets/img/banners/`)
- `title` — headline shown on the slide
- `caption` — optional short description
- `link` — where the slide goes when clicked (e.g. `/news/2026-06-01-your-title/`)

Example:

```yaml
- image: assets/img/banners/your-banner.jpg
  title: Paper Accepted at ISCAS 2026
  caption: Our work on hardware obfuscation was accepted.
  link: /news/2026-06-01-your-title/
```

Add, remove, or reorder entries in that file. Slides autoplay every 6 seconds and link to the news item or blog post you specify.

### Add a full news / blog post

1. Create `_posts/2026-06-01-your-title.md`:

```markdown
---
layout: post
title: Paper Accepted at ISCAS 2026
date: 2026-06-01
description: Brief summary for search and previews.
tags: news
---

Full announcement text here. Include authors, venue, and links if helpful.
```

### Add a team member

1. Save a headshot to `assets/img/team/first-last.jpg` (roughly square, ≥400×400 px).
2. Create `_team/first-last.md`:

```markdown
---
layout: page
title: First Last
description: Ph.D. Student | email@drexel.edu
img: assets/img/team/first-last.jpg
importance: 9
category: phd
---

Short bio: research interests, education, prior experience.
```

**Categories:** `faculty`, `phd`, or `alumni`. Lower `importance` numbers appear first within a category.

### Add a research project

1. Optional: add a figure to `assets/img/projects/`.
2. Create `_projects/project-slug.md`:

```markdown
---
layout: page
title: Project Title
description: One-sentence summary for the project card.
importance: 1
category: active
---

Longer project description migrated from legacy research pages or a new write-up.
```

Use `category: active` or `category: completed`.

### Add a publication

1. Add a BibTeX entry to `_bibliography/papers.bib`:

```bibtex
@inproceedings{chen2026example,
  title     = {Your Paper Title},
  author    = {Chen, Ziyi and Savidis, Ioannis},
  booktitle = {IEEE International Symposium on Circuits and Systems (ISCAS)},
  year      = {2026},
  abbr      = {ISCAS},
  pdf       = {assets/pdf/conferences/chen2026example.pdf},
  selected  = {true},
}
```

2. Upload the PDF to the matching folder under `assets/pdf/` (`journals/`, `conferences/`, `dissertations/`, `tutorials/`, etc.).
3. Set `selected = {true}` only for papers you want highlighted on the homepage.

---

## Review process

1. Create a branch: `git checkout -b content/your-change`
2. Commit your markdown/BibTeX/PDF changes
3. Open a **Pull Request** on GitHub
4. Wait for CI (build + BibTeX validation)
5. Ask **Prof. Savidis** or the site maintainer for review
6. Merge to `main` → site deploys to https://jiwanizakir.github.io/icelab-website/

---

## Image naming conventions

| Type | Path | Example |
| ---- | ---- | ------- |
| Team headshots | `assets/img/team/{slug}.jpg` | `assets/img/team/pratik-shrestha.png` |
| Research figures | `assets/img/research/{topic}.jpg` | `assets/img/research/3d-ics.jpg` |
| Project thumbnails | `assets/img/projects/{slug}.jpg` | optional |
| Lab logo | `assets/img/icelab_logo.png` | homepage / branding |

---

## Questions?

See [CONTRIBUTING.md](CONTRIBUTING.md) for developer setup, or open a GitHub issue.
