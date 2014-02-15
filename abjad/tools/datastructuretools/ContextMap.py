# -*- encoding: utf-8 -*-
import collections
from abjad.tools.abctools import AbjadObject
from abjad.tools.topleveltools import inspect_
from abjad.tools.topleveltools import iterate


class ContextMap(AbjadObject):
    r'''A context map.

    ::

        >>> template = templatetools.StringOrchestraScoreTemplate()
        >>> context_map = datastructuretools.ContextMap(template)

    ::

        >>> context_map['String Orchestra Score']['color'] = 'red'
        >>> context_map['Violin Staff Group']['color'] = 'blue'
        >>> context_map['Contrabass Staff Group']['color'] = 'green'
        >>> context_map['Contrabass 1 Voice']['color'] = 'yellow'

    ::

        >>> print format(context_map)
        datastructuretools.ContextMap(
            score_template=templatetools.StringOrchestraScoreTemplate(
                violin_count=6,
                viola_count=4,
                cello_count=3,
                contrabass_count=2,
                ),
            settings=[
                (
                    'Contrabass 1 Voice',
                    [
                        ('color', 'yellow'),
                        ],
                    ),
                (
                    'Contrabass Staff Group',
                    [
                        ('color', 'green'),
                        ],
                    ),
                (
                    'String Orchestra Score',
                    [
                        ('color', 'red'),
                        ],
                    ),
                (
                    'Violin Staff Group',
                    [
                        ('color', 'blue'),
                        ],
                    ),
                ],
            )

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
        '_score_template',
        )

    ### INITIALIZER ###

    def __init__(self, score_template=None, settings=None):
        from abjad.tools import scoretools
        from abjad.tools import templatetools
        if score_template is None:
            score_template = templatetools.StringOrchestraScoreTemplate()
        score = score_template()
        assert isinstance(score, scoretools.Score), repr(score)
        self._score = score
        self._score_template = score_template
        self._components = {}
        for context in iterate(self._score).by_class(scoretools.Context):
            assert context.name is not None, context.name
            component = _ContextMapComponent(
                self,
                context.name,
                )
            self._components[context.name] = component
        assert isinstance(settings, (dict, type(None)))
        if isinstance(settings, dict):
            for context_name, context_settings in settings.iteritems():
                for key, value in context_settings.iteritems():
                    self[context_name][key] = value

    ### SPECIAL METHODS ###

    def __getitem__(self, context_name):
        r'''Gets context map component for `context_name`.

        Returns context map component.
        '''
        from abjad.tools import scoretools
        if isinstance(context_name, scoretools.Context):
            context_name = context_name.name
        return self._components[context_name]

    ### PUBLIC METHODS ###

    def copy(self):
        r'''Copy context map.

        ::

            >>> copied_context_map = context_map.copy()
            >>> print format(copied_context_map)
            datastructuretools.ContextMap(
                score_template=templatetools.StringOrchestraScoreTemplate(
                    violin_count=6,
                    viola_count=4,
                    cello_count=3,
                    contrabass_count=2,
                    ),
                settings=[
                    (
                        'Contrabass 1 Voice',
                        [
                            ('color', 'yellow'),
                            ],
                        ),
                    (
                        'Contrabass Staff Group',
                        [
                            ('color', 'green'),
                            ],
                        ),
                    (
                        'String Orchestra Score',
                        [
                            ('color', 'red'),
                            ],
                        ),
                    (
                        'Violin Staff Group',
                        [
                            ('color', 'blue'),
                            ],
                        ),
                    ],
                )

        '''
        score_template = self.score_template
        settings = self.settings
        copied = type(self)(
            score_template=score_template,
            settings=settings,
            )
        return copied

    def update(self, expr):
        r'''Updates context map with information in context map `expr`.

        ::

            >>> template = templatetools.StringQuartetScoreTemplate()
            >>> context_map_one = datastructuretools.ContextMap(template)
            >>> context_map_one['Cello Voice']['one'] = 1
            >>> context_map_one['Viola Voice']['foo'] = 'bar'
            >>> context_map_two = datastructuretools.ContextMap(template)
            >>> context_map_two['Cello Voice']['one'] = 'a'
            >>> context_map_two['String Quartet Score']['baz'] = (1, 2, 3)

        ::

            >>> print format(context_map_one)
            datastructuretools.ContextMap(
                score_template=templatetools.StringQuartetScoreTemplate(),
                settings=[
                    (
                        'Cello Voice',
                        [
                            ('one', 1),
                            ],
                        ),
                    (
                        'Viola Voice',
                        [
                            ('foo', 'bar'),
                            ],
                        ),
                    ],
                )

        ::

            >>> print format(context_map_two)
            datastructuretools.ContextMap(
                score_template=templatetools.StringQuartetScoreTemplate(),
                settings=[
                    (
                        'Cello Voice',
                        [
                            ('one', 'a'),
                            ],
                        ),
                    (
                        'String Quartet Score',
                        [
                            (
                                'baz',
                                (1, 2, 3),
                                ),
                            ],
                        ),
                    ],
                )

        ::

            >>> context_map_one.update(context_map_two)
            >>> print format(context_map_one)
            datastructuretools.ContextMap(
                score_template=templatetools.StringQuartetScoreTemplate(),
                settings=[
                    (
                        'Cello Voice',
                        [
                            ('one', 'a'),
                            ],
                        ),
                    (
                        'String Quartet Score',
                        [
                            (
                                'baz',
                                (1, 2, 3),
                                ),
                            ],
                        ),
                    (
                        'Viola Voice',
                        [
                            ('foo', 'bar'),
                            ],
                        ),
                    ],
                )


        Operates in place and returns none.
        '''
        assert isinstance(expr, type(self))
        assert self.score_template == expr.score_template
        for context_name in self._components:
            self_component = self._components[context_name]
            expr_component = expr._components[context_name]
            for key, value in expr_component._context_settings.iteritems():
                self_component[key] = value

    ### PUBLIC PROPERTIES ###

    @property
    def score_template(self):
        r'''Score template on which context map is based.

        ..  container:: example

            ::

                >>> print format(context_map.score_template)
                templatetools.StringOrchestraScoreTemplate(
                    violin_count=6,
                    viola_count=4,
                    cello_count=3,
                    contrabass_count=2,
                    )

        Returns score template or none.
        '''
        return self._score_template

    @property
    def settings(self):
        r'''All settings for context map.

        Returns ordered dict or none.
        '''
        settings = collections.OrderedDict()
        for context_name in sorted(self._components):
            component = self._components[context_name]
            if not len(component):
                continue
            context_settings = collections.OrderedDict()
            for key in sorted(component._context_settings):
                context_settings[key] = component._context_settings[key]
            if context_settings:
                settings[context_name] = context_settings
        if not settings:
            return None
        return settings


class _ContextMapComponent(AbjadObject):
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
        dictionaries = []
        components = self._client._components
        score = self._client._score
        if self._context_name == score.name:
            context = score
        else:
            context = score[self._context_name]
        parentage = inspect_(context).get_parentage()
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

    def __getitem__(self, key):
        r'''Gets `key` for context map component.

        Returns value of `key`.
        '''
        assert isinstance(key, str)
        return self._as_chain_map().__getitem__(key)

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

    def __setitem__(self, key, value):
        r'''Sets `key` to `value` in context map component.

        Returns none.
        '''
        assert isinstance(key, str)
        self._context_settings[key] = value
