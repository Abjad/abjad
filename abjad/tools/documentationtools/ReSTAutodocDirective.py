# -*- coding: utf-8 -*-
import types
from abjad.tools.documentationtools.ReSTDirective import ReSTDirective


class ReSTAutodocDirective(ReSTDirective):
    r'''A ReST autodoc directive.

    ::

        >>> autodoc = documentationtools.ReSTAutodocDirective(
        ...     argument='abjad.tools.spannertools.Beam.Beam',
        ...     directive='autoclass',
        ...     )
        >>> autodoc.options['noindex'] = True
        >>> autodoc
        ReSTAutodocDirective(
            argument='abjad.tools.spannertools.Beam.Beam',
            directive='autoclass',
            options={
                'noindex': True,
                }
            )

    ::

        >>> print(autodoc.rest_format)
        .. autoclass:: abjad.tools.spannertools.Beam.Beam
           :noindex:

    '''

    ### CLASS VARIABLES ###

    __documentation_section__ = 'reStructuredText'

    ### INITIALIZER ###

    def __init__(
        self,
        argument=None,
        children=None,
        directive='automodule',
        name=None,
        options=None,
        ):
        ReSTDirective.__init__(
            self,
            argument=argument,
            children=children,
            name=name,
            options=options,
            )
        self.directive = directive

    ### PUBLIC PROPERTIES ###

    @property
    def directive(self):
        r'''Gets and set directive of ReST autodoc directive.
        '''
        return self._directive

    @directive.setter
    def directive(self, arg):
        assert arg in (
            'autoattribute',
            'autoclass',
            'autodata',
            'autoexception',
            'autofunction',
            'automethod',
            'automodule',
        )
        self._directive = arg
