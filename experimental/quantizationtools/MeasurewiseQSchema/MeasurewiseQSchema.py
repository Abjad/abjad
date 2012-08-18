from abjad.tools import contexttools
from abjad.tools import durationtools
from experimental.quantizationtools.MeasurewiseQSchemaItem import MeasurewiseQSchemaItem
from experimental.quantizationtools.MeasurewiseQTarget import MeasurewiseQTarget
from experimental.quantizationtools.SearchTree import SearchTree
from experimental.quantizationtools.SimpleSearchTree import SimpleSearchTree
from experimental.quantizationtools.QSchema import QSchema
from experimental.quantizationtools.QTargetMeasure import QTargetMeasure


class MeasurewiseQSchema(QSchema):

    ### CLASS ATTRIBUTES ###

    __slots__ = ('_items', '_lookups', '_search_tree', '_tempo', '_time_signature', '_use_full_measure')

    ### INITIALIZER ###

    def __init__(self, *args, **kwargs):

        search_tree = kwargs.get('search_tree', SimpleSearchTree())
        assert isinstance(search_tree, SearchTree)
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
        return MeasurewiseQSchemaItem

    @property
    def target_item_klass(self):
        return QTargetMeasure

    @property
    def target_klass(self):
        return MeasurewiseQTarget

    @property
    def time_signature(self):
        '''The default time signature.'''
        return self._time_signature

    @property
    def use_full_measure(self):
        '''The full-measure-as-beatspan default.'''
        return self._use_full_measure
