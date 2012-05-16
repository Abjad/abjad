from abjad.tools.abctools import AbjadObject
from abjad.tools import durationtools
from abjad.tools import tempotools


class SpacingIndication(AbjadObject):
    '''Spacing indication token.

    LilyPond ``Score.proportionalNotationDuration``
    will equal ``proportional_notation_duration`` when tempo
    equals ``tempo_indication``::

        abjad> from abjad.tools import layouttools

    Initialize from tempo mark and proportional notation duration::

        abjad> tempo = contexttools.TempoMark(Duration(1, 8), 44)
        abjad> indication = layouttools.SpacingIndication(tempo, Duration(1, 68))
        
    ::

        abjad> indication
        SpacingIndication(TempoMark(Duration(1, 8), 44), Duration(1, 68))

    Initialize from other spacing indication::

        abjad> layouttools.SpacingIndication(indication)
        SpacingIndication(TempoMark(Duration(1, 8), 44), Duration(1, 68))

    Spacing indications are immutable.
    '''

    ### INITIALIZER ###

    def __init__(self, *args):
        if len(args) == 1 and isinstance(args[0], type(self)):
            object.__setattr__(self, '_tempo_indication', args[0].tempo_indication)
            object.__setattr__(
                self, '_proportional_notation_duration', args[0].proportional_notation_duration)
        elif len(args) == 2:
            object.__setattr__(self, '_tempo_indication', args[0])
            object.__setattr__(self, '_proportional_notation_duration', args[1])
        else:
            raise ValueError('can not initialize spacing indication from {!r}'.format(args))

    ### SPECIAL METHODS ###

    def __eq__(self, expr):
        '''Spacing indications compare equal when normalized spacing durations compare equal.
        '''
        if isinstance(expr, SpacingIndication):
            if self.normalized_spacing_duration == expr.normalized_spacing_duration:
                return True
        return False

    def __ne__(self, expr):
        '''Spacing indications compare unequal when normalized spacing durations compare unequal.
        '''
        return not self == expr

    ### READ-ONLY PRIVATE PROPERTIES ###

    @property
    def _mandatory_argument_names(self):
        return ('_tempo_indication', '_proportional_notation_duration')

    ### READ-ONLY PUBLIC PROPERTIES ###

    @property
    def normalized_spacing_duration(self):
        '''Read-only proportional notation duration at 60 MM.
        '''
        indication = self.tempo_indication
        duration = self.proportional_notation_duration
        scalar = indication.duration / indication.units_per_minute * 60 / durationtools.Duration(1, 4)
        return scalar * self.proportional_notation_duration

    @property
    def proportional_notation_duration(self):
        '''LilyPond proportional notation duration context setting.
        '''
        return self._proportional_notation_duration

    @property
    def tempo_indication(self):
        '''Abjad tempo indication object.
        '''
        return self._tempo_indication
