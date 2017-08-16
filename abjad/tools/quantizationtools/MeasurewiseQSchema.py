from abjad.tools import indicatortools
from abjad.tools import systemtools
from abjad.tools.quantizationtools.QSchema import QSchema


class MeasurewiseQSchema(QSchema):
    r'''Measurewise q-schema.

    Treats measures as its timestep unit.

    ::

        >>> q_schema = abjad.quantizationtools.MeasurewiseQSchema()

    ..  container:: example

        Without arguments, it uses smart defaults:

        ::

            >>> f(q_schema)
            abjad.quantizationtools.MeasurewiseQSchema(
                search_tree=abjad.quantizationtools.UnweightedSearchTree(
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
                tempo=abjad.MetronomeMark(
                    reference_duration=abjad.Duration(1, 4),
                    units_per_minute=60,
                    ),
                time_signature=abjad.TimeSignature((4, 4)),
                use_full_measure=False,
                )

    ..  container:: example

        Each time-step in a ``MeasurewiseQSchema`` is composed of four settings:

            * ``search_tree``
            * ``tempo``
            * ``time_signature``
            * ``use_full_measure``

        These settings can be applied as global defaults for the schema via keyword
        arguments, which persist until overridden:

        ::

            >>> search_tree = abjad.quantizationtools.UnweightedSearchTree({7: None})
            >>> time_signature = abjad.TimeSignature((3, 4))
            >>> tempo = abjad.MetronomeMark((1, 4), 54)
            >>> use_full_measure = True
            >>> q_schema = abjad.quantizationtools.MeasurewiseQSchema(
            ...     search_tree=search_tree,
            ...     tempo=tempo,
            ...     time_signature=time_signature,
            ...     use_full_measure=use_full_measure,
            ...     )

        All of these settings are self-descriptive, except for
        ``use_full_measure``, which controls whether the measure is subdivided by
        the ``Quantizer`` into beats according to its time signature.

        If ``use_full_measure`` is ``False``, the time-step's measure will be
        divided into units according to its time-signature.  For example, a 4/4
        measure will be divided into 4 units, each having a beatspan of 1/4.

        On the other hand, if ``use_full_measure`` is set to ``True``, the
        time-step's measure will not be subdivided into independent quantization
        units. This usually results in full-measure tuplets.

    ..  container:: example

        The computed value at any non-negative time-step can be found by
        subscripting:

        ::

            >>> index = 0
            >>> for key, value in sorted(q_schema[index].items()):
            ...     print('{}:'.format(key), value)
            ...
            search_tree: UnweightedSearchTree(definition={7: None})
            tempo: 4=54
            time_signature: 3/4
            use_full_measure: True

        ::

            >>> index = 1000
            >>> for key, value in sorted(q_schema[index].items()):
            ...     print('{}:'.format(key), value)
            ...
            search_tree: UnweightedSearchTree(definition={7: None})
            tempo: 4=54
            time_signature: 3/4
            use_full_measure: True

    ..  container:: example

        Per-time-step settings can be applied in a variety of ways.

        Instantiating the schema via ``*arguments`` with a series of either
        ``MeasurewiseQSchemaItem`` instances, or dictionaries which could be used
        to instantiate ``MeasurewiseQSchemaItem`` instances, will apply those
        settings sequentially, starting from time-step ``0``:

        ::

            >>> a = {'search_tree': abjad.quantizationtools.UnweightedSearchTree({2: None})}
            >>> b = {'search_tree': abjad.quantizationtools.UnweightedSearchTree({3: None})}
            >>> c = {'search_tree': abjad.quantizationtools.UnweightedSearchTree({5: None})}

        ::

            >>> q_schema = abjad.quantizationtools.MeasurewiseQSchema(a, b, c)

        ::

            >>> q_schema[0]['search_tree']
            UnweightedSearchTree(definition={2: None})

        ::

            >>> q_schema[1]['search_tree']
            UnweightedSearchTree(definition={3: None})

        ::

            >>> q_schema[2]['search_tree']
            UnweightedSearchTree(definition={5: None})

        ::

            >>> q_schema[1000]['search_tree']
            UnweightedSearchTree(definition={5: None})

    ..  container:: example

        Similarly, instantiating the schema from a single dictionary, consisting of
        integer:specification pairs, or a sequence via ``*arguments`` of (integer,
        specification) pairs, allows for applying settings to non-sequential
        time-steps:

        ::

            >>> a = {'time_signature': abjad.TimeSignature((7, 32))}
            >>> b = {'time_signature': abjad.TimeSignature((3, 4))}
            >>> c = {'time_signature': abjad.TimeSignature((5, 8))}

        ::

            >>> settings = {
            ...     2: a,
            ...     4: b,
            ...     6: c,
            ... }

        ::

            >>> q_schema = abjad.quantizationtools.MeasurewiseQSchema(settings)

        ::

            >>> q_schema[0]['time_signature']
            TimeSignature((4, 4))

        ::

            >>> q_schema[1]['time_signature']
            TimeSignature((4, 4))

        ::

            >>> q_schema[2]['time_signature']
            TimeSignature((7, 32))

        ::

            >>> q_schema[3]['time_signature']
            TimeSignature((7, 32))

        ::

            >>> q_schema[4]['time_signature']
            TimeSignature((3, 4))

        ::

            >>> q_schema[5]['time_signature']
            TimeSignature((3, 4))

        ::

            >>> q_schema[6]['time_signature']
            TimeSignature((5, 8))

        ::

            >>> q_schema[1000]['time_signature']
            TimeSignature((5, 8))

    ..  container:: example

        The following is equivalent to the above schema definition:

        ::

            >>> q_schema = abjad.quantizationtools.MeasurewiseQSchema(
            ...     (2, {'time_signature': abjad.TimeSignature((7, 32))}),
            ...     (4, {'time_signature': abjad.TimeSignature((3, 4))}),
            ...     (6, {'time_signature': abjad.TimeSignature((5, 8))}),
            ...     )

    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        '_items',
        '_lookups',
        '_search_tree',
        '_tempo',
        '_time_signature',
        '_use_full_measure',
        )

    _keyword_argument_names = (
        'search_tree',
        'tempo',
        'time_signature',
        'use_full_measure',
        )

    _publish_storage_format = True

    ### INITIALIZER ###

    def __init__(self, *arguments, **keywords):
        from abjad.tools import quantizationtools
        search_tree = keywords.get(
            'search_tree', quantizationtools.UnweightedSearchTree())
        assert isinstance(search_tree, quantizationtools.SearchTree)
        self._search_tree = search_tree
        tempo = keywords.get('tempo', ((1, 4), 60))
        if isinstance(tempo, tuple):
            tempo = indicatortools.MetronomeMark(*tempo)
        self._tempo = tempo
        self._time_signature = indicatortools.TimeSignature(
            keywords.get('time_signature', (4, 4)))
        self._use_full_measure = bool(keywords.get('use_full_measure'))
        QSchema.__init__(self, *arguments, **keywords)

    ### PRIVATE METHODS ###

    def _get_format_specification(self):
        return systemtools.FormatSpecification(
            client=self,
            storage_format_args_values=self.items or (),
            storage_format_kwargs_names=[
                'search_tree',
                'tempo',
                'time_signature',
                'use_full_measure',
                ],
            )

    ### PUBLIC PROPERTIES ###

    @property
    def item_class(self):
        r'''Item class of measurewise q-schema.

        Returns ``MeasurewiseQSchemaItem``.
        '''
        from abjad.tools import quantizationtools
        return quantizationtools.MeasurewiseQSchemaItem

    @property
    def target_class(self):
        r'''Target class of measurewise q-schema.

        Returns ``MeasurewiseQTarget``.
        '''
        from abjad.tools import quantizationtools
        return quantizationtools.MeasurewiseQTarget

    @property
    def target_item_class(self):
        r'''Target item class of measurewise q-schema.

        Returns ``QTargetMeasure``.
        '''
        from abjad.tools import quantizationtools
        return quantizationtools.QTargetMeasure

    @property
    def time_signature(self):
        r'''Default time signature of measurewise q-schema.

        Returns time signature.
        '''
        return self._time_signature

    @property
    def use_full_measure(self):
        r'''The full-measure-as-beatspan default.

        Returns true or false.
        '''
        return self._use_full_measure
