from abjad.tools.spannertools.Spanner._SpannerFormatInterface import _SpannerFormatInterface


class _GlissandoSpannerFormatInterface(_SpannerFormatInterface):
   '''Create ``Glissando`` spanner format-time contributions.'''

   def __init__(self, spanner):
      '''Bind to spanner and initialize as type of spanner format interface.'''
      _SpannerFormatInterface.__init__(self, spanner)

   ## PUBLIC METHODS ##

   def _right(self, leaf):
      '''Spanner contribution to right of leaf.'''
      result = [ ]
      if not self.spanner._is_my_last_leaf(leaf):
         result.append(r'\glissando')
      return result
