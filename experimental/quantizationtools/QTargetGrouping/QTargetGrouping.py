from abjad.tools import abctools


class QTargetGrouping(abctools.ImmutableAbjadObject):

    ### CLASS ATTRIBUTES ###

    __slots__ = ('_items', '_offset_in_ms', '_tempo', '_time_signature')

    ### INITIALIZER ###

    def __init__(self, offset_in_ms=None, search_tree=None, time_signature=None,
        tempo=None, use_full_measure=None):

        assert isinstance(offset_in_ms, durationtools.Offset)
        assert isinstance(search_tree, QGridSearchTree)
        assert isinstance(tempo, contexttools.TempoMark) and not tempo.is_imprecise
        assert isinstance(time_signature, contexttools.TimeSignatureMark)
        assert isinstance(use_full_measure, bool)

        items = []

        if use_full_measure:
            beatspan = time_signature.duration
            item = QTargetItem(
                beatspan=beatspan,
                grouping=self,
                offset_in_ms=offset_in_ms,
                search_tree=search_tree,
                tempo=tempo
                )
            items.append(item)
        else:
            beatspan = Duration(1, time_signature.denominator)
            current_offset_in_ms = offset_in_ms
            beatspan_duration_in_ms = tempo_scaled_rational_to_milliseconds(beatspan, tempo)
            for i in range(time_signature.numerator):
                item = QTargetItem(
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
    def beatspan(self):
        return self._beatspan
    
    @property
    def duration_in_ms(self):
        return tempo_scaled_rational_to_milliseconds(self.beatspan, self.tempo)

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

