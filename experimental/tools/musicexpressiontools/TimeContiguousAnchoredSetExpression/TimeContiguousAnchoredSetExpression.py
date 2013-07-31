import abc
import copy
from experimental.tools.musicexpressiontools.AnchoredExpression \
    import AnchoredExpression
from experimental.tools.musicexpressiontools.SetExpression \
    import SetExpression


class TimeContiguousAnchoredSetExpression(SetExpression, AnchoredExpression):
    r'''Anchored set expression.
    '''

    ### CLASS VARIABLES ##

    __metaclass__ = abc.ABCMeta

    ### INITIALIZER ###

    @abc.abstractmethod
    def __init__(self, 
        attribute=None, 
        source_expression=None, 
        target_timespan=None,
        persist=True, 
        truncate=None,
        ):
        from experimental.tools import musicexpressiontools
        assert isinstance(source_expression, (musicexpressiontools.Expression))
        assert isinstance(persist, bool)
        assert isinstance(truncate, (bool, type(None)))
        SetExpression.__init__(
            self,
            attribute=attribute, 
            source_expression=source_expression, 
            target_timespan=target_timespan,
            )
        AnchoredExpression.__init__(self, anchor=target_timespan)
        self._persist = persist
        self._truncate = truncate

    ### PUBLIC PROPERTIES ###

    @property
    def persist(self):
        r'''True when set expression should persist.

        Return boolean.
        '''
        return self._persist

    @property
    def target_timespan(self):
        r'''Anchored set expression target timespan.

        Return timespan expression.
        '''
        return self.anchor

    @property
    def truncate(self):
        r'''True when set expression should truncate.

        Return boolean.
        '''
        return self._truncate
