# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#
import os
import sys

sys.path.insert(0, os.path.abspath("../../../scqubits"))
sys.path.append(os.path.abspath("sphinxext"))

import scqubits

# -- Project information -----------------------------------------------------

project = "scqubits"
copyright = "2019 and later (latest update: 2026), Jens Koch, Peter Groszkowski"
author = "Jens Koch, Peter Groszkowski"

import pydata_sphinx_theme

html_theme = "pydata_sphinx_theme"

# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    "sphinx_design",
    "sphinx.ext.napoleon",
    "sphinx.ext.autodoc",
    "sphinx.ext.todo",
    "sphinx.ext.doctest",
    "sphinx.ext.autosummary",
    "sphinx.ext.extlinks",
    "sphinx.ext.viewcode",
    "sphinx.ext.ifconfig",
    "sphinx.ext.intersphinx",
    "nbsphinx",
    "sphinx.ext.mathjax",
    "sphinx_autodoc_typehints",
    "sphinx.ext.autosectionlabel",
    "IPython.sphinxext.ipython_console_highlighting",
    "IPython.sphinxext.ipython_directive",
    "sphinx_copybutton"
]

intersphinx_mapping = {
    "python": ("https://docs.python.org/3", None),
    "numpy": ("https://numpy.org/doc/stable", None),
    "scipy": ("https://docs.scipy.org/doc/scipy", None),
    "matplotlib": ("https://matplotlib.org/stable", None),
    "qutip": ("https://qutip.readthedocs.io/en/qutip-5.0.x", None),
    "sympy": ("https://docs.sympy.org/latest", None),
    "traitlets": ("https://traitlets.readthedocs.io/en/stable", None),
}

# Suppress nitpicky warnings for short-form references that recur in
# upstream scqubits docstrings (bare class names instead of fully
# qualified). Listed here so the nitpicky build is actionable; remove
# entries once the corresponding docstrings get fully qualified upstream.
nitpick_ignore_regex = [
    # nitpick_ignore_regex uses re.fullmatch, so each pattern must match
    # the entire target string. Suppresses noise from upstream scqubits
    # docstrings that use bare class names instead of fully qualified ones.
    ("py:class", r"(HilbertSpace|SpectrumData|ParameterSweep|QuantumSystem|QuantumSys)"),
    ("py:class", r"(NamedSlotsNdarray|Parameters|GIndexTuple|GIndex|Serializable|IOData|DataStore)"),
    ("py:class", r"(Transmon|TunableTransmon|Fluxonium|FluxQubit|ZeroPi|FullZeroPi|Cos2PhiQubit)"),
    ("py:class", r"(Oscillator|KerrOscillator|GenericQubit)"),
    ("py:class", r"(Circuit|SymbolicCircuit|Branch|Node|Coupler|Subsystem)"),
    ("py:class", r"(Figure|Axes)"),
    ("py:class", r"(optional|callable|iterable|sequence|All|default:.*)"),
    ("py:attr", r"(flux|truncated_dim|ng|ncut|EJ|EC|EL|EJmax|cutoff|grid|n_g)"),
    ("py:meth", r"(supported_noise_channels|effective_noise_channels)"),
    ("py:obj", r"scqubits\..*"),
    ("py:data", r"scqubits\..*"),
    ("py:data", r"(CENTRAL_DISPATCH|EVENTS|DIAG_METHODS|MODE_FUNC_DICT)"),
    ("py:data", r"constants\..*"),
    ("py:data", r"typing\.Union.*"),
]


# -- Internationalization ------------------------------------------------
# specifying the natural language populates some key tags
language = "en"

html_show_sourcelink = False
html_sourcelink_suffix = ""

autodoc_mock_imports = ["qutip", "pytest", "tqdm"]
autodoc_typehints = "description"
autodoc_type_aliases = {
    "QuantumSys": "scqubits.utils.typedefs.QuantumSys",
}
autodoc_default_options = {
    "exclude-members": "_ctypes, _ctypes.data, _ctypes.shape, _ctypes.strides, _ctypes.data_as, _ctypes.shape_as, _ctypes.strides_as"
}
autosectionlabel_prefix_document = True
autosummary_generate = True

# Options for sphinx_autodoc_typehints
set_type_checking_flag = True
simplify_optional_unions = False

# The master toctree document.
master_doc = "contents"


# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
# Add any paths that contain templates here, relative to this directory.
templates_path = ["_templates"]

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = [
    "_build",
    "_templates",
    "tmp",
    "**.ipynb_checkpoints",
    "Thumbs.db",
    ".DS_Store",
]


# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ["_static"]
html_css_files = ["theme_overrides.css", "pygments.css"]

html_logo = "./_static/scqubits-logo.svg"
html_favicon = "./_static/scqubits-logo-icon.png"

# Add any paths that contain custom themes here, relative to this directory.

# The name for this set of Sphinx documents.  If None, it defaults to
# "<project> v<release> documentation".
html_title = "scqubits documentation"

# A shorter title for the navigation bar.  Default is the same as html_title.
html_short_title = "scqubits"

html_context = {
    "github_user": "scqubits",
    "github_repo": "scqubits-doc",
    "github_version": "rtd",
    "doc_path": "docs/source",
    "default_mode": "light",
}

html_theme_options = {
    "logo": {
        "alt_text": "scqubits logo",
        "image_light": "scqubits-logo.svg",
        "image_dark": "scqubits-logo.svg",
        "link": "../index"
    },
    "github_url": "https://github.com/scqubits/scqubits",
    "twitter_url": "https://twitter.com/scqubits",
    "icon_links": [
        {
            "name": "YouTube",
            "url": "https://www.youtube.com/channel/UCI43mhRw6oY01FbPuOc5CVQ",
            "icon": "fa fa-youtube",
        },
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
    "navbar_start": ["navbar-logo"],
    "navbar_end": ["navbar-icon-links"],
    "navigation_depth": 5,
    "show_nav_level": 3,
    "collapse_navigation": True,
}

html_sidebars = {
    "contribute/index": [
        "search-field",
        "sidebar-nav-bs",
        "custom-template",
    ],  # This ensures we test for custom sidebars
    "demo/no-sidebar": [],
}

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
