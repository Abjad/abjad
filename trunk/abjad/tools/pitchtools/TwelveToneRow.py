# -*- encoding: utf-8 -*-
from abjad.tools.pitchtools.PitchClassSegment \
    import PitchClassSegment


class TwelveToneRow(PitchClassSegment):
    '''A twelve-tone row.

    ::

        >>> pitchtools.TwelveToneRow([0, 1, 11, 9, 3, 6, 7, 5, 4, 10, 2, 8])
        TwelveToneRow([0, 1, 11, 9, 3, 6, 7, 5, 4, 10, 2, 8])

    Twelve-tone rows validate pitch-classes at initialization.

    Twelve-tone rows inherit canonical operators from numbered
    pitch-class segment.

    Twelve-tone rows return numbered pitch-class segments
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
        PitchClassSegment.__init__(
            self,
            tokens=tokens,
            item_class=pitchtools.NumberedPitchClass,
            name=name,
            )
        self._validate_pitch_classes(self)

    ### SPECIAL METHODS ###

    def __getslice__(self, start, stop):
        from abjad.tools import pitchtools
        tokens = self._collection[start:stop]
        return PitchClassSegment(
            tokens=tokens,
            item_class=pitchtools.NumberedPitchClass,
            name=self.name,
            )

    def __mul__(self, expr):
        return PitchClassSegment(self) * expr

    def __rmul__(self, expr):
        return PitchClassSegment(self) * expr

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

    ### PUBLIC METHODS ###d

    @classmethod
    def from_selection(cls, selection, item_class=None, name=None):
        raise NotImplementedError

    def new(self, tokens=None, name=None):
        from abjad.tools import pitchtools
        # Allow for empty iterables:
        if tokens is None:
            tokens = self._collection
        name = name or self.name
        return type(self)(
            tokens=tokens,
            name=name,
            )
