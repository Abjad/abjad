from experimental.tools.settingtools.AbsoluteExpression import AbsoluteExpression
from experimental.tools.settingtools.StartPositionedObject import StartPositionedObject


class StartPositionedAbsoluteExpression(AbsoluteExpression, StartPositionedObject):
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
        AbsoluteExpression.__init__(self, payload=payload, callbacks=callbacks)
        StartPositionedObject.__init__(self, start_offset=start_offset)

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

    @property
    def stop_offset(self):
        '''Start-positioned absolute expression stop offset:

        ::

            >>> expression.stop_offset
            Offset(43, 8)

        Return offset.
        '''
        return StartPositionedObject.stop_offset.fget(self)

    @property
    def timespan(self):
        '''Start-positioned absolute expression stop offset:

        ::

            >>> expression.timespan
            Timespan(start_offset=Offset(5, 1), stop_offset=Offset(43, 8))

        Return timespan.
        '''
        return StartPositionedObject.timespan.fget(self)
