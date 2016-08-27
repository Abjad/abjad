# -*- coding: utf-8 -*-
from abjad.tools import durationtools
from abjad.tools import systemtools
from abjad.tools.abctools import AbjadValueObject


class SpacingIndication(AbjadValueObject):
    r'''Spacing indication token.

    LilyPond ``Score.proportionalNotationDuration``
    will equal ``proportional_notation_duration`` when tempo
    equals ``tempo_indication``.

    Initialize from tempo and proportional notation duration:

    ::

        >>> tempo = Tempo(Duration(1, 8), 44)
        >>> indication = indicatortools.SpacingIndication(tempo, Duration(1, 68))

    ::

        >>> indication
        SpacingIndication(Tempo(reference_duration=Duration(1, 8), units_per_minute=44), Duration(1, 68))

    Initialize from constants:

    ::

        >>> indicatortools.SpacingIndication(((1, 8), 44), (1, 68))
        SpacingIndication(Tempo(reference_duration=Duration(1, 8), units_per_minute=44), Duration(1, 68))

    Initialize from other spacing indication:

    ::

        >>> indicatortools.SpacingIndication(indication)
        SpacingIndication(Tempo(reference_duration=Duration(1, 8), units_per_minute=44), Duration(1, 68))

    Spacing indications are immutable.
    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        '_proportional_notation_duration',
        '_tempo_indication',
        )

    ### INITIALIZER ###

    def __init__(self, *args):
        from abjad.tools import indicatortools
        if len(args) == 1 and isinstance(args[0], type(self)):
            self._tempo_indication = args[0].tempo_indication
            self._proportional_notation_duration = \
                args[0].proportional_notation_duration
        elif len(args) == 2:
            tempo = args[0]
            if isinstance(tempo, tuple):
                tempo = indicatortools.Tempo(*tempo)
            tempo_indication = tempo
            proportional_notation_duration = durationtools.Duration(args[1])
            self._tempo_indication = tempo_indication
            self._proportional_notation_duration = \
                proportional_notation_duration
        elif len(args) == 0:
            tempo = indicatortools.Tempo()
            proportional_notation_duration = durationtools.Duration(1, 68)
            self._tempo_indication = tempo
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

    def __hash__(self):
        r'''Hashes spacing indication.

        Required to be explicitly redefined on Python 3 if __eq__ changes.

        Returns integer.
        '''
        return super(SpacingIndication, self).__hash__()

    ### PRIVATE METHODS ###

    def _get_format_specification(self):
        return systemtools.FormatSpecification(
            client=self,
            repr_is_indented=False,
            storage_format_args_values=[
                self._tempo_indication,
                self._proportional_notation_duration,
                ],
            )

    ### PUBLIC PROPERTIES ###

    @property
    def normalized_spacing_duration(self):
        r'''Proportional notation duration normalized to 60 MM.

        Returns duration.
        '''
        indication = self.tempo_indication
        scalar = indication.reference_duration / indication.units_per_minute * \
            60 / durationtools.Duration(1, 4)
        return scalar * self.proportional_notation_duration

    @property
    def proportional_notation_duration(self):
        r'''LilyPond proportional notation duration of spacing indication.

        Returns duration.
        '''
        return self._proportional_notation_duration

    @property
    def tempo_indication(self):
        r'''Tempo of spacing indication.

        Returns tempo.
        '''
        return self._tempo_indication
