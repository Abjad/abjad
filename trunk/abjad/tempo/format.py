from abjad.exceptions import UndefinedSpacingError
from abjad.exceptions import UndefinedTempoError
from abjad.spanner.format import _SpannerFormatInterface


class _TempoSpannerFormatInterface(_SpannerFormatInterface):
   '''Encapsulate ``Tempo`` spanner format logic.'''

   def __init__(self, spanner):
      '''Init as type of spanner format interface.'''
      _SpannerFormatInterface.__init__(self, spanner)

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

   def _before(self, leaf):
      '''Spanner format contribution before leaf.'''
      result = [ ]
      result.extend(_SpannerFormatInterface._before(self, leaf))
      spanner = self.spanner
      if spanner._isMyFirstLeaf(leaf):
         if spanner.indication:
            result.append(spanner.indication.format)
      return result
