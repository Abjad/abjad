# -*- coding: utf-8 -*-
from abjad.tools import durationtools
from abjad.tools import indicatortools
from abjad.tools import systemtools
from abjad.tools.quantizationtools.QSchema import QSchema


class BeatwiseQSchema(QSchema):
    r'''Concrete ``QSchema`` subclass which treats "beats" as its time-step
    unit.

    ::

        >>> q_schema = quantizationtools.BeatwiseQSchema()

    Without arguments, it uses smart defaults:

    ::

        >>> print(format(q_schema, 'storage'))
        quantizationtools.BeatwiseQSchema(
            beatspan=durationtools.Duration(1, 4),
            search_tree=quantizationtools.UnweightedSearchTree(
                definition={
                    2: {
                        2: {
                            2: {
                                2: None,
                                },
                            3: None,
                            },
                        3: None,
                        5: None,
                        7: None,
                        },
                    3: {
                        2: {
                            2: None,
                            },
                        3: None,
                        5: None,
                        },
                    5: {
                        2: None,
                        3: None,
                        },
                    7: {
                        2: None,
                        },
                    11: None,
                    13: None,
                    },
                ),
            tempo=indicatortools.Tempo(
                reference_duration=durationtools.Duration(1, 4),
                units_per_minute=60,
                ),
            )

    Each time-step in a ``BeatwiseQSchema`` is composed of three settings:

        * ``beatspan``
        * ``search_tree``
        * ``tempo``

    These settings can be applied as global defaults for the schema via keyword
    arguments, which persist until overridden:

    ::

        >>> beatspan = Duration(5, 16)
        >>> search_tree = quantizationtools.UnweightedSearchTree({7: None})
        >>> tempo = Tempo((1, 4), 54)
        >>> q_schema = quantizationtools.BeatwiseQSchema(
        ...     beatspan=beatspan,
        ...     search_tree=search_tree,
        ...     tempo=tempo,
        ...     )

    The computed value at any non-negative time-step can be found by
    subscripting:

    ::

        >>> index = 0
        >>> for key, value in sorted(q_schema[index].items()):
        ...     print('{}:'.format(key), value)
        ...
        beatspan: 5/16
        search_tree: UnweightedSearchTree(definition={7: None})
        tempo: 4=54

    ::

        >>> index = 1000
        >>> for key, value in sorted(q_schema[index].items()):
        ...     print('{}:'.format(key), value)
        ...
        beatspan: 5/16
        search_tree: UnweightedSearchTree(definition={7: None})
        tempo: 4=54

    Per-time-step settings can be applied in a variety of ways.

    Instantiating the schema via ``*args`` with a series of either
    ``BeatwiseQSchemaItem`` instances, or dictionaries which could be used to
    instantiate ``BeatwiseQSchemaItem`` instances, will apply those settings
    sequentially, starting from time-step ``0``:

    ::

        >>> a = {'beatspan': Duration(5, 32)}
        >>> b = {'beatspan': Duration(3, 16)}
        >>> c = {'beatspan': Duration(1, 8)}

    ::

        >>> q_schema = quantizationtools.BeatwiseQSchema(a, b, c)

    ::

        >>> q_schema[0]['beatspan']
        Duration(5, 32)

    ::

        >>> q_schema[1]['beatspan']
        Duration(3, 16)

    ::

        >>> q_schema[2]['beatspan']
        Duration(1, 8)

    ::

        >>> q_schema[3]['beatspan']
        Duration(1, 8)

    Similarly, instantiating the schema from a single dictionary, consisting
    of integer:specification pairs, or a sequence via ``*args`` of (integer,
    specification) pairs, allows for applying settings to  non-sequential
    time-steps:

    ::

        >>> a = {'search_tree': quantizationtools.UnweightedSearchTree({2: None})}
        >>> b = {'search_tree': quantizationtools.UnweightedSearchTree({3: None})}

    ::

        >>> settings = {
        ...     2: a,
        ...     4: b,
        ... }

    ::

        >>> q_schema = quantizationtools.MeasurewiseQSchema(settings)

    ::

        >>> print(format(q_schema[0]['search_tree']))
        quantizationtools.UnweightedSearchTree(
            definition={
                2: {
                    2: {
                        2: {
                            2: None,
                            },
                        3: None,
                        },
                    3: None,
                    5: None,
                    7: None,
                    },
                3: {
                    2: {
                        2: None,
                        },
                    3: None,
                    5: None,
                    },
                5: {
                    2: None,
                    3: None,
                    },
                7: {
                    2: None,
                    },
                11: None,
                13: None,
                },
            )

    ::

        >>> print(format(q_schema[1]['search_tree']))
        quantizationtools.UnweightedSearchTree(
            definition={
                2: {
                    2: {
                        2: {
                            2: None,
                            },
                        3: None,
                        },
                    3: None,
                    5: None,
                    7: None,
                    },
                3: {
                    2: {
                        2: None,
                        },
                    3: None,
                    5: None,
                    },
                5: {
                    2: None,
                    3: None,
                    },
                7: {
                    2: None,
                    },
                11: None,
                13: None,
                },
            )

    ::

        >>> q_schema[2]['search_tree']
        UnweightedSearchTree(definition={2: None})

    ::

        >>> q_schema[3]['search_tree']
        UnweightedSearchTree(definition={2: None})

    ::

        >>> q_schema[4]['search_tree']
        UnweightedSearchTree(definition={3: None})

    ::

        >>> q_schema[1000]['search_tree']
        UnweightedSearchTree(definition={3: None})

    The following is equivalent to the above schema definition:

    ::

        >>> q_schema = quantizationtools.MeasurewiseQSchema(
        ...     (2, {'search_tree': quantizationtools.UnweightedSearchTree({2: None})}),
        ...     (4, {'search_tree': quantizationtools.UnweightedSearchTree({3: None})}),
        ...     )

    Return ``BeatwiseQSchema`` instance.
    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        '_beatspan',
        '_items',
        '_lookups',
        '_search_tree',
        '_tempo',
        )

    _keyword_argument_names = (
        'beatspan',
        'search_tree',
        'tempo',
        )

    ### INITIALIZER ###

    def __init__(self, *args, **kwargs):
        from abjad.tools import quantizationtools
        self._beatspan = durationtools.Duration(
            kwargs.get('beatspan',
                (1, 4)))
        search_tree = kwargs.get('search_tree',
            quantizationtools.UnweightedSearchTree())
        assert isinstance(search_tree, quantizationtools.SearchTree)
        self._search_tree = search_tree
        tempo = kwargs.get('tempo', ((1, 4), 60))
        if isinstance(tempo, tuple):
            tempo = indicatortools.Tempo(*tempo)
        self._tempo = tempo
        QSchema.__init__(self, *args, **kwargs)

    ### PRIVATE METHODS ###

    def _get_format_specification(self):
        return systemtools.FormatSpecification(
            client=self,
            storage_format_args_values=self.items or (),
            storage_format_kwargs_names=[
                'beatspan',
                'search_tree',
                'tempo',
                ],
            )

    ### PUBLIC PROPERTIES ###

    @property
    def beatspan(self):
        r'''Default beatspan of beatwise q-schema.
        '''
        return self._beatspan

    @property
    def item_class(self):
        r'''The schema's item class.

        Returns beatwise q-schema item.
        '''
        from abjad.tools import quantizationtools
        return quantizationtools.BeatwiseQSchemaItem

    @property
    def target_class(self):
        r'''Target class of beatwise q-schema.

        Returns beatwise q-target.
        '''
        from abjad.tools import quantizationtools
        return quantizationtools.BeatwiseQTarget

    @property
    def target_item_class(self):
        r'''Target item class of beatwise q-schema.

        Returns q-target beat.
        '''
        from abjad.tools import quantizationtools
        return quantizationtools.QTargetBeat
