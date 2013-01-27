import abc
import copy
from experimental.tools.expressiontools.AnchoredExpression import AnchoredExpression


class SetExpression(AnchoredExpression):
    r'''Set expression.
    '''

    ### CLASS ATTRIBUTES ##

    __metaclass__ = abc.ABCMeta

    ### INITIALIZER ###

    # TODO: eventually remove 'truncate' in favor of SingleContextDivisionSetExpression.truncate
    @abc.abstractmethod
    def __init__(self, attribute=None, expression=None, anchor=None, fresh=True, persist=True, truncate=None):
        from experimental.tools import expressiontools
        assert isinstance(attribute, str)
        assert isinstance(expression, (expressiontools.Expression)), repr(expression)
        assert isinstance(fresh, bool)
        assert isinstance(persist, bool)
        assert isinstance(truncate, (bool, type(None)))
        AnchoredExpression.__init__(self, anchor=anchor)
        self._attribute = attribute
        self._expression = expression
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
        '''SetExpression attribute.

        Return string.
        '''
        return self._attribute

    @property
    def expression(self):
        '''SetExpression expression.

        Return expression.
        '''
        return self._expression

    @property
    def fresh(self):
        '''True when set expression results from explicit composer command.
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
    def truncate(self):
        '''True when set expression should truncate.

        Return boolean.
        '''
        return self._truncate
