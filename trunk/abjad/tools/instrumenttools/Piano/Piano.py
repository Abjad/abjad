from abjad.tools import contexttools
from abjad.tools import pitchtools
from abjad.tools import scoretools
from abjad.tools.instrumenttools._KeyboardInstrument import _KeyboardInstrument


class Piano(_KeyboardInstrument):
   r'''.. versionadded:: 1.1.2

   Abjad model of the piano::

      abjad> piano_staff = scoretools.PianoStaff([Staff("c'8 d'8 e'8 f'8"), Staff("c'4 b4")])

   ::

      abjad> instrumenttools.Piano( )(piano_staff)
      Piano('Piano', 'Pf.')

   ::

      abjad> f(piano_staff)
      \new PianoStaff <<
         \set PianoStaff.instrumentName = \markup { Piano }
         \set PianoStaff.shortInstrumentName = \markup { Pf. }
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

   The piano target piano staff context by default.
   '''

   def __init__(self,
      instrument_name = 'Piano', short_instrument_name = 'Pf.', target_context = None):
      if target_context is None:
         target_context = scoretools.PianoStaff
      _KeyboardInstrument.__init__(self, instrument_name, short_instrument_name, target_context)
      self.sounding_pitch_of_written_middle_c = pitchtools.NamedChromaticPitch("c'")
      self.primary_clefs = [contexttools.ClefMark('treble'), contexttools.ClefMark('bass')]
      self._copy_primary_clefs_to_all_clefs( )
