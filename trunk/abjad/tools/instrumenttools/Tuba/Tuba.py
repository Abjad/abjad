from abjad.tools import contexttools
from abjad.tools import pitchtools
from abjad.tools.instrumenttools._BrassInstrument import _BrassInstrument


class Tuba(_BrassInstrument):
   r'''.. versionadded:: 2.0

   Abjad model of the tuba::

      abjad> staff = Staff("c'8 d'8 e'8 f'8")
      abjad> contexttools.ClefMark('bass')(staff)
      ClefMark('bass')(Staff{4})

   ::

      abjad> instrumenttools.Tuba( )(staff)
      Tuba('Tuba', 'Tb.')

   ::

      abjad> f(staff)
      \new Staff {
         \clef "bass"
         \set Staff.instrumentName = \markup { Tuba }
         \set Staff.shortInstrumentName = \markup { Tb. }
         c'8
         d'8
         e'8
         f'8
      }

   The tuba targets staff context by default.
   '''

   def __init__(self,
      instrument_name = 'Tuba', short_instrument_name = 'Tb.', target_context = None):
      _BrassInstrument.__init__(self, instrument_name, short_instrument_name, target_context)
      self.sounding_pitch_of_written_middle_c = pitchtools.NamedChromaticPitch("c'")
      self.primary_clefs = [contexttools.ClefMark('bass')]
      self._copy_primary_clefs_to_all_clefs( )
      self.traditional_range = (-34, 5)
