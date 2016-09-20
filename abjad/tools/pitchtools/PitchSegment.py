# -*- coding: utf-8 -*-
from abjad.tools.pitchtools.Segment import Segment
from abjad.tools.topleveltools import iterate
from abjad.tools.topleveltools import new
from abjad.tools.topleveltools import select


class PitchSegment(Segment):
    r'''Pitch segment.

    ..  container:: example

        **Example 1.** Numbered pitch segment:

        ::

            >>> numbered_pitch_segment = pitchtools.PitchSegment(
            ...     items=[-2, -1.5, 6, 7, -1.5, 7],
            ...     item_class=pitchtools.NumberedPitch,
            ...     )
            >>> numbered_pitch_segment
            PitchSegment([-2, -1.5, 6, 7, -1.5, 7])

        ::

            >>> show(numbered_pitch_segment) # doctest: +SKIP

    ..  container:: example

        **Example 2.** Named pitch segment:

        ::

            >>> named_pitch_segment = pitchtools.PitchSegment(
            ...     ['bf,', 'aqs', "fs'", "g'", 'bqf', "g'"],
            ...     item_class=NamedPitch,
            ...     )
            >>> named_pitch_segment
            PitchSegment(['bf,', 'aqs', "fs'", "g'", 'bqf', "g'"])

        ::

            >>> show(named_pitch_segment) # doctest: +SKIP

    Pitch segments are immutable.
    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        )

    ### INITIALIZER ###

    def __init__(
        self,
        items=None,
        item_class=None,
        ):
        if not items and not item_class:
            item_class = self._named_item_class
        Segment.__init__(
            self,
            items=items,
            item_class=item_class,
            )

    ### SPECIAL METHODS ###

    def __illustrate__(self):
        r'''Illustrates pitch segment.

        ::

            >>> named_pitch_segment = pitchtools.PitchSegment(
            ...     ['bf,', 'aqs', "fs'", "g'", 'bqf', "g'"],
            ...     item_class=NamedPitch,
            ...     )
            >>> show(named_pitch_segment) # doctest: +SKIP

        Returns LilyPond file.
        '''
        from abjad.tools import durationtools
        from abjad.tools import lilypondfiletools
        from abjad.tools import pitchtools
        from abjad.tools import scoretools
        from abjad.tools.topleveltools import attach
        from abjad.tools.topleveltools import iterate
        from abjad.tools.topleveltools import override
        named_pitches = [pitchtools.NamedPitch(x) for x in self]
        notes = scoretools.make_notes(named_pitches, [1])
        score, treble_staff, bass_staff = \
            scoretools.make_piano_sketch_score_from_leaves(notes)
        for leaf in iterate(score).by_class(scoretools.Leaf):
            attach(durationtools.Multiplier(1, 8), leaf)
        override(score).rest.transparent = True
        lilypond_file = lilypondfiletools.make_basic_lilypond_file(score)
        lilypond_file.header_block.tagline = False
        return lilypond_file

    ### PUBLIC METHODS ###

    @classmethod
    def from_selection(
        class_,
        selection,
        item_class=None,
        ):
        r'''Makes pitch segment from `selection`.

        ::

            >>> staff_1 = Staff("c'4 <d' fs' a'>4 b2")
            >>> staff_2 = Staff("c4. r8 g2")
            >>> selection = select((staff_1, staff_2))
            >>> pitch_segment = pitchtools.PitchSegment.from_selection(
            ...     selection)
            >>> pitch_segment
            PitchSegment(["c'", "d'", "fs'", "a'", 'b', 'c', 'g'])

        ::

            >>> show(pitch_segment) # doctest: +SKIP

        Returns pitch segment.
        '''
        from abjad.tools import scoretools
        from abjad.tools import selectiontools
        if not isinstance(selection, selectiontools.Selection):
            selection = select(selection)
        named_pitches = []
        for component in iterate(selection).by_class(
            (scoretools.Note, scoretools.Chord)):
            if hasattr(component, 'written_pitches'):
                named_pitches.extend(component.written_pitches)
            elif hasattr(component, 'written_pitch'):
                named_pitches.append(component.written_pitch)
        return class_(
            items=named_pitches,
            item_class=item_class,
            )

    def invert(self, axis=None):
        r'''Inverts pitch segment about `axis`.

        Returns new pitch segment.
        '''
        items = (pitch.invert(axis) for pitch in self)
        return new(self, items=items)

    def is_equivalent_under_transposition(self, expr):
        r'''True if pitch segment is equivalent to `expr` under transposition.
        Otherwise false.

        Returns true or false.
        '''
        from abjad.tools import pitchtools
        if not isinstance(expr, type(self)):
            return False
        if not len(self) == len(expr):
            return False
        difference = -(pitchtools.NamedPitch(expr[0], 4) -
            pitchtools.NamedPitch(self[0], 4))
        new_pitches = (x + difference for x in self)
        new_pitches = new(self, items=new_pitches)
        return expr == new_pitches

    def make_notes(self, n=None, written_duration=None):
        r'''Makes first `n` notes in pitch segment.

        Set `n` equal to `n` or length of segment.

        Set `written_duration` equal to `written_duration` or ``1/8``:

        ::

            >>> notes = named_pitch_segment.make_notes()
            >>> staff = Staff(notes)
            >>> show(staff) # doctest: +SKIP

        ..  doctest::

            >>> f(staff)
            \new Staff {
                bf,8
                aqs8
                fs'8
                g'8
                bqf8
                g'8
            }

        Allows nonassignable `written_duration`:

        ::

            >>> notes = named_pitch_segment.make_notes(4, Duration(5, 16))
            >>> staff = Staff(notes)
            >>> time_signature = TimeSignature((5, 4))
            >>> attach(time_signature, staff)
            >>> show(staff) # doctest: +SKIP

        ..  doctest::

            >>> f(staff)
            \new Staff {
                \time 5/4
                bf,4 ~
                bf,16
                aqs4 ~
                aqs16
                fs'4 ~
                fs'16
                g'4 ~
                g'16
            }

        Returns list of notes.
        '''
        from abjad.tools import durationtools
        from abjad.tools import scoretools
        n = n or len(self)
        written_duration = written_duration or durationtools.Duration(1, 8)
        result = scoretools.make_notes([0] * n, [written_duration])
        for i, logical_tie in enumerate(iterate(result).by_logical_tie()):
            pitch = self[i % len(self)]
            for note in logical_tie:
                note.written_pitch = pitch
        return result

    def multiply(self, index):
        r'''Multiplies pitch segment.

        ::

            >>> result = named_pitch_segment.multiply(3)
            >>> result
            PitchSegment(['fs,', 'eqs', "fs'", "a'", 'gqs', "a'"])

        ::

            >>> show(result) # doctest: +SKIP

        Returns new pitch segment.
        '''
        items = (x.multiply(index) for x in self)
        return new(self, items=items)

    def retrograde(self):
        r'''Retrograde of pitch segment.

        ::

            >>> result = named_pitch_segment.retrograde()
            >>> result
            PitchSegment(["g'", 'bqf', "g'", "fs'", 'aqs', 'bf,'])

        ::

            >>> show(result) # doctest: +SKIP

        Returns new pitch segment.
        '''
        return new(self, items=reversed(self))

    def rotate(self, n, transpose=False):
        r'''Rotates pitch segment.

        ::

            >>> result = numbered_pitch_segment.rotate(1)
            >>> result
            PitchSegment([7, -2, -1.5, 6, 7, -1.5])

        ::

            >>> show(result) # doctest: +SKIP

        ::

            >>> result = named_pitch_segment.rotate(-2)
            >>> result
            PitchSegment(["fs'", "g'", 'bqf', "g'", 'bf,', 'aqs'])

        ::

            >>> show(result) # doctest: +SKIP

        ::

            >>> pitch_segment = pitchtools.PitchSegment("c' d' e' f'")
            >>> result = pitch_segment.rotate(-1, transpose=True)
            >>> result
            PitchSegment(["c'", "d'", "ef'", 'bf'])

        ::

            >>> show(result) # doctest: +SKIP

        Returns new pitch segment.
        '''
        from abjad.tools import sequencetools
        rotated_pitches = sequencetools.rotate_sequence(
            self._collection, n)
        new_segment = new(self, items=rotated_pitches)
        if transpose:
            if self[0] != new_segment[0]:
                interval = new_segment[0] - self[0]
                new_segment = new_segment.transpose(interval)
        return new_segment

    def transpose(self, expr):
        r'''Transposes pitch segment by `expr`.

        Returns new pitch segment.
        '''
        items = (pitch.transpose(expr) for pitch in self)
        return new(self, items=items)

    ### PRIVATE PROPERTIES ###

    @property
    def _named_item_class(self):
        from abjad.tools import pitchtools
        return pitchtools.NamedPitch

    @property
    def _numbered_item_class(self):
        from abjad.tools import pitchtools
        return pitchtools.NumberedPitch

    @property
    def _parent_item_class(self):
        from abjad.tools import pitchtools
        return pitchtools.Pitch

    ### PUBLIC PROPERTIES ###

    @property
    def has_duplicates(self):
        r'''True if pitch segment has duplicate items. Otherwise false.

        ::

            >>> pitch_class_segment = pitchtools.PitchSegment(
            ...     items=[-2, -1.5, 6, 7, -1.5, 7],
            ...     )
            >>> pitch_class_segment.has_duplicates
            True

        ::

            >>> pitch_class_segment = pitchtools.PitchSegment(
            ...     items="c d e f g a b",
            ...     )
            >>> pitch_class_segment.has_duplicates
            False

        Returns true or false.
        '''
        from abjad.tools import pitchtools
        return len(pitchtools.PitchSet(self)) < len(self)

    @property
    def hertz(self):
        r'''Gets hertz of pitches in pitch segment.

        ::

            >>> pitch_segment = pitchtools.PitchSegment('c e g b')
            >>> pitch_segment.hertz
            (130.81..., 164.81..., 195.99..., 246.94...)

        Returns tuple.
        '''
        return tuple(_.hertz for _ in self)

    @property
    def inflection_point_count(self):
        r'''Inflection point count of pitch segment.

        Returns nonnegative integer.
        '''
        return len(self.local_minima) + len(self.local_maxima)

    @property
    def local_maxima(self):
        r'''Local maxima of pitch segment.

        Returns tuple.
        '''
        result = []
        if 3 <= len(self):
            for i in range(1, len(self) - 1):
                left, middle, right = self[i - 1], self[i], self[i + 1]
                if left < middle and right < middle:
                    result.append(middle)
        return tuple(result)

    @property
    def local_minima(self):
        r'''Local minima of pitch segment.

        Returns tuple.
        '''
        result = []
        if 3 <= len(self):
            for i in range(1, len(self) - 1):
                left, middle, right = self[i - 1], self[i], self[i + 1]
                if middle < left and middle < right:
                    result.append(middle)
        return tuple(result)
