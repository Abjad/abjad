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

        >>> context_hierarchy.set(
        ...     'String Orchestra Score', 'color', 'red')
        >>> context_hierarchy.set(
        ...     'Violin Staff Group', 'color', 'blue')
        >>> context_hierarchy.set(
        ...     'Contrabass Staff Group', 'color', 'green')
        >>> context_hierarchy.set(
        ...     'Contrabass 1 Voice', 'color', 'yellow')

    ::

        >>> context_hierarchy.get('Violin 1 Voice', 'color')
        'blue'

    ::

        >>> context_hierarchy.get('Viola 3 Voice', 'color')
        'red'

    ::

        >>> context_hierarchy.get('Contrabass 1 Voice', 'color')
        'yellow'

    ::

        >>> context_hierarchy.get('Contrabass 2 Voice', 'color')
        'green'

    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        '_context_names',
        '_context_settings',
        '_score',
        )

    ### INITIALIZER ###

    def __init__(self, score):
        from abjad.tools import scoretools
        assert isinstance(score, scoretools.Score), repr(score)
        self._score = score
        context_names = []
        if self._score is not None:
            for context in \
                iterate(self._score).by_class(scoretools.Context):
                assert context.context_name is not None, context.name_name
                context_names.append(context.name)
        self._context_names = tuple(sorted(context_names))
        context_settings = {}
        for context_name in self._context_names:
            context_settings[context_name] = {}
        self._context_settings = context_settings

    ### PUBLIC METHODS ###

    def get(self, context_name, key):
        r'''Gets `key` for `context_name`.

        Returns `value` or none.
        '''
        from abjad.tools.agenttools.InspectionAgent import inspect
        assert context_name in self._context_names, context_name
        parentage = inspect(self._score[context_name]).get_parentage()
        for context in parentage:
            context_name = context.name
            context_settings = self._context_settings[context_name]
            if key in context_settings:
                return context_settings[key]
        return None

    def set(self, context_name, key, value):
        r'''Sets `key` to `value` for `context_name`.

        Returns none.
        '''
        assert context_name in self._context_names, context_name
        context_settings = self._context_settings[context_name]
        context_settings[key] = value

