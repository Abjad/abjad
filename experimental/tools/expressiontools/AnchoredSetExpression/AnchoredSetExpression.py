import abc
import copy
from experimental.tools.expressiontools.AnchoredExpression import AnchoredExpression


class AnchoredSetExpression(AnchoredExpression):
    '''Anchored set expression.
    '''

    ### CLASS ATTRIBUTES ##

    __metaclass__ = abc.ABCMeta

    ### INITIALIZER ###

    @abc.abstractmethod
    def __init__(self, source=None, target_timespan=None):
        AnchoredExpression.__init__(self, anchor=target_timespan)
        self._source = source

    ### READ-ONLY PUBLIC PROPERTIES ###

    @property
    def source(self):
        return self._source

    @property
    def target_timespan(self):
        return self.anchor
