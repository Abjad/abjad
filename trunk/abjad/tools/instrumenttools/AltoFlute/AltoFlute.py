from abjad.tools import pitchtools
from abjad.tools.instrumenttools.Flute import Flute


class AltoFlute(Flute):
   r'''.. versionadded 1.1.2

   Abjad model of the alto flute::

      abjad> staff = Staff("c'8 d'8 e'8 f'8")

   ::

      abjad> instrumenttools.AltoFlute( )(staff)
      AltoFlute('Alto Flute', 'Alt. Fl.')

   ::

      abjad> f(staff)
      \new Staff {
         \set Staff.instrumentName = \markup { Alto Flute }
         \set Staff.shortInstrumentName = \markup { Alt. Fl. }
         c'8
         d'8
         e'8
         f'8
      }

   Alto flute targets staff context by default.
   '''

   def __init__(self,
      instrument_name = 'Alto Flute', short_instrument_name = 'Alt. Fl.', target_context = None):
      Flute.__init__(self, instrument_name, short_instrument_name, target_context)
      self.sounding_pitch_of_written_middle_c = pitchtools.NamedChromaticPitch("g")
