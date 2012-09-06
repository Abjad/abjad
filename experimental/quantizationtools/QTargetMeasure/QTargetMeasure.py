from abjad.tools import contexttools
from abjad.tools import durationtools
from abjad.tools.abctools import AbjadObject


class QTargetMeasure(AbjadObject):
    '''Representation of a single "measure" in a measure-wise quantization target.

    QTargetMeasures group QTargetBeats.

    Not composer-safe.

    Used internally by quantizationtools.Quantizer.
    '''

    ### CLASS ATTRIBUTES ###

    __slots__ = ('_beats', '_offset_in_ms', '_search_tree', '_tempo', '_time_signature',
        '_use_full_measure')

    ### INITIALIZER ###

    def __init__(self, offset_in_ms=None, search_tree=None, time_signature=None,
        tempo=None, use_full_measure=False):

        from experimental import quantizationtools

        offset_in_ms = durationtools.Offset(offset_in_ms)

        if search_tree is None:
            search_tree = quantizationtools.SimpleSearchTree()
        assert isinstance(search_tree, quantizationtools.SearchTree)
        tempo = contexttools.TempoMark(tempo)
        assert not tempo.is_imprecise
        time_signature = contexttools.TimeSignatureMark(time_signature)
        use_full_measure = bool(use_full_measure)

        beats = []

        if use_full_measure:
            beatspan = time_signature.duration
            beat = QTargetBeat(
                beatspan=beatspan,
                offset_in_ms=offset_in_ms,
                search_tree=search_tree,
                tempo=tempo
                )
            beats.append(beat)
        else:
            beatspan = durationtools.Duration(1, time_signature.denominator)
            current_offset_in_ms = offset_in_ms
            beatspan_duration_in_ms = quantizationtools.tempo_scaled_rational_to_milliseconds(beatspan, tempo)
            for i in range(time_signature.numerator):
                beat = quantizationtools.QTargetBeat(
                    beatspan=beatspan,
                    offset_in_ms=current_offset_in_ms,
                    search_tree=search_tree,
                    tempo=tempo
                    )
                beats.append(beat)
                current_offset_in_ms += beatspan_duration_in_ms

        self._beats = tuple(beats)
        self._offset_in_ms = offset_in_ms
        self._search_tree = search_tree
        self._tempo = tempo
        self._time_signature = time_signature
        self._use_full_measure = use_full_measure

    ### READ-ONLY PUBLIC PROPERTIES ###
        
    @property
    def beats(self):
        return self._beats

    @property
    def duration_in_ms(self):
        from experimental import quantizationtools
        return quantizationtools.tempo_scaled_rational_to_milliseconds(
            self.time_signature.duration, self.tempo)

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

