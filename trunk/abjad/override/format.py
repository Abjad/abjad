from abjad.spanner.format import _SpannerFormatInterface


class _OverrideSpannerFormatInterface(_SpannerFormatInterface):

   def __init__(self, spanner):
      _SpannerFormatInterface.__init__(self, spanner)

   ## PUBLIC METHODS ##

   def after(self, leaf):
      '''Spanner format contribution after leaf.'''
      spanner = self.spanner
      if spanner._isMyLastLeaf(leaf) and \
         not spanner._isMyOnlyLeaf(leaf) and spanner._attribute:
         grob = spanner._prependContext(spanner._grob)
         attribute = spanner._parser.formatAttribute(spanner._attribute)
         result = r'\revert %s %s' % (grob, attribute)
         return [result]
      else:
         return [ ]

   def before(self, leaf):
      '''Spanner format contribution before leaf.'''
      spanner = self.spanner
      if spanner._isMyFirstLeaf(leaf) and spanner._attribute and \
         spanner._value:
         grob = spanner._prependContext(spanner._grob)
         attribute = spanner._parser.formatAttribute(spanner._attribute)
         value = spanner._parser.formatValue(spanner._value)
         result = r'\override %s %s = %s' % (grob, attribute, value)
         result = spanner._prependCounter(result)
         return [result]
      else:
         return [ ]
