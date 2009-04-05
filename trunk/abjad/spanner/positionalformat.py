from abjad.spanner.format import _SpannerFormatInterface


class _PositionalSpannerFormatInterface(_SpannerFormatInterface):

   def __init__(self, spanner):
      _SpannerFormatInterface.__init__(self, spanner)

   ## PUBLIC METHODS ##

   def before(self, leaf):
      '''Spanner format contribution before leaf.'''
      result = [ ]
      #result.extend(_GrobHandlerSpanner.before(self, leaf))
      result.extend(_SpannerFormatInterface.before(self, leaf))
      spanner = self.spanner
      if spanner._isMyFirstLeaf(leaf):
         if not spanner.position is None:
            result.append(spanner._positions[spanner.position])
      return result
