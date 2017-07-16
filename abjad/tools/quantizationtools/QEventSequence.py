# -*- coding: utf-8 -*-
import collections
import copy
import itertools
import numbers
from abjad.tools import datastructuretools
from abjad.tools import durationtools
from abjad.tools import indicatortools
from abjad.tools import mathtools
from abjad.tools import scoretools
from abjad.tools import systemtools
from abjad.tools.abctools import AbjadObject


class QEventSequence(AbjadObject):
    r'''Q-event sequence.

    ::

        >>> import abjad
        >>> from abjad.tools import quantizationtools

    Contains only pitched q-events and silent q-events, and terminates with a
    single terminal q-event.

    A q-event sequence is the primary input to the quantizer.

    ..  container:: example

        A q-event sequence provides a number of convenience functions to assist
        with instantiating new sequences:

        ::

            >>> durations = (1000, -500, 1250, -500, 750)

        ::

            >>> sequence = \
            ...     quantizationtools.QEventSequence.from_millisecond_durations(
            ...     durations)

        ::

            >>> for q_event in sequence:
            ...     f(q_event)
            ...
            quantizationtools.PitchedQEvent(
                offset=abjad.Offset(0, 1),
                pitches=(
                    abjad.NamedPitch("c'"),
                    ),
                )
            quantizationtools.SilentQEvent(
                offset=abjad.Offset(1000, 1),
                )
            quantizationtools.PitchedQEvent(
                offset=abjad.Offset(1500, 1),
                pitches=(
                    abjad.NamedPitch("c'"),
                    ),
                )
            quantizationtools.SilentQEvent(
                offset=abjad.Offset(2750, 1),
                )
            quantizationtools.PitchedQEvent(
                offset=abjad.Offset(3250, 1),
                pitches=(
                    abjad.NamedPitch("c'"),
                    ),
                )
            quantizationtools.TerminalQEvent(
                offset=abjad.Offset(4000, 1),
                )

    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        '_sequence',
        )

    _publish_storage_format = True

    ### INITIALIZER ###

    def __init__(self, sequence=None):
        from abjad.tools import quantizationtools
        q_event_classes = (
            quantizationtools.PitchedQEvent,
            quantizationtools.SilentQEvent,
            )
        #sequence = sequence or []
        if sequence is None:
            self._sequence = ()
            return
        else:
            assert 1 < len(sequence)
            assert all(isinstance(q_event, q_event_classes)
                for q_event in sequence[:-1])
            assert isinstance(sequence[-1], quantizationtools.TerminalQEvent)
            offsets = [x.offset for x in sequence]
            offsets = datastructuretools.Sequence(offsets)
            assert offsets.is_increasing(strict=False)
            assert 0 <= sequence[0].offset
            self._sequence = tuple(sequence)

    ### SPECIAL METHODS ###

    def __contains__(self, argument):
        r'''Is true when q-event sequence contains `argument`. Otherwise false.

        Returns true or false.
        '''
        return argument in self._sequence

    def __eq__(self, argument):
        r'''Is true when q-event sequence equals `argument`. Otherwise false.

        Returns true or false.
        '''
        if type(self) == type(argument):
            if self.sequence == argument.sequence:
                return True
        return False

    def __format__(self, format_specification=''):
        r'''Formats q-event sequence.

        Set `format_specification` to `''` or `'storage'`.
        Interprets `''` equal to `'storage'`.

            >>> print(format(sequence))
            quantizationtools.QEventSequence(
                (
                    quantizationtools.PitchedQEvent(
                        offset=abjad.Offset(0, 1),
                        pitches=(
                            abjad.NamedPitch("c'"),
                            ),
                        ),
                    quantizationtools.SilentQEvent(
                        offset=abjad.Offset(1000, 1),
                        ),
                    quantizationtools.PitchedQEvent(
                        offset=abjad.Offset(1500, 1),
                        pitches=(
                            abjad.NamedPitch("c'"),
                            ),
                        ),
                    quantizationtools.SilentQEvent(
                        offset=abjad.Offset(2750, 1),
                        ),
                    quantizationtools.PitchedQEvent(
                        offset=abjad.Offset(3250, 1),
                        pitches=(
                            abjad.NamedPitch("c'"),
                            ),
                        ),
                    quantizationtools.TerminalQEvent(
                        offset=abjad.Offset(4000, 1),
                        ),
                    )
                )

        Returns string.
        '''
        from abjad.tools import systemtools
        if format_specification in ('', 'storage'):
            return systemtools.StorageFormatAgent(self).get_storage_format()
        return str(self)

    def __getitem__(self, argument):
        r'''Gets item or slice identified by `argument`.

        Returns item or slice.
        '''
        return self._sequence.__getitem__(argument)

    def __hash__(self):
        r'''Hashes q-event sequence.

        Required to be explicitly redefined on Python 3 if __eq__ changes.

        Returns integer.
        '''
        return super(QEventSequence, self).__hash__()

    def __iter__(self):
        r'''Iterates q-event sequence.

        Yields items.
        '''
        for x in self._sequence:
            yield x

    def __len__(self):
        r'''Length of q-event sequence.

        Returns nonnegative integer.
        '''
        return len(self._sequence)

    ### PRIVATE METHODS ###

    def _get_format_specification(self):
        values = []
        if self.sequence:
            values.append(self.sequence)
        return systemtools.FormatSpecification(
            client=self,
            storage_format_args_values=values,
            storage_format_kwargs_names=[],
            )

    ### PUBLIC METHODS ###

    @classmethod
    def from_millisecond_durations(class_, milliseconds, fuse_silences=False):
        r'''Convert a sequence of millisecond durations ``durations`` into
        a ``QEventSequence``:

        ::

            >>> durations = [-250, 500, -1000, 1250, -1000]

        ::

            >>> sequence = \
            ...     quantizationtools.QEventSequence.from_millisecond_durations(
            ...     durations)

        ::

            >>> for q_event in sequence:
            ...     print(format(q_event, 'storage'))
            ...
            quantizationtools.SilentQEvent(
                offset=abjad.Offset(0, 1),
                )
            quantizationtools.PitchedQEvent(
                offset=abjad.Offset(250, 1),
                pitches=(
                    abjad.NamedPitch("c'"),
                    ),
                )
            quantizationtools.SilentQEvent(
                offset=abjad.Offset(750, 1),
                )
            quantizationtools.PitchedQEvent(
                offset=abjad.Offset(1750, 1),
                pitches=(
                    abjad.NamedPitch("c'"),
                    ),
                )
            quantizationtools.SilentQEvent(
                offset=abjad.Offset(3000, 1),
                )
            quantizationtools.TerminalQEvent(
                offset=abjad.Offset(4000, 1),
                )

        Returns ``QEventSequence`` instance.
        '''
        from abjad.tools import quantizationtools
        if fuse_silences:
            durations = [
                x for x in
                datastructuretools.Sequence(milliseconds).sum_by_sign(sign=[-1])
                if x
                ]
        else:
            durations = milliseconds
        offsets = mathtools.cumulative_sums([abs(x) for x in durations])
        q_events = []
        for pair in zip(offsets, durations):
            offset = durationtools.Offset(pair[0])
            duration = pair[1]
            if duration < 0: # negative duration indicates silence
                q_event = quantizationtools.SilentQEvent(offset)
            else:
                q_event = quantizationtools.PitchedQEvent(offset, [0])
            q_events.append(q_event)
        q_events.append(quantizationtools.TerminalQEvent(
            durationtools.Offset(offsets[-1])))
        return class_(q_events)

    @classmethod
    def from_millisecond_offsets(class_, offsets):
        r'''Convert millisecond offsets ``offsets`` into a ``QEventSequence``:

        ::

            >>> offsets = [0, 250, 750, 1750, 3000, 4000]

        ::

            >>> sequence = \
            ...     quantizationtools.QEventSequence.from_millisecond_offsets(
            ...     offsets)

        ::

            >>> for q_event in sequence:
            ...     print(format(q_event, 'storage'))
            ...
            quantizationtools.PitchedQEvent(
                offset=abjad.Offset(0, 1),
                pitches=(
                    abjad.NamedPitch("c'"),
                    ),
                )
            quantizationtools.PitchedQEvent(
                offset=abjad.Offset(250, 1),
                pitches=(
                    abjad.NamedPitch("c'"),
                    ),
                )
            quantizationtools.PitchedQEvent(
                offset=abjad.Offset(750, 1),
                pitches=(
                    abjad.NamedPitch("c'"),
                    ),
                )
            quantizationtools.PitchedQEvent(
                offset=abjad.Offset(1750, 1),
                pitches=(
                    abjad.NamedPitch("c'"),
                    ),
                )
            quantizationtools.PitchedQEvent(
                offset=abjad.Offset(3000, 1),
                pitches=(
                    abjad.NamedPitch("c'"),
                    ),
                )
            quantizationtools.TerminalQEvent(
                offset=abjad.Offset(4000, 1),
                )

        Returns ``QEventSequence`` instance.
        '''
        from abjad.tools import quantizationtools
        q_events = [quantizationtools.PitchedQEvent(x, [0])
            for x in offsets[:-1]]
        q_events.append(quantizationtools.TerminalQEvent(offsets[-1]))
        return class_(q_events)

    @classmethod
    def from_millisecond_pitch_pairs(class_, pairs):
        r'''Convert millisecond-duration:pitch pairs ``pairs`` into a
        ``QEventSequence``:

        ::

            >>> durations = [250, 500, 1000, 1250, 1000]
            >>> pitches = [(0,), None, (2, 3), None, (1,)]
            >>> pairs = tuple(zip(durations, pitches))

        ::

            >>> sequence = \
            ...     quantizationtools.QEventSequence.from_millisecond_pitch_pairs(
            ...     pairs)

        ::

            >>> for q_event in sequence:
            ...     print(format(q_event, 'storage'))
            ...
            quantizationtools.PitchedQEvent(
                offset=abjad.Offset(0, 1),
                pitches=(
                    abjad.NamedPitch("c'"),
                    ),
                )
            quantizationtools.SilentQEvent(
                offset=abjad.Offset(250, 1),
                )
            quantizationtools.PitchedQEvent(
                offset=abjad.Offset(750, 1),
                pitches=(
                    abjad.NamedPitch("d'"),
                    abjad.NamedPitch("ef'"),
                    ),
                )
            quantizationtools.SilentQEvent(
                offset=abjad.Offset(1750, 1),
                )
            quantizationtools.PitchedQEvent(
                offset=abjad.Offset(3000, 1),
                pitches=(
                    abjad.NamedPitch("cs'"),
                    ),
                )
            quantizationtools.TerminalQEvent(
                offset=abjad.Offset(4000, 1),
                )

        Returns ``QEventSequence`` instance.
        '''
        from abjad.tools import quantizationtools
        assert isinstance(pairs, collections.Iterable)
        assert all(isinstance(x, collections.Iterable) for x in pairs)
        assert all(len(x) == 2 for x in pairs)
        assert all(0 < x[0] for x in pairs)
        for pair in pairs:
            assert isinstance(pair[1], (
                numbers.Number, type(None), collections.Iterable))
            if isinstance(pair[1], collections.Iterable):
                assert 0 < len(pair[1])
                assert all(isinstance(x, numbers.Number) for x in pair[1])
        # fuse silences
        g = itertools.groupby(pairs, lambda x: x[1] is not None)
        groups = []
        for value, group in g:
            if value:
                groups.extend(list(group))
            else:
                duration = sum(x[0] for x in group)
                groups.append((duration, None))
        # find offsets
        offsets = mathtools.cumulative_sums([abs(x[0]) for x in groups])
        # build QEvents
        q_events = []
        for pair in zip(offsets, groups):
            offset = durationtools.Offset(pair[0])
            pitches = pair[1][1]
            if isinstance(pitches, collections.Iterable):
                assert all(isinstance(x, numbers.Number) for x in pitches)
                q_events.append(quantizationtools.PitchedQEvent(offset, pitches))
            elif isinstance(pitches, type(None)):
                q_events.append(quantizationtools.SilentQEvent(offset))
            elif isinstance(pitches, numbers.Number):
                q_events.append(quantizationtools.PitchedQEvent(offset, [pitches]))
        q_events.append(quantizationtools.TerminalQEvent(
            durationtools.Offset(offsets[-1])))
        return class_(q_events)

    @classmethod
    def from_tempo_scaled_durations(class_, durations, tempo=None):
        r'''Convert ``durations``, scaled by ``tempo``
        into a ``QEventSequence``:

        ::

            >>> tempo = abjad.MetronomeMark((1, 4), 174)
            >>> durations = [(1, 4), (-3, 16), (1, 16), (-1, 2)]

        ::

            >>> sequence = \
            ...     quantizationtools.QEventSequence.from_tempo_scaled_durations(
            ...     durations, tempo=tempo)

        ::

            >>> for q_event in sequence:
            ...     print(format(q_event, 'storage'))
            ...
            quantizationtools.PitchedQEvent(
                offset=abjad.Offset(0, 1),
                pitches=(
                    abjad.NamedPitch("c'"),
                    ),
                )
            quantizationtools.SilentQEvent(
                offset=abjad.Offset(10000, 29),
                )
            quantizationtools.PitchedQEvent(
                offset=abjad.Offset(17500, 29),
                pitches=(
                    abjad.NamedPitch("c'"),
                    ),
                )
            quantizationtools.SilentQEvent(
                offset=abjad.Offset(20000, 29),
                )
            quantizationtools.TerminalQEvent(
                offset=abjad.Offset(40000, 29),
                )

        Returns ``QEventSequence`` instance.
        '''
        from abjad.tools import quantizationtools
        durations = [durationtools.Duration(x) for x in durations]
        assert isinstance(tempo, indicatortools.MetronomeMark)
        durations = [
            x for x in
            datastructuretools.Sequence(durations).sum_by_sign(sign=[-1])
            if x
            ]
        durations = [tempo.duration_to_milliseconds(_) for _ in durations]
        offsets = mathtools.cumulative_sums([abs(_) for _ in durations])
        q_events = []
        for pair in zip(offsets, durations):
            offset = durationtools.Offset(pair[0])
            duration = pair[1]
            if duration < 0: # negative duration indicates silence
                q_event = quantizationtools.SilentQEvent(offset)
            else: # otherwise, use middle-C
                q_event = quantizationtools.PitchedQEvent(offset, [0])
            q_events.append(q_event)
        # insert terminating silence QEvent
        q_events.append(quantizationtools.TerminalQEvent(offsets[-1]))
        return class_(q_events)

    @classmethod
    def from_tempo_scaled_leaves(class_, leaves, tempo=None):
        r'''Convert ``leaves``, optionally with ``tempo`` into a
        ``QEventSequence``:

        ::

            >>> staff = abjad.Staff("c'4 <d' fs'>8. r16 gqs'2")
            >>> tempo = abjad.MetronomeMark((1, 4), 72)

        ::

            >>> sequence = \
            ...     quantizationtools.QEventSequence.from_tempo_scaled_leaves(
            ...     staff[:], tempo=tempo)

        ::

            >>> for q_event in sequence:
            ...     print(format(q_event, 'storage'))
            ...
            quantizationtools.PitchedQEvent(
                offset=abjad.Offset(0, 1),
                pitches=(
                    abjad.NamedPitch("c'"),
                    ),
                )
            quantizationtools.PitchedQEvent(
                offset=abjad.Offset(2500, 3),
                pitches=(
                    abjad.NamedPitch("d'"),
                    abjad.NamedPitch("fs'"),
                    ),
                )
            quantizationtools.SilentQEvent(
                offset=abjad.Offset(4375, 3),
                )
            quantizationtools.PitchedQEvent(
                offset=abjad.Offset(5000, 3),
                pitches=(
                    abjad.NamedPitch("gqs'"),
                    ),
                )
            quantizationtools.TerminalQEvent(
                offset=abjad.Offset(10000, 3),
                )

        If ``tempo`` is ``None``, all leaves in ``leaves`` must
        have an effective, non-imprecise tempo.
        The millisecond-duration of each leaf will be determined
        by its effective tempo.

        Return ``QEventSequence`` instance.
        '''
        from abjad.tools import quantizationtools
        from abjad.tools import selectiontools
        Selection = selectiontools.Selection
        assert Selection._all_in_same_logical_voice(leaves, contiguous=True)
        assert len(leaves)
        if tempo is None:
            prototype = indicatortools.MetronomeMark
            assert leaves[0]._get_effective(prototype) is not None
        #else:
        #    #tempo = indicatortools.MetronomeMark(tempo)
        elif isinstance(tempo, indicatortools.MetronomeMark):
            tempo = copy.copy(tempo)
        elif isinstance(tempo, tuple):
            tempo = indicatortools.MetronomeMark(*tempo)
        else:
            raise TypeError(tempo)
        # sort by silence and tied leaves
        groups = []
        for rvalue, rgroup in itertools.groupby(
            leaves,
            lambda x: isinstance(x, (scoretools.Rest, scoretools.Skip))):
            if rvalue:
                groups.append(list(rgroup))
            else:
                for tvalue, tgroup in itertools.groupby(
                    rgroup, lambda x: x._get_logical_tie()):
                    groups.append(list(tgroup))
        # calculate lists of pitches and durations
        durations = []
        pitches = []
        for group in groups:
            # get millisecond cumulative duration
            if tempo is not None:
                duration = sum(
                    tempo.duration_to_milliseconds(x._get_duration())
                    for x in group)
            else:
                duration = sum(x._get_effective(
                    indicatortools.MetronomeMark).duration_to_milliseconds(
                    x._get_duration())
                    for x in group)
            durations.append(duration)
            # get pitch of first leaf in group
            if isinstance(group[0], (scoretools.Rest, scoretools.Skip)):
                pitch = None
            elif isinstance(group[0], scoretools.Note):
                pitch = group[0].written_pitch.number
            else: # chord
                pitch = [x.written_pitch.number for x in group[0].note_heads]
            pitches.append(pitch)
        # convert durations and pitches to QEvents and return
        return class_.from_millisecond_pitch_pairs(
            tuple(zip(durations, pitches)))

    ### PUBLIC PROPERTIES ###

    @property
    def duration_in_ms(self):
        r'''Duration in milliseconds of the ``QEventSequence``:

        ::

            >>> durations = (1000, -500, 1250, -500, 750)

        ::

            >>> sequence = \
            ...     quantizationtools.QEventSequence.from_millisecond_durations(
            ...     durations)

        ::

            >>> sequence.duration_in_ms
            Duration(4000, 1)

        Return ``Duration`` instance.
        '''
        return durationtools.Duration(self[-1].offset)

    @property
    def sequence(self):
        r'''Sequence of q-events.

        ::

            >>> for q_event in sequence.sequence:
            ...     print(format(q_event, 'storage'))
            ...
            quantizationtools.PitchedQEvent(
                offset=abjad.Offset(0, 1),
                pitches=(
                    abjad.NamedPitch("c'"),
                    ),
                )
            quantizationtools.SilentQEvent(
                offset=abjad.Offset(1000, 1),
                )
            quantizationtools.PitchedQEvent(
                offset=abjad.Offset(1500, 1),
                pitches=(
                    abjad.NamedPitch("c'"),
                    ),
                )
            quantizationtools.SilentQEvent(
                offset=abjad.Offset(2750, 1),
                )
            quantizationtools.PitchedQEvent(
                offset=abjad.Offset(3250, 1),
                pitches=(
                    abjad.NamedPitch("c'"),
                    ),
                )
            quantizationtools.TerminalQEvent(
                offset=abjad.Offset(4000, 1),
                )

        Returns tuple.
        '''
        return self._sequence
