from abjad.tools.spannertools.Spanner._SpannerFormatInterface import _SpannerFormatInterface


class _BeamSpannerFormatInterface(_SpannerFormatInterface):

    def __init__(self, spanner):
        _SpannerFormatInterface.__init__(self, spanner)

    ### PUBLIC METHODS ###

    def _before(self, leaf):
        '''Spanner format contribution before leaf.'''
        result = []
        result.extend(_SpannerFormatInterface._before(self, leaf))
        return result

    def _right(self, leaf):
        '''Spanner format contribution right of leaf.'''
        result = []
        spanner = self.spanner
        if spanner._is_my_first_leaf(leaf):
            if spanner.direction is not None:
                result.append('%s [' % spanner.direction)
            else:
                result.append('[')
        if spanner._is_my_last_leaf(leaf):
            result.append(']')
        return result
