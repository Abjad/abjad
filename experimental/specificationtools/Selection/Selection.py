from abjad.tools import contexttools
from abjad.tools.abctools.AbjadObject import AbjadObject
from experimental.specificationtools.Timespan import Timespan


class Selection(AbjadObject):
    r'''.. versionadded:: 1.0

    Arbitrarily many contexts taken over arbitrary timespan.

    (Object-oriented delayed evaluation.)

    Initialize with optional `contexts` and `timespan`.

    Select the entire score::

        >>> from experimental import specificationtools

    ::

        >>> specificationtools.Selection()
        Selection()

    Select all of ``'Voice 1'``::

        >>> specificationtools.Selection(contexts=['Voice 1'])
        Selection(contexts=['Voice 1'])

    Select all of ``'Voice 1'`` and ``'Voice 3'``::

        >>> specificationtools.Selection(contexts=['Voice 1', 'Voice 3'])
        Selection(contexts=['Voice 1', 'Voice 3'])

    Select the timespan of segment ``'red'``::

        >>> timespan = specificationtools.segment_to_timespan('red')

    ::

        >>> specificationtools.Selection(timespan=timespan)
        Selection(timespan=Timespan(start=Timepoint(anchor=ScoreObjectIndicator(segment='red')), stop=Timepoint(anchor=ScoreObjectIndicator(segment='red'), edge=Right)))

    Select ``'Voice 1'`` taken over the timepsan of segment ``'red'``::

        >>> specificationtools.Selection(contexts=['Voice 1'], timespan=timespan)
        Selection(contexts=['Voice 1'], timespan=Timespan(start=Timepoint(anchor=ScoreObjectIndicator(segment='red')), stop=Timepoint(anchor=ScoreObjectIndicator(segment='red'), edge=Right)))

    Select ``'Voice 1'`` and ``'Voice 3'`` over the timespan of segment ``'red'``::

        >>> specificationtools.Selection(contexts=['Voice 1', 'Voice 3'], timespan=timespan)
        Selection(contexts=['Voice 1', 'Voice 3'], timespan=Timespan(start=Timepoint(anchor=ScoreObjectIndicator(segment='red')), stop=Timepoint(anchor=ScoreObjectIndicator(segment='red'), edge=Right)))

    Selection objects are immutable.
    '''

    ### INITIALIZER ###

    def __init__(self, contexts=None, timespan=None):
        assert isinstance(contexts, (list, type(None))), repr(contexts)
        assert isinstance(timespan, (Timespan, type(None))), repr(timespan)
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
