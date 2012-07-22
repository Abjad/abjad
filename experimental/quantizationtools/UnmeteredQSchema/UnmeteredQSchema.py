from abjad.tools import contexttools
from abjad.tools import durationtools
from experimental.quantizationtools.QGridSearchTree import QGridSearchTree
from experimental.quantizationtools.QSchema import QSchema
from experimental.quantizationtools.UnmeteredQSchemaItem import UnmeteredQSchemaItem


class UnmeteredQSchema(QSchema):

    ### CLASS ATTRIBUTES ###

    __slots__ = ('_beatspan', '_items', '_lookups', '_search_tree', '_tempo',)

    ### INITIALIZER ###

    def __init__(self, *args, **kwargs):

        self._beatspan = durationtools.Duration(
            kwargs.get('beatspan',
                (1, 4)))

        self._search_tree = QGridSearchTree(
            kwargs.get('search_tree',
                QGridSearchTree()))

        self._tempo = contexttools.TempoMark(
            kwargs.get('tempo',
                ((1, 4), 60)))

        QSchema.__init__(self, *args, **kwargs)

    ### READ-ONLY PUBLIC PROPERTIES ###

    @property
    def beatspan(self):
        '''The default beatspan.'''
        return self._beatspan

    @property
    def item_klass(self):
        '''The schema's item class.'''
        return UnmeteredQSchemaItem

    @property
    def target_klass(self):
        return QTargetItem
