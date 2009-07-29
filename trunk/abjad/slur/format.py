from abjad.spanner.positionalformat import _PositionalSpannerFormatInterface


class _SlurSpannerFormatInterface(_PositionalSpannerFormatInterface):

   def __init__(self, spanner):
      _PositionalSpannerFormatInterface.__init__(self, spanner)

   ## PUBLIC METHODS ##

   def _right(self, leaf):
      '''Spanner format contribution right of leaf.'''
      result = [ ]
      spanner = self.spanner
      if spanner._isMyFirstLeaf(leaf):
         result.append('(')
      if spanner._isMyLastLeaf(leaf):
         result.append(')')   
      return result
