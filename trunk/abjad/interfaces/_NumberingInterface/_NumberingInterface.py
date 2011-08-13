from abjad.exceptions import MeasureContiguityError
from abjad.interfaces._Interface import _Interface


class _NumberingInterface(_Interface):
    '''Number score components but handle no LilyPond grob.'''

    __slots__ = ('_leaf', '_measure')

    def __init__(self, _client, update_interface):
        '''Bind to client and register self as observer.
            Init leaf and measure numbers to zero.'''
        _Interface.__init__(self, _client)
        self._leaf = 0
        self._measure = 1

    ### PRIVATE METHODS ###

    def _update_component(self):
        '''Update number of any one node in score.'''
        from abjad.tools.leaftools._Leaf import _Leaf
        from abjad.tools.measuretools.Measure import Measure
        client = self._client
        if isinstance(client, _Leaf):
            self._update_leaf_number( )
        elif isinstance(client, Measure):
            self._update_measure_number( )

    def _update_leaf_number(self):
        '''Update (zero-indexed) number of any one leaf in score.'''
        from abjad.tools.leaftools._Leaf import _Leaf
        prevLeaf = self._client.prev
        if prevLeaf:
            assert isinstance(prevLeaf, _Leaf)
            self._leaf = prevLeaf._numbering._leaf + 1
        else:
            self._leaf = 0

    def _update_measure_number(self):
        '''Update (one-indexed) number of any one measure in score.'''
        from abjad.tools import measuretools
        prevMeasure = measuretools.get_prev_measure_from_component(self._client)
        if prevMeasure is not None:
            self._measure = prevMeasure._numbering._measure + 1
        else:
            self._measure = 1
