# -*- coding: utf-8 -*-
from sphinx.util.compat import Directive
from sphinx.util.nodes import set_source_info


class RevealDirective(Directive):
    r'''An abjad-book reveal directive.

    Generates an ``abjad_reveal_block`` node.
    '''

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Sphinx Internals'

    has_content = False
    required_arguments = 1
    optional_arguments = 0
    final_argument_whitespace = True
    option_spec = {}

    ### PUBLIC METHODS ###

    def run(self):
        r'''Executes the directive.
        '''
        from abjad.tools import abjadbooktools
        block = abjadbooktools.abjad_reveal_block()
        block['reveal-label'] = self.arguments[0]
        set_source_info(self, block)
        return [block]
