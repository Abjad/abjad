from abjad.tools import contexttools
from abjad.tools import pitchtools
from abjad.tools.instrumenttools.Oboe import Oboe


class EnglishHorn(Oboe):
   r'''.. versionadded:: 2.0

   Abjad model of the English horn::

      abjad> staff = Staff("c'8 d'8 e'8 f'8")

   ::

      abjad> instrumenttools.EnglishHorn( )(staff)
      EnglishHorn('English Horn', 'Eng. hn.')

   ::

      abjad> f(staff)
      \new Staff {
         \set Staff.instrumentName = \markup { English Horn }
         \set Staff.shortInstrumentName = \markup { Eng. hn. }
         c'8
         d'8
         e'8
         f'8
      }

   The English horn targets staff context by default.
   '''

   def __init__(self, 
      instrument_name = 'English Horn', short_instrument_name = 'Eng. hn.', target_context = None):
      Oboe.__init__(self, instrument_name, short_instrument_name, target_context)
      self.sounding_pitch_of_fingered_middle_c = pitchtools.NamedChromaticPitch('f')
      self.primary_clefs = [contexttools.ClefMark('treble')]
      self._copy_primary_clefs_to_all_clefs( )
      self.traditional_range = (-8, 24)
