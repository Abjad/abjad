from abjad.spanner.format import _SpannerFormatInterface


class _TieSpannerFormatInterface(_SpannerFormatInterface):

   def __init__(self, spanner):
      _SpannerFormatInterface.__init__(self, spanner)

   ## PUBLIC METHODS ##

   def _right(self, leaf):
      '''Spanner format contribution right of leaf.'''
      result = [ ]
      if not self.spanner._isMyLastLeaf(leaf):
         result.append('~')
      return result
