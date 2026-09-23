"""Sphinx configuration for the LimaNix documentation website."""

project = "LimaNix"
author = "LimaNix"
language = "en"

extensions = ["myst_parser", "sphinxcontrib.mermaid"]
source_suffix = {".md": "markdown"}
myst_fence_as_directive = ["mermaid"]
root_doc = "index"
nitpicky = True
smartquotes = False

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
