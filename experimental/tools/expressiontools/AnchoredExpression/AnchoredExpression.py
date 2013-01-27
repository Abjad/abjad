from experimental.tools.expressiontools.AnchoredObject import AnchoredObject
from experimental.tools.expressiontools.Expression import Expression


class AnchoredExpression(Expression, AnchoredObject):
    '''Anchored expression.
    '''

    ### INITIALIZER ###

    def __init__(self, anchor=None):
        Expression.__init__(self)
        AnchoredObject.__init__(self, anchor=anchor)
