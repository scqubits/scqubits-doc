# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#
import os
import sys

sys.path.insert(0, os.path.abspath("../../../scqubits"))
sys.path.append(os.path.abspath("sphinxext"))

# -- Project information -----------------------------------------------------

project = "scqubits"
copyright = "2019 and later (latest update: 2022), Jens Koch, Peter Groszkowski"
author = "Jens Koch, Peter Groszkowski"

import pydata_sphinx_theme
html_theme = "pydata_sphinx_theme"

# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    "sphinx.ext.napoleon",
    "sphinx.ext.autodoc",
    "sphinx.ext.autosummary",
    "sphinx.ext.todo",
    "sphinx.ext.doctest",
    "sphinx.ext.extlinks",
    "sphinx.ext.viewcode",
    "sphinx_design",
    "nbsphinx",
    "sphinx.ext.mathjax",
    "sphinx_autodoc_typehints",
    "IPython.sphinxext.ipython_console_highlighting",
    "IPython.sphinxext.ipython_directive",
]


# -- Internationalization ------------------------------------------------
# specifying the natural language populates some key tags
language = "en"

html_show_sourcelink = False
html_sourcelink_suffix = ""


# Options for sphinx_autodoc_typehints
set_type_checking_flag = True
simplify_optional_unions = True

# The master toctree document.
master_doc = "index"


autodoc_mock_imports = ["qutip", "pytest", "ipywidgets", "IPython", "tqdm"]
autodoc_typehints = "description"
autosummary_generate = True

# Options for sphinx_autodoc_typehints
set_type_checking_flag = True
simplify_optional_unions = True

# The master toctree document.
master_doc = "index"

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
# Add any paths that contain templates here, relative to this directory.
templates_path = ["_templates"]

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = ["_build", "_templates", "tmp", "**.ipynb_checkpoints", "Thumbs.db", ".DS_Store"]

autosummary_generate = True

html_logo = "./logo/scqubits-logo3.png"
html_favicon = "./logo/scqubits-logo3.png"

# Add any paths that contain custom themes here, relative to this directory.

# The name for this set of Sphinx documents.  If None, it defaults to
# "<project> v<release> documentation".
html_title = "scqubits Documentation"

# A shorter title for the navigation bar.  Default is the same as html_title.
html_short_title = "scqubits"

html_context = {
    "github_user": "scqubits",
    "github_repo": "scqubits-doc",
    "github_version": "rtd",
    "doc_path": "docs/source",
}

html_theme_options = {
    "github_url": "https://github.com/scqubits/scubits",
    "twitter_url": "https://twitter.com/scqubits",
    "icon_links": [
        {
            "name": "PyPI",
            "url": "https://pypi.org/project/scqubits/",
            "icon": "fas fa-box",
        },
        {
            "name": "conda",
            "url": "https://anaconda.org/conda-forge/scqubits",
            "icon": "fas fa-box-open",
        },
    ],
    "use_edit_page_button": True,
    "show_toc_level": 1,
    "navbar_start": ["navbar-logo"],
    "navbar_end": ["navbar-icon-links"],
}

html_sidebars = {
    "contribute/index": [
        "search-field",
        "sidebar-nav-bs",
        "custom-template",
    ],  # This ensures we test for custom sidebars
    "demo/no-sidebar": [],  # Test what page looks like with no sidebar items
}

myst_heading_anchors = 2



highlight_language = "python"
# The name of the Pygments (syntax highlighting) style to use.
pygments_style = "algol_nu"

# If true, '()' will be appended to :func: etc. cross-reference text.
add_function_parentheses = False

# If true, the current module name will be prepended to all description
# unit titles (such as .. function::).
add_module_names = True

# If true, section author and module author directives will be shown in the
# output. They are ignored by default.
show_authors = True

# A list of ignored prefixes for module index sorting.
todo_include_todos = True

napoleon_numpy_docstring = True
napoleon_use_admonition_for_notes = True

nbsphinx_execute_arguments = [
    "--InlineBackend.figure_formats={'svg', 'pdf'}",
    "--InlineBackend.rc=figure.dpi=96",
]

nbsphinx_prompt_width = "0ex"
nbsphinx_codecell_lexer = "ipython3"
# The following only to be enabled for debugging purposes
# nbsphinx_allow_errors = True

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ["_static"]
html_css_files = ["theme_overrides.css", "pygments.css"]
