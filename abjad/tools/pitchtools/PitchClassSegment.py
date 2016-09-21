# -*- coding: utf-8 -*-
from abjad.tools import durationtools
from abjad.tools.pitchtools.Segment import Segment
from abjad.tools.topleveltools import iterate
from abjad.tools.topleveltools import new


class PitchClassSegment(Segment):
    r'''Pitch-class segment.

    ..  container:: example

        **Example 1.** Numbered pitch-class segment:

        ::

            >>> pitch_class_segment = pitchtools.PitchClassSegment(
            ...     items=[-2, -1.5, 6, 7, -1.5, 7],
            ...     item_class=pitchtools.NumberedPitchClass,
            ...     )
            >>> show(pitch_class_segment) # doctest: +SKIP

        ..  doctest::

            >>> lilypond_file = pitch_class_segment.__illustrate__()
            >>> voice = lilypond_file.score_block.items[0][0][0]
            >>> f(voice)
            \new Voice {
                bf'8
                bqf'8
                fs'8
                g'8
                bqf'8
                g'8
                \bar "|."
                \override Score.BarLine.transparent = ##f
            }

    ..  container:: example

        **Example 2.** Named pitch-class segment:

        ::

            >>> pitch_class_segment = pitchtools.PitchClassSegment(
            ...     items=['c', 'ef', 'bqs,', 'd'],
            ...     item_class=pitchtools.NamedPitchClass,
            ...     )
            >>> show(pitch_class_segment) # doctest: +SKIP

        ..  doctest::

            >>> lilypond_file = pitch_class_segment.__illustrate__()
            >>> voice = lilypond_file.score_block.items[0][0][0]
            >>> f(voice)
            \new Voice {
                c'8
                ef'8
                bqs'8
                d'8
                \bar "|."
                \override Score.BarLine.transparent = ##f
            }

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

    def __illustrate__(self, **kwargs):
        r'''Illustrates pitch-class segment.

        ..  container:: example

            **Example 1.** Numbered pitch-class segment:

            ::

                >>> pitch_class_segment = pitchtools.PitchClassSegment(
                ...     items=[-2, -1.5, 6, 7, -1.5, 7],
                ...     item_class=pitchtools.NumberedPitchClass,
                ...     )
                >>> show(pitch_class_segment) # doctest: +SKIP

            ..  doctest::

                >>> lilypond_file = pitch_class_segment.__illustrate__()
                >>> voice = lilypond_file.score_block.items[0][0][0]
                >>> f(voice)
                \new Voice {
                    bf'8
                    bqf'8
                    fs'8
                    g'8
                    bqf'8
                    g'8
                    \bar "|."
                    \override Score.BarLine.transparent = ##f
                }

        Returns LilyPond file.
        '''
        return Segment.__illustrate__(self, **kwargs)

    ### PUBLIC METHODS ###

    def alpha(self):
        r'''Morris alpha transform of pitch-class segment:

        ::

            >>> pitch_class_segment = pitchtools.PitchClassSegment(
            ...     items=[-2, -1.5, 6, 7, -1.5, 7],
            ...     )
            >>> pitch_class_segment.alpha()
            PitchClassSegment([11, 11.5, 7, 6, 11.5, 6])

        Returns new pitch-class segment.
        '''
        from abjad.tools import mathtools
        numbers = []
        for pc in self:
            pc = abs(float(pc))
            is_integer = True
            if not mathtools.is_integer_equivalent_number(pc):
                is_integer = False
                fraction_part = pc - int(pc)
                pc = int(pc)
            if abs(pc) % 2 == 0:
                number = (abs(pc) + 1) % 12
            else:
                number = abs(pc) - 1
            if not is_integer:
                number += fraction_part
            else:
                number = int(number)
            numbers.append(number)
        return new(self, items=numbers)

    @classmethod
    def from_selection(class_, selection, item_class=None):
        r'''Initialize pitch-class segment from component selection:

        ::

            >>> staff_1 = Staff("c'4 <d' fs' a'>4 b2")
            >>> staff_2 = Staff("c4. r8 g2")
            >>> selection = select((staff_1, staff_2))
            >>> pitchtools.PitchClassSegment.from_selection(selection)
            PitchClassSegment(['c', 'd', 'fs', 'a', 'b', 'c', 'g'])

        Returns pitch-class segment.
        '''
        from abjad.tools import pitchtools
        pitch_segment = pitchtools.PitchSegment.from_selection(selection)
        return class_(
            items=pitch_segment,
            item_class=item_class,
            )

    def invert(self, axis=None):
        r'''Inverts pitch-class segment:

        ::

            >>> pitch_class_segment = pitchtools.PitchClassSegment(
            ...     items=[-2, -1.5, 6, 7, -1.5, 7],
            ...     )
            >>> pitch_class_segment.invert()
            PitchClassSegment([2, 1.5, 6, 5, 1.5, 5])

        Returns new pitch-class segment.
        '''
        items = (pc.invert(axis=axis) for pc in self)
        return new(self, items=items)

    def is_equivalent_under_transposition(self, expr):
        r'''True if equivalent under transposition to `expr`. Otherwise False.

        Returns true or false.
        '''
        from abjad.tools import pitchtools
        if not isinstance(expr, type(self)):
            return False
        if not len(self) == len(expr):
            return False
        difference = -(pitchtools.NamedPitch(expr[0], 4) -
            pitchtools.NamedPitch(self[0], 4))
        new_pitch_classes = (x + difference for x in self)
        new_pitch_classes = new(self, items=new_pitch_classes)
        return expr == new_pitch_classes

    def make_notes(self, n=None, written_duration=None):
        r'''Make first `n` notes in pitch class segment.

        Set `n` equal to `n` or length of segment.

        Set `written_duration` equal to `written_duration` or ``1/8``:

        ::

            >>> pitch_class_segment = pitchtools.PitchClassSegment(
            ...     [2, 4.5, 6, 11, 4.5, 10])

        ::

            >>> notes = pitch_class_segment.make_notes()
            >>> staff = Staff(notes)
            >>> show(staff) # doctest: +SKIP

        ..  doctest::

            >>> f(staff)
            \new Staff {
                d'8
                eqs'8
                fs'8
                b'8
                eqs'8
                bf'8
            }

        Allow nonassignable `written_duration`:

        ::

            >>> notes = pitch_class_segment.make_notes(4, Duration(5, 16))
            >>> staff = Staff(notes)
            >>> time_signature = TimeSignature((5, 4))
            >>> attach(time_signature, staff)
            >>> show(staff) # doctest: +SKIP

        ..  doctest::

            >>> f(staff)
            \new Staff {
                \time 5/4
                d'4 ~
                d'16
                eqs'4 ~
                eqs'16
                fs'4 ~
                fs'16
                b'4 ~
                b'16
            }

        Returns list of notes.
        '''
        from abjad.tools import scoretools
        from abjad.tools import pitchtools
        n = n or len(self)
        written_duration = written_duration or durationtools.Duration(1, 8)
        result = scoretools.make_notes([0] * n, [written_duration])
        for i, logical_tie in enumerate(iterate(result).by_logical_tie()):
            pitch_class = pitchtools.NamedPitchClass(self[i % len(self)])
            pitch = pitchtools.NamedPitch(pitch_class, 4)
            for note in logical_tie:
                note.written_pitch = pitch
        return result

    def multiply(self, n):
        r'''Multiply pitch-class segment by `n`:

        ::

            >>> pitch_class_segment = pitchtools.PitchClassSegment(
            ...     items=[-2, -1.5, 6, 7, -1.5, 7],
            ...     )
            >>> pitch_class_segment.multiply(5)
            PitchClassSegment([2, 4.5, 6, 11, 4.5, 11])

        Returns new pitch-class segment.
        '''
        from abjad.tools import pitchtools
        items = (pitchtools.NumberedPitchClass(pc).multiply(n)
            for pc in self)
        return new(self, items=items)

    def retrograde(self):
        r'''Retrograde of pitch-class segment:

        ::

            >>> pitchtools.PitchClassSegment(
            ...     items=[-2, -1.5, 6, 7, -1.5, 7],
            ...     ).retrograde()
            PitchClassSegment([7, 10.5, 7, 6, 10.5, 10])

        Returns new pitch-class segment.
        '''
        return new(self, items=reversed(self))

    def rotate(self, n, transpose=False):
        r'''Rotate pitch-class segment:

        ::

            >>> pitchtools.PitchClassSegment(
            ...     items=[-2, -1.5, 6, 7, -1.5, 7],
            ...     ).rotate(1)
            PitchClassSegment([7, 10, 10.5, 6, 7, 10.5])

        ::

            >>> pitchtools.PitchClassSegment(
            ...     items=['c', 'ef', 'bqs,', 'd'],
            ...     ).rotate(-2)
            PitchClassSegment(['bqs', 'd', 'c', 'ef'])

        If `transpose` is true, transpose the rotated segment to begin at the
        same pitch class as this segment:

        ::

            >>> pitchtools.PitchClassSegment(
            ...     items=['c', 'b', 'd']
            ...     ).rotate(1, transpose=True)
            PitchClassSegment(['c', 'bf', 'a'])

        Returns new pitch-class segment.
        '''
        from abjad.tools import sequencetools
        items = sequencetools.rotate_sequence(self._collection, n)
        new_segment = new(self, items=items)
        if transpose:
            interval_of_transposition = float(self[0]) - float(new_segment[0])
            new_segment = new_segment.transpose(interval_of_transposition)
        return new_segment

    def transpose(self, expr):
        r'''Transpose pitch-class segment:

        ::

            >>> pitchtools.PitchClassSegment(
            ...     items=[-2, -1.5, 6, 7, -1.5, 7],
            ...     ).transpose(10)
            PitchClassSegment([8, 8.5, 4, 5, 8.5, 5])

        Returns new pitch-class segment.
        '''
        items = (pitch_class.transpose(expr) for pitch_class in self)
        return new(self, items=items)

    def voice_horizontally(self, initial_octave=4):
        r'''Voices pitch-class segment as pitch segment, with each pitch as
        close in distance to the previous pitch as possible.

        ::

            >>> pitch_classes = pitchtools.PitchClassSegment(
            ...     "c b d e f g e b a c")
            >>> pitch_segment = pitch_classes.voice_horizontally()
            >>> show(pitch_segment) # doctest: +SKIP

        Returns pitch segment.
        '''
        from abjad.tools import pitchtools
        initial_octave = pitchtools.Octave(initial_octave)
        pitches = []
        if self:
            pitch_class = pitchtools.NamedPitchClass(self[0])
            pitch = pitchtools.NamedPitch(pitch_class, initial_octave)
            pitches.append(pitch)
            for pitch_class in self[1:]:
                pitch_class = pitchtools.NamedPitchClass(pitch_class)
                pitch = pitchtools.NamedPitch(pitch_class, initial_octave)
                semitones = abs((pitch - pitches[-1]).semitones)
                while 6 < semitones:
                    if pitch < pitches[-1]:
                        pitch += 12
                    else:
                        pitch -= 12
                    semitones = abs((pitch - pitches[-1]).semitones)
                pitches.append(pitch)
        if self.item_class is pitchtools.NamedPitchClass:
            item_class = pitchtools.NamedPitch
        else:
            item_class = pitchtools.NumberedPitch
        return pitchtools.PitchSegment(
            items=pitches,
            item_class=item_class,
            )

    def voice_vertically(self, initial_octave=4):
        r'''Voices pitch-class segment as pitch segment, with each pitch always
        higher than the previous.

        ::

            >>> scale_degree_numbers = [1, 3, 5, 7, 9, 11, 13]
            >>> scale = tonalanalysistools.Scale('c', 'minor')
            >>> pitch_classes = pitchtools.PitchClassSegment((
            ...     scale.scale_degree_to_named_pitch_class(x)
            ...     for x in scale_degree_numbers))
            >>> pitch_segment = pitch_classes.voice_vertically()
            >>> pitch_segment
            PitchSegment(["c'", "ef'", "g'", "bf'", "d''", "f''", "af''"])
            >>> show(pitch_segment) # doctest: +SKIP

        Returns pitch segment.
        '''
        from abjad.tools import pitchtools
        initial_octave = pitchtools.Octave(initial_octave)
        pitches = []
        if self:
            pitch_class = pitchtools.NamedPitchClass(self[0])
            pitch = pitchtools.NamedPitch(pitch_class, initial_octave)
            pitches.append(pitch)
            for pitch_class in self[1:]:
                pitch_class = pitchtools.NamedPitchClass(pitch_class)
                pitch = pitchtools.NamedPitch(pitch_class, initial_octave)
                while pitch < pitches[-1]:
                    pitch += 12
                pitches.append(pitch)
        if self.item_class is pitchtools.NamedPitchClass:
            item_class = pitchtools.NamedPitch
        else:
            item_class = pitchtools.NumberedPitch
        return pitchtools.PitchSegment(
            items=pitches,
            item_class=item_class,
            )

    ### PRIVATE PROPERTIES ###

    @property
    def _named_item_class(self):
        from abjad.tools import pitchtools
        return pitchtools.NamedPitchClass

    @property
    def _numbered_item_class(self):
        from abjad.tools import pitchtools
        return pitchtools.NumberedPitchClass

    @property
    def _parent_item_class(self):
        from abjad.tools import pitchtools
        return pitchtools.PitchClass

    ### PUBLIC PROPERTIES ###

    @property
    def has_duplicates(self):
        r'''True if segment contains duplicate items:

        ::

            >>> pitch_class_segment = pitchtools.PitchClassSegment(
            ...     items=[-2, -1.5, 6, 7, -1.5, 7],
            ...     )
            >>> pitch_class_segment.has_duplicates
            True

        ::

            >>> pitch_class_segment = pitchtools.PitchClassSegment(
            ...     items="c d e f g a b",
            ...     )
            >>> pitch_class_segment.has_duplicates
            False

        Returns true or false.
        '''
        from abjad.tools import pitchtools
        return len(pitchtools.PitchClassSet(self)) < len(self)
