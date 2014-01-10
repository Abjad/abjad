# -*- encoding: utf-8 -*-

import collections
from abjad.tools.abctools.AbjadObject import AbjadObject


class ContextHierarchyComponent(AbjadObject):
    r'''A component in a context hierarchy.
    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        '_context_hierarchy',
        '_context_name',
        '_context_settings',
        )

    ### INITIALIZER ###

    def __init__(self, context_hierarchy, context_name):
        from abjad.tools import datastructuretools
        assert isinstance(context_hierarchy,
            datastructuretools.ContextHierarchy)
        assert isinstance(context_name, str) and context_name
        self._context_hierarchy = context_hierarchy
        self._context_name = context_name
        self._context_settings = {}

    ### PRIVATE METHODS ###

    def _as_chain_map(self):
        from abjad.tools.agenttools.InspectionAgent import inspect
        dictionaries = []
        components = self._context_hierarchy._components
        score = self._context_hierarchy._score
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
        r'''Is true if context hierarchy component contains `key`. Otherwise
        false.

        Returns boolean.
        '''
        return self._as_chain_map().__contains__(key)

    def __iter__(self):
        r'''Iterates over keys in context hierarchy component.

        Returns generator.
        '''
        return self._as_chain_map().__iter__()

    def __len__(self):
        r'''Gets number of keys reachable from context hierarchy component.

        Returns int.
        '''
        return len(self._as_chain_map())

    def __getitem__(self, key):
        r'''Gets `key` for context hierarchy component.

        Returns value of `key`.
        '''
        return self._as_chain_map().__getitem__(key)

    def __setitem__(self, key, value):
        r'''Sets `key` to `value` in context hierarchy component.

        Returns none.
        '''
        self._context_settings[key] = value
