from abjad.tools.spannertools.Spanner._SpannerFormatInterface import _SpannerFormatInterface


class _OctavationSpannerFormatInterface(_SpannerFormatInterface):

    def __init__(self, spanner):
        _SpannerFormatInterface.__init__(self, spanner)

    ### PRIVATE METHODS ###

    def _after(self, leaf):
        '''Spanner format contributions after leaf.'''
        result = []
        result.extend(_SpannerFormatInterface._after(self, leaf))
        spanner = self.spanner
        if spanner._is_my_last_leaf(leaf):
            result.append(r'\ottava #%s' % spanner.stop)
        return result

    def _before(self, leaf):
        '''Spanner format contributions before leaf.'''
        result = []
        result.extend(_SpannerFormatInterface._before(self, leaf))
        spanner = self.spanner
        if spanner._is_my_first_leaf(leaf):
            result.append(r'\ottava #%s' % spanner.start)
        return result
