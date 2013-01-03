import types
from abjad.tools.documentationtools.ReSTDirective import ReSTDirective


class ReSTLineageDirective(ReSTDirective):
    '''An ReST Abjad lineage diagram directive:

    ::

        >>> documentationtools.ReSTLineageDirective(argument=beamtools.BeamSpanner)
        ReSTLineageDirective(
            argument='abjad.tools.beamtools.BeamSpanner.BeamSpanner.BeamSpanner'
            )

    ::

        >>> print _.rest_format
        .. abjad-lineage:: abjad.tools.beamtools.BeamSpanner.BeamSpanner.BeamSpanner

    Return `ReSTLineageDirective` instance.
    '''

    ### INITIALIZER ###

    def __init__(self, argument=None, children=None, name=None, options=None):
        if isinstance(argument, types.TypeType):
            argument = argument.__module__ + '.' + argument.__name__
        ReSTDirective.__init__(self, argument=argument, children=children, name=name, options=options)

    ### READ-ONLY PUBLIC PROPERTIES ###

    @property
    def directive(self):
        return 'abjad-lineage'
