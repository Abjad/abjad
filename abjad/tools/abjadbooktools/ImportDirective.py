# -*- encoding: utf-8 -*-
from docutils.parsers.rst import directives
from sphinx.util.compat import Directive
from sphinx.util.nodes import set_source_info


class ImportDirective(Directive):
    r'''An abjad-book import directive.

    Represents a class or function to be imported into an interactive session.

    Generates a `abjad_import_block node`.
    '''

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Sphinx Internals'

    has_content = False
    required_arguments = 1
    optional_arguments = 0
    final_argument_whitespace = True
    option_spec = {
        'hide': directives.flag,
        }

    ### PUBLIC METHODS ###

    def run(self):
        r'''Executes the directive.
        '''
        from abjad.tools import abjadbooktools
        path = self.arguments[0]
        block = abjadbooktools.abjad_import_block()
        block['path'] = path
        block['hide'] = 'hide' in self.options
        set_source_info(self, block)
        return [block]