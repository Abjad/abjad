from abjad.tools.spannertools.Spanner._SpannerFormatInterface import _SpannerFormatInterface


class _PianoPedalSpannerFormatInterface(_SpannerFormatInterface):

    def __init__(self, spanner):
        _SpannerFormatInterface.__init__(self, spanner)

    ### PUBLIC METHODS ###

    def _before(self, leaf):
        '''Spanner format contribution before leaf.'''
        result = []
        spanner = self.spanner
        if spanner._is_my_first_leaf(leaf):
            result.append(r"\set Staff.pedalSustainStyle = #'%s" % spanner.style)
        return result

    def _right(self, leaf):
        '''Spanner format contribution right of leaf.'''
        result = []
        spanner = self.spanner
        if spanner._is_my_first_leaf(leaf):
            result.append(spanner._kinds[spanner.kind][0])
        if spanner._is_my_last_leaf(leaf):
            result.append(spanner._kinds[spanner.kind][1])
        return result
