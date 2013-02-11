from abjad.tools import durationtools
from abjad.tools import sequencetools
from abjad.tools.abctools import ImmutableAbjadObject


class QEventSequence(tuple, ImmutableAbjadObject):
    '''A well-formed sequence of ``QEvent`` instances, containing only
    ``PitchedQEvents`` and ``SilentQEvents``, and terminating with a
    single ``TerminalQEvent`` instance.

    ``QEventSequence`` is the primary input to the ``Quantizer``.

    ``QEventSequence`` provides a number of convenience functions to
    assist with instantiating new sequences:

    ::

        >>> durations = (1000, -500, 1250, -500, 750)

    ::

        >>> sequence = quantizationtools.QEventSequence.from_millisecond_durations(
        ...     durations)

    ::

        >>> for q_event in sequence:
        ...     q_event
        quantizationtools.PitchedQEvent(
            durationtools.Offset(0, 1),
            (NamedChromaticPitch("c'"),),
            attachments=()
            )
        quantizationtools.SilentQEvent(
            durationtools.Offset(1000, 1),
            attachments=()
            )
        quantizationtools.PitchedQEvent(
            durationtools.Offset(1500, 1),
            (NamedChromaticPitch("c'"),),
            attachments=()
            )
        quantizationtools.SilentQEvent(
            durationtools.Offset(2750, 1),
            attachments=()
            )
        quantizationtools.PitchedQEvent(
            durationtools.Offset(3250, 1),
            (NamedChromaticPitch("c'"),),
            attachments=()
            )
        quantizationtools.TerminalQEvent(
            durationtools.Offset(4000, 1)
            )

    Return ``QEventSequence`` instance.
    '''

    ### CLASS ATTRIBUTES ###

    __slots__ = ()

    ### INITIALIZER ###

    def __new__(klass, args):
        from abjad.tools import quantizationtools
        klasses = (quantizationtools.PitchedQEvent, quantizationtools.SilentQEvent)
        assert 1 < len(args)
        assert all([isinstance(x, klasses) for x in args[:-1]])
        assert isinstance(args[-1], quantizationtools.TerminalQEvent)
        assert sequencetools.is_monotonically_increasing_sequence([x.offset for x in args])
        assert 0 <= args[0].offset
        return tuple.__new__(klass, args)

    ### SPECIAL METHODS ###

    def __repr__(self):
        return '{}({})'.format(self._class_name, tuple.__repr__(self))

    ### READ-ONLY PUBLIC PROPERTIES ###

    @property
    def duration_in_ms(self):
        '''The total duration in milliseconds of the ``QEventSequence``:

        ::

            >>> sequence.duration_in_ms
            Duration(4000, 1)

        Return ``Duration`` instance.
        '''
        return durationtools.Duration(self[-1].offset)

    ### PUBLIC METHODS ###

    @classmethod
    def from_millisecond_durations(klass, durations, fuse_silences=False):
        '''Convert a sequence of millisecond durations ``durations`` into
        a ``QEventSequence``:

        ::

            >>> durations = [-250, 500, -1000, 1250, -1000]

        ::

            >>> sequence = quantizationtools.QEventSequence.from_millisecond_durations(
            ...     durations)

        ::

            >>> for q_event in sequence:
            ...     q_event
            ...
            quantizationtools.SilentQEvent(
                durationtools.Offset(0, 1),
                attachments=()
                )
            quantizationtools.PitchedQEvent(
                durationtools.Offset(250, 1),
                (NamedChromaticPitch("c'"),),
                attachments=()
                )
            quantizationtools.SilentQEvent(
                durationtools.Offset(750, 1),
                attachments=()
                )
            quantizationtools.PitchedQEvent(
                durationtools.Offset(1750, 1),
                (NamedChromaticPitch("c'"),),
                attachments=()
                )
            quantizationtools.SilentQEvent(
                durationtools.Offset(3000, 1),
                attachments=()
                )
            quantizationtools.TerminalQEvent(
                durationtools.Offset(4000, 1)
                )

        Return ``QEventSequence`` instance.
        '''
        from abjad.tools.quantizationtools import milliseconds_to_q_events
        return klass(milliseconds_to_q_events(durations, fuse_silences))

    @classmethod
    def from_millisecond_offsets(klass, offsets):
        '''Convert millisecond offsets ``offsets`` into a ``QEventSequence``:

        ::
        
            >>> offsets = [0, 250, 750, 1750, 3000, 4000]

        ::

            >>> sequence = quantizationtools.QEventSequence.from_millisecond_offsets(
            ...     offsets)

        ::

            >>> for q_event in sequence:
            ...     q_event
            ...
            quantizationtools.PitchedQEvent(
                durationtools.Offset(0, 1),
                (NamedChromaticPitch("c'"),),
                attachments=()
                )
            quantizationtools.PitchedQEvent(
                durationtools.Offset(250, 1),
                (NamedChromaticPitch("c'"),),
                attachments=()
                )
            quantizationtools.PitchedQEvent(
                durationtools.Offset(750, 1),
                (NamedChromaticPitch("c'"),),
                attachments=()
                )
            quantizationtools.PitchedQEvent(
                durationtools.Offset(1750, 1),
                (NamedChromaticPitch("c'"),),
                attachments=()
                )
            quantizationtools.PitchedQEvent(
                durationtools.Offset(3000, 1),
                (NamedChromaticPitch("c'"),),
                attachments=()
                )
            quantizationtools.TerminalQEvent(
                durationtools.Offset(4000, 1)
                )

        Return ``QEventSequence`` instance.
        '''
        from abjad.tools import quantizationtools
        q_events = [quantizationtools.PitchedQEvent(x, [0]) for x in offsets[:-1]]
        q_events.append(quantizationtools.TerminalQEvent(offsets[-1]))
        return klass(q_events)

    @classmethod
    def from_millisecond_pitch_pairs(klass, pairs):
        '''Convert millisecond-duration:pitch pairs ``pairs`` into a ``QEventSequence``:

        ::

            >>> durations = [250, 500, 1000, 1250, 1000]
            >>> pitches = [(0,), None, (2, 3), None, (1,)]
            >>> pairs = zip(durations, pitches)

        ::

            >>> sequence = quantizationtools.QEventSequence.from_millisecond_pitch_pairs(
            ...     pairs)

        ::

            >>> for q_event in sequence:
            ...     q_event
            ...
            quantizationtools.PitchedQEvent(
                durationtools.Offset(0, 1),
                (NamedChromaticPitch("c'"),),
                attachments=()
                )
            quantizationtools.SilentQEvent(
                durationtools.Offset(250, 1),
                attachments=()
                )
            quantizationtools.PitchedQEvent(
                durationtools.Offset(750, 1),
                (NamedChromaticPitch("d'"), NamedChromaticPitch("ef'")),
                attachments=()
                )
            quantizationtools.SilentQEvent(
                durationtools.Offset(1750, 1),
                attachments=()
                )
            quantizationtools.PitchedQEvent(
                durationtools.Offset(3000, 1),
                (NamedChromaticPitch("cs'"),),
                attachments=()
                )
            quantizationtools.TerminalQEvent(
                durationtools.Offset(4000, 1)
                )

        Return ``QEventSequence`` instance.
        '''
        from abjad.tools.quantizationtools import millisecond_pitch_pairs_to_q_events
        return klass(millisecond_pitch_pairs_to_q_events(pairs))

    @classmethod
    def from_tempo_scaled_durations(klass, durations, tempo=None):
        '''Convert ``durations``, scaled by ``tempo`` into a ``QEventSequence``:

        ::

            >>> tempo = contexttools.TempoMark((1, 4), 174)
            >>> durations = [(1, 4), (-3, 16), (1, 16), (-1, 2)]

        ::

            >>> sequence = quantizationtools.QEventSequence.from_tempo_scaled_durations(
            ...     durations, tempo=tempo)

        ::

            >>> for q_event in sequence:
            ...     q_event
            ...
            quantizationtools.PitchedQEvent(
                durationtools.Offset(0, 1),
                (NamedChromaticPitch("c'"),),
                attachments=()
                )
            quantizationtools.SilentQEvent(
                durationtools.Offset(10000, 29),
                attachments=()
                )
            quantizationtools.PitchedQEvent(
                durationtools.Offset(17500, 29),
                (NamedChromaticPitch("c'"),),
                attachments=()
                )
            quantizationtools.SilentQEvent(
                durationtools.Offset(20000, 29),
                attachments=()
                )
            quantizationtools.TerminalQEvent(
                durationtools.Offset(40000, 29)
                )

        Return ``QEventSequence`` instance.
        '''
        from abjad.tools.quantizationtools import tempo_scaled_durations_to_q_events
        return klass(tempo_scaled_durations_to_q_events(durations, tempo))

    @classmethod
    def from_tempo_scaled_leaves(klass, leaves, tempo=None):
        '''Convert ``leaves``, optionally with ``tempo`` into a ``QEventSequence``:

        ::

            >>> staff = Staff("c'4 <d' fs'>8. r16 gqs'2")
            >>> tempo = contexttools.TempoMark((1, 4), 72)

        ::

            >>> sequence = quantizationtools.QEventSequence.from_tempo_scaled_leaves(
            ...     staff.leaves, tempo=tempo)

        ::

            >>> for q_event in sequence:
            ...     q_event
            ...
            quantizationtools.PitchedQEvent(
                durationtools.Offset(0, 1),
                (NamedChromaticPitch("c'"),),
                attachments=()
                )
            quantizationtools.PitchedQEvent(
                durationtools.Offset(2500, 3),
                (NamedChromaticPitch("d'"), NamedChromaticPitch("fs'")),
                attachments=()
                )
            quantizationtools.SilentQEvent(
                durationtools.Offset(4375, 3),
                attachments=()
                )
            quantizationtools.PitchedQEvent(
                durationtools.Offset(5000, 3),
                (NamedChromaticPitch("gqs'"),),
                attachments=()
                )
            quantizationtools.TerminalQEvent(
                durationtools.Offset(10000, 3)
                )

        If ``tempo`` is ``None``, all leaves in ``leaves`` must have an effective,
        non-imprecise tempo.  The millisecond-duration of each leaf will be
        determined by its effective tempo.

        Return ``QEventSequence`` instance.
        '''
        from abjad.tools.quantizationtools import tempo_scaled_leaves_to_q_events
        return klass(tempo_scaled_leaves_to_q_events(leaves, tempo))
