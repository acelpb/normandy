"""Production settings (`make build`)."""

import os
import sys

sys.path.append(os.curdir)
from pelicanconf import *  # noqa: E402,F403

SITEURL = "https://acelpb.com"
RELATIVE_URLS = False

FEED_DOMAIN = SITEURL

DELETE_OUTPUT_DIRECTORY = True
