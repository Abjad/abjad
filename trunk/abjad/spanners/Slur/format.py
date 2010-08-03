from abjad.spanners.Spanner.positionalformat import \
   _PositionalSpannerFormatInterface


class _SlurSpannerFormatInterface(_PositionalSpannerFormatInterface):

   def __init__(self, spanner):
      _PositionalSpannerFormatInterface.__init__(self, spanner)

   ## PRIVATE METHODS ##

   def _before(self, leaf):
      '''Spanner format contribution before leaf.'''
      result = [ ]
      result.extend(_PositionalSpannerFormatInterface._before(self, leaf))
      if self.spanner._is_my_first_leaf(leaf):
         style = self.spanner.style
         if style == 'solid':
            result.append(r'\slurSolid')
         elif style == 'dashed':
            result.append(r'\slurDashed')
         elif style == 'dotted':
            result.append(r'\slurDotted')
      return result

   def _right(self, leaf):
      '''Spanner format contribution right of leaf.'''
      result = [ ]
      spanner = self.spanner
      if spanner._is_my_first_leaf(leaf):
         result.append('(')
      if spanner._is_my_last_leaf(leaf):
         result.append(')')   
      return result
