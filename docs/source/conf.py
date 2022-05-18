# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# http://www.sphinx-doc.org/en/master/config

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
copyright = "2019 and later (latest update: 2021), Jens Koch, Peter Groszkowski"
author = "Jens Koch, Peter Groszkowski"

# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    "sphinx_rtd_theme",
    "sphinx.ext.napoleon",
    "sphinx.ext.autodoc",
    "sphinx.ext.todo",
    "sphinx.ext.doctest",
    "sphinx.ext.autosummary",
    "sphinx.ext.extlinks",
    "sphinx.ext.viewcode",
    "sphinx.ext.ifconfig",
    "nbsphinx",
    "sphinx.ext.mathjax",
    "sphinx_autodoc_typehints",
]

html_show_sourcelink = False

autodoc_mock_imports = ["qutip", "pytest", "ipywidgets", "IPython", "tqdm"]
autodoc_typehints = "description"
autosummary_generate = True

# Options for sphinx_autodoc_typehints
set_type_checking_flag = True
simplify_optional_unions = True

# The master toctree document.
master_doc = "index"


# Add any paths that contain templates here, relative to this directory.
templates_path = ["_templates"]

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = ["_build", "_templates", "tmp", "**.ipynb_checkpoints"]


# -- Options for HTML output -------------------------------------------------

# These folders are copied to the documentation's HTML output
html_static_path = ["_static"]

# These paths are either relative to html_static_path
# or fully qualified paths (eg. https://...)
html_context = {
    "css_files": [
        "_static/theme_overrides.css",  # override wide tables in RTD theme
    ],
}


# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.

html_theme = "sphinx_rtd_theme"
html_logo = "./logo/scqubits-logo2.png"
full_logo = True

html_theme_options = {"logo_only": True}
# Add any paths that contain custom themes here, relative to this directory.

# The name for this set of Sphinx documents.  If None, it defaults to
# "<project> v<release> documentation".
html_title = "scqubits Documentation"

# A shorter title for the navigation bar.  Default is the same as html_title.
html_short_title = "scqubits"

# The name of the Pygments (syntax highlighting) style to use.
pygments_style = "sphinx"

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

# Do not print input/output cell numbers
nbsphinx_prompt_width = "0ex"
# TODO:  remove the following
nbsphinx_ignore_errors = True