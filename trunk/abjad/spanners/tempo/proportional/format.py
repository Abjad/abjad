from abjad.scm import Moment
from abjad.spanners.tempo.format import _TempoSpannerFormatInterface


class _TempoProportionalFormatInterface(_TempoSpannerFormatInterface):
   '''Encapsulate ``TempoProportional`` format logic.'''
  
   def __init__(self, spanner):
      '''Init as type of tempo spanner format interface.'''
      _TempoSpannerFormatInterface.__init__(self, spanner)

   ## PRIVATE METHODS ##

   def _format_proportional_directive(self, proportional_notation_duration):
      '''Return proportional notation duration directive as string.'''
      setting = 'proportionalNotationDuration'
      moment = Moment(proportional_notation_duration)
      return r'\set Score.%s = #%s' % (setting, moment.format)

   def _make_proportional_directive(self, scorewide_spacing, local_tempo):
      '''Calculate proportional notation duration for local tempo.'''
      local_quarters_per_minute = local_tempo.quarters_per_minute
      scorewide_quarters_per_minute = \
         scorewide_spacing.tempo_indication.quarters_per_minute
      scorewide_pnd = scorewide_spacing.proportional_notation_duration
      local_pnd = local_quarters_per_minute / scorewide_quarters_per_minute * \
         scorewide_pnd
      directive = self._format_proportional_directive(local_pnd)
      return directive

   ## PUBLIC METHODS ##

   def _before(self, leaf):
      '''Spanner format contribution before leaf.'''
      from abjad.tools import spacing
      result = [ ]
      result.extend(_TempoSpannerFormatInterface._before(self, leaf))
      spanner = self.spanner
      if spanner._isMyFirstLeaf(leaf):
         result.append(r'\newSpacingSection')
         scorewide_spacing = spacing.get_scorewide(leaf)
         if scorewide_spacing is not None:
            directive = self._make_proportional_directive(
               scorewide_spacing, spanner.tempo_indication)
            result.append(directive)
      return result
