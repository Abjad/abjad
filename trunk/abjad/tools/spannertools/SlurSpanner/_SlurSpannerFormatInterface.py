from abjad.tools.spannertools.Spanner._SpannerFormatInterface import _SpannerFormatInterface


class _SlurSpannerFormatInterface(_SpannerFormatInterface):

    def __init__(self, spanner):
        _SpannerFormatInterface.__init__(self, spanner)

    ### PRIVATE METHODS ###

    def _right(self, leaf):
        '''Spanner format contribution right of leaf.'''
        result = []
        spanner = self.spanner
        if spanner._is_my_first_leaf(leaf):
            result.append('(')
        if spanner._is_my_last_leaf(leaf):
            result.append(')')
        return result
