from abjad.exceptions import UndefinedSpacingError
from abjad.exceptions import UndefinedTempoError
from abjad.spanners.Spanner._SpannerFormatInterface import _SpannerFormatInterface


class _TempoSpannerFormatInterface(_SpannerFormatInterface):
   '''Encapsulate ``Tempo`` spanner format logic.'''

   def __init__(self, spanner):
      '''Init as type of spanner format interface.'''
      _SpannerFormatInterface.__init__(self, spanner)

   ## PUBLIC METHODS ##

   def _after(self, leaf):
      '''Spanner format contribution after leaf.'''
      result = [ ]
      result.extend(_SpannerFormatInterface._after(self, leaf))
      spanner = self.spanner
      if spanner._is_my_last_leaf(leaf):
         if spanner.tempo_indication:
            result.append(
               r'%%%% %s ends here' % spanner.tempo_indication.format[1:])
      return result

   def _before(self, leaf):
      '''Spanner format contribution before leaf.'''
      result = [ ]
      result.extend(_SpannerFormatInterface._before(self, leaf))
      spanner = self.spanner
      if spanner._is_my_first_leaf(leaf):
         if spanner.tempo_indication:
            result.append(spanner.tempo_indication.format)
      return result
