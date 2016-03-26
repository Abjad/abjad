# -*- coding: utf-8 -*-
from sphinx.util.compat import Directive


class DoctestDirective(Directive):
    r'''An abjad-book doctest directive.

    Contributes no formatting to documents built by Sphinx.
    '''

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Sphinx Internals'

    has_content = True
    required_arguments = 0
    optional_arguments = 0
    final_argument_whitespace = True
    option_spec = {}

    ### PUBLIC METHODS ###

    def run(self):
        r'''Executes the directive.
        '''
        self.assert_has_content()
        return []
