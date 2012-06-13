from abjad.tools.abctools.AbjadObject import AbjadObject
from experimental.specificationtools.TemporalScope import TemporalScope


class Selection(AbjadObject):
    r'''.. versionadded:: 1.0

    Arbitrary contexts taken over arbitrary temporal scope.

    (Object-oriented delayed evaluation.)

    Selection objects are immutable.
    
    .. note:: initializer signature currently migrating to ``Selection(contexts=None, scope=None)``.
    '''

    ### INITIALIZER ###

    def __init__(self, segment_name, contexts=None, scope=None):
    #def __init__(self, segment_name, contexts=None, scope=None):
        assert isinstance(segment_name, str)
        assert isinstance(contexts, (list, type(None)))
        assert isinstance(scope, (TemporalScope, type(None)))
        self._segment_name = segment_name
        self._contexts = contexts
        self._scope = scope

    ### SPECIAL METHODS ###

    def __eq__(self, expr):
        if not isinstance(expr, type(self)):
            return False
        if not self._mandatory_argument_values == expr._mandatory_argument_values:
            return False
        for keyword_argument_name in self._keyword_argument_names:
            if not getattr(self, keyword_argument_name) == getattr(expr, keyword_argument_name):
                return False
        return True

    def __ne__(self, expr):
        return not self == expr

    ### READ-ONLY PUBLIC PROPERTIES ###

    @property
    def contexts(self):
        '''Selection contexts specified by user.

        Value of none taken equal to all contexts in score.

        Return list of strings or none.
        '''
        return self._contexts

    @property
    def segment_name(self):
        '''Deprecated.
        '''
        return self._segment_name

    @property
    def scope(self):
        '''Selection temporal scope specified by user.

        Value of none taken equal to timespan of entire score.

        Return temporal scope or none.
        '''
        return self._scope
