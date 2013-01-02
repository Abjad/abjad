import types
from abjad.tools.documentationtools.ReSTDirective import ReSTDirective


class ReSTAutodocDirective(ReSTDirective):
    '''An ReST autodoc directive:

    ::

        >>> autodoc = documentationtools.ReSTAutodocDirective(
        ...     argument=beamtools.BeamSpanner,
        ...     directive='autoclass',
        ...     )
        >>> autodoc.options['noindex'] = True
        >>> autodoc
        ReSTAutodocDirective(
            argument='abjad.tools.beamtools.BeamSpanner.BeamSpanner.BeamSpanner',
            directive='autoclass',
            options={
                'noindex': True
                }
            )

    ::

        >>> print autodoc.rest_format
        .. autoclass:: abjad.tools.beamtools.BeamSpanner.BeamSpanner.BeamSpanner
           :noindex:

    Return `ReSTAutodocDirective` instance.
    '''

    ### INITIALIZER ###

    def __init__(self, argument=None, children=None, directive=None, name=None, options=None):
        if isinstance(argument, types.InstanceType):
            argument = argument.__class__
        if isinstance(argument, types.TypeType):
            argument=argument.__module__ + '.' + argument.__name__
        ReSTDirective.__init__(self, argument=argument, children=children, name=name, options=options)
        self.directive = directive

    ### READ/WRITE PUBLIC PROPERTIES ###

    @apply
    def directive():
        def fget(self):
            return self._directive
        def fset(self, arg):
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
        return property(**locals())
