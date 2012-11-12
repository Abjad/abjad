from abjad.tools import contexttools
from abjad.tools import durationtools
from experimental.quantizationtools.QSchema import QSchema


class BeatwiseQSchema(QSchema):
    '''Concrete ``QSchema`` subclass which treats "beats" as its time-step unit:

    ::

        >>> q_schema = quantizationtools.BeatwiseQSchema()

    Without arguments, it uses smart defaults:

    ::

        >>> q_schema
        quantizationtools.BeatwiseQSchema(
            beatspan=durationtools.Duration(1, 4),
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
            )

    Return ``BeatwiseQSchema`` instance.
    '''

    ### CLASS ATTRIBUTES ###

    __slots__ = ('_beatspan', '_items', '_lookups', '_search_tree', '_tempo',)

    ### INITIALIZER ###

    def __init__(self, *args, **kwargs):
        from experimental import quantizationtools

        self._beatspan = durationtools.Duration(
            kwargs.get('beatspan',
                (1, 4)))

        search_tree = kwargs.get('search_tree', quantizationtools.SimpleSearchTree()) 
        assert isinstance(search_tree, quantizationtools.SearchTree)
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
        from experimental import quantizationtools
        return quantizationtools.BeatwiseQSchemaItem

    @property
    def target_item_klass(self):
        from experimental import quantizationtools
        return quantizationtools.QTargetBeat

    @property
    def target_klass(self):
        from experimental import quantizationtools
        return quantizationtools.BeatwiseQTarget
