from abjad.tools import contexttools
from abjad.tools import pitchtools
from abjad.tools.instrumenttools._BrassInstrument import _BrassInstrument
from abjad.tools.instrumenttools._WindInstrument import _WindInstrument


class FrenchHorn(_BrassInstrument, _WindInstrument):
   r'''.. versionadded:: 1.1.2

   Abjad model of the French horn::

      abjad> staff = Staff("c'8 d'8 e'8 f'8")

   ::

      abjad> instrumenttools.FrenchHorn( )(staff)
      FrenchHorn('French Horn', 'Fr. hn.')

   ::

      abjad> f(staff)
      \new Staff {
         \set Staff.instrumentName = \markup { French Horn }
         \set Staff.shortInstrumentName = \markup { Fr. hn. }
         c'8
         d'8
         e'8
         f'8
      }

   The French horn targets staff context by default.
   '''

   def __init__(self,
      instrument_name = 'French Horn', short_instrument_name = 'Fr. hn.', target_context = None):
      _BrassInstrument.__init__(self, instrument_name, short_instrument_name, target_context)
      self.sounding_pitch_of_fingered_middle_c = pitchtools.NamedChromaticPitch('f')
      self.primary_clefs = [contexttools.ClefMark('treble'), contexttools.ClefMark('bass')]
      self._copy_primary_clefs_to_all_clefs( )
      self.traditional_range = (-25, 17)
