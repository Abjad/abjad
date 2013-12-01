# -*- encoding: utf-8 -*-
from abjad.tools.pitchtools.PitchClassSegment import PitchClassSegment


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

    def __init__(self, tokens=None, custom_identifier=None):
        from abjad.tools import pitchtools
        assert tokens is not None
        PitchClassSegment.__init__(
            self,
            tokens=tokens,
            item_class=pitchtools.NumberedPitchClass,
            custom_identifier=custom_identifier,
            )
        self._validate_pitch_classes(self)

    ### SPECIAL METHODS ###

    def __getslice__(self, start, stop):
        r'''Gets items from `start` to `stop` in twelve-tone row.

        Returns pitch-class segment.
        '''
        from abjad.tools import pitchtools
        tokens = self._collection[start:stop]
        return PitchClassSegment(
            tokens=tokens,
            item_class=pitchtools.NumberedPitchClass,
            custom_identifier=self.custom_identifier,
            )

    def __makenew__(self, tokens=None, custom_identifier=None):
        r'''Makes new twelve-tone row with optional `tokens` and
        `custom_identifier`.

        Returns new twelve-tone row.
        '''
        from abjad.tools import pitchtools
        # allow for empty iterables:
        if tokens is None:
            tokens = self._collection
        custom_identifier = custom_identifier or self.custom_identifier
        return type(self)(
            tokens=tokens,
            custom_identifier=custom_identifier,
            )

    def __mul__(self, expr):
        r'''Multiplies twelve-tone row by `expr`.

        Returns pitch-class segment.
        '''
        return PitchClassSegment(self) * expr

    def __rmul__(self, expr):
        r'''Multiplies `expr` by twelve-tone row.

        Returns pitch-class segment.
        '''
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
            message = 'must contain all twelve pitch-classes: {!r}.'
            message = message.format(pitch_classes)
            raise ValueError(message)

    ### PUBLIC METHODS ###d

    @classmethod
    def from_selection(
        cls, 
        selection, 
        item_class=None, 
        custom_identifier=None,
        ):
        r'''Makes twelve-tone row from `selection`.

        Returns twelve-tone row.
        '''
        raise NotImplementedError
