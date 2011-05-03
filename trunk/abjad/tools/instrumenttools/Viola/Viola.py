from abjad.tools import contexttools
from abjad.tools import pitchtools
from abjad.tools.instrumenttools._StringInstrument import _StringInstrument


class Viola(_StringInstrument):
   r'''.. versionadded:: 1.1.2

   Abjad model of the viola::

      abjad> staff = Staff("c'8 d'8 e'8 f'8")
      abjad> contexttools.ClefMark('alto')(staff)
      ClefMark('alto')(Staff{4})

   ::

      abjad> instrumenttools.Viola( )(staff)
      Viola('Viola', 'Va.')

   ::

      abjad> f(staff)
      \new Staff {
         \clef "alto"
         \set Staff.instrumentName = \markup { Viola }
         \set Staff.shortInstrumentName = \markup { Va. }
         c'8
         d'8
         e'8
         f'8
      }

   The viola targets staff context by default.
   '''

   def __init__(self,
      instrument_name = 'Viola', short_instrument_name = 'Va.', target_context = None):
      _StringInstrument.__init__(self, instrument_name, short_instrument_name, target_context)
      self.sounding_pitch_of_written_middle_c = pitchtools.NamedChromaticPitch("c'")
      self.primary_clefs = [contexttools.ClefMark('alto')]
      self.all_clefs = [
         contexttools.ClefMark('alto'),
         contexttools.ClefMark('treble')]
