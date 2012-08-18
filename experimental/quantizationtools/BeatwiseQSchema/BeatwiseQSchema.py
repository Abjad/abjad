from abjad.tools import contexttools
from abjad.tools import durationtools
from experimental.quantizationtools.BeatwiseQTarget import BeatwiseQTarget
from experimental.quantizationtools.BeatwiseQSchemaItem import BeatwiseQSchemaItem
from experimental.quantizationtools.SearchTree import SearchTree
from experimental.quantizationtools.SimpleSearchTree import SimpleSearchTree
from experimental.quantizationtools.QSchema import QSchema
from experimental.quantizationtools.QTargetBeat import QTargetBeat


class BeatwiseQSchema(QSchema):

    ### CLASS ATTRIBUTES ###

    __slots__ = ('_beatspan', '_items', '_lookups', '_search_tree', '_tempo',)

    ### INITIALIZER ###

    def __init__(self, *args, **kwargs):

        self._beatspan = durationtools.Duration(
            kwargs.get('beatspan',
                (1, 4)))

        search_tree = kwargs.get('search_tree', SimpleSearchTree()) 
        assert isinstance(search_tree, SearchTree)
        self._search_tree = search_tree

        self._tempo = contexttools.TempoMark(
            kwargs.get('tempo',
                ((1, 4), 60)))

        QSchema.__init__(self, *args, **kwargs)

    ### READ-ONLY PRIVATE PROPERTIES ###

    @property
    def _keyword_argument_names(self):
        return ('beatspan', 'search_tree', 'tempo')

    ### READ-ONLY PUBLIC PROPERTIES ###

    @property
    def beatspan(self):
        '''The default beatspan.'''
        return self._beatspan

    @property
    def item_klass(self):
        '''The schema's item class.'''
        return BeatwiseQSchemaItem

    @property
    def target_item_klass(self):
        return QTargetBeat

    @property
    def target_klass(self):
        return BeatwiseQTarget
