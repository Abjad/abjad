from experimental.tools.settingtools.ExpressionAnchoredObject import ExpressionAnchoredObject
from experimental.tools.settingtools.Expression import Expression


class AnchoredExpression(Expression, ExpressionAnchoredObject):
    '''Anchored expression.
    '''

    ### INITIALIZER ###

    def __init__(self, anchor=None):
        Expression.__init__(self)
        ExpressionAnchoredObject.__init__(self, anchor=anchor)
