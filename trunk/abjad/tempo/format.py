from abjad.exceptions.exceptions import UndefinedSpacingError
from abjad.exceptions.exceptions import UndefinedTempoError
from abjad.spanner.format import _SpannerFormatInterface


class _TempoSpannerFormatInterface(_SpannerFormatInterface):

   def __init__(self, spanner):
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
#         try:
#            scaling_factor = self._scaling_factor
#            if not scaling_factor == 1:
#               result.append('}')
#         except UndefinedTempoError:
#            pass
      return result

   def before(self, leaf):
      '''Spanner format contribution before leaf.'''
      result = [ ]
      result.extend(_SpannerFormatInterface.before(self, leaf))
      spanner = self.spanner
      if spanner._isMyFirstLeaf(leaf):
         try:
            duration = spanner.proportional_notation_duration_effective
            result.append(r'\newSpacingSection')
            directive = r'\set Score.proportionalNotationDuration = '
            directive += ' #(ly:make-moment %s . %s)'
            directive %= (duration._n, duration._d)
            result.append(directive)
         except (UndefinedTempoError, UndefinedSpacingError):
            pass
         if spanner.indication:
            result.append(spanner.indication.format)
      return result
