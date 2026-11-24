"""Fail if any URL served by the old Phenomic site is missing from dist/.

The list comes from the sitemap published at https://acelpb.com/sitemap.xml
before the migration to Pelican (plus the feed). Search engines have these
indexed, so each one must keep resolving. New posts don't need to be added
here; this guards against regressions in URL settings.

Usage: python scripts/check_urls.py [output_dir]
"""

import sys
from pathlib import Path

LEGACY_URLS = [
    "/",
    "/404.html",
    "/about/",
    "/eliza/",  # now a redirect to /
    "/feed.xml",
    "/sitemap.xml",
    "/posts/2015-03-05-Combining-apache-spark-and-ipython-notebook/",
    "/posts/2015-09-07-Setting-up-a-test-cluster/",
    "/posts/2015-09-26-Install-NixOS-on-So-You-Start-dedicated-server/",
    "/posts/2015-12-12-SteamOS-KODI/",
]


def main(output_dir: str = "dist") -> int:
    root = Path(output_dir)
    missing = []
    for url in LEGACY_URLS:
        path = root / url.lstrip("/")
        if url.endswith("/"):
            path = path / "index.html"
        if not path.is_file():
            missing.append(f"{url}  (expected {path})")
    if missing:
        print("Missing legacy URLs:\n  " + "\n  ".join(missing))
        return 1
    print(f"All {len(LEGACY_URLS)} legacy URLs present in {root}/")
    return 0


if __name__ == "__main__":
    sys.exit(main(*sys.argv[1:]))
