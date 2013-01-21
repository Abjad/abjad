from experimental.tools.settingtools.AbsoluteExpression import AbsoluteExpression
from experimental.tools.settingtools.StartPositionedObject import StartPositionedObject
from experimental.tools.settingtools.StartPositionedPayloadCallbackMixin import StartPositionedPayloadCallbackMixin


class StartPositionedAbsoluteExpression(AbsoluteExpression, StartPositionedObject, StartPositionedPayloadCallbackMixin):
    '''Start-positioned absolute expression.

        >>> expression = settingtools.StartPositionedAbsoluteExpression(
        ...     [(4, 16), (2, 16)], start_offset=Offset(40, 8))

    ::

        >>> expression = expression.repeat_to_length(6)

    ::

        >>> z(expression)
        settingtools.StartPositionedAbsoluteExpression(
            ((4, 16), (2, 16)),
            start_offset=durationtools.Offset(5, 1),
            callbacks=settingtools.CallbackInventory([
                'result = self._repeat_to_length(expr, 6, start_offset)'
                ])
            )

    Start-positioned absolute expressions are assumed to evaluate
    to a list or other iterable.
    '''

    ### INITIALIZER ###

    def __init__(self, payload, start_offset=None, callbacks=None):
        AbsoluteExpression.__init__(self, payload=payload)
        StartPositionedObject.__init__(self, start_offset=start_offset)
        StartPositionedPayloadCallbackMixin.__init__(self, callbacks=callbacks)

    ### PRIVATE METHODS ###

    def _evaluate(self, score_specification=None, voice_name=None):
        from experimental.tools import settingtools
        # ignore voice_name input parameter
        voice_name = None
        if isinstance(self.payload, (str, tuple)):
            result = self.payload
        else:
            raise TypeError(self.payload)
        # TODO: eventually change to result = self._apply_callbacks(result)
        result, dummy = self._apply_callbacks(result, result.start_offset)
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
