from abjad.tools import contexttools
from abjad.tools import pitchtools
from abjad.tools.instrumenttools.Clarinet import Clarinet


class BassClarinet(Clarinet):
   r'''.. versionadded:: 1.1.2

   Abjad model of the bass clarinet::

      abjad> staff = Staff("c'8 d'8 e'8 f'8")

   ::

      abjad> instrumenttools.BassClarinet( )(staff)
      BassClarinet('Bass Clarinet', 'Bass Cl.')

   ::

      abjad> f(staff)
      \new Staff {
         \set Staff.instrumentName = \markup { Bass Clarinet }
         \set Staff.shortInstrumentName = \markup { Bass Cl. }
         c'8
         d'8
         e'8
         f'8
      }

   Bass clarinet targets staff context by default.
   '''

   def __init__(self,
      instrument_name = 'Bass Clarinet', short_instrument_name = 'Bass Cl.', target_context = None):
      Clarinet.__init__(self, instrument_name, short_instrument_name, target_context)
      self.sounding_pitch_of_fingered_middle_c = pitchtools.NamedChromaticPitch('bf,')
      self.primary_clefs = [contexttools.ClefMark('treble')]
      self.all_clefs = [contexttools.ClefMark('treble'), contexttools.ClefMark('bass')]
