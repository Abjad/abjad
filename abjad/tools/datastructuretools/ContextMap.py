# -*- encoding: utf-8 -*-
from abjad.tools.abctools import AbjadObject
from abjad.tools.topleveltools import iterate


class ContextMap(AbjadObject):
    r'''A context map.

    ::

        >>> template = templatetools.StringOrchestraScoreTemplate()
        >>> score = template()
        >>> context_map = datastructuretools.ContextMap(score)

    ::

        >>> context_map['String Orchestra Score']['color'] = 'red'
        >>> context_map['Violin Staff Group']['color'] = 'blue'
        >>> context_map['Contrabass Staff Group']['color'] = 'green'
        >>> context_map['Contrabass 1 Voice']['color'] = 'yellow'

    ::

        >>> context_map['Violin 1 Voice']['color']
        'blue'

    ::

        >>> context_map['Viola 3 Voice']['color']
        'red'

    ::

        >>> context_map['Contrabass 1 Voice']['color']
        'yellow'

    ::

        >>> context_map['Contrabass 2 Voice']['color']
        'green'

    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        '_components',
        '_score',
        )

    ### INITIALIZER ###

    def __init__(self, score=None):
        from abjad.tools import datastructuretools
        from abjad.tools import scoretools
        from abjad.tools import templatetools
        if score is None:
            template = templatetools.StringOrchestraScoreTemplate()
            score = template()
        assert isinstance(score, scoretools.Score), repr(score)
        self._score = score
        self._components = {}
        if self._score is None:
            return
        for context in iterate(self._score).by_class(scoretools.Context):
            assert context.name is not None, context.name
            component = datastructuretools.ContextMapComponent(
                self,
                context.name,
                )
            self._components[context.name] = component

    ### SPECIAL METHODS ###

    def __getitem__(self, context_name):
        r'''Gets context map component for `context_name`.

        Returns context map component.
        '''
        from abjad.tools import scoretools
        if isinstance(context_name, scoretools.Context):
            context_name = context_name.name
        return self._components[context_name]
