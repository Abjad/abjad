# -*- encoding: utf-8 -*-
from abjad.tools.pitchtools.PitchClassSegment import PitchClassSegment
import copy


class NumberedPitchClassSegment(PitchClassSegment):
    '''Abjad model of a numbered chromatic pitch-class segment:

    ::

        >>> segment = pitchtools.NumberedPitchClassSegment(
        ...     [-2, -1.5, 6, 7, -1.5, 7])
        >>> segment
        NumberedPitchClassSegment([10, 10.5, 6, 7, 10.5, 7])

    Numbered chromatic pitch-class segments are immutable.
    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        )

    _default_positional_input_arguments = (
        [-2, -1.5, 6, 7, -1.5, 7],
        )

    ### INITIALIZER ###

    def __new__(self, pitch_class_tokens):
        from abjad.tools import pitchtools
        pitch_classes = [pitchtools.NumberedPitchClass(x) 
            for x in pitch_class_tokens]
        return tuple.__new__(self, pitch_classes)

    ### SPECIAL METHODS ###

    def __repr__(self):
        return '%s([%s])' % (self._class_name, self._repr_string)

    def __str__(self):
        return '<%s>' % self._format_string

    ### PRIVATE PROPERTIES ###

    @property
    def _format_string(self):
        return ', '.join([str(x) for x in self])

    @property
    def _repr_string(self):
        return self._format_string

    ### PUBLIC PROPERTIES ###

    @property
    def inversion_equivalent_chromatic_interval_class_segment(self):
        r'''Inversion-equivalent chromatic interval-class segment:

        ::

            >>> segment.inversion_equivalent_chromatic_interval_class_segment
            InversionEquivalentChromaticIntervalClassSegment(0.5, 4.5, 1, 3.5, 3.5)

        Return inversion-equivalent chromatic interval-class segment.
        '''
        from abjad.tools import mathtools
        from abjad.tools import pitchtools
        interval_classes = list(mathtools.difference_series(self))
        return pitchtools.InversionEquivalentChromaticIntervalClassSegment(
            interval_classes)

    @property
    def numbered_chromatic_pitch_class_set(self):
        r'''Numbered chromatic pitch-class set from numbered 
        chromatic pitch-class segment:

        ::

            >>> segment.numbered_chromatic_pitch_class_set
            NumberedPitchClassSet([6, 7, 10, 10.5])

        Return numbered chromatic pitch-class set.
        '''
        from abjad.tools import pitchtools
        return pitchtools.NumberedPitchClassSet(self)

    ### PUBLIC METHODS ###

    def alpha(self):
        r'''Morris alpha transform of numbered chromatic pitch-class segment:

        ::

            >>> segment.alpha()
            NumberedPitchClassSegment([11, 11.5, 7, 6, 11.5, 6])

        Return numbered chromatic pitch-class segment.
        '''
        from abjad.tools import mathtools
        numbers = []
        for pc in self:
            pc = abs(pc)
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
            numbers.append(number)
        return type(self)(numbers)

    def invert(self):
        r'''Invert numbered chromatic pitch-class segment:

        ::

            >>> segment.invert()
            NumberedPitchClassSegment([2, 1.5, 6, 5, 1.5, 5])

        Return numbered chromatic pitch-class segment.
        '''
        return type(self)([pc.invert() for pc in self])

    def multiply(self, n):
        r'''Multiply numbered chromatic pitch-class segment by `n`:

        ::

            >>> segment.multiply(5)
            NumberedPitchClassSegment([2, 4.5, 6, 11, 4.5, 11])

        Return numbered chromatic pitch-class segment.
        '''
        return type(self)([pc.multiply(n) for pc in self])

    def retrograde(self):
        r'''Retrograde of numbered chromatic pitch-class segment:

        ::

            >>> segment.retrograde()
            NumberedPitchClassSegment([7, 10.5, 7, 6, 10.5, 10])

        Return numbered chromatic pitch-class segment.
        '''
        return type(self)(reversed(self))

    def rotate(self, n):
        r'''Rotate numbered chromatic pitch-class segment:

        ::

            >>> segment.rotate(1)
            NumberedPitchClassSegment([7, 10, 10.5, 6, 7, 10.5])

        Return numbered chromatic pitch-class segment.
        '''
        from abjad.tools import sequencetools
        pitch_classes = sequencetools.rotate_sequence(tuple(self), n)
        return type(self)(pitch_classes)

    def transpose(self, n):
        r'''Transpose numbered chromatic pitch-class segment:

        ::

            >>> segment.transpose(10)
            NumberedPitchClassSegment([8, 8.5, 4, 5, 8.5, 5])

        Return numbered chromatic pitch-class segment.
        '''
        return type(self)([pc.transpose(n) for pc in self])
