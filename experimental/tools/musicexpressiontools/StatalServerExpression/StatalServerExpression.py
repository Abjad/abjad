from experimental.tools.musicexpressiontools.Expression import Expression
from experimental.tools.musicexpressiontools.IterablePayloadCallbackMixin import IterablePayloadCallbackMixin


class StatalServerExpression(Expression, IterablePayloadCallbackMixin):
    r'''Statal server expression.
    '''

    ### INITIALIZER ###

    def __init__(self, statal_server=None, callbacks=None):
        assert isinstance(statal_server, musicexpressiontools.StatalServer), repr(statal_server)
        Expression.__init__(self)
        IterablePayloadCallbackMixin.__init__(self, callbacks=callbacks)
        self._statal_server = statal_server

    ### SPECIAL METHODS ###

    def __call__(self):
        '''Evaluate statal server expression.
        '''
        return self.statal_server(self)

    ### PRIVATE METHODS ###

    def evaluate(self):
        '''Evaluate statal server expression.
        '''
        raise NotImplementedError

    ### READ-ONLY PUBLIC PROPERTIES ###

    @property
    def statal_server(self):
        '''Statal server expression statal server.

        Return statal server.
        '''
        return self._statal_server
