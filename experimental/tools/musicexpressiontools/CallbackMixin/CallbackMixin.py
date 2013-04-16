import abc
import copy
from abjad.tools.abctools import AbjadObject
from experimental.tools.musicexpressiontools.AttributeNameEnumeration import AttributeNameEnumeration


class CallbackMixin(AbjadObject):
    '''Callback mixin.
    '''

    ### CLASS ATTRIBUTES ###

    __metaclass__ = abc.ABCMeta

    attributes = AttributeNameEnumeration()

    ### INITIALIZER ###

    @abc.abstractmethod
    def __init__(self, callbacks=None):
        from experimental.tools import musicexpressiontools
        callbacks = callbacks or []
        self._callbacks = musicexpressiontools.CallbackInventory(callbacks)

    ### PRIVATE METHODS ###

    @abc.abstractmethod
    def _apply_callbacks(self):
        pass

    def _copy_and_append_callback(self, callback):
        result = copy.deepcopy(self)
        result.callbacks.append(callback)
        return result

    ### READ-ONLY PUBLIC PROPERTIES ###

    @property
    def callbacks(self):
        '''Read-only list of callbacks to be applied during evaluation.

        Return callback inventory.
        '''
        return self._callbacks
