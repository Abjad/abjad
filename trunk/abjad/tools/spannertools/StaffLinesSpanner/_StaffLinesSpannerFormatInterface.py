from abjad.tools.schemetools import SchemeVector
from abjad.tools.spannertools.Spanner._SpannerFormatInterface import _SpannerFormatInterface


class _StaffLinesSpannerFormatInterface(_SpannerFormatInterface):

    ### PRIVATE METHODS ###

    def _after(self, leaf):
        result = []
        if self.spanner._is_my_last_leaf(leaf):
            result.append(r'\stopStaff')
            if isinstance(self.spanner.lines, int):
                result.append(r"\revert Staff.StaffSymbol #'line-count")
            else:
                result.append(r"\revert Staff.StaffSymbol #'line-positions")
            result.append(r'\startStaff')
        return result

    def _before(self, leaf):
        result = []
        if self.spanner._is_my_first_leaf(leaf):
            result.append(r'\stopStaff')
            if isinstance(self.spanner.lines, int):
                result.append(r"\override Staff.StaffSymbol #'line-count = #%s" % \
                    self.spanner.lines)
            else:
                result.append(r"\override Staff.StaffSymbol #'line-positions = %s" % \
                    SchemeVector(*self.spanner.lines).format)
            result.append(r'\startStaff')
        return result
