from experimental.tools.specificationtools.SetExpressionLookupExpression import SetExpressionLookupExpression


class TimeSignatureSetExpressionLookupExpression(SetExpressionLookupExpression):
    '''Time signature set expression lookup expression.
    '''

    ### INITIALIZER ###

    def __init__(self, offset=None, voice_name=None, callbacks=None):
        SetExpressionLookupExpression.__init__(self, attribute='time_signatures',
            offset=offset, voice_name=voice_name, callbacks=callbacks)

    ### PUBLIC METHODS ###

    def evaluate(self):
        '''Evaluate time signature set expression lookup expression.

        Return payload expression.
        '''
        from experimental.tools import specificationtools
        time_signatures = self.root_specification.time_signatures[:]
        expression = specificationtools.IterablePayloadExpression(time_signatures)
        expression = self._apply_callbacks(expression)
        return expression
