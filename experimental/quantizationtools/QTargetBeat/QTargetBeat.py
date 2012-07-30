from abjad.tools import abctools
from abjad.tools import contexttools
from abjad.tools import durationtools
from experimental.quantizationtools.QuantizationJob import QuantizationJob
from experimental.quantizationtools.QEvent import QEvent
from experimental.quantizationtools.SearchTree import SearchTree
from experimental.quantizationtools.tempo_scaled_rational_to_milliseconds import tempo_scaled_rational_to_milliseconds


class QTargetBeat(abctools.AbjadObject):

    ### CLASS ATTRIBUTES ###

    __slots__ = ('_beatspan', '_distances', '_grouping', '_offset_in_ms',
        '_q_events', '_q_grids', '_search_tree', '_tempo')

    ### INITIALIZER ###

    def __init__(self, beatspan=None, offset_in_ms=None, search_tree=None, tempo=None):

        from experimental.quantizationtools.QTargetMeasure import QTargetMeasure

        beatspan = durationtools.Duration(beatspan)
        offset_in_ms = durationtools.Offset(offset_in_ms)
        search_tree = SearchTree(search_tree)
        tempo = contexttools.TempoMark(tempo)
        assert not tempo.is_imprecise

        q_events = []
        q_grids = []
        
        self._beatspan = beatspan
        self._distances = {}
        self._offset_in_ms = offset_in_ms
        self._q_events = q_events
        self._q_grids = q_grids
        self._search_tree = search_tree
        self._tempo = tempo

    ### SPECIAL METHODS ###

    def __call__(self, job_id):
        if not self.q_events:
            return None
        assert all([isinstance(x, QEvent) for x in self.q_events])
        q_event_proxies = []
        for q_event in self.q_events:
            q_event_proxy = QEventProxy(q_event, self.offset_in_ms, self.offset_in_ms + self.duration_in_ms)
            q_event_proxies.append(q_event_proxy)
        return QuantizationJob(job_id, self.search_tree, q_event_proxies)

    ### READ-ONLY PUBLIC PROPERTIES ###

    @property
    def beatspan(self):
        return self._beatspan

    @property
    def distances(self):
        return self._distances

    @property
    def duration_in_ms(self):
        return tempo_scaled_rational_to_milliseconds(self.beatspan, self.tempo)

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
