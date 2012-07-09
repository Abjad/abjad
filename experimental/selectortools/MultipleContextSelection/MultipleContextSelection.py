from abjad.tools import contexttools
from abjad.tools.abctools.AbjadObject import AbjadObject
from experimental.timespantools.Timespan import Timespan


class MultipleContextSelection(AbjadObject):
    r'''.. versionadded:: 1.0

    ::

        >>> from experimental import selectortools
        >>> from experimental import specificationtools

    Arbitrarily many contexts taken over a shared timespan.

    Select the entire score::

        >>> selectortools.MultipleContextSelection()
        MultipleContextSelection()

    Select all of ``'Voice 1'``::

        >>> selectortools.MultipleContextSelection(contexts=['Voice 1'])
        MultipleContextSelection(contexts=['Voice 1'])

    Select all of ``'Voice 1'`` and ``'Voice 3'``::

        >>> selectortools.MultipleContextSelection(contexts=['Voice 1', 'Voice 3'])
        MultipleContextSelection(contexts=['Voice 1', 'Voice 3'])

    Select the timespan of segment ``'red'``::

        >>> timespan = specificationtools.segments_to_timespan('red')

    ::

        >>> selectortools.MultipleContextSelection(timespan=timespan)
        MultipleContextSelection(timespan=Timespan(selector=SegmentSelector(index='red')))

    Select ``'Voice 1'`` taken over the timepsan of segment ``'red'``::

        >>> selectortools.MultipleContextSelection(contexts=['Voice 1'], timespan=timespan)
        MultipleContextSelection(contexts=['Voice 1'], timespan=Timespan(selector=SegmentSelector(index='red')))

    Select ``'Voice 1'`` and ``'Voice 3'`` over the timespan of segment ``'red'``::

        >>> selectortools.MultipleContextSelection(contexts=['Voice 1', 'Voice 3'], timespan=timespan)
        MultipleContextSelection(contexts=['Voice 1', 'Voice 3'], timespan=Timespan(selector=SegmentSelector(index='red')))

    MultipleContextSelection objects are immutable.
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

    ### READ-ONLY PRIVATE PROPERTIES ###

    @property
    def _one_line_format(self):
        contexts = self.contexts or []
        contexts = ', '.join(contexts)
        if contexts:
            contexts = contexts + ': '
        timespan = self.timespan._one_line_format
        result = '{}{}'.format(contexts, timespan)
        return result

    ### READ-ONLY PUBLIC PROPERTIES ###

    @property
    def contexts(self):
        '''MultipleContextSelection contexts specified by user.

        Value of none taken equal to all contexts in score.

        Return list of strings or none.
        '''
        return self._contexts

    @property
    def timespan(self):
        '''MultipleContextSelection timespan specified by user.

        Value of none taken equal to timespan of entire score.

        Return timespan or none.
        '''
        return self._timespan
