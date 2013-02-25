from abjad.tools.pitchtools.PitchClassObjectSegment import PitchClassObjectSegment
import copy


class NumberedChromaticPitchClassSegment(PitchClassObjectSegment):
    '''.. versionadded:: 2.0

    Abjad model of a numbered chromatic pitch-class segment::

        >>> pitchtools.NumberedChromaticPitchClassSegment([-2, -1.5, 6, 7, -1.5, 7])
        NumberedChromaticPitchClassSegment([10, 10.5, 6, 7, 10.5, 7])

    Numbered chromatic pitch-class segments are immutable.
    '''

    ### CLASS ATTRIBUTES ###

    __slots__ = ()

    _default_positional_input_arguments = ([-2, -1.5, 6, 7, -1.5, 7], )

    ### INITIALIZER ###

    def __new__(self, pitch_class_tokens):
        from abjad.tools import pitchtools
        pitch_classes = [pitchtools.NumberedChromaticPitchClass(x) for x in pitch_class_tokens]
        return tuple.__new__(self, pitch_classes)

    ### SPECIAL METHODS ###

    def __repr__(self):
        return '%s([%s])' % (type(self).__name__, self._repr_string)

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
        '''Read-only inversion-equivalent chromatic interval-class segment::

            >>> segment = pitchtools.NumberedChromaticPitchClassSegment([10, 10.5, 6, 7, 10.5, 7])

        ::

            >>> segment.inversion_equivalent_chromatic_interval_class_segment
            InversionEquivalentChromaticIntervalClassSegment(0.5, 4.5, 1, 3.5, 3.5)

        Return inversion-equivalent chromatic interval-class segment.
        '''
        from abjad.tools import mathtools
        from abjad.tools import pitchtools
        interval_classes = list(mathtools.difference_series(self))
        return pitchtools.InversionEquivalentChromaticIntervalClassSegment(interval_classes)

    @property
    def numbered_chromatic_pitch_class_set(self):
        '''Read-only numbered chromatic pitch-class set from numbered chromatic
        pitch-class segment::

            >>> segment.numbered_chromatic_pitch_class_set
            NumberedChromaticPitchClassSet([6, 7, 10, 10.5])

        Return numbered chromatic pitch-class set.
        '''
        from abjad.tools import pitchtools
        return pitchtools.NumberedChromaticPitchClassSet(self)

    ### PUBLIC METHODS ###

    def alpha(self):
        '''Morris alpha transform of numbered chromatic pitch-class segment::

            >>> segment.alpha()
            NumberedChromaticPitchClassSegment([11, 11.5, 7, 6, 11.5, 6])

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
        '''Invert numbered chromatic pitch-class segment::

            >>> segment.invert()
            NumberedChromaticPitchClassSegment([2, 1.5, 6, 5, 1.5, 5])

        Return numbered chromatic pitch-class segment.
        '''
        return type(self)([pc.invert() for pc in self])

    def multiply(self, n):
        '''Multiply numbered chromatic pitch-class segment by `n`::

            >>> segment.multiply(5)
            NumberedChromaticPitchClassSegment([2, 4.5, 6, 11, 4.5, 11])

        Return numbered chromatic pitch-class segment.
        '''
        return type(self)([pc.multiply(n) for pc in self])

    def retrograde(self):
        '''Retrograde of numbered chromatic pitch-class segment::

            >>> segment.retrograde()
            NumberedChromaticPitchClassSegment([7, 10.5, 7, 6, 10.5, 10])

        Return numbered chromatic pitch-class segment.
        '''
        return type(self)(reversed(self))

    def rotate(self, n):
        '''Rotate numbered chromatic pitch-class segment::

            >>> segment.rotate(1)
            NumberedChromaticPitchClassSegment([7, 10, 10.5, 6, 7, 10.5])

        Return numbered chromatic pitch-class segment.
        '''
        from abjad.tools import sequencetools
        pitch_classes = sequencetools.rotate_sequence(tuple(self), n)
        return type(self)(pitch_classes)

    def transpose(self, n):
        '''Transpose numbered chromatic pitch-class segment::

            >>> segment.transpose(10)
            NumberedChromaticPitchClassSegment([8, 8.5, 4, 5, 8.5, 5])

        Return numbered chromatic pitch-class segment.
        '''
        return type(self)([pc.transpose(n) for pc in self])
