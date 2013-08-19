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

    ### INITIALIZER ###

    def __init__(self, tokens=None, name=None):
        from abjad.tools import pitchtools
        assert tokens is not None
        NumberedPitchClassSegment.__init__(
            self,
            tokens=tokens,
            name=name,
            )
        self._validate_pitch_classes(self)

    ### SPECIAL METHODS ###

    def __getslice__(self, start, stop):
        tokens = self._collection[start:stop]
        return NumberedPitchClassSegment(
            tokens=tokens,
            name=self.name,
            )

    def __mul__(self, expr):
        return NumberedPitchClassSegment(self) * expr

    def __rmul__(self, expr):
        return NumberedPitchClassSegment(self) * expr

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
