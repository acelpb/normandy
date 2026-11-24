"""Read Markdown files whose metadata is a YAML front-matter block.

The posts were written for Jekyll/Phenomic, so they start with:

    ---
    title: "Some title"
    date: 2015-03-05 14:18:00
    ---

Pelican's built-in Markdown reader expects `Key: value` lines without
quoting, so this plugin replaces it for `.md` / `.markdown` files.
"""

import re

import yaml
from markdown import Markdown
from pelican import signals
from pelican.readers import BaseReader
from pelican.utils import pelican_open

FRONT_MATTER = re.compile(r"\A---\s*\n(.*?)\n---\s*(?:\n|\Z)", re.DOTALL)


class YamlMarkdownReader(BaseReader):
    enabled = True
    file_extensions = ["md", "markdown"]

    def read(self, source_path):
        with pelican_open(source_path) as text:
            match = FRONT_MATTER.match(text)
            raw_meta = yaml.safe_load(match.group(1)) if match else {}
            body = text[match.end():] if match else text

        md = Markdown(**self.settings["MARKDOWN"])
        content = md.convert(body)

        metadata = {}
        for key, value in (raw_meta or {}).items():
            name = key.lower()
            # YAML turns dates into date/datetime objects; Pelican's
            # processors expect the raw string.
            if not isinstance(value, (str, list, dict)):
                value = "" if value is None else str(value)
            metadata[name] = self.process_metadata(name, value)
        return content, metadata


def add_reader(readers):
    for ext in YamlMarkdownReader.file_extensions:
        readers.reader_classes[ext] = YamlMarkdownReader


def register():
    signals.readers_init.connect(add_reader)
