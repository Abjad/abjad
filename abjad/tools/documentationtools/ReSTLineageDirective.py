# -*- encoding: utf-8 -*-
import types
from abjad.tools.documentationtools.ReSTDirective import ReSTDirective


class ReSTLineageDirective(ReSTDirective):
    r'''A ReST lineage directive.

    Digrams inheritance of Abjad classes.

    ::

        >>> documentationtools.ReSTLineageDirective(argument=spannertools.Beam)
        ReSTLineageDirective(
            argument='abjad.tools.spannertools.Beam.Beam'
            )

    ::

        >>> print _.rest_format
        .. abjad-lineage:: abjad.tools.spannertools.Beam.Beam

    '''

    ### INITIALIZER ###

    def __init__(self, argument=None, children=None, name=None, options=None):
        if isinstance(argument, types.TypeType):
            argument = argument.__module__ + '.' + argument.__name__
        ReSTDirective.__init__(
            self, 
            argument=argument, 
            children=children, 
            name=name, 
            options=options,
            )

    ### PUBLIC PROPERTIES ###

    @property
    def directive(self):
        r'''Returns ``'abjad-lineage'``.
        '''
        return 'abjad-lineage'
