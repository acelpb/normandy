PELICAN ?= uv run pelican
PORT ?= 8000

.PHONY: install serve build check clean publish

install:  ## Install Python dependencies into .venv
	uv sync

serve:  ## Dev server with live reload on http://localhost:$(PORT)
	$(PELICAN) -s pelicanconf.py --autoreload --listen --port $(PORT)

build:  ## Production build into dist/
	$(PELICAN) -s publishconf.py --fatal errors

check: build  ## Build and verify all legacy URLs still exist
	uv run python scripts/check_urls.py dist

clean:
	rm -rf dist

# Upload dist/ to the web root nginx serves (see README "Deploying").
# The trailing slash on dist/ copies its contents, not the folder itself.
# The remote side runs as the nginx user, which owns /var/www/root.
DEPLOY_HOST ?= ac
DEPLOY_PATH ?= /var/www/root/
RSYNC_FLAGS ?= -rltvz

publish: check  ## Build, verify URLs, then upload to the server
	rsync $(RSYNC_FLAGS) --rsync-path="sudo -u nginx rsync" dist/ $(DEPLOY_HOST):$(DEPLOY_PATH)
