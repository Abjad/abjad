# -*- encoding: utf-8 -*-

from abjad.tools.abctools import AbjadObject
from abjad.tools.topleveltools import iterate


class ContextHierarchy(AbjadObject):
    r'''A context hierarchy.

    ::

        >>> template = templatetools.StringOrchestraScoreTemplate()
        >>> score = template()
        >>> context_hierarchy = datastructuretools.ContextHierarchy(score)

    ::

        >>> context_hierarchy['String Orchestra Score']['color'] = 'red'
        >>> context_hierarchy['Violin Staff Group']['color'] = 'blue'
        >>> context_hierarchy['Contrabass Staff Group']['color'] = 'green'
        >>> context_hierarchy['Contrabass 1 Voice']['color'] = 'yellow'

    ::

        >>> context_hierarchy['Violin 1 Voice']['color']
        'blue'

    ::

        >>> context_hierarchy['Viola 3 Voice']['color']
        'red'

    ::

        >>> context_hierarchy['Contrabass 1 Voice']['color']
        'yellow'

    ::

        >>> context_hierarchy['Contrabass 2 Voice']['color']
        'green'

    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        '_components',
        '_score',
        )

    ### INITIALIZER ###

    def __init__(self, score):
        from abjad.tools import datastructuretools
        from abjad.tools import scoretools
        assert isinstance(score, scoretools.Score), repr(score)
        self._score = score
        self._components = {}
        if self._score is None:
            return
        for context in iterate(self._score).by_class(scoretools.Context):
            assert context.name is not None, context.name
            component = datastructuretools.ContextHierarchyComponent(
                self,
                context.name,
                )
            self._components[context.name] = component

    ### SPECIAL METHODS ###

    def __getitem__(self, context_name):
        r'''Gets context hierarchy component for `context_name`.

        Returns context hierarchy component.
        '''
        from abjad.tools import scoretools
        if isinstance(context_name, scoretools.Context):
            context_name = context_name.name
        return self._components[context_name]
