from abjad.tools import abctools
from abjad.tools import contexttools
from abjad.tools import durationtools
from collections import OrderedDict
from experimental.quantizationtools.QGridSearchTree import QGridSearchTree
from experimental.quantizationtools.QTargetGrouping import QTargetGrouping
from experimental.quantizationtools.tempo_scaled_rational_to_milliseconds import tempo_scaled_rational_to_milliseconds


class QTargetItem(tuple, abctools.ImmutableAbjadObject):

    ### CLASS ATTRIBUTES ###

    __slots__ = ()
    _fields = ('beatspan', 'duration_in_ms', 'grouping', 'offset_in_ms',
        'q_events', 'q_grids', 'search_tree', 'tempo')

    ### INITIALIZER ###

    def __new__(klass, beatspan, grouping, offset_in_ms, search_tree, tempo):

        assert isinstance(offset_in_ms, durationtools.Offset)
        assert isinstance(beatspan, durationtools.Duration)
        assert isinstance(grouping, (QTargetGrouping, type(None)))
        assert isinstance(search_tree, QGridSearchTree)
        assert isinstance(tempo, contexttools.TempoMark) and not tempo.is_imprecise

        duration_in_ms = tempo_scaled_rational_to_milliseconds(beatspan, tempo)
        q_events = []
        q_grids = []
        
        return tuple.__new__(klass, (beatspan, duration_in_ms, grouping, offset_in_ms,
            q_events, q_grids, search_tree, tempo))

    ### SPECIAL METHODS ###

    def __getnewargs__(self):
        'Return self as a plain tuple.  Used by copy and pickle.'
        return tuple(self)

    ### SPECIAL PROPERTIES ###

    @property
    def __dict__(self):
        return OrderedDict(zip(self._fields, self))

    ### READ-ONLY PUBLIC PROPERTIES ###

    @property
    def beatspan(self):
        return self[0]

    @property
    def duration_in_ms(self):
        return self[1]

    @property
    def grouping(self):
        return self[2]

    @property
    def offset_in_ms(self):
        return self[3]

    @property
    def q_events(self):
        return self[4]

    @property
    def q_grids(self):
        return self[5]

    @property
    def search_tree(self):
        return self[6]

    @property
    def tempo(self):
        return self[7]

