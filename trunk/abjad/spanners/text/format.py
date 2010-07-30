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
      if spanner._is_my_first_leaf(leaf):
         result.append(r'\startTextSpan')
      if spanner._is_my_last_leaf(leaf):
         result.append(r'\stopTextSpan')   
      return result
