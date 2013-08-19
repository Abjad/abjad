# -*- encoding: utf-8 -*-
from abjad.tools.pitchtools.NumberedPitchClassSegment \
    import NumberedPitchClassSegment


class TwelveToneRow(NumberedPitchClassSegment):
    '''Abjad model of twelve-tone row:

    ::

        >>> pitchtools.TwelveToneRow([0, 1, 11, 9, 3, 6, 7, 5, 4, 10, 2, 8])
        TwelveToneRow([0, 1, 11, 9, 3, 6, 7, 5, 4, 10, 2, 8])

    Twelve-tone rows validate pitch-classes at initialization.

    Twelve-tone rows inherit canonical operators from numbered 
    chromatic pitch-class segment.

    Twelve-tone rows return numbered chromatic pitch-class segments 
    on calls to getslice.

    Twelve-tone rows are immutable.
    '''

    ### CLASS VARIABLES ###

    _default_positional_input_arguments = (
        [0, 1, 11, 9, 3, 6, 7, 5, 4, 10, 2, 8],
        )

    ### CONSTRUCTOR ###

    def __new__(cls, pitch_classes):
        from abjad.tools import pitchtools
        pitch_classes = [
            pitchtools.NumberedPitchClass(pc) 
            for pc in pitch_classes]
        self = pitchtools.NumberedPitchClassSegment.__new__(
            cls, pitch_classes)
        self._validate_pitch_classes(pitch_classes)
        return self

    ### SPECIAL METHODS ###

    def __copy__(self):
        return type(self)(self)

    def __eq__(self, arg):
        if isinstance(arg, type(self)):
            return tuple(self) == tuple(arg)
        return False

    def __getslice__(self, start, stop):
        return NumberedPitchClassSegment(
            tuple.__getslice__(self, start, stop))

    def __mul__(self, n):
        return NumberedPitchClassSegment(tuple.__mul__(self, n))

    def __ne__(self, arg):
        return not self == arg

    def __rmul__(self, n):
        return NumberedPitchClassSegment(tuple.__rmul__(self, n))

    ### PRIVATE PROPERTIES ###

    @property
    def _contents_string(self):
        return ', '.join([str(abs(pc)) for pc in self])

    ### PRIVATE METHODS ###

    @staticmethod
    def _validate_pitch_classes(pitch_classes):
        numbers = [abs(pc) for pc in pitch_classes]
        numbers.sort()
        if not numbers == range(12):
            raise ValueError('must contain all twelve pitch-classes.')
