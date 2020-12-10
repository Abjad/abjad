import sphinx_rtd_theme

import abjad

### CORE ###

add_function_parentheses = True
copyright = "2008-2020, Trevor Bača & Josiah Wolf Oberholtzer"
exclude_patterns = []

extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.autosummary",
    "sphinx.ext.coverage",
    "sphinx.ext.graphviz",
    "sphinx.ext.intersphinx",
    "sphinx.ext.todo",
    # temporarily commenting-out prevents "highlighting module code ...";
    # uncomment viewcode when building official release of docs:
    # "sphinx.ext.viewcode",
    "abjad.ext.sphinx",
    "sphinx_autodoc_typehints",
    "uqbar.sphinx.api",
    "uqbar.sphinx.book",
    "uqbar.sphinx.inheritance",
    "uqbar.sphinx.style",
]

master_doc = "index"
project = "Abjad"
pygments_style = "sphinx"
release = abjad.__version__
source_suffix = ".rst"
templates_path = ["_templates"]
version = abjad.__version__

### HTML ###

html_favicon = "_static/favicon.ico"
html_last_updated_fmt = "%b %d, %Y"
html_logo = "_static/abjad-logo.png"
html_show_sourcelink = True
html_static_path = ["_static"]
html_theme = "sphinx_rtd_theme"
html_theme_options = {
    "navigation_depth": 2,
    "style_nav_header_background": "#dbc2ff",
}
html_theme_path = [sphinx_rtd_theme.get_html_theme_path()]

### EXTENSIONS ###

autodoc_member_order = "groupwise"
graphviz_dot_args = ["-s32"]
graphviz_output_format = "svg"
intersphinx_mapping = {
    "http://josiahwolfoberholtzer.com/uqbar/": None,
    "http://www.sphinx-doc.org/en/master/": None,
    "https://docs.python.org/3.9/": None,
}
todo_include_todos = True

uqbar_api_title = "Abjad API"
uqbar_api_source_paths = ["abjad"]
uqbar_api_root_documenter_class = "uqbar.apis.SummarizingRootDocumenter"
uqbar_api_module_documenter_class = "uqbar.apis.SummarizingModuleDocumenter"
uqbar_api_member_documenter_classes = [
    "uqbar.apis.FunctionDocumenter",
    "uqbar.apis.SummarizingClassDocumenter",
]

uqbar_book_console_setup = ["import abjad", "from quicktions import Fraction"]
uqbar_book_console_teardown = []
uqbar_book_extensions = [
    "uqbar.book.extensions.GraphExtension",
    "abjad.ext.sphinx.LilyPondExtension",
]
uqbar_book_strict = False
uqbar_book_use_black = True
uqbar_book_use_cache = True

try:
    import abjadext  # noqa

    uqbar_api_source_paths.append("abjadext")
    uqbar_book_console_setup.append("import abjadext")
except ImportError:
    pass

try:
    from abjadext import rmakers  # noqa

    uqbar_book_console_setup.append("from abjadext import rmakers")
except ImportError:
    pass

try:
    from abjadext import microtones  # noqa

    uqbar_book_console_setup.append("from abjadext import microtones")
except ImportError:
    pass
