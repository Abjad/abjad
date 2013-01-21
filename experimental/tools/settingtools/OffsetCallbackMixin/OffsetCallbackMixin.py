from abjad.tools import durationtools
from experimental.tools.settingtools.CallbackMixin import CallbackMixin


class OffsetCallbackMixin(CallbackMixin):
    '''Offset callback mixin.

    .. note:: add examples.

    '''

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

    def _scale(self, offset, multiplier):
        assert 0 <= multiplier
        offset *= multiplier
        return offset

    def _translate(self, offset, translation):
        offset += translation
        return offset

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
