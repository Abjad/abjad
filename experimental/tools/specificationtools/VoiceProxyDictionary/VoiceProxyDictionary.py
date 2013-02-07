from collections import OrderedDict
from abjad.tools import iterationtools
from abjad.tools import scoretools
from abjad.tools.abctools.AbjadObject import AbjadObject


class VoiceProxyDictionary(AbjadObject, OrderedDict):

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
        from experimental.tools import specificationtools
        assert isinstance(key, str), repr(key)
        assert isinstance(value, specificationtools.ContextProxy), repr(value)
        OrderedDict.__setitem__(self, key, value)

    ### PRIVATE METHODS ###

    def _initialize_voice_proxies(self):
        from experimental.tools import specificationtools
        context_names = []
        if self.score is not None:
            for voice in iterationtools.iterate_voices_in_expr(self.score):
                assert voice.context_name is not None, voice.name_name
                voice_names.append(voice.name)
        for voice_name in sorted(voice_names):
            self[voice_name] = specificationtools.VoiceProxy()

    ### READ-ONLY PUBLIC PROPERTIES ###

    @property
    def score(self):
        return self._score
