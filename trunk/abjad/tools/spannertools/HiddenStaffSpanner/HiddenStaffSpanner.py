from abjad.tools.spannertools.Spanner import Spanner
from abjad.tools.spannertools.HiddenStaffSpanner._HiddenStaffSpannerFormatInterface import \
   _HiddenStaffSpannerFormatInterface


class HiddenStaffSpanner(Spanner):

   def __init__(self, music = None):
      Spanner.__init__(self, music)
      self._format = _HiddenStaffSpannerFormatInterface(self)
