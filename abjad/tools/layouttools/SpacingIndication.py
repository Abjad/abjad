# -*- encoding: utf-8 -*-
from abjad.tools.abctools import AbjadObject
from abjad.tools import durationtools
from abjad.tools import tempotools


class SpacingIndication(AbjadObject):
    r'''Spacing indication token.

    LilyPond ``Score.proportionalNotationDuration``
    will equal ``proportional_notation_duration`` when tempo
    equals ``tempo_indication``.

    Initialize from tempo mark and proportional notation duration:

    ::

        >>> tempo = marktools.TempoMark(Duration(1, 8), 44)
        >>> indication = layouttools.SpacingIndication(tempo, Duration(1, 68))

    ::

        >>> indication
        SpacingIndication(TempoMark(Duration(1, 8), 44), Duration(1, 68))

    Initialize from constants:

    ::

        >>> layouttools.SpacingIndication(((1, 8), 44), (1, 68))
        SpacingIndication(TempoMark(Duration(1, 8), 44), Duration(1, 68))

    Initialize from other spacing indication:

    ::

        >>> layouttools.SpacingIndication(indication)
        SpacingIndication(TempoMark(Duration(1, 8), 44), Duration(1, 68))

    Spacing indications are immutable.
    '''

    ### CLASS VARIABLES ###

    _default_positional_input_arguments = (
        ((1, 8), 44),
        (1, 68),
        )

    ### INITIALIZER ###

    def __init__(self, *args):
        from abjad.tools import marktools
        if len(args) == 1 and isinstance(args[0], type(self)):
            self._tempo_indication = args[0].tempo_indication
            self._proportional_notation_duration = \
                args[0].proportional_notation_duration
        elif len(args) == 2:
            tempo_indication = marktools.TempoMark(args[0])
            proportional_notation_duration = durationtools.Duration(args[1])
            self._tempo_indication = tempo_indication
            self._proportional_notation_duration = \
                proportional_notation_duration
        else:
            message = 'can not initialize spacing indication from {!r}'
            message = message.format(args)
            raise ValueError(message)

    ### SPECIAL METHODS ###

    def __eq__(self, expr):
        r'''Spacing indications compare equal when normalized 
        spacing durations compare equal.
        '''
        if isinstance(expr, SpacingIndication):
            if self.normalized_spacing_duration == \
                expr.normalized_spacing_duration:
                return True
        return False

    ### PRIVATE PROPERTIES ###

    @property
    def _positional_argument_names(self):
        return ('_tempo_indication', '_proportional_notation_duration')

    ### PUBLIC PROPERTIES ###

    @property
    def normalized_spacing_duration(self):
        r'''Proportional notation duration at 60 MM.
        '''
        indication = self.tempo_indication
        duration = self.proportional_notation_duration
        scalar = indication.duration / indication.units_per_minute * \
            60 / durationtools.Duration(1, 4)
        return scalar * self.proportional_notation_duration

    @property
    def proportional_notation_duration(self):
        r'''LilyPond proportional notation duration context setting.
        '''
        return self._proportional_notation_duration

    @property
    def tempo_indication(self):
        r'''Abjad tempo indication object.
        '''
        return self._tempo_indication
