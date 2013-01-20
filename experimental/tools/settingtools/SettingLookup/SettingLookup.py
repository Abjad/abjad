import abc
from experimental.tools.settingtools.Expression import Expression
from experimental.tools.settingtools.PayloadCallbackMixin import PayloadCallbackMixin


class SettingLookup(Expression, PayloadCallbackMixin):
    r'''Setting lookup request.

    Look up `attribute` setting active at `offset` in `voice_name`.

    Setting is assumed to resolve to a list or other iterable payload.

    Because of this setting lookup requests afford payload callbacks.

    Composers create concrete setting lookup request classes during specification.

    Composers create concrete setting lookup request classes with lookup methods.

    All lookup methods implement against ``OffsetExpression``.
    '''

    ### INITIALIZER ###

    __metaclass__ = abc.ABCMeta

    ### INITIALIZER ###

    @abc.abstractmethod
    def __init__(self, attribute=None, voice_name=None, offset=None, callbacks=None):
        from experimental.tools import settingtools
        assert attribute in self.attributes, repr(attribute)
        assert isinstance(voice_name, str), repr(voice_name)
        assert isinstance(offset, settingtools.OffsetExpression)
        Expression.__init__(self, anchor=offset)
        PayloadCallbackMixin.__init__(self, callbacks=callbacks)
        self._attribute = attribute
        self._voice_name = voice_name
        self._offset = offset

    ### READ-ONLY PUBLIC PROPERTIES ###

    @property
    def attribute(self):
        '''Setting lookup request attribute.

        Return string.
        '''
        return self._attribute

    @property
    def offset(self):
        '''Setting lookup request offset.

        Return offset expression.
        '''
        return self._offset

    @property
    def voice_name(self):
        '''Setting lookup request voice name.

        Return string.
        '''
        return self._voice_name

    ### PRIVATE METHODS ###
    
    @abc.abstractmethod
    def _evaluate(self, score_specification=None, voice_name=None):
        # ignore voice_name input parameter
        voice_name = None
        pass
