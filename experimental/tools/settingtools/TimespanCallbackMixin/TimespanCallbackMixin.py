import abc
from experimental.tools.settingtools.Expression import Expression


class TimespanCallbackMixin(Expression):
    '''Timespan callback mixin.

    Base class from which timespan-carrying expressions inherit.
    '''

    ### CLASS ATTRIBUTES ###

    __metaclass__ = abc.ABCMeta

    ### INITIALIZER ###

    @abc.abstractmethod
    def __init__(self, timespan_callbacks=None):
        from experimental.tools import settingtools
        timespan_callbacks = timespan_callbacks or []
        self._timespan_callbacks = settingtools.CallbackInventory(timespan_callbacks)

    ### READ-ONLY PUBLIC PROPERTIES ###

    @property
    def timespan_callbacks(self):
        return self._timespan_callbacks
