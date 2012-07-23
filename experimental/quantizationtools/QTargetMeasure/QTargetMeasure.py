from abjad.tools import abctools
from abjad.tools import contexttools
from abjad.tools import durationtools
from experimental.quantizationtools.QGridSearchTree import QGridSearchTree
from experimental.quantizationtools.tempo_scaled_rational_to_milliseconds \
    import tempo_scaled_rational_to_milliseconds


class QTargetMeasure(abctools.AbjadObject):

    ### CLASS ATTRIBUTES ###

    __slots__ = ('_items', '_offset_in_ms', '_search_tree', '_tempo', '_time_signature',
        '_use_full_measure')

    ### INITIALIZER ###

    def __init__(self, offset_in_ms=None, search_tree=None, time_signature=None,
        tempo=None, use_full_measure=False):

        from experimental.quantizationtools.QTargetBeat import QTargetBeat

        offset_in_ms = durationtools.Offset(offset_in_ms)
        search_tree = QGridSearchTree(search_tree)
        tempo = contexttools.TempoMark(tempo)
        assert not tempo.is_imprecise
        time_signature = contexttools.TimeSignatureMark(time_signature)
        use_full_measure = bool(use_full_measure)

        items = []

        if use_full_measure:
            beatspan = time_signature.duration
            item = QTargetBeat(
                beatspan=beatspan,
                grouping=self,
                offset_in_ms=offset_in_ms,
                search_tree=search_tree,
                tempo=tempo
                )
            items.append(item)
        else:
            beatspan = durationtools.Duration(1, time_signature.denominator)
            current_offset_in_ms = offset_in_ms
            beatspan_duration_in_ms = tempo_scaled_rational_to_milliseconds(beatspan, tempo)
            for i in range(time_signature.numerator):
                item = QTargetBeat(
                    beatspan=beatspan,
                    grouping=self,
                    offset_in_ms=current_offset_in_ms,
                    search_tree=search_tree,
                    tempo=tempo
                    )
                items.append(item)
                current_offset_in_ms += beatspan_duration_in_ms

        self._items = tuple(items)
        self._offset_in_ms = offset_in_ms
        self._search_tree = search_tree
        self._tempo = tempo
        self._time_signature = time_signature
        self._use_full_measure = use_full_measure

    ### READ-ONLY PUBLIC PROPERTIES ###
        
    @property
    def duration_in_ms(self):
        return tempo_scaled_rational_to_milliseconds(self.time_signature.duration, self.tempo)

    @property
    def offset_in_ms(self):
        return self._offset_in_ms

    @property
    def search_tree(self):
        return self._search_tree

    @property
    def tempo(self):
        return self._tempo

    @property
    def time_signature(self):
        return self._time_signature

    @property
    def use_full_measure(self):
        return self._use_full_measure

