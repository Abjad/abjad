from experimental.tools.settingtools.AbsoluteExpression import AbsoluteExpression
from experimental.tools.settingtools.StartPositionedObject import StartPositionedObject
from experimental.tools.settingtools.PayloadCallbackMixin import PayloadCallbackMixin


class StartPositionedAbsoluteExpression(AbsoluteExpression, StartPositionedObject, PayloadCallbackMixin):
    '''Start-positioned absolute expression.

        >>> expression = settingtools.StartPositionedAbsoluteExpression(
        ...     [(4, 16), (2, 16)], start_offset=Offset(40, 8))

    ::

        >>> expression = expression.repeat_to_length(6)

    ::

        >>> z(expression)
        settingtools.StartPositionedAbsoluteExpression(
            ((4, 16), (2, 16), (4, 16), (2, 16), (4, 16), (2, 16)),
            start_offset=durationtools.Offset(5, 1)
            )

    Start-positioned absolute expressions are assumed to evaluate
    to a list or other iterable.
    '''

    ### INITIALIZER ###

    def __init__(self, payload, start_offset=None, callbacks=None):
        AbsoluteExpression.__init__(self, payload=payload)
        StartPositionedObject.__init__(self, start_offset=start_offset)
        PayloadCallbackMixin.__init__(self, callbacks=callbacks)

    ### PRIVATE METHODS ###

    def _evaluate(self, score_specification=None):
        from experimental.tools import settingtools
        if isinstance(self.payload, (str, tuple)):
            result = self.payload
        else:
            raise TypeError(self.payload)
        result = self._apply_callbacks(result)
        return result

    ### READ-ONLY PUBLIC PROPERTIES ###

    @property
    def start_offset(self):
        '''Start-positioned absolute expression start offset:

        ::

            >>> expression.start_offset
            Offset(5, 1)

        Return offset.
        '''
        return StartPositionedObject.start_offset.fget(self)
