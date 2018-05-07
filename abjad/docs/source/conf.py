import sphinx_rtd_theme
import sys
from abjad import abjad_configuration
from pygments.formatters.latex import LatexFormatter
from sphinx.highlighting import PygmentsBridge

class CustomLatexFormatter(LatexFormatter):
    def __init__(self, **options):
        super(CustomLatexFormatter, self).__init__(**options)
        self.verboptions = r'''formatcom=\footnotesize'''

PygmentsBridge.latex_formatter = CustomLatexFormatter

### CORE ###

add_function_parentheses = True
copyright = u'2008-2018, Trevor Bača & Josiah Wolf Oberholtzer'
exclude_patterns = []

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.autosummary',
    'sphinx.ext.coverage',
    'sphinx.ext.graphviz',
    'sphinx.ext.intersphinx',
    'sphinx.ext.todo',
    'sphinx_autodoc_typehints',
    'uqbar.sphinx.api',
    'uqbar.sphinx.inheritance',
    'uqbar.sphinx.style',
    'abjadext.book.sphinx',
    ]

master_doc = 'index'
project = u'Abjad'
pygments_style = 'sphinx'
release = abjad_configuration.get_abjad_version_string()
source_suffix = '.rst'
templates_path = ['_templates']
version = abjad_configuration.get_abjad_version_string()

### HTML ###

html_domain_indices = False
html_favicon = '_static/favicon.ico'
html_last_updated_fmt = '%b %d, %Y'
html_logo = '_static/abjad-logo.png'
html_show_sourcelink = True
html_static_path = ['_static']
html_theme = "sphinx_rtd_theme"
html_theme_path = [sphinx_rtd_theme.get_html_theme_path()]
html_use_index = False

### HTML HELP ###

htmlhelp_basename = 'Abjaddoc'

### LATEX ###

latex_elements = {
    'inputenc': r'\usepackage[utf8x]{inputenc}',
    'utf8extra': '',
    'papersize': 'letterpaper',
    'pointsize': '10pt',
    'preamble': r'''
    \usepackage{upquote}
    \pdfminorversion=5
    \setcounter{tocdepth}{2}
    \definecolor{VerbatimColor}{rgb}{0.95,0.95,0.95}
    \definecolor{VerbatimBorderColor}{rgb}{1.0,1.0,1.0}
    \hypersetup{unicode=true}
    ''',
    }

latex_documents = [
    (
        'index',
        'Abjad.tex',
        u'Abjad Documentation',
        u'Trevor Bača & Josiah Wolf Oberholtzer',
        'manual',
        ),
    (
        'api/index',
        'AbjadAPI.tex',
        u'Abjad API',
        u'Trevor Bača & Josiah Wolf Oberholtzer',
        'manual',
        ),
    ]

#latex_use_parts = True
latex_toplevel_sectioning = 'chapter' # just guessing?

### MAN ###

man_pages = [
    (
        'index',
        'abjad',
        u'Abjad Documentation',
        [u'2008-2018, Trevor Bača & Josiah Wolf Oberholtzer'],
        1,
        )
    ]

### TEXINFO ###

texinfo_documents = [
    (
        'index',
        'Abjad',
        u'Abjad Documentation',
        u'2008-2018, Trevor Bača & Josiah Wolf Oberholtzer',
        'Abjad',
        'One line description of project.',
        'Miscellaneous',
        ),
    ]

### EXTENSIONS ###

abjadbook_ignored_documents = ()
autodoc_member_order = 'groupwise'
graphviz_dot_args = ['-s32']
graphviz_output_format = 'svg'
intersphinx_mapping = {
    'https://docs.python.org/3.6/': None,
    'http://www.sphinx-doc.org/en/stable/': None,
    }
todo_include_todos = True

uqbar_api_title = 'Abjad API'
uqbar_api_source_paths = ['abjad']
uqbar_api_root_documenter_class = 'uqbar.apis.SummarizingRootDocumenter'
uqbar_api_module_documenter_class = 'uqbar.apis.SummarizingModuleDocumenter'
uqbar_api_member_documenter_classes = [
    'uqbar.apis.FunctionDocumenter',
    'uqbar.apis.SummarizingClassDocumenter',
    ]
