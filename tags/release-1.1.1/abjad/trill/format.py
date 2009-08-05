from abjad.spanner.format import _SpannerFormatInterface


class _TrillSpannerFormatInterface(_SpannerFormatInterface):

   def __init__(self, spanner):
      _SpannerFormatInterface.__init__(self, spanner)

   ## PUBLIC METHODS ##

   def left(self, leaf):
      '''Spanner format contribution left of leaf.'''
      result = [ ]
      spanner = self.spanner
      if spanner.pitch is not None:
         if spanner._isMyFirstLeaf(leaf):
            result.append(r'\pitchedTrill')
      return result

   def _right(self, leaf):
      '''Spanner format contribution right of leaf.'''
      result = [ ]
      spanner = self.spanner
      if spanner._isMyFirstLeaf(leaf):
         result.append(r'\startTrillSpan')
         if spanner.pitch is not None:
            result.append(str(spanner.pitch))
      if spanner._isMyLastLeaf(leaf):
         result.append(r'\stopTrillSpan')
      return result
