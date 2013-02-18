from abjad.tools import rhythmmakertools
from experimental.tools.expressiontools.PayloadExpression import PayloadExpression


class RhythmMakerPayloadExpression(PayloadExpression):
    r'''Rhythm-maker payload expression.
    '''

    ### INTIAILIZER ###

    def __init__(self, payload=None):
        assert isinstance(payload, rhythmmakertools.RhythmMaker), repr(payload)
        PayloadExpression.__init__(self, payload=payload)

    ### PUBLIC METHODS ###

    def reflect(self):
        '''Reflect rhythm maker payload expression.
        
        ::
    
            >>> rhythm_maker = library.dotted_sixteenths
            >>> payload_expression = expressiontools.RhythmMakerPayloadExpression(rhythm_maker)
            >>> z(payload_expression)
            expressiontools.RhythmMakerPayloadExpression(
                payload=rhythmmakertools.TaleaRhythmMaker(
                    [3, 1],
                    32,
                    prolation_addenda=[],
                    secondary_divisions=[],
                    beam_each_cell=False,
                    beam_cells_together=True,
                    tie_split_notes=False
                    )
                )

        ::

            >>> result = payload_expression.reflect()

        ::

            >>> z(result)
            expressiontools.RhythmMakerPayloadExpression(
                payload=rhythmmakertools.TaleaRhythmMaker(
                    [1, 3],
                    32,
                    prolation_addenda=[],
                    secondary_divisions=[],
                    beam_each_cell=False,
                    beam_cells_together=True,
                    tie_split_notes=False
                    )
                )

        Return newly constructed rhythm-maker payload expression.
        '''
        rhythm_maker = self.payload.reverse()
        result = self.new(payload=rhythm_maker) 
        return result
