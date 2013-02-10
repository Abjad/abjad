import abc
import copy
from experimental.tools.expressiontools.AnchoredExpression import AnchoredExpression
from experimental.tools.expressiontools.SetExpression import SetExpression


class AnchoredSetExpression(SetExpression, AnchoredExpression):
    '''Anchored set expression.
    '''

    ### CLASS ATTRIBUTES ##

    __metaclass__ = abc.ABCMeta

    ### INITIALIZER ###

    @abc.abstractmethod
    def __init__(self, attribute=None, source=None, target_timespan=None, 
        fresh=True, persist=True, truncate=None):
        from experimental.tools import expressiontools
        assert isinstance(attribute, str)
        assert isinstance(source, (expressiontools.Expression)), repr(expression)
        assert isinstance(fresh, bool)
        assert isinstance(persist, bool)
        assert isinstance(truncate, (bool, type(None)))
        SetExpression.__init__(self, source=source)
        AnchoredExpression.__init__(self, anchor=target_timespan)
        self._attribute = attribute
        self._fresh = fresh
        self._persist = persist
        self._truncate = truncate

    ### SPECIAL METHODS ###

    def __eq__(self, expr):
        '''True when mandatory and keyword arguments compare equal.
        Otherwise false.

        Return boolean.
        '''
        if not isinstance(expr, type(self)):
            return False
        if not self._positional_argument_values == expr._positional_argument_values:
            return False
        return self._keyword_argument_values == expr._keyword_argument_values

    ### READ-ONLY PUBLIC PROPERTIES ###

    @property
    def attribute(self):
        '''Set expression attribute.

        Return string.
        '''
        return self._attribute

    @property
    def fresh(self):
        '''True when set expression results from explicit composer input.
        Otherwise false.

        Return boolean.
        '''
        return self._fresh

    @property
    def persist(self):
        '''True when set expression should persist.
         
        Return boolean.
        '''
        return self._persist

    @property
    def target_timespan(self):
        return self.anchor

    @property
    def truncate(self):
        '''True when set expression should truncate.

        Return boolean.
        '''
        return self._truncate
