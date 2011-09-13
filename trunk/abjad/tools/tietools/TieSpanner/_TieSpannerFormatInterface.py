from abjad.tools.spannertools.Spanner._SpannerFormatInterface import _SpannerFormatInterface


class _TieSpannerFormatInterface(_SpannerFormatInterface):

    def __init__(self, spanner):
        _SpannerFormatInterface.__init__(self, spanner)

    ### PUBLIC METHODS ###

    def _right(self, leaf):
        '''Spanner format contribution right of leaf.'''
        result = []
        if not self.spanner._is_my_last_leaf(leaf):
            result.append('~')
        return result
