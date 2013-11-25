# -*- encoding: utf-8 -*-
from abjad.tools import rhythmmakertools
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
            >>> print format(payload_expression)
            musicexpressiontools.RhythmMakerExpression(
                payload=rhythmmakertools.TaleaRhythmMaker(
                    talea=[3, 1],
                    talea_denominator=32,
                    prolation_addenda=[],
                    secondary_divisions=[],
                    beam_each_cell=False,
                    beam_cells_together=True,
                    tie_split_notes=False,
                    ),
                )

        ::

            >>> result = payload_expression.reflect()

        ::

            >>> print format(result)
            musicexpressiontools.RhythmMakerExpression(
                payload=rhythmmakertools.TaleaRhythmMaker(
                    talea=[1, 3],
                    talea_denominator=32,
                    prolation_addenda=[],
                    secondary_divisions=[],
                    beam_each_cell=False,
                    beam_cells_together=True,
                    tie_split_notes=False,
                    ),
                )

        Returns newly constructed rhythm-maker payload expression.
        '''
        rhythm_maker = self.payload.reverse()
        result = self.__makenew__(payload=rhythm_maker)
        return result
