import abc
from experimental.tools.expressiontools.AnchoredExpression import AnchoredExpression


class SetExpression(AnchoredExpression):
    '''Base set expression.
    '''

    ### CLASS ATTRIBUTES ##

    __metaclass__ = abc.ABCMeta

    ### INITIALIZER ###

    @abc.abstractmethod
    def __init__(self, source=None, anchor=None):
        AnchoredExpression.__init__(self, anchor=anchor)
        self._source = source

    ### READ-ONLY PUBLIC PROPERTIES ###

    @property
    def source(self):
        return self._source
