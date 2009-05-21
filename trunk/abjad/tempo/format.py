from abjad.spanner.format import _SpannerFormatInterface


class _TempoSpannerFormatInterface(_SpannerFormatInterface):

   def __init__(self, spanner):
      _SpannerFormatInterface.__init__(self, spanner)

   ## PRIVATE ATTRIBUTES ##

   @property
   def _scaling_factor(self):
      indication, reference = spanner.indication, spanner.reference
      if reference and not indication == reference:
         pass

   ## PUBLIC METHODS ##

   def after(self, leaf):
      '''Spanner format contribution after leaf.'''
      result = [ ]
      result.extend(_SpannerFormatInterface.after(self, leaf))
      spanner = self.spanner
      if spanner._isMyLastLeaf(leaf):
         if spanner.indication:
            result.append(r'%%%% %s ends here' % spanner.indication.format[1:])
      return result

   def before(self, leaf):
      '''Spanner format contribution before leaf.'''
      result = [ ]
      result.extend(_SpannerFormatInterface.before(self, leaf))
      spanner = self.spanner
      if spanner._isMyFirstLeaf(leaf):
         if spanner.indication:
            result.append(spanner.indication.format)
      return result
