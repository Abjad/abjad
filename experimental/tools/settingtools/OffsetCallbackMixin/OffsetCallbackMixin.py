import abc
import copy
from abjad.tools import durationtools
from abjad.tools.abctools import AbjadObject


class OffsetCallbackMixin(AbjadObject):
    '''Offset callback mixin.

    .. note:: add examples.

    '''

    ### CLASS ATTRIBUTES ###

    __metaclass__ = abc.ABCMeta

    ### INITIALIZER ###

    @abc.abstractmethod
    def __init__(self, callbacks=None):
        from experimental.tools import settingtools
        callbacks = callbacks or []
        self._callbacks = settingtools.CallbackInventory(callbacks)

    ### PRIVATE METHODS ###

    def _apply_callbacks(self, offset):
        assert isinstance(offset, durationtools.Offset), repr(offset)
        evaluation_context = {
            'self': self,
            'Duration': durationtools.Duration,
            'Multiplier': durationtools.Multiplier,
            'Offset': durationtools.Offset,
            }
        for callback in self.callbacks:
            callback = callback.replace('offset', repr(offset))
            offset = eval(callback, evaluation_context)
        return offset

    def _copy_and_append_callback(self, callback):
        result = copy.deepcopy(self)
        result.callbacks.append(callback)
        return result

    def _scale(self, offset, multiplier):
        assert 0 <= multiplier
        offset *= multiplier
        return offset

    def _translate(self, offset, translation):
        offset += translation
        return offset

    ### READ-ONLY PUBLIC PROPERTIES ###

    @property
    def callbacks(self):
        return self._callbacks

    ### PUBLIC METHODS ###

    def scale(self, multiplier):
        multiplier = durationtools.Multiplier(multiplier)
        callback = 'self._scale(offset, {!r})'
        callback = callback.format(multiplier)
        return self._copy_and_append_callback(callback)

    def translate(self, translation):
        translation = durationtools.Duration(translation)
        callback = 'self._translate(offset, {!r})'
        callback = callback.format(translation)
        return self._copy_and_append_callback(callback)
