# acelpb.com

Source of [acelpb.com](https://acelpb.com), my personal blog and landing page.

It is a static site built with [Pelican](https://getpelican.com/) (Python), using
Markdown posts and a fork of the
[dev-random2](https://github.com/getpelican/pelican-themes/tree/master/dev-random2)
theme. Python dependencies are managed with
[uv](https://docs.astral.sh/uv/).

## Requirements

- [uv](https://docs.astral.sh/uv/getting-started/installation/) (it installs a
  suitable Python automatically; Python ≥ 3.12)
- `make` (optional, for the shortcuts below)

## Quick start

```sh
make install   # uv sync: creates .venv and installs Pelican
make serve     # dev server with live reload at http://localhost:8000
```

| Command        | What it does                                                         |
| -------------- | -------------------------------------------------------------------- |
| `make install` | Install dependencies into `.venv` (`uv sync`)                        |
| `make serve`   | Build with `pelicanconf.py` and serve with autoreload (`PORT=8000`)  |
| `make build`   | Production build into `dist/` with `publishconf.py`                 |
| `make check`   | Production build, then verify every legacy URL still exists          |
| `make clean`   | Remove `dist/`                                                       |

Without `make`, run the same commands directly, e.g.
`uv run pelican -s publishconf.py`.

## Writing a post

Add a Markdown file to `content/posts/`. **The file name is the URL**: the file
`content/posts/2026-11-02-Four-years-in-the-basement.md` is published at
`/posts/2026-11-02-Four-years-in-the-basement/`, with its capitalisation unchanged.

Front matter is YAML:

```markdown
---
title:    "My post title"
subtitle: "One-line summary, shown on the homepage and used as meta description"
date:     2026-11-24 09:00:00
author:   "Augustin Borsu"
---

Post body in Markdown. Raw HTML and tables are allowed.
```

Images and other files go in `content/assets/` and are copied to `/assets/`.
From a post, reference them relatively, e.g.
`![alt text](../../assets/my-post/photo.jpg)`.

Standalone pages (like `/about/`) live in `content/pages/`. The homepage intro
text is `content/pages/index.md`.

## Project layout

```
content/
  posts/        blog posts           -> /posts/<file-name>/
  pages/        standalone pages     -> /<file-name>/  (index.md = homepage intro)
  assets/       images and files     -> /assets/...
theme/          fork of dev-random2 (see "Theme" below)
  templates/    Jinja2 templates (base, index, article, page, archives, 404, sitemap, ...)
  static/css/   skeleton.css (layout), theme.css (look), pygments.css (code)
plugins/
  yaml_frontmatter.py   reads the YAML (`---`) front matter used by the posts
scripts/
  check_urls.py         guards the URLs indexed by search engines
pelicanconf.py  dev settings (relative URLs)
publishconf.py  production settings (https://acelpb.com, absolute URLs)
```

## URLs and search engines

The site was previously built with Phenomic (2017). The Pelican configuration
reproduces its URL scheme exactly so existing links and search results keep
working:

- `/`, `/about/`, `/404.html`
- `/posts/<file-name>/` for every post
- `/feed.xml` (RSS, 20 latest posts) and `/sitemap.xml`
- `/archives/` (new with the dev-random2 theme)
- `/eliza/`: the Eliza chat bot was removed; this URL now redirects to `/`
  (with `noindex` and a canonical link to the homepage)

`make check` fails if any of these disappear. If you change URL settings in
`pelicanconf.py`, run it before deploying.

## Deploying

```sh
make publish                       # build, check URLs, upload dist/ with rsync
make publish RSYNC_FLAGS=-rltvzn   # dry run: list what would be uploaded
```

`make publish` uploads the contents of `dist/` to `/var/www/root/` on the
`ac` SSH host (acelpb.com), the root nginx serves for acelpb.com. That folder
is owned by `nginx`, so the remote rsync runs as `sudo -u nginx`. Override
`DEPLOY_HOST` / `DEPLOY_PATH` if needed.

The upload never deletes files on the server; files from earlier builds stay
until removed by hand. nginx should serve `404.html` for missing pages
(`error_page 404 /404.html;`).

## Theme

`theme/` is a fork of dev-random2 from
[getpelican/pelican-themes](https://github.com/getpelican/pelican-themes)
(WTFPL, see `theme/LICENSE.txt`, screenshot in `theme/screenshot.png`).
Changes from upstream:

- translated from French to English
- category, tag and author links removed (the site doesn't use them); the
  sidebar lists pages, archives, the RSS feed and the `SOCIAL` links from
  `pelicanconf.py`
- Pelican 4 feed settings (`FEED_ALL_RSS`), Open Graph / Twitter meta tags
- homepage shows the intro from `content/pages/index.md` above the posts
- removed the IE8 shim, legacy Google Analytics snippet, Disqus and favicon links
- added `notfound.html` (404), `sitemap.html` and `eliza.html` (redirect)
- heading permalink style at the end of `theme.css`

To change code-highlighting colours, regenerate `pygments.css` with any
[Pygments style](https://pygments.org/styles/):

```sh
uv run pygmentize -S <style> -f html -a .highlight > theme/static/css/pygments.css
```
