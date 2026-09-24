"""Sphinx configuration for the LimaNix documentation website."""

import os

# Project
project = "LimaNix"
author = "LimaNix"
language = "en"

client_tag = os.environ.get("CLIENT_TAG", "")
release = client_tag
version = client_tag

# Source pages
extensions = ["myst_parser", "sphinxcontrib.mermaid"]
source_suffix = {".md": "markdown"}
root_doc = "index"
nitpicky = True
smartquotes = False

exclude_patterns = ["projects/*/_generated/**"]
if not client_tag:
    exclude_patterns.append("projects/client/reference/**")

# HTML appearance
html_theme = "sphinx_book_theme"
html_title = "Limanix documentation"
html_theme_options = {
    "repository_url": "https://github.com/limanix/docs",
    "use_repository_button": True,
    "navbar_persistent": [],
}

html_static_path = ["_static"]
html_css_files = ["mermaid.css", "toolbar.css"]
html_show_sourcelink = False
html_use_index = False

# Client release title and version navigation
if client_tag:
    modules_tag = os.environ["MODULES_TAG"]
    html_title = f"Limanix {client_tag} · modules {modules_tag}"
    html_theme_options["switcher"] = {
        "json_url": "/client/versions.json",
        "version_match": client_tag,
    }
    html_theme_options["check_switcher"] = False
    html_sidebars = {
        "**": [
            "navbar-logo.html",
            "version-switcher.html",
            "icon-links.html",
            "search-button-field.html",
            "sbt-sidebar-nav.html",
        ]
    }

# Mermaid diagrams
myst_fence_as_directive = ["mermaid"]
mermaid_version = "11.12.1"
mermaid_fullscreen = False
mermaid_height = "auto"
mermaid_light_theme = "neutral"
mermaid_init_config = {
    "startOnLoad": False,
    "flowchart": {
        "useMaxWidth": True,
        "htmlLabels": False,
        "nodeSpacing": 24,
        "rankSpacing": 32,
        "padding": 12,
    },
}
