# -*- encoding: utf-8 -*-
from experimental.tools.musicexpressiontools.SetExpressionLookupExpression \
    import SetExpressionLookupExpression


class TimeSignatureSetExpressionLookupExpression(
    SetExpressionLookupExpression):
    r'''Time signature set expression lookup expression.
    '''

    ### INITIALIZER ###

    def __init__(self, offset=None, voice_name=None, callbacks=None):
        SetExpressionLookupExpression.__init__(
            self,
            attribute='time_signatures',
            offset=offset,
            voice_name=voice_name,
            callbacks=callbacks,
            )

    ### PUBLIC METHODS ###

    def evaluate(self):
        r'''Evaluate time signature set expression lookup expression.

        Returns payload expression.
        '''
        from experimental.tools import musicexpressiontools
        time_signatures = self.root_specification.time_signatures[:]
        expression = \
            musicexpressiontools.IterablePayloadExpression(time_signatures)
        expression = self._apply_callbacks(expression)
        return expression