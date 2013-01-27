from experimental.tools.expressiontools.SetLookupExpression import SetLookupExpression


class SetTimeSignatureLookupExpression(SetLookupExpression):
    '''Set-time signature lookup expression.
    '''

    ### INITIALIZER ###

    def __init__(self, voice_name=None, offset=None, callbacks=None):
        SetLookupExpression.__init__(self, attribute='time_signatures', voice_name=voice_name, 
            offset=offset, callbacks=callbacks)

    ### PUBLIC METHODS ###

    def evaluate(self):
        from experimental.tools import expressiontools
        segment_specification = self.score_specification.get_start_segment_specification(self.offset)
        time_signatures = segment_specification.time_signatures[:]
        expression = expressiontools.PayloadExpression(time_signatures)
        expression = self._apply_callbacks(expression)
        return expression
