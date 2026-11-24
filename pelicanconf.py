"""Pelican settings for local development (`make serve`).

Production overrides live in publishconf.py.

URL layout mirrors the previous Phenomic site so links indexed by search
engines keep working; `make check` verifies it (see scripts/check_urls.py).
"""

AUTHOR = "Augustin Borsu"
SITENAME = "ACELPB"
SITEURL = ""
SOCIAL = [
    ("LinkedIn", "https://www.linkedin.com/in/aborsu/"),
    ("GitHub", "https://github.com/aborsu"),
    ("Source of this site", "https://github.com/acelpb/normandy"),
]

PATH = "content"
OUTPUT_PATH = "dist"
THEME = "theme"  # fork of dev-random2 from getpelican/pelican-themes
TIMEZONE = "Europe/Brussels"
DEFAULT_LANG = "en"
DEFAULT_DATE_FORMAT = "%a %b %d %Y"

# Content front matter is YAML (`---` delimited), parsed by a local plugin.
PLUGIN_PATHS = ["plugins"]
PLUGINS = ["yaml_frontmatter"]

ARTICLE_PATHS = ["posts"]
PAGE_PATHS = ["pages"]
STATIC_PATHS = ["assets"]

# --- URLs (must stay compatible with the old site) -------------------------
# The slug is the file name verbatim (case preserved), e.g.
# posts/2015-12-12-SteamOS-KODI.md -> /posts/2015-12-12-SteamOS-KODI/
FILENAME_METADATA = r"(?P<slug>.*)"
ARTICLE_URL = "posts/{slug}/"
ARTICLE_SAVE_AS = "posts/{slug}/index.html"
PAGE_URL = "{slug}/"
PAGE_SAVE_AS = "{slug}/index.html"

# Generated pages: homepage, archives, 404, sitemap, and a redirect for the
# retired /eliza/ page (the chat bot was removed in the Pelican migration).
DIRECT_TEMPLATES = ["index", "archives", "notfound", "sitemap", "eliza"]
INDEX_SAVE_AS = "index.html"
ARCHIVES_SAVE_AS = "archives/index.html"
ARCHIVES_URL = "archives/"
NOTFOUND_SAVE_AS = "404.html"
SITEMAP_SAVE_AS = "sitemap.xml"
ELIZA_SAVE_AS = "eliza/index.html"
DEFAULT_PAGINATION = False

# Things Pelican generates by default that the old site never had.
TAG_SAVE_AS = TAGS_SAVE_AS = ""
CATEGORY_SAVE_AS = CATEGORIES_SAVE_AS = ""
AUTHOR_SAVE_AS = AUTHORS_SAVE_AS = ""

# --- Feeds -----------------------------------------------------------------
# Only the RSS feed at /feed.xml, like before.
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None
TRANSLATION_FEED_ATOM = None
FEED_ALL_RSS = "feed.xml"
FEED_MAX_ITEMS = 20

# --- Markdown --------------------------------------------------------------
MARKDOWN = {
    "extension_configs": {
        "markdown.extensions.codehilite": {"css_class": "highlight"},
        "markdown.extensions.extra": {},
        "markdown.extensions.toc": {"permalink": "#"},
    },
    "output_format": "html5",
}

RELATIVE_URLS = True
