from abjad.spanner.format import _SpannerFormatInterface


class _InstrumentSpannerFormatInterface(_SpannerFormatInterface):

   def __init__(self, spanner):
      _SpannerFormatInterface.__init__(self, spanner)

   ## PUBLIC METHODS ##

   def after(self, leaf):
      '''Spanner format contribution after leaf.'''
      result = [ ]
      #result.extend(Spanner.after(spanner, leaf))
      result.extend(_SpannerFormatInterface.after(self, leaf))
      spanner = self.spanner
      if spanner._isMyLastLeaf(leaf):
         #staff = leaf.staff.context
         staff = 'Staff'
         if spanner.long is not None:
            result.append(r'\unset %s.instrumentName' % staff)
         if spanner.short is not None:
            result.append(r'\unset %s.shortInstrumentName' % staff)
      return result

   def before(self, leaf):
      '''Spanner format contribution before leaf.'''
      result = [ ]
      #result.extend(Spanner.before(spanner, leaf))
      result.extend(_SpannerFormatInterface.before(self, leaf))
      spanner = self.spanner
      if spanner._isMyFirstLeaf(leaf):
         #staff = leaf.staff.context
         staff = 'Staff'
         if spanner.long is not None:
            result.append(r'\set %s.instrumentName = %s' % (
               staff, spanner.long))
         if spanner.short is not None:
            result.append(r'\set %s.shortInstrumentName = %s' % (
               staff, spanner.short))
      return result
