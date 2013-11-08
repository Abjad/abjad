# -*- encoding: utf-8 -*-
import types
from abjad.tools.documentationtools.ReSTDirective import ReSTDirective


class ReSTLineageDirective(ReSTDirective):
    r'''An ReST Abjad lineage diagram directive:

    ::

        >>> documentationtools.ReSTLineageDirective(argument=spannertools.Beam)
        ReSTLineageDirective(
            argument='abjad.tools.spannertools.Beam.Beam'
            )

    ::

        >>> print _.rest_format
        .. abjad-lineage:: abjad.tools.spannertools.Beam.Beam

    Return `ReSTLineageDirective` instance.
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
        return 'abjad-lineage'
