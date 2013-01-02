import types
from abjad.tools.documentationtools.ReSTDirective import ReSTDirective


class ReSTInheritanceDiagram(ReSTDirective):
    '''An ReST inheritance diagram directive:

    ::

        >>> documentationtools.ReSTInheritanceDiagram(argument=beamtools.BeamSpanner)
        ReSTInheritanceDiagram(
            argument='abjad.tools.beamtools.BeamSpanner.BeamSpanner.BeamSpanner',
            options={
                'private-bases': True
                }
            )

    ::

        >>> print _.rest_format
        .. inheritance-diagram:: abjad.tools.beamtools.BeamSpanner.BeamSpanner.BeamSpanner
           :private-bases:

    Return `ReSTInheritanceDiagram` instance.
    '''

    ### INITIALIZER ###

    def __init__(self, argument=None, children=None, name=None, options=None):
        if isinstance(argument, types.TypeType):
            argument = argument.__module__ + '.' + argument.__name__
        new_options = {'private-bases': True}
        if options is not None:
            new_options.update(options)
        ReSTDirective.__init__(self, argument=argument, children=children, name=name, options=new_options)

    ### READ-ONLY PUBLIC PROPERTIES ###

    @property
    def directive(self):
        return 'inheritance-diagram'
