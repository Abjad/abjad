from abjad.tools import contexttools
from abjad.tools import pitchtools
from abjad.tools.instrumenttools._PercussionInstrument import _PercussionInstrument


class Glockenspiel(_PercussionInstrument):
   r'''.. versionadded:: 2.0

   Abjad model of the glockenspiel::

      abjad> staff = Staff("c'8 d'8 e'8 f'8")

   ::

      abjad> instrumenttools.Glockenspiel( )(staff)
      Glockenspiel('Glockenspiel', 'Gkspl.')

   ::

      abjad> f(staff)
      \new Staff {
         \set Staff.instrumentName = \markup { Glockenspiel }
         \set Staff.shortInstrumentName = \markup { Gkspl. }
         c'8
         d'8
         e'8
         f'8
      }

   The glockenspiel targets staff context by default.
   '''

   def __init__(self, 
      instrument_name = 'Glockenspiel', short_instrument_name = 'Gkspl.', target_context = None):
      _PercussionInstrument.__init__(self, instrument_name, short_instrument_name, target_context)
      self.sounding_pitch_of_fingered_middle_c = pitchtools.NamedChromaticPitch("c'''")
      self.primary_clefs = [contexttools.ClefMark('treble')]
      self._copy_primary_clefs_to_all_clefs( )
      self.traditional_range = (19, 48)
