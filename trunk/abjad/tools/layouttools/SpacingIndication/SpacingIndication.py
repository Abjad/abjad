from abjad.core import _Immutable
from abjad.core import _StrictComparator
from abjad.tools import tempotools
from abjad.tools import durationtools


class SpacingIndication(_StrictComparator, _Immutable):
    '''Spacing indication token.

    LilyPond ``Score.proportionalNotationDuration``
    will equal ``proportional_notation_duration`` when tempo
    equals ``tempo_indication``. ::

        abjad> from abjad.tools import layouttools

    ::

        abjad> tempo = contexttools.TempoMark(Duration(1, 8), 44)
        abjad> spacing_indication = layouttools.SpacingIndication(tempo, Duration(1, 68))
        abjad> spacing_indication
        SpacingIndication(TempoMark(Duration(1, 8), 44), 1/68)

    Spacing indications are immutable.
    '''

    def __init__(self, tempo_indication, proportional_notation_duration):
        object.__setattr__(self, '_tempo_indication', tempo_indication)
        object.__setattr__(self, '_proportional_notation_duration', proportional_notation_duration)

    ### OVERLOADS ###

    def __eq__(self, expr):
        '''Spacing indications compare equal when
        normalized spacing durations compare equal.'''
        if isinstance(expr, SpacingIndication):
            if self.normalized_spacing_duration == \
                expr.normalized_spacing_duration:
                return True
        return False

    def __ne__(self, expr):
        '''Spacing indications compare unequal when
        normalized spacing durations compare unequal.'''
        return not self == expr

    def __repr__(self):
        return '%s(%s, %s)' % (type(self).__name__,
            self.tempo_indication, self.proportional_notation_duration)

    ### PUBLIC ATTRIBUTES ###

    @property
    def normalized_spacing_duration(self):
        '''Read-only proportional notation duration at 60 MM.'''
        indication = self.tempo_indication
        duration = self.proportional_notation_duration
        scalar = indication.duration / indication.units_per_minute * 60 / durationtools.Duration(1, 4)
        return scalar * self.proportional_notation_duration

    @property
    def proportional_notation_duration(self):
        '''LilyPond proportional notation duration context setting.'''
        return self._proportional_notation_duration

    @property
    def tempo_indication(self):
        '''Abjad tempo indication object.'''
        return self._tempo_indication
