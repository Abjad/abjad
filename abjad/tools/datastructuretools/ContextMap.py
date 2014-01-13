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

    class ContextMapComponent(AbjadObject):
        r'''A component in a context map.
        '''

        ### CLASS VARIABLES ###

        __slots__ = (
            '_client',
            '_context_name',
            '_context_settings',
            )

        ### INITIALIZER ###

        def __init__(self, context_map, context_name):
            from abjad.tools import datastructuretools
            assert isinstance(context_map, datastructuretools.ContextMap)
            assert isinstance(context_name, str) and context_name
            self._client = context_map
            self._context_name = context_name
            self._context_settings = {}

        ### PRIVATE METHODS ###

        def _as_chain_map(self):
            from abjad.tools.agenttools.InspectionAgent import inspect
            dictionaries = []
            components = self._client._components
            score = self._client._score
            if self._context_name == score.name:
                context = score
            else:
                context = score[self._context_name]
            parentage = inspect(context).get_parentage()
            for context in parentage:
                context_name = context.name
                context_settings = components[context_name]._context_settings
                dictionaries.append(context_settings)
            dictionaries.reverse()
            chain_map = dictionaries[0].copy()
            for dictionary in dictionaries[1:]:
                chain_map.update(dictionary)
            return chain_map

        ### PRIVATE PROPERTIES ###

        @property
        def _storage_format_specification(self):
            from abjad.tools import systemtools
            return systemtools.StorageFormatSpecification(
                self,
                positional_argument_values=(
                    self._context_name,
                    )
                )

        ### SPECIAL METHODS ###

        def __contains__(self, key):
            r'''Is true if context map component contains `key`. Otherwise
            false.

            Returns boolean.
            '''
            return self._as_chain_map().__contains__(key)

        def __iter__(self):
            r'''Iterates over keys in context map component.

            Returns generator.
            '''
            return self._as_chain_map().__iter__()

        def __len__(self):
            r'''Gets number of keys reachable from context map component.

            Returns int.
            '''
            return len(self._as_chain_map())

        def __getitem__(self, key):
            r'''Gets `key` for context map component.

            Returns value of `key`.
            '''
            return self._as_chain_map().__getitem__(key)

        def __setitem__(self, key, value):
            r'''Sets `key` to `value` in context map component.

            Returns none.
            '''
            self._context_settings[key] = value

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
            component = self.ContextMapComponent(
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

    ### PUBLIC PROPERTIES ###

    @property
    def score(self):
        r'''Score on which context map is based.
        
        ..  container:: example

            ::

                >>> context_map.score
                Score-"String Orchestra Score"<<4>>

        Returns score or none.
        '''
        return self._score
