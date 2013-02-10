from abjad.tools import rhythmmakertools
from experimental.tools.expressiontools.PayloadExpression import PayloadExpression


class RhythmMakerPayloadExpression(PayloadExpression):
    r'''Rhythm-maker payload expression.
    '''

    ### INTIAILIZER ###

    def __init__(self, payload=None):
        assert isinstance(payload, rhythmmakertools.RhythmMaker), repr(payload)
        PayloadExpression.__init__(self, payload=[payload])

    ### PUBLIC METHODS ###

    def reflect(self):
        '''Reflect rhythm maker payload expression.
        
        ::
    
            >>> rhythm_maker = library.dotted_sixteenths
            >>> payload_expression = expressiontools.RhythmMakerPayloadExpression(rhythm_maker)
            >>> z(payload_expression)
            expressiontools.RhythmMakerPayloadExpression(
                payload=(TaleaRhythmMaker('dotted_sixteenths'),)
                )

        ::

            >>> result = payload_expression.reflect()

        ::

            >>> z(result)
            expressiontools.RhythmMakerPayloadExpression(
                payload=(TaleaRhythmMaker('dotted_sixteenths'),)
                )

        Return newly constructed rhythm-maker payload expression.
        '''
        rhythm_maker = self.payload[0].reverse()
        result = self.new(payload=rhythm_maker) 
        return result
