from abjad.spanners.Spanner.format import _SpannerFormatInterface


class _InstrumentSpannerFormatInterface(_SpannerFormatInterface):

   def __init__(self, spanner):
      _SpannerFormatInterface.__init__(self, spanner)

   ## PUBLIC METHODS ##

   def _after(self, leaf):
      '''Spanner format contribution after leaf.'''
      result = [ ]
      #result.extend(Spanner._after(spanner, leaf))
      result.extend(_SpannerFormatInterface._after(self, leaf))
      spanner = self.spanner
      if spanner._is_my_last_leaf(leaf):
         #staff = leaf.staff.context
         staff = 'Staff'
         if spanner.long is not None:
            result.append(r'\unset %s.instrumentName' % staff)
         if spanner.short is not None:
            result.append(r'\unset %s.shortInstrumentName' % staff)
      return result

   def _before(self, leaf):
      '''Spanner format contribution before leaf.'''
      result = [ ]
      #result.extend(Spanner._before(spanner, leaf))
      result.extend(_SpannerFormatInterface._before(self, leaf))
      spanner = self.spanner
      if spanner._is_my_first_leaf(leaf):
         #staff = leaf.staff.context
         staff = 'Staff'
         if spanner.long is not None:
            result.append(r'\set %s.instrumentName = %s' % (
               staff, spanner.long))
         if spanner.short is not None:
            result.append(r'\set %s.shortInstrumentName = %s' % (
               staff, spanner.short))
      return result
