from abjad.tools import contexttools
from abjad.tools import durationtools
from experimental.quantizationtools.QGridSearchTree import QGridSearchTree
from experimental.quantizationtools.QSchema import QSchema



class MeteredQSchema(QSchema):

    ### CLASS ATTRIBUTES ###

    __slots__ = ('_cyclic', '_items', '_search_tree', '_tempo', '_time_signature')

    ### INITIALIZER ###

    def __init__(self, *args, **kwargs):
        QSchema.__init__(self, *args, **kwargs)

        self._search_tree = QGridSearchTree(
            kwargs.get('search_tree',
                QGridSearchTree()))

        self._tempo = contexttools.TempoMark(
            kwargs.get('tempo',
                ((1, 4), 60)))

        self._time_signature = contexttools.TimeSignatureMark(
            kwargs.get('time_signature',
                (4, 4)))

    ### READ-ONLY PUBLIC PROPERTIES ###

    @property
    def item_klass(self):
        '''The schema's item class.'''        
        raise UnmeteredQSchemaItem

    @property
    def time_signature(self):
        '''The default time signature.'''
        return self._time_signature
