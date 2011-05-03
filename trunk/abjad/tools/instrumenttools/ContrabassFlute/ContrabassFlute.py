from abjad.tools import pitchtools
from abjad.tools.instrumenttools.Flute import Flute


class ContrabassFlute(Flute):
   r'''.. versionadded:: 1.1.2

   Abjad model of the contrabass flute::

      abjad> staff = Staff("c'8 d'8 e'8 f'8")

   ::

      abjad> instrumenttools.ContrabassFlute( )(staff)
      ContrabassFlute('Contrabass Flute', 'Contrabass Fl.')

   ::

      abjad> f(staff)
      \new Staff {
         \set Staff.instrumentName = \markup { Contrabass Flute }
         \set Staff.shortInstrumentName = \markup { Contrabass Fl. }
         c'8
         d'8
         e'8
         f'8
      }

   The contrabass flute targets staff context by default.
   '''

   def __init__(self,
      instrument_name = 'Contrabass Flute', short_instrument_name = 'Contrabass Fl.',
      target_context = None):
      Flute.__init__(self, instrument_name, short_instrument_name, target_context)
      self.sounding_pitch_of_fingered_middle_c = pitchtools.NamedChromaticPitch('g,')
