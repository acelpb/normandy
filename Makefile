PELICAN ?= uv run pelican
PORT ?= 8000

.PHONY: install serve build check clean

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
