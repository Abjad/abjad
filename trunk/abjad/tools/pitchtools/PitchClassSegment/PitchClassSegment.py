# -*- encoding: utf-8 -*-
import abc
from abjad.tools import durationtools
from abjad.tools.datastructuretools.TypedTuple import TypedTuple


class PitchClassSegment(TypedTuple):
    '''Pitch-class segment base class:

    ::

        >>> numbered_pitch_class_segment = pitchtools.PitchClassSegment(
        ...     tokens=[-2, -1.5, 6, 7, -1.5, 7],
        ...     item_class=pitchtools.NumberedPitchClass,
        ...     )
        >>> numbered_pitch_class_segment
        PitchClassSegment([10, 10.5, 6, 7, 10.5, 7])

    ::

        >>> named_pitch_class_segment = pitchtools.PitchClassSegment(
        ...     tokens=['c', 'ef', 'bqs,', 'd'],
        ...     item_class=pitchtools.NamedPitchClass,
        ...     )
        >>> named_pitch_class_segment
        PitchClassSegment(['c', 'ef', 'bqs', 'd'])

    Return pitch-class segment.
    '''

    ### CLASS VARIABLES ###

    _default_positional_input_arguments = (
        [-2, -1.5, 6, 7, -1.5, 7],
        )

    __slots__ = ()

    ### INITIALIZER ###

    def __init__(self, tokens=None, item_class=None, name=None):
        from abjad.tools import pitchtools
        assert item_class in (
            None,
            pitchtools.NamedPitchClass,
            pitchtools.NumberedPitchClass,
            )
        if item_class is None:
            item_class = pitchtools.NumberedPitchClass
        TypedTuple.__init__(
            self,
            tokens=tokens,
            item_class=item_class,
            )

    ### SPECIAL METHODS ###

    def __repr__(self):
        return '{}([{}])'.format(self._class_name, self._repr_string)

    def __str__(self):
        return '<{}>'.format(self._format_string)

    ### PRIVATE PROPERTIES ###

    @property
    def _format_string(self):
        from abjad.tools import pitchtools
        parts = []
        if self.item_class is pitchtools.NamedPitchClass:
            parts = [repr(str(x)) for x in self]
        else:
            parts = [str(x) for x in self]
        return ', '.join(parts)

    @property
    def _repr_string(self):
        return self._format_string

    ### PUBLIC METHODS ###

    def alpha(self):
        r'''Morris alpha transform of pitch-class segment:

        ::

            >>> numbered_pitch_class_segment.alpha()
            PitchClassSegment([11, 11.5, 7, 6, 11.5, 6])

        Emit new pitch-class segment.
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
        return self.new(tokens=numbers)

    def invert(self):
        r'''Invert pitch-class segment:

        ::

            >>> numbered_pitch_class_segment.invert()
            PitchClassSegment([2, 1.5, 6, 5, 1.5, 5])

        Emit new pitch-class segment.
        '''
        tokens = (pc.invert() for pc in self)
        return self.new(tokens=tokens)

    def is_equivalent_under_transposition(self, expr):
        r'''True if equivalent under transposition to `expr`, otherwise False.
        
        Return boolean.
        '''
        from abjad.tools import pitchtools
        if not isinstance(expr, type(self)):
            return False
        if not len(self) == len(expr):
            return False
        difference = -(pitchtools.NamedPitch(expr[0], 4) -
            pitchtools.NamedPitch(self[0], 4))
        new_pitch_classes = (x + difference for x in self)
        new_pitch_classes = self.new(tokens=new_pitch_classes)
        return arg == new_pitch_classes

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
            >>> time_signature = contexttools.TimeSignatureMark((5, 4))(staff)
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

        Return list of notes.
        '''
        from abjad.tools import iterationtools
        from abjad.tools import notetools
        from abjad.tools import pitchtools
        n = n or len(self)
        written_duration = written_duration or durationtools.Duration(1, 8)
        result = notetools.make_notes([0] * n, [written_duration])
        for i, tie_chain in enumerate(
            iterationtools.iterate_tie_chains_in_expr(result)):
            pitch_class = pitchtools.NamedPitchClass(self[i % len(self)])
            pitch = pitchtools.NamedPitch(pitch_class, 4)
            for note in tie_chain:
                note.written_pitch = pitch
        return result

    def multiply(self, n):
        r'''Multiply pitch-class segment by `n`:

        ::

            >>> numbered_pitch_class_segment.multiply(5)
            PitchClassSegment([2, 4.5, 6, 11, 4.5, 11])

        Emit new pitch-class segment.
        '''
        from abjad.tools import pitchtools
        tokens = (pitchtools.NumberedPitchClass(pc).multiply(n)
            for pc in self)
        return self.new(tokens=tokens)

    def retrograde(self):
        r'''Retrograde of pitch-class segment:

        ::

            >>> numbered_pitch_class_segment.retrograde()
            PitchClassSegment([7, 10.5, 7, 6, 10.5, 10])

        Emit new pitch-class segment.
        '''
        return self.new(tokens=reversed(self))

    def rotate(self, n):
        r'''Rotate pitch-class segment:

        ::

            >>> numbered_pitch_class_segment.rotate(1)
            PitchClassSegment([7, 10, 10.5, 6, 7, 10.5])

        ::

            >>> named_pitch_class_segment.rotate(-2)
            PitchClassSegment(['bqs', 'd', 'c', 'ef'])

        Emit new pitch-class segment.
        '''
        from abjad.tools import sequencetools
        tokens = sequencetools.rotate_sequence(self._collection, n)
        return self.new(tokens=tokens)

    def transpose(self, expr):
        r'''Transpose pitch-class segment:

        ::

            >>> numbered_pitch_class_segment.transpose(10)
            PitchClassSegment([8, 8.5, 4, 5, 8.5, 5])

        Emit new pitch-class segment.
        '''
        tokens = (pitch_class.transpose(expr) for pitch_class in self)
        return self.new(tokens=tokens)

