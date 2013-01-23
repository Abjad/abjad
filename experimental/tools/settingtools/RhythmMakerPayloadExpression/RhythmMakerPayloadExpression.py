from abjad.tools import rhythmmakertools
from experimental.tools.settingtools.PayloadExpression import PayloadExpression


class RhythmMakerPayloadExpression(PayloadExpression):
    r'''Rhythm-maker expression.
    '''

    ### INTIAILIZER ###

    def __init__(self, payload=None):
        assert isinstance(payload, rhythmmakertools.RhythmMaker), repr(payload)
        PayloadExpression.__init__(self, payload=payload)

    ### PUBLIC METHODS ###

    def reflect(self):
        '''Reflect.
        
        .. note:: add example.
        
        Return newly constructed rhythm-maker expression.
        '''
        rhythm_maker = self.payload.reverse()
        result = self.new(payload=rhythm_maker) 
        return result
