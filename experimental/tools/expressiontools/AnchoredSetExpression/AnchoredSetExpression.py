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
    def __init__(self, source=None, target_timespan=None):
        SetExpression.__init__(self, source=source)
        AnchoredExpression.__init__(self, anchor=target_timespan)

    ### READ-ONLY PUBLIC PROPERTIES ###

    @property
    def target_timespan(self):
        return self.anchor
