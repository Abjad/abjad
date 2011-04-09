from abjad.components import Chord
from abjad.tools.pitchtools.NamedChromaticPitch.NamedChromaticPitch import NamedChromaticPitch
from abjad.tools.pitchtools.chromatic_pitch_number_to_octave_number import chromatic_pitch_number_to_octave_number
from abjad.tools.pitchtools.chromatic_pitch_class_number_to_chromatic_pitch_class_name_with_sharps import chromatic_pitch_class_number_to_chromatic_pitch_class_name_with_sharps


def respell_named_chromatic_pitches_in_expr_with_sharps(expr):
   r'''.. versionadded:: 1.1.1

   Respell named chromatic pitches in `expr` with sharps::

      abjad> staff = Staff(notetools.make_repeated_notes(6))
      abjad> macros.chromaticize(staff)

   ::

      abjad> f(staff)
      \new Staff {
         c'8
         cs'8
         d'8
         ef'8
         e'8
         f'8
      }

   ::

      abjad> pitchtools.respell_named_chromatic_pitches_in_expr_with_sharps(staff)

   ::

      abjad> f(staff)
      \new Staff {
         c'8
         cs'8
         d'8
         ds'8
         e'8
         f'8
      }

   Return none.

   .. versionchanged:: 1.1.2
      renamed ``pitchtools.make_sharp( )`` to
      ``pitchtools.respell_named_chromatic_pitches_in_expr_with_sharps( )``.
   '''
   from abjad.tools import leaftools

   if isinstance(expr, NamedChromaticPitch):
      return _new_pitch_with_sharps(expr)
   else:
      for leaf in leaftools.iterate_leaves_forward_in_expr(expr):
         if isinstance(leaf, Chord):
            for note_head in leaf.note_heads:
               note_head.pitch = _new_pitch_with_sharps(note_head.pitch)
         elif hasattr(leaf, 'pitch'):
            leaf.pitch = _new_pitch_with_sharps(leaf.pitch)


def _new_pitch_with_sharps(pitch):
   octave = chromatic_pitch_number_to_octave_number(abs(pitch.numbered_chromatic_pitch))
   name = chromatic_pitch_class_number_to_chromatic_pitch_class_name_with_sharps(
      pitch.numbered_chromatic_pitch_class)
   pitch = type(pitch)(name, octave)
   return pitch
