from abjad.tools import contexttools
from abjad.tools.abctools.AbjadObject import AbjadObject
from experimental.specificationtools.Timespan import Timespan


class Selection(AbjadObject):
    r'''.. versionadded:: 1.0

    Arbitrarily many contexts taken over arbitrary timespan.

    (Object-oriented delayed evaluation.)

    Selection objects are immutable.
    
    .. note:: initializer signature currently migrating to ``Selection(contexts=None, timespan=None)``.
    '''

    ### INITIALIZER ###

    #def __init__(self, segment_name, contexts=None, timespan=None):
    def __init__(self, contexts=None, timespan=None):
        #assert isinstance(segment_name, str), repr(segment_name)
        assert isinstance(contexts, (list, type(None))), repr(contexts)
        assert isinstance(timespan, (Timespan, type(None))), repr(timespan)
        #self._segment_name = segment_name
        self._contexts = contexts
        self._timespan = timespan

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
    def timespan(self):
        '''Selection timespan specified by user.

        Value of none taken equal to timespan of entire score.

        Return timespan or none.
        '''
        return self._timespan
