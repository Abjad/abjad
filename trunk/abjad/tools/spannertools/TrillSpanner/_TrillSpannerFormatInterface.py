from abjad.tools.spannertools.Spanner._SpannerFormatInterface import _SpannerFormatInterface


class _TrillSpannerFormatInterface(_SpannerFormatInterface):

    def __init__(self, spanner):
        _SpannerFormatInterface.__init__(self, spanner)

    ### PUBLIC METHODS ###

    #def _left(self, leaf):
    def _before(self, leaf):
        '''Spanner format contribution left of leaf.'''
        result = []
        spanner = self.spanner
        if spanner.pitch is not None:
            if spanner._is_my_first_leaf(leaf):
                result.append(r'\pitchedTrill')
        return result

    def _right(self, leaf):
        '''Spanner format contribution right of leaf.'''
        result = []
        spanner = self.spanner
        if spanner._is_my_first_leaf(leaf):
            result.append(r'\startTrillSpan')
            if spanner.pitch is not None:
                result.append(str(spanner.pitch))
        if spanner._is_my_last_leaf(leaf):
            result.append(r'\stopTrillSpan')
        return result
