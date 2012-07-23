from abjad.tools import abctools
from abjad.tools import contexttools
from abjad.tools import durationtools
from experimental.quantizationtools.QGridSearchTree import QGridSearchTree
from experimental.quantizationtools.tempo_scaled_rational_to_milliseconds import tempo_scaled_rational_to_milliseconds


class QTargetBeat(abctools.AbjadObject):

    ### CLASS ATTRIBUTES ###

    __slots__ = ('_beatspan', '_grouping', '_offset_in_ms',
        '_q_events', '_q_grids', '_search_tree', '_tempo')

    ### INITIALIZER ###

    def __init__(self, beatspan=None, grouping=None, offset_in_ms=None, search_tree=None, tempo=None):

        from experimental.quantizationtools.QTargetMeasure import QTargetMeasure

        beatspan = durationtools.Duration(beatspan)
        offset_in_ms = durationtools.Offset(offset_in_ms)
        assert isinstance(grouping, (QTargetMeasure, type(None)))
        search_tree = QGridSearchTree(search_tree)
        tempo = contexttools.TempoMark(tempo)
        assert not tempo.is_imprecise

        q_events = []
        q_grids = []
        
        self._beatspan = beatspan
        self._grouping = grouping
        self._offset_in_ms = offset_in_ms
        self._q_events = q_events
        self._q_grids = q_grids
        self._search_tree = search_tree
        self._tempo = tempo

    ### READ-ONLY PUBLIC PROPERTIES ###

    @property
    def beatspan(self):
        return self._beatspan

    @property
    def duration_in_ms(self):
        return tempo_scaled_rational_to_milliseconds(self.beatspan, self.tempo)

    @property
    def grouping(self):
        return self._grouping

    @property
    def offset_in_ms(self):
        return self._offset_in_ms

    @property
    def q_events(self):
        return self._q_events

    @property
    def q_grids(self):
        return self._q_grids

    @property
    def search_tree(self):
        return self._search_tree

    @property
    def tempo(self):
        return self._tempo

