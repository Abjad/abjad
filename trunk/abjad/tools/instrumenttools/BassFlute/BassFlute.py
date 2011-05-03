from abjad.tools import pitchtools
from abjad.tools.instrumenttools.Flute import Flute


class BassFlute(Flute):
   r'''.. versionadded:: 1.1.2

   Abjad model of the bass flute::

      abjad> staff = Staff("c'8 d'8 e'8 f'8")

   ::

      abjad> instrumenttools.BassFlute( )(staff)
      BassFlute('Bass Flute', 'Bass Fl.')

   ::

      abjad> f(staff)
      \new Staff {
         \set Staff.instrumentName = \markup { Bass Flute }
         \set Staff.shortInstrumentName = \markup { Bass Fl. }
         c'8
         d'8
         e'8
         f'8
      }
   
   Bass flute targets staff context by default.
   '''

   def __init__(self, 
      instrument_name = 'Bass Flute', short_instrument_name = 'Bass Fl.', target_context = None):
      Flute.__init__(self, instrument_name, short_instrument_name, target_context)
      self.sounding_pitch_of_fingered_middle_c = pitchtools.NamedChromaticPitch('c')
