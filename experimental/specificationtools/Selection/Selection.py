from abjad.tools.abctools.AbjadObject import AbjadObject
from experimental.specificationtools.TemporalScope import TemporalScope


class Selection(AbjadObject):

    ### INITIALIZER ###

    def __init__(self, segment_name, context_names=None, scope=None):
        assert isinstance(segment_name, str)
        assert isinstance(context_names, (list, type(None)))
        assert isinstance(scope, (TemporalScope, type(None)))
        self.segment_name = segment_name
        self.context_names = context_names
        self.scope = scope

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
