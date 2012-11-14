from abjad.tools import contexttools
from abjad.tools import durationtools
from abjad.tools.abctools import AbjadObject


class QTargetMeasure(AbjadObject):
    '''Representation of a single "measure" in a measure-wise quantization target.

    ::

        >>> search_tree = quantizationtools.SimpleSearchTree({2: None})
        >>> tempo = contexttools.TempoMark((1, 4), 60)
        >>> time_signature = contexttools.TimeSignatureMark((4, 4))

    ::

        >>> q_target_measure = quantizationtools.QTargetMeasure(
        ...     offset_in_ms=1000,
        ...     search_tree=search_tree,
        ...     tempo=tempo,
        ...     time_signature=time_signature,
        ...     )

    ::

        >>> q_target_measure
        quantizationtools.QTargetMeasure(
            offset_in_ms=durationtools.Offset(1000, 1),
            search_tree=quantizationtools.SimpleSearchTree(
                definition={   2: None}
                ),
            time_signature=contexttools.TimeSignatureMark(
                (4, 4)
                ),
            tempo=contexttools.TempoMark(
                durationtools.Duration(1, 4),
                60
                ),
            use_full_measure=False
            )

    ``QTargetMeasures`` group ``QTargetBeats``:

    ::

        >>> for q_target_beat in q_target_measure.beats:
        ...     print q_target_beat.offset_in_ms, q_target_beat.duration_in_ms
        1000 1000
        2000 1000
        3000 1000
        4000 1000

    If ``use_full_measure`` is set, the ``QTargetMeasure`` will only ever contain
    a single ``QTargetBeat`` instance:

    ::

        >>> another_q_target_measure = quantizationtools.QTargetMeasure(
        ...     offset_in_ms=1000,
        ...     search_tree=search_tree,
        ...     tempo=tempo,
        ...     time_signature=time_signature,
        ...     use_full_measure=True,
        ...     )
    
    ::

        >>> for q_target_beat in another_q_target_measure.beats:
        ...     print q_target_beat.offset_in_ms, q_target_beat.duration_in_ms
        1000 4000

    Not composer-safe.

    Used internally by ``Quantizer``.

    Return ``QTargetMeasure`` instance.
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
            beat = quantizationtools.QTargetBeat(
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

    ### SPECIAL METHODS ###

    def __repr__(self):
        return self._tools_package_qualified_indented_repr

    ### READ-ONLY PUBLIC PROPERTIES ###
        
    @property
    def beats(self):
        '''The tuple of ``QTargetBeats`` contained by the ``QTargetMeasure``:

        ::

            >>> for q_target_beat in q_target_measure.beats:
            ...     q_target_beat
            quantizationtools.QTargetBeat(
                beatspan=durationtools.Duration(1, 4),
                offset_in_ms=durationtools.Offset(1000, 1),
                search_tree=quantizationtools.SimpleSearchTree(
                    definition={   2: None}
                    ),
                tempo=contexttools.TempoMark(
                    durationtools.Duration(1, 4),
                    60
                    )
                )
            quantizationtools.QTargetBeat(
                beatspan=durationtools.Duration(1, 4),
                offset_in_ms=durationtools.Offset(2000, 1),
                search_tree=quantizationtools.SimpleSearchTree(
                    definition={   2: None}
                    ),
                tempo=contexttools.TempoMark(
                    durationtools.Duration(1, 4),
                    60
                    )
                )
            quantizationtools.QTargetBeat(
                beatspan=durationtools.Duration(1, 4),
                offset_in_ms=durationtools.Offset(3000, 1),
                search_tree=quantizationtools.SimpleSearchTree(
                    definition={   2: None}
                    ),
                tempo=contexttools.TempoMark(
                    durationtools.Duration(1, 4),
                    60
                    )
                )
            quantizationtools.QTargetBeat(
                beatspan=durationtools.Duration(1, 4),
                offset_in_ms=durationtools.Offset(4000, 1),
                search_tree=quantizationtools.SimpleSearchTree(
                    definition={   2: None}
                    ),
                tempo=contexttools.TempoMark(
                    durationtools.Duration(1, 4),
                    60
                    )
                )

        Return tuple.
        '''

        return self._beats

    @property
    def duration_in_ms(self):
        '''The duration in milliseconds of the ``QTargetMeasure``:

        ::

            >>> q_target_measure.duration_in_ms
            Duration(4000, 1)

        Return Duration.
        '''
        from experimental import quantizationtools
        return quantizationtools.tempo_scaled_rational_to_milliseconds(
            self.time_signature.duration, self.tempo)

    @property
    def offset_in_ms(self):
        '''The offset in milliseconds of the ``QTargetMeasure``:

        ::

            >>> q_target_measure.offset_in_ms
            Offset(1000, 1)

        Return Offset.
        '''
        return self._offset_in_ms

    @property
    def search_tree(self):
        '''The search tree of the ``QTargetMeasure``:

        ::

            >>> q_target_measure.search_tree
            SimpleSearchTree(
                definition={   2: None}
                )

        Return ``SearchTree`` instance.
        '''
        return self._search_tree

    @property
    def tempo(self):
        '''The tempo of the ``QTargetMeasure``:

        ::

            >>> q_target_measure.tempo
            TempoMark(Duration(1, 4), 60)

        Return ``TempoMark`` instance.
        '''
        return self._tempo

    @property
    def time_signature(self):
        '''The time signature of the ``QTargetMeasure``:

        ::

            >>> q_target_measure.time_signature
            TimeSignatureMark((4, 4))

        Return ```TimeSignatureMark`` instance.
        '''
        return self._time_signature

    @property
    def use_full_measure(self):
        '''The ``use_full_measure`` flag of the ``QTargetMeasure``:

        ::

            >>> q_target_measure.use_full_measure
            False

        Return boolean.
        '''
        return self._use_full_measure

