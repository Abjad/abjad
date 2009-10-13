from abjad.spanners.spanner.positionalformat import \
   _PositionalSpannerFormatInterface


class _TextSpannerFormatInterface(_PositionalSpannerFormatInterface):

   def __init__(self, spanner):
      _PositionalSpannerFormatInterface.__init__(self, spanner)

   ## PUBLIC METHODS ##

   def _right(self, leaf):
      '''Spanner format contribution right of leaf.'''
      result = [ ]
      spanner = self.spanner
      if spanner._isMyFirstLeaf(leaf):
         result.append(r'\startTextSpan')
      if spanner._isMyLastLeaf(leaf):
         result.append(r'\stopTextSpan')   
      return result
