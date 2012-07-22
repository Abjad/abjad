from abjad.tools import contexttools
from abjad.tools import durationtools
from experimental.quantizationtools.MeteredQSchemaItem import MeteredQSchemaItem
from experimental.quantizationtools.QGridSearchTree import QGridSearchTree
from experimental.quantizationtools.QSchema import QSchema


class MeteredQSchema(QSchema):

    ### CLASS ATTRIBUTES ###

    __slots__ = ('_items', '_lookups', '_search_tree', '_tempo', '_time_signature', '_use_full_measure')

    ### INITIALIZER ###

    def __init__(self, *args, **kwargs):

        self._search_tree = QGridSearchTree(
            kwargs.get('search_tree',
                QGridSearchTree()))

        self._tempo = contexttools.TempoMark(
            kwargs.get('tempo',
                ((1, 4), 60)))

        self._time_signature = contexttools.TimeSignatureMark(
            kwargs.get('time_signature',
                (4, 4)))

        self._use_full_measure = bool(kwargs.get('use_full_measure'))

        QSchema.__init__(self, *args, **kwargs)

    ### READ-ONLY PUBLIC PROPERTIES ###

    @property
    def item_klass(self):
        '''The schema's item class.'''        
        return MeteredQSchemaItem

    @property
    def target_klass(self):
        return QTargetGrouping

    @property
    def time_signature(self):
        '''The default time signature.'''
        return self._time_signature

    @property
    def use_full_measure(self):
        '''The full-measure-as-beatspan default.'''
        return self._use_full_measure
