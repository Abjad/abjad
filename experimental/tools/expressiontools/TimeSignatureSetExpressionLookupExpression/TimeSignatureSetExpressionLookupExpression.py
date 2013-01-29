from experimental.tools.expressiontools.SetExpressionLookupExpression import SetExpressionLookupExpression


class TimeSignatureSetExpressionLookupExpression(SetExpressionLookupExpression):
    '''Set-time signature lookup expression.
    '''

    ### INITIALIZER ###

    def __init__(self, offset=None, voice_name=None, callbacks=None):
        SetExpressionLookupExpression.__init__(self, attribute='time_signatures', 
            offset=offset, voice_name=voice_name, callbacks=callbacks)

    ### PUBLIC METHODS ###

    def evaluate(self):
        from experimental.tools import expressiontools
        time_signatures = self.start_segment_specification.time_signatures[:]
        expression = expressiontools.PayloadExpression(time_signatures)
        expression = self._apply_callbacks(expression)
        return expression
