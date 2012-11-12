from abjad.tools import contexttools
from abjad.tools import durationtools
from experimental.quantizationtools.QSchema import QSchema


class MeasurewiseQSchema(QSchema):
    '''Concrete QSchema subclass which treats "measures" as its time-step unit:

    ::

        >>> q_schema = quantizationtools.MeasurewiseQSchema()

    Without arguments, it uses smart defaults:

    ::

        >>> q_schema
        quantizationtools.MeasurewiseQSchema(
            search_tree=quantizationtools.SimpleSearchTree(
                definition={   2: {   2: {   2: {   2: None}, 3: None}, 3: None, 5: None, 7: None},
                    3: {   2: {   2: None}, 3: None, 5: None},
                    5: {   2: None, 3: None},
                    7: {   2: None},
                    11: None,
                    13: None}
                ),
            tempo=contexttools.TempoMark(
                durationtools.Duration(1, 4),
                60
                ),
            time_signature=contexttools.TimeSignatureMark(
                (4, 4)
                ),
            use_full_measure=False,
            )

    Return ``MeasurewiseQSchema`` instance.
    '''

    ### CLASS ATTRIBUTES ###

    __slots__ = ('_items', '_lookups', '_search_tree', '_tempo', '_time_signature', '_use_full_measure')

    ### INITIALIZER ###

    def __init__(self, *args, **kwargs):
        from experimental import quantizationtools

        search_tree = kwargs.get('search_tree', quantizationtools.SimpleSearchTree())
        assert isinstance(search_tree, quantizationtools.SearchTree)
        self._search_tree = search_tree

        self._tempo = contexttools.TempoMark(
            kwargs.get('tempo',
                ((1, 4), 60)))

        self._time_signature = contexttools.TimeSignatureMark(
            kwargs.get('time_signature',
                (4, 4)))

        self._use_full_measure = bool(kwargs.get('use_full_measure'))

        QSchema.__init__(self, *args, **kwargs)

    ### READ-ONLY PRIVATE PROPERTIES ###

    @property
    def _keyword_argument_names(self):
        return ('search_tree', 'tempo', 'time_signature', 'use_full_measure')

    ### READ-ONLY PUBLIC PROPERTIES ###

    @property
    def item_klass(self):
        '''The schema's item class.'''
        from experimental import quantizationtools
        return quantizationtools.MeasurewiseQSchemaItem

    @property
    def target_item_klass(self):
        from experimental import quantizationtools
        return quantizationtools.QTargetMeasure

    @property
    def target_klass(self):
        from experimental import quantizationtools
        return quantizationtools.MeasurewiseQTarget

    @property
    def time_signature(self):
        '''The default time signature.'''
        return self._time_signature

    @property
    def use_full_measure(self):
        '''The full-measure-as-beatspan default.'''
        return self._use_full_measure
