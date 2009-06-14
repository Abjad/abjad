from abjad.scm.moment import Moment
from abjad.tempo.format import _TempoSpannerFormatInterface
#from abjad.tools import spacing


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

   def _make_proportional_directive(self, global_spacing, local_tempo):
      '''Calculate proportional notation duration for local tempo.'''
      local_maelzel = local_tempo.maelzel
      global_maelzel = global_spacing.tempo_indication.maelzel
      global_pnd = global_spacing.proportional_notation_duration
      local_pnd = local_maelzel / global_maelzel * global_pnd
      directive = self._format_proportional_directive(local_pnd)
      return directive

   ## PUBLIC METHODS ##

   def before(self, leaf):
      '''Spanner format contribution before leaf.'''
      from abjad.tools import spacing
      result = [ ]
      result.extend(_TempoSpannerFormatInterface.before(self, leaf))
      spanner = self.spanner
      if spanner._isMyFirstLeaf(leaf):
         result.append(r'\newSpacingSection')
         global_spacing = spacing.get_global(leaf)
         if global_spacing is not None:
            directive = self._make_proportional_directive(
               global_spacing, spanner.indication)
            result.append(directive)
      return result
