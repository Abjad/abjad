from abjad.spanners.spanner.format import _SpannerFormatInterface


class _PositionalSpannerFormatInterface(_SpannerFormatInterface):

   def __init__(self, spanner):
      _SpannerFormatInterface.__init__(self, spanner)

   ## PUBLIC METHODS ##

   def _before(self, leaf):
      '''Spanner format contribution before leaf.'''
      result = [ ]
      #result.extend(_GrobHandlerSpanner._before(self, leaf))
      result.extend(_SpannerFormatInterface._before(self, leaf))
      spanner = self.spanner
      if spanner._is_my_first_leaf(leaf):
         if not spanner.position is None:
            result.append(spanner._positions[spanner.position])
      return result
