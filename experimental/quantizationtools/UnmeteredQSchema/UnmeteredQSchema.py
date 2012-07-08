from abjad.tools import contexttools
from abjad.tools import durationtools
from experimental.quantizationtools.QGridSearchTree import QGridSearchTree
from experimental.quantizationtools.QSchema import QSchema


class UnmeteredQSchema(QSchema):

    ### CLASS ATTRIBUTES ###

    __slots__ = ('_beatspan', '_cyclic', '_items', '_search_tree', '_tempo',)

    ### INITIALIZER ###

    def __init__(self, *args, **kwargs):
        QSchema.__init__(self, *args, **kwargs)

        self._beatspan = durationtools.Duration(
            kwargs.get('beatspan',
                (1, 4)))

        self._search_tree = QGridSearchTree(
            kwargs.get('search_tree',
                QGridSearchTree()))

        self._tempo = contexttools.TempoMark(
            kwargs.get('tempo',
                ((1, 4), 60)))

    ### READ-ONLY PUBLIC PROPERTIES ###

    @property
    def beatspan(self):
        '''The default beatspan.'''
        return self._beatspan

    @property
    def item_klass(self):
        '''The schema's item class.'''
        raise UnmeteredQSchemaItem
