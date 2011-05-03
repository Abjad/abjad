from abjad.tools import contexttools
from abjad.tools import pitchtools
from abjad.tools.instrumenttools._StringInstrument import _StringInstrument


class Cello(_StringInstrument):
   r'''.. versionadded:: 1.1.2

   Abjad model of the cello::

      abjad> staff = Staff("c'8 d'8 e'8 f'8")
      abjad> contexttools.ClefMark('bass')(staff)
      ClefMark('bass')(Staff{4})

   ::

      abjad> instrumenttools.Cello( )(staff)
      Cello('Cello', 'Vc.')

   ::

      abjad> f(staff)
      \new Staff {
         \clef "bass"
         \set Staff.instrumentName = \markup { Cello }
         \set Staff.shortInstrumentName = \markup { Vc. }
         c'8
         d'8
         e'8
         f'8
      }

   The cello targets staff context by default.
   '''

   def __init__(self,
      instrument_name = 'Cello', short_instrument_name = 'Vc.', target_context = None):
      _StringInstrument.__init__(self, instrument_name, short_instrument_name, target_context)
      self.sounding_pitch_of_written_middle_c = pitchtools.NamedChromaticPitch("c'")
      self.primary_clefs = [contexttools.ClefMark('bass')]
      self.all_clefs = [
         contexttools.ClefMark('bass'), 
         contexttools.ClefMark('tenor'), 
         contexttools.ClefMark('treble')]
