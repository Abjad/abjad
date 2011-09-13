from abjad.tools.spannertools.Spanner._SpannerFormatInterface import _SpannerFormatInterface


class _DynamicTextSpannerFormatInterface(_SpannerFormatInterface):

    def __init__(self, spanner):
        _SpannerFormatInterface.__init__(self, spanner)

    ### PUBLIC METHODS ###

    def _right(self, leaf):
        '''Spanner format contribution to right of leaf.'''
        result = []
        spanner = self.spanner
        if spanner._is_my_first_leaf(leaf):
            result.append(r'\%s' % spanner.mark)
        return result
