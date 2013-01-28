import abc
from experimental.tools.expressiontools.AnchoredExpression import AnchoredExpression
from experimental.tools.expressiontools.PayloadCallbackMixin import PayloadCallbackMixin


class SetExpressionLookupExpression(AnchoredExpression, PayloadCallbackMixin):
    r'''Set expression lookup expression.

    Look up `attribute` set expression active at `offset` in `voice_name`.

    Lookup expression is assumed to resolve to a list or other iterable payload.

    Because of this lookup expressions afford payload callbacks.

    Composers create concrete lookup expressions with lookup methods.
    '''

    ### INITIALIZER ###

    __metaclass__ = abc.ABCMeta

    ### INITIALIZER ###

    @abc.abstractmethod
    def __init__(self, attribute=None, offset=None, voice_name=None, callbacks=None):
        from experimental.tools import expressiontools
        assert attribute in self.attributes, repr(attribute)
        assert isinstance(voice_name, str), repr(voice_name)
        assert isinstance(offset, expressiontools.OffsetExpression)
        AnchoredExpression.__init__(self, anchor=offset)
        PayloadCallbackMixin.__init__(self, callbacks=callbacks)
        self._attribute = attribute
        self._offset = offset
        self._voice_name = voice_name

    ### READ-ONLY PUBLIC PROPERTIES ###

    @property
    def attribute(self):
        '''Set expression lookup expression attribute.

        Return string.
        '''
        return self._attribute

    @property
    def offset(self):
        '''Set expression lookup expression offset.

        Return offset expression.
        '''
        return self.anchor

    @property
    def voice_name(self):
        '''Set expression lookup expression voice name.

        Return string.
        '''
        return self._voice_name

    ### PRIVATE METHODS ###
    
    @abc.abstractmethod
    def evaluate(self):
        pass
