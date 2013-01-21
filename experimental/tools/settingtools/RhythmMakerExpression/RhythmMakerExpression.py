from abjad.tools import rhythmmakertools
from experimental.tools.settingtools.Expression import Expression
from experimental.tools.settingtools.NonstartPositionedPayloadCallbackMixin import NonstartPositionedPayloadCallbackMixin


class RhythmMakerExpression(Expression, NonstartPositionedPayloadCallbackMixin):
    r'''Rhythm-maker expression.

    Create behind-the-scenes at setting-time.
    '''

    ### INTIAILIZER ###

    def __init__(self, payload=None, callbacks=None):
        assert isinstance(payload, rhythmmakertools.RhythmMaker), repr(payload)
        Expression.__init__(self)
        NonstartPositionedPayloadCallbackMixin.__init__(self, callbacks=callbacks)
        self._payload = payload

    ### PRIVATE METHODS ###

    def _evaluate(self, score_specification=None, voice_name=None):
        # ignore voice_name input parameter
        voice_name = None
        raise NotImplementedError

    ### READ-ONLY PUBLIC PROPERTIES ###

    @property
    def payload(self):
        return self._payload

    ### PUBLIC METHODS ###

    # TODO: hoist to Expression
    def new(self, **kwargs):
        positional_argument_dictionary = self._positional_argument_dictionary
        keyword_argument_dictionary = self._keyword_argument_dictionary
        for key, value in kwargs.iteritems():
            if key in positional_argument_dictionary:
                positional_argument_dictionary[key] = value
            elif key in keyword_argument_dictionary:
                keyword_argument_dictionary[key] = value
            else:
                raise KeyError(key)
        positional_argument_values = []
        for positional_argument_name in self._positional_argument_names:
            positional_argument_value = positional_argument_dictionary[positional_argument_name]
            positional_argument_values.append(positional_argument_value)
        result = type(self)(*positional_argument_values, **keyword_argument_dictionary)
        return result

    def reflect(self):
        '''Reflect.
        
        .. note:: add example.
        
        Return newly constructed rhythm-maker expression.
        '''
        rhythm_maker = self.payload.reverse()
        result = self.new(payload=rhythm_maker) 
        return result
