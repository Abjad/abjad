from experimental.tools.specificationtools.PayloadExpression import PayloadExpression


class PitchClassTransformExpression(PayloadExpression):
    '''Pitch-class transform expression.
    '''

    ### INITIALIZER ###

    def __init__(self, payload=None):
        if isinstance(payload, type(self)):
            payload = payload.payload
        assert isinstance(payload, str), repr(payload)
        PayloadExpression.__init__(self, payload=payload)
