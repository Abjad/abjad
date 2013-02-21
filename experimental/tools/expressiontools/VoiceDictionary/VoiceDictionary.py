from collections import OrderedDict
from abjad.tools import iterationtools
from abjad.tools import scoretools
from abjad.tools.abctools.AbjadObject import AbjadObject


class VoiceDictionary(AbjadObject, OrderedDict):
    '''Voice dictionary.
    '''

    ### INITIALIZER ###

    def __init__(self, score):
        assert isinstance(score, scoretools.Score), repr(score)
        OrderedDict.__init__(self)
        self._score = score
        self._initialize_voice_proxies()

    ### SPECIAL METHODS ###

    def __repr__(self):
        contents = ', '.join([repr(x) for x in self])
        return '{}([{}])'.format(self._class_name, contents)

    def __setitem__(self, key, value):
        from experimental.tools import expressiontools
        assert isinstance(key, str), repr(key)
        assert isinstance(value, expressiontools.VoiceProxy), repr(value)
        OrderedDict.__setitem__(self, key, value)

    ### PRIVATE METHODS ###

    def _initialize_voice_proxies(self):
        from experimental.tools import expressiontools
        voice_names = []
        if self.score is not None:
            for voice in iterationtools.iterate_voices_in_expr(self.score):
                assert voice.context_name is not None, voice.name_name
                voice_names.append(voice.name)
        for voice_name in sorted(voice_names):
            self[voice_name] = expressiontools.VoiceProxy()

    ### READ-ONLY PUBLIC PROPERTIES ###

    @property
    def score(self):
        '''Voice dictionary score.

        Return score.
        '''
        return self._score
