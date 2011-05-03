from abjad.tools import contexttools
from abjad.tools import pitchtools
from abjad.tools import scoretools
from abjad.tools.instrumenttools._StringInstrument import _StringInstrument


## TODO: make work at the right context
class Harp(_StringInstrument):
   r'''.. versionadded:: 1.1.2

   Abjad model of the harp::

      abjad> piano_staff = scoretools.PianoStaff([Staff("c'8 d'8 e'8 f'8"), Staff("c'4 b4")])

   ::

      abjad> instrumenttools.Harp( )(piano_staff)
      Harp('Harp', 'Hp.')

   ::

      abjad> f(piano_staff)
      \new PianoStaff <<
         %%% \set Staff.instrumentName = \markup { Harp } %%%
         %%% \set Staff.shortInstrumentName = \markup { Hp. } %%%
         \new Staff {
            c'8
            d'8
            e'8
            f'8
         }
         \new Staff {
            c'4
            b4
         }
      >>

   The harp targets piano staff context by default.
   '''

   def __init__(self,
      instrument_name = 'Harp', short_instrument_name = 'Hp.', target_context = None):
      if target_context is None:
         target_context = scoretools.PianoStaff
      _StringInstrument.__init__(self, instrument_name, short_instrument_name, target_context)
      self.sounding_pitch_of_written_middle_c = pitchtools.NamedChromaticPitch("c'")
      self.primary_clefs = [contexttools.ClefMark('treble'), contexttools.ClefMark('bass')]
      self._copy_primary_clefs_to_all_clefs( )
      self.traditional_range = (-37, 44)
