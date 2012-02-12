from abjad.tools.pitchtools.NumberedChromaticPitchClassSegment import NumberedChromaticPitchClassSegment


class TwelveToneRow(NumberedChromaticPitchClassSegment):
    '''.. versionadded:: 2.0

    Abjad model of twelve-tone row::

        abjad> pitchtools.TwelveToneRow([0, 1, 11, 9, 3, 6, 7, 5, 4, 10, 2, 8])
        TwelveToneRow([0, 1, 11, 9, 3, 6, 7, 5, 4, 10, 2, 8])

    Twelve-tone rows validate pitch-classes at initialization.

    Twelve-tone rows inherit canonical operators from numbered chromatic pitch-class segment.

    Twelve-tone rows return numbered chromatic pitch-class segments on calls to getslice.

    Twelve-tone rows are immutable.
    '''

    def __new__(klass, pitch_classes):
        from abjad.tools import pitchtools
        from abjad.tools.pitchtools.TwelveToneRow._validate_pitch_classes import _validate_pitch_classes
        pitch_classes = [pitchtools.NumberedChromaticPitchClass(pc) for pc in pitch_classes]
        _validate_pitch_classes(pitch_classes)
        return pitchtools.NumberedChromaticPitchClassSegment.__new__(klass, pitch_classes)

    ### OVERLOADS ###

    def __copy__(self):
        return type(self)(self)

    def __eq__(self, arg):
        if isinstance(arg, type(self)):
            return tuple(self) == tuple(arg)
        return False

    def __getslice__(self, start, stop):
        return NumberedChromaticPitchClassSegment(tuple.__getslice__(self, start, stop))

    def __mul__(self, n):
        return NumberedChromaticPitchClassSegment(tuple.__mul__(self, n))

    def __ne__(self, arg):
        return not self == arg

    def __rmul__(self, n):
        return NumberedChromaticPitchClassSegment(tuple.__rmul__(self, n))

    ### PRIVATE ATTRIBUTES ###

    @property
    def _contents_string(self):
        return ', '.join([str(abs(pc)) for pc in self])
