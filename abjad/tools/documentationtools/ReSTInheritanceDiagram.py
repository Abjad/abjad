# -*- coding: utf-8 -*-
from abjad.tools.documentationtools.ReSTDirective import ReSTDirective


class ReSTInheritanceDiagram(ReSTDirective):
    r'''A ReST inheritance diagram directive.

    ::

        >>> documentationtools.ReSTInheritanceDiagram(
        ...     argument=spannertools.Beam)
        ReSTInheritanceDiagram(
            argument='abjad.tools.spannertools.Beam.Beam',
            options={
                'private-bases': True,
                }
            )

    ::

        >>> print(_.rest_format)
        .. inheritance-diagram:: abjad.tools.spannertools.Beam.Beam
           :private-bases:

    '''

    ### CLASS VARIABLES ###

    __documentation_section__ = 'reStructuredText'

    ### INITIALIZER ###

    def __init__(self, argument=None, children=None, name=None, options=None):
        if isinstance(argument, type):
            argument = argument.__module__ + '.' + argument.__name__
        new_options = {'private-bases': True}
        if options is not None:
            new_options.update(options)
        ReSTDirective.__init__(
            self,
            argument=argument,
            children=children,
            name=name,
            options=new_options,
            )

    ### PUBLIC PROPERTIES ###

    @property
    def directive(self):
        r'''Directive of ReSt inheritance diagram.

        Returns ``'inheritance-diagram'``.
        '''
        return 'inheritance-diagram'
