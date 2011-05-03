from abjad.tools import contexttools
from abjad.tools import pitchtools
from abjad.tools.instrumenttools._BrassInstrument import _BrassInstrument


class Trombone(_BrassInstrument):
   r'''.. versionadded:: 1.1.2

   Abjad model of the trombone::

      abjad> staff = Staff("c'8 d'8 e'8 f'8")
      abjad> contexttools.ClefMark('bass')(staff)
      ClefMark('bass')(Staff{4})

   ::

      abjad> instrumenttools.Trombone( )(staff)
      Trombone('Trombone', 'Trb.')

   ::

      abjad> f(staff)
      \new Staff {
         \clef "bass"
         \set Staff.instrumentName = \markup { Trombone }
         \set Staff.shortInstrumentName = \markup { Trb. }
         c'8
         d'8
         e'8
         f'8
      }

   The trombone targets staff context by default.
   '''

   def __init__(self,
      instrument_name = 'Trombone', short_instrument_name = 'Trb.', target_context = None):
      _BrassInstrument.__init__(self, instrument_name, short_instrument_name, target_context)
      self.sounding_pitch_of_written_middle_c = pitchtools.NamedChromaticPitch("c'")
      self.primary_clefs = [contexttools.ClefMark('bass'), contexttools.ClefMark('tenor')]
      self._copy_primary_clefs_to_all_clefs( )
      self.traditional_range = (-20, 15)
