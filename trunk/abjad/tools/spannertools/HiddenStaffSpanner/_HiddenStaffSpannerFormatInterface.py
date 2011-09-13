from abjad.tools.spannertools.Spanner._SpannerFormatInterface import _SpannerFormatInterface


class _HiddenStaffSpannerFormatInterface(_SpannerFormatInterface):

    ### PRIVATE METHODS ###

    def _after(self, leaf):
        result = []
        if self.spanner._is_my_last_leaf(leaf):
            result.append(r'\startStaff')
        return result

    def _before(self, leaf):
        result = []
        if self.spanner._is_my_first_leaf(leaf):
            result.append(r'\stopStaff')
        return result
