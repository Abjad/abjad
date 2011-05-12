from abjad.tools import leaftools
from abjad.tools import pitchtools
from abjad.tools import voicetools
from abjad.tools.instrumenttools.get_effective_instrument import get_effective_instrument


def notes_and_chords_in_expr_are_within_traditional_instrument_ranges(expr):
   '''.. versionadded:: 1.1.2

   True when notes and chords in `expr` are within traditional instrument ranges::

      abjad> staff = Staff("c'8 r8 <d' fs'>8 r8")
      abjad> instrumenttools.Violin( )(staff)
   
   ::

      abjad> instrumenttools.notes_and_chords_in_expr_are_within_traditional_instrument_ranges(staff)
      True

   False otherwise::

      abjad> staff = Staff("c'8 r8 <d fs>8 r8")
      abjad> instrumenttools.Violin( )(staff)
   
   ::

      abjad> instrumenttools.notes_and_chords_in_expr_are_within_traditional_instrument_ranges(staff)
      False

   Return boolean.
   '''

   for note_or_chord in leaftools.iterate_notes_and_chords_forward_in_expr(expr):
      instrument = get_effective_instrument(note_or_chord)
      if note_or_chord not in instrument.traditional_range:
         return False
   else:
      return True
