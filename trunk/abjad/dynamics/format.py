from abjad.spanner.format import _SpannerFormatInterface


class _DynamicSpannerFormatInterface(_SpannerFormatInterface):

   def __init__(self, spanner):
      _SpannerFormatInterface.__init__(self, spanner)

   ## PUBLIC METHODS ##

   def right(self, leaf):
      '''Spanner format contribution to right of leaf.'''
      result = [ ]
      spanner = self.spanner
      if spanner._isMyFirstLeaf(leaf):
         result.append(r'\%s' % spanner.mark)
      return result
