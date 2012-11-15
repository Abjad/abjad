from abjad.tools import contexttools
from abjad.tools import durationtools
from abjad.tools.quantizationtools.QSchemaItem import QSchemaItem


class BeatwiseQSchemaItem(QSchemaItem):
    '''`BeatwiseQSchemaItem` represents a change of state in the timeline of an unmetered
    quantization process.

    ::

        >>> from abjad.tools import quantizationtools
        >>> quantizationtools.BeatwiseQSchemaItem()
        BeatwiseQSchemaItem()

    Define a change in tempo:

    ::

        >>> quantizationtools.BeatwiseQSchemaItem(tempo=((1, 4), 60))
        BeatwiseQSchemaItem(
            tempo=contexttools.TempoMark(
                    durationtools.Duration(1, 4),
                    60
                    ),
            )
           
    Define a change in beatspan:

    ::

        >>> quantizationtools.BeatwiseQSchemaItem(beatspan=(1, 8))
        BeatwiseQSchemaItem(
            beatspan=durationtools.Duration(1, 8),
            )

    `BeatwiseQSchemaItem` is immutable.

    Return `BeatwiseQSchemaItem` instance.
    '''

    ### CLASS ATTRIBUTES ###

    __slots__ = ()
    _fields = ('beatspan', 'search_tree', 'tempo')

    ### INITIALIZER ###

    def __init__(self, beatspan=None, search_tree=None, tempo=None):
        pass

    def __new__(klass, beatspan=None, search_tree=None, tempo=None):
        from abjad.tools import quantizationtools

        if beatspan is not None:
            beatspan = durationtools.Duration(beatspan)
            assert 0 < beatspan

        if search_tree is not None:
            assert isinstance(search_tree, quantizationtools.SearchTree)

        if tempo is not None:
            tempo = contexttools.TempoMark(tempo)
            assert not tempo.is_imprecise

        return tuple.__new__(klass, (beatspan, search_tree, tempo))

    ### PUBLIC READ-ONLY ATTRIBUTES ###

    @property
    def beatspan(self):
        '''The optionally defined beatspan duration.

        Return `Duration` or `None`.
        '''
        return self[0]

    @property
    def search_tree(self):
        '''The optionally defined search tree.

        Return `OldSearchTree` or `None`.
        '''
        return self[1]

    @property
    def tempo(self):
        '''The optionally defined `TempoMark`.

        Return `TempoMark` or `None`.
        '''
        return self[2]
