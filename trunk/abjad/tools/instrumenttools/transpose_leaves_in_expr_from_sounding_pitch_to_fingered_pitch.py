from abjad.components import Chord
from abjad.components import Note
from abjad.tools import leaftools
from abjad.tools import pitchtools
from abjad.tools.instrumenttools.get_effective_instrument import get_effective_instrument


def transpose_leaves_in_expr_from_sounding_pitch_to_fingered_pitch(expr):
   r'''.. versionadded:: 1.1.2

   Transpose leaves in `expr` from sounding pitch to fingered pitch::

      abjad> staff = Staff("<c' e' g'>4 d'4 r4 e'4")
      abjad> instrumenttools.Clarinet( )(staff)

   ::

      abjad> f(staff)
      \new Staff {
         \set Staff.instrumentName = \markup { Clarinet }
         \set Staff.shortInstrumentName = \markup { Cl. }
         <c' e' g'>4
         d'4
         r4
         e'4
      }

   ::

      abjad> instrumenttools.transpose_leaves_in_expr_from_sounding_pitch_to_fingered_pitch(staff)

   ::

      abjad> f(staff)
      \new Staff {
         \set Staff.instrumentName = \markup { Clarinet }
         \set Staff.shortInstrumentName = \markup { Cl. }
         <d' fs' a'>4
         e'4
         r4
         fs'4
      }

   Return none.
   '''

   for leaf in leaftools.iterate_leaves_forward_in_expr(expr):
      if not leaf.written_pitch_indication_is_at_sounding_pitch:
         continue
      instrument = get_effective_instrument(leaf)
      if not instrument:
         continue
      t_n = instrument.interval_of_transposition
      t_n *= -1
      if isinstance(leaf, Note):
         leaf.pitch = pitchtools.transpose_pitch_carrier_by_melodic_interval(leaf.pitch, t_n)
         leaf.written_pitch_indication_is_at_sounding_pitch = False
      elif isinstance(leaf, Chord):               
         pitches = [pitchtools.transpose_pitch_carrier_by_melodic_interval(pitch, t_n)
            for pitch in leaf.pitches]
         leaf.pitches = pitches
         leaf.written_pitch_indication_is_at_sounding_pitch = False
