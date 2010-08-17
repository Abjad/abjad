from abjad.tools.spannertools.Spanner._SpannerFormatInterface import _SpannerFormatInterface


class _SpacingSpannerFormatInterface(_SpannerFormatInterface):
   '''Create ``SpacingSpanner`` format-time contributions.'''

   def __init__(self, spanner):
      '''Bind to spanner and initialize as type of spanner format interface.'''
      _SpannerFormatInterface.__init__(self, spanner)

   ## PUBLIC METHODS ##

   def _after(self, leaf):
      '''Spanner format contribution after leaf.'''
      result = [ ]
      result.extend(_SpannerFormatInterface._after(self, leaf))
      new_section = self.spanner.new_section
      if new_section:
         if self.spanner._is_my_last_leaf(leaf):
            result.append(r'%%% spacing section ends here %%%')
      return result

   def _before(self, leaf):
      '''Spanner format contribution before leaf.'''
      result = [ ]
      new_section = self.spanner.new_section
      if new_section:
         if self.spanner._is_my_first_leaf(leaf):
            result.append(r'\newSpacingSection')
            pnd = self.spanner.proportional_notation_duration
            if pnd is not None:
               setting = r'\set Score.proportionalNotationDuration = ' + \
                  '#(ly:make-moment %s %s)' % (
                  pnd._numerator, pnd._denominator)
               result.append(setting)
      result.extend(_SpannerFormatInterface._before(self, leaf))
      return result
