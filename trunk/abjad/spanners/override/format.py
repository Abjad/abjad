from abjad.spanners.spanner.format import _SpannerFormatInterface


class _OverrideSpannerFormatInterface(_SpannerFormatInterface):

   def __init__(self, spanner):
      _SpannerFormatInterface.__init__(self, spanner)

   ## PUBLIC METHODS ##

   def _after(self, leaf):
      '''Spanner format contribution after leaf.'''
      spanner = self.spanner
      if spanner._is_my_last_leaf(leaf) and \
         not spanner._is_my_only_leaf(leaf) and \
         (spanner._attribute is not None):
         grob = spanner._prepend_context(spanner._grob)
         attribute = spanner._parser.format_attribute(spanner._attribute)
         result = r'\revert %s %s' % (grob, attribute)
         return [result]
      else:
         return [ ]

   def _before(self, leaf):
      '''Spanner format contribution before leaf.'''
      spanner = self.spanner
      if spanner._is_my_first_leaf(leaf) and \
         spanner._attribute and \
         (spanner._value is not None):
         grob = spanner._prepend_context(spanner._grob)
         attribute = spanner._parser.format_attribute(spanner._attribute)
         value = spanner._parser.format_value(spanner._value)
         result = r'\override %s %s = %s' % (grob, attribute, value)
         result = spanner._prepend_counter(result)
         return [result]
      else:
         return [ ]
