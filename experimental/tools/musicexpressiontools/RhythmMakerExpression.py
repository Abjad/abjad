# -*- encoding: utf-8 -*-
from abjad.tools import rhythmmakertools
from abjad.tools.topleveltools import new
from experimental.tools.musicexpressiontools.PayloadExpression \
    import PayloadExpression


class RhythmMakerExpression(PayloadExpression):
    r'''Rhythm-maker payload expression.
    '''

    ### INTIAILIZER ###

    def __init__(self, payload=None):
        assert isinstance(payload, rhythmmakertools.RhythmMaker)
        PayloadExpression.__init__(self, payload=payload)

    ### PUBLIC METHODS ###

    def reflect(self):
        r'''Reflect rhythm maker payload expression.

        ::

            >>> rhythm_maker = library.dotted_sixteenths
            >>> payload_expression = \
            ...     musicexpressiontools.RhythmMakerExpression(rhythm_maker)
            >>> print(format(payload_expression))
            musicexpressiontools.RhythmMakerExpression(
                payload=rhythmmakertools.TaleaRhythmMaker(
                    talea=rhythmmakertools.Talea(
                        counts=(3, 1),
                        denominator=32,
                    ),
                ),
            )

        ::

            >>> result = payload_expression.reflect()

        ::

            >>> print(format(result))
            musicexpressiontools.RhythmMakerExpression(
                payload=rhythmmakertools.TaleaRhythmMaker(
                    talea=rhythmmakertools.Talea(
                        counts=(1, 3),
                        denominator=32,
                    ),
                    burnish_specifier=rhythmmakertools.BurnishSpecifier(
                        burnish_divisions=False,
                        burnish_output=False,
                        ),
                    duration_spelling_specifier=rhythmmakertools.DurationSpellingSpecifier(
                        decrease_durations_monotonically=False,
                        ),
                    ),
                )

        Returns newly constructed rhythm-maker payload expression.
        '''
        rhythm_maker = self.payload.reverse()
        result = new(self, payload=rhythm_maker)
        return result
