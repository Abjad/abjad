master_doc = "index"

extensions = ["uqbar.sphinx.book", "abjad.ext.sphinx"]

html_static_path = ["_static"]

uqbar_book_console_setup = ["import abjad", "from abjad import *"]
uqbar_book_extensions = ["abjad.ext.sphinx.LilyPondExtension"]
