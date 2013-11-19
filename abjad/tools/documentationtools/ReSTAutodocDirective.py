# -*- encoding: utf-8 -*-
import types
from abjad.tools.documentationtools.ReSTDirective import ReSTDirective


class ReSTAutodocDirective(ReSTDirective):
    r'''An ReST autodoc directive:

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

        >>> print autodoc.rest_format
        .. autoclass:: abjad.tools.spannertools.Beam.Beam
           :noindex:

    Return `ReSTAutodocDirective` instance.
    '''

    ### INITIALIZER ###

    def __init__(self, 
        argument=None, 
        children=None, 
        directive=None, 
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
