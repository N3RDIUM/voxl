import os
import sys

sys.path.insert(0, os.path.abspath(".."))  # project root

# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = "voxl"
copyright = "2026, n3rdium"
author = "n3rdium"

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.todo",
    "sphinx.ext.napoleon",  # Google / NumPy style docstrings
    "sphinx.ext.viewcode",  # link to source
    "sphinx_copybutton",
    "sphinx_sitemap",
]

templates_path = ["_templates"]
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]

html_baseurl = "https://voxl.n3rdium.dev/docs/"
sitemap_excludes = [
    "search.html",
    "genindex.html",
]
sitemap_show_lastmod = True
sitemap_indent = 4

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = "furo"
html_theme_options = {  # Gruvbox theme to match with n3rdium.dev
    "light_css_variables": {
        "color-problematic": "#cc241d",
        "color-foreground-primary": "#3c3836",
        "color-foreground-secondary": "#665c54",
        "color-foreground-muted": "#7c6f64",
        "color-foreground-border": "#928374",
        "color-background-primary": "#fbf1c7",
        "color-background-secondary": "#f2e5bc",
        "color-background-hover": "#f9f5d7",
        "color-background-hover--transparent": "#f9f5d700",
        "color-background-border": "#ebdbb2",
        "color-background-item": "#d5c4a1",
        "color-announcement-background": "#3c3836dd",
        "color-announcement-text": "#fbf1c7",
        "color-brand-primary": "#458588",
        "color-brand-content": "#689d6a",
        "color-brand-visited": "#b16286",
        "color-api-background": "var(--color-background-hover--transparent)",
        "color-api-background-hover": "var(--color-background-hover)",
        "color-api-overall": "var(--color-foreground-secondary)",
        "color-api-name": "var(--color-problematic)",
        "color-api-pre-name": "var(--color-problematic)",
        "color-api-paren": "var(--color-foreground-secondary)",
        "color-api-keyword": "var(--color-foreground-primary)",
        "color-api-added": "#98971a",
        "color-api-added-border": "#b8bb26",
        "color-api-changed": "#d79921",
        "color-api-changed-border": "#fabd2f",
        "color-api-deprecated": "#b16286",
        "color-api-deprecated-border": "#d3869b",
        "color-api-removed": "#cc241d",
        "color-api-removed-border": "#fb4934",
        "color-highlight-on-target": "#fdf6e3",
        "color-inline-code-background": "var(--color-background-secondary)",
        "color-highlighted-background": "#d5c4a1",
        "color-highlighted-text": "var(--color-foreground-primary)",
        "color-guilabel-background": "#fabd2f40",
        "color-guilabel-border": "#d7992140",
        "color-guilabel-text": "var(--color-foreground-primary)",
        "color-admonition-background": "transparent",
        "color-table-header-background": "var(--color-background-secondary)",
        "color-table-border": "var(--color-background-border)",
        "color-card-border": "var(--color-background-secondary)",
        "color-card-background": "transparent",
        "color-card-marginals-background": "var(--color-background-secondary)",
        "color-header-background": "var(--color-background-primary)",
        "color-header-border": "var(--color-background-border)",
        "color-header-text": "var(--color-foreground-primary)",
        "color-sidebar-background": "var(--color-background-secondary)",
        "color-sidebar-background-border": "var(--color-background-border)",
        "color-sidebar-brand-text": "var(--color-foreground-primary)",
        "color-sidebar-caption-text": "var(--color-foreground-muted)",
        "color-sidebar-link-text": "var(--color-foreground-secondary)",
        "color-sidebar-link-text--top-level": "var(--color-brand-primary)",
        "color-sidebar-item-background": "var(--color-sidebar-background)",
        "color-sidebar-item-background--current": "var(--color-sidebar-item-background)",
        "color-sidebar-item-background--hover": "linear-gradient(90deg, var(--color-background-hover--transparent) 0%, var(--color-background-hover) var(--sidebar-item-spacing-horizontal), var(--color-background-hover) 100%)",
        "color-sidebar-item-expander-background": "transparent",
        "color-sidebar-item-expander-background--hover": "var(--color-background-hover)",
        "color-sidebar-search-text": "var(--color-foreground-primary)",
        "color-sidebar-search-background": "var(--color-background-secondary)",
        "color-sidebar-search-background--focus": "var(--color-background-primary)",
        "color-sidebar-search-border": "var(--color-background-border)",
        "color-sidebar-search-icon": "var(--color-foreground-muted)",
        "color-toc-background": "var(--color-background-primary)",
        "color-toc-title-text": "var(--color-foreground-muted)",
        "color-toc-item-text": "var(--color-foreground-secondary)",
        "color-toc-item-text--hover": "var(--color-foreground-primary)",
        "color-toc-item-text--active": "var(--color-brand-primary)",
        "color-content-foreground": "var(--color-foreground-primary)",
        "color-content-background": "transparent",
        "color-link": "var(--color-brand-content)",
        "color-link-underline": "var(--color-background-border)",
        "color-link--hover": "var(--color-brand-content)",
        "color-link-underline--hover": "var(--color-foreground-border)",
        "color-link--visited": "var(--color-brand-visited)",
        "color-link-underline--visited": "var(--color-background-border)",
        "color-link--visited--hover": "var(--color-brand-visited)",
        "color-link-underline--visited--hover": "var(--color-foreground-border)",
    },
    "dark_css_variables": {
        "color-problematic": "#fb4934",
        "color-foreground-primary": "#ebdbb2",
        "color-foreground-secondary": "#bdae93",
        "color-foreground-muted": "#a89984",
        "color-foreground-border": "#7c6f64",
        "color-background-primary": "#282828",
        "color-background-secondary": "#3c3836",
        "color-background-hover": "#504945",
        "color-background-hover--transparent": "#50494500",
        "color-background-border": "#665c54",
        "color-background-item": "#7c6f64",
        "color-announcement-background": "#3c3836dd",
        "color-announcement-text": "#ebdbb2",
        "color-brand-primary": "#83a598",
        "color-brand-content": "#8ec07c",
        "color-brand-visited": "#b16286",
        "color-highlighted-background": "#504945",
        "color-guilabel-background": "#fabd2f40",
        "color-guilabel-border": "#d7992140",
        "color-api-keyword": "var(--color-foreground-secondary)",
        "color-highlight-on-target": "#665c54",
        "color-api-added": "#b8bb26",
        "color-api-added-border": "#98971a",
        "color-api-changed": "#d79921",
        "color-api-changed-border": "#fabd2f",
        "color-api-deprecated": "#b16286",
        "color-api-deprecated-border": "#d3869b",
        "color-api-removed": "#fb4934",
        "color-api-removed-border": "#cc241d",
        "color-admonition-background": "#3c3836",
        "color-card-border": "var(--color-background-secondary)",
        "color-card-background": "#3c3836",
        "color-card-marginals-background": "var(--color-background-hover)",
    },
}
html_static_path = ["_static"]
