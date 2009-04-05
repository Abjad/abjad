from abjad.spanner.format import _SpannerFormatInterface


class _GlissandoSpannerFormatInterface(_SpannerFormatInterface):

   def __init__(self, spanner):
      _SpannerFormatInterface.__init__(self, spanner)

   ## PUBLIC METHODS ##

   def right(self, leaf):
      '''Spanner contribution to right of leaf.'''
      result = [ ]
      if not self.spanner._isMyLastLeaf(leaf):
         result.append(r'\glissando')
      return result
